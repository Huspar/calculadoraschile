/**
 * Vercel Serverless Function: send-lead
 * Intermediates between Cálculo Laboral client forms and EmailJS API.
 * Keeps EmailJS credentials secure and supports server-side private tokens.
 *
 * Hardened (2026-06):
 *  - Strict CORS allowlist (no wildcard)
 *  - In-memory IP rate limit (10 req / 10 min per IP)
 *  - Honeypot field to catch bots
 *  - Input validation: name (1-80), email RFC-lite, phone digits-only (<=20), tipo enum, monto numeric (<=20 chars)
 *  - Body size limit (1KB)
 *  - No hardcoded credential fallbacks: EmailJS_* must be set in Vercel env or the request fails fast.
 *  - Generic error responses (no internal details leaked)
 *  - HTML-escaped template params before forwarding to EmailJS
 */

const ALLOWED_ORIGINS = new Set([
    'https://calculolaboral.cl',
    'https://www.calculolaboral.cl',
    'http://localhost:3000',
    'http://localhost:5500'
]);

const TIPO_ALLOWED = new Set(['Finiquito', 'Sueldo Liquido', 'Sueldo Líquido', 'Contacto', 'LeadMagnet', 'Otro']);

const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000; // 10 minutes
const RATE_LIMIT_MAX = 10; // max requests per IP per window
const ipBuckets = new Map(); // ip -> { count, resetAt }

const MAX_BODY_BYTES = 1024;

function getClientIp(req) {
    const xff = req.headers['x-forwarded-for'];
    if (typeof xff === 'string' && xff.length > 0) {
        return xff.split(',')[0].trim();
    }
    return (req.socket && req.socket.remoteAddress) || 'unknown';
}

function rateLimit(ip) {
    const now = Date.now();
    const bucket = ipBuckets.get(ip);
    if (!bucket || now > bucket.resetAt) {
        ipBuckets.set(ip, { count: 1, resetAt: now + RATE_LIMIT_WINDOW_MS });
        return { allowed: true, remaining: RATE_LIMIT_MAX - 1 };
    }
    if (bucket.count >= RATE_LIMIT_MAX) {
        return { allowed: false, remaining: 0, retryAfter: Math.ceil((bucket.resetAt - now) / 1000) };
    }
    bucket.count += 1;
    return { allowed: true, remaining: RATE_LIMIT_MAX - bucket.count };
}

function escapeHtml(value) {
    if (typeof value !== 'string') return '';
    return value
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function isValidEmail(email) {
    return typeof email === 'string'
        && email.length <= 254
        && /^[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]+$/.test(email);
}

function sanitizeName(value) {
    if (typeof value !== 'string') return '';
    return value.trim().slice(0, 80);
}

function sanitizePhone(value) {
    if (typeof value !== 'string') return '';
    const digits = value.replace(/[^\d+\s\-]/g, '').trim();
    return digits.slice(0, 20);
}

function sanitizeMonto(value) {
    if (typeof value === 'number' && Number.isFinite(value)) return String(Math.min(Math.max(value, 0), 1e12));
    if (typeof value !== 'string') return '0';
    const cleaned = value.replace(/[^\d.,\-]/g, '').slice(0, 20);
    return cleaned || '0';
}

function sanitizeTipo(value) {
    if (typeof value !== 'string') return 'Finiquito';
    const trimmed = value.trim().slice(0, 40);
    return TIPO_ALLOWED.has(trimmed) ? trimmed : 'Otro';
}

function setCors(req, res) {
    const origin = req.headers.origin;
    if (typeof origin === 'string' && ALLOWED_ORIGINS.has(origin)) {
        res.setHeader('Access-Control-Allow-Origin', origin);
        res.setHeader('Vary', 'Origin');
        res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
        res.setHeader('Access-Control-Max-Age', '600');
    }
}

module.exports = async (req, res) => {
    setCors(req, res);

    if (req.method === 'OPTIONS') {
        return res.status(204).end();
    }

    if (req.method !== 'POST') {
        res.setHeader('Allow', 'POST');
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const origin = req.headers.origin;
    if (typeof origin === 'string' && !ALLOWED_ORIGINS.has(origin)) {
        return res.status(403).json({ error: 'Origin not allowed' });
    }

    const contentLength = parseInt(req.headers['content-length'] || '0', 10);
    if (contentLength > MAX_BODY_BYTES) {
        return res.status(413).json({ error: 'Payload too large' });
    }

    const ip = getClientIp(req);
    const rl = rateLimit(ip);
    if (!rl.allowed) {
        res.setHeader('Retry-After', String(rl.retryAfter || 60));
        return res.status(429).json({ error: 'Too many requests' });
    }

    try {
        const body = req.body && typeof req.body === 'object' ? req.body : {};
        const {
            nombre,
            correo,
            telefono,
            monto_calculado,
            tipo,
            website,
            form_rendered_at
        } = body;

        if (typeof website === 'string' && website.trim().length > 0) {
            return res.status(200).json({ success: true });
        }

        if (typeof form_rendered_at === 'number' && Date.now() - form_rendered_at < 1500) {
            return res.status(200).json({ success: true });
        }

        const cleanName = sanitizeName(nombre);
        const cleanEmail = (typeof correo === 'string' ? correo.trim().toLowerCase() : '');

        if (!cleanName) {
            return res.status(400).json({ error: 'Nombre es obligatorio.' });
        }
        if (!isValidEmail(cleanEmail)) {
            return res.status(400).json({ error: 'Correo no válido.' });
        }

        const cleanPhone = sanitizePhone(telefono);
        const cleanMonto = sanitizeMonto(monto_calculado);
        const cleanTipo = sanitizeTipo(tipo);

        const serviceId = process.env.EMAILJS_SERVICE_ID;
        const templateId = process.env.EMAILJS_TEMPLATE_ID;
        const publicKey = process.env.EMAILJS_PUBLIC_KEY;
        const privateKey = process.env.EMAILJS_PRIVATE_KEY;

        if (!serviceId || !templateId || !publicKey) {
            console.error('send-lead: missing EmailJS env vars');
            return res.status(500).json({ error: 'Service not configured' });
        }

        const payload = {
            service_id: serviceId,
            template_id: templateId,
            user_id: publicKey,
            template_params: {
                nombre: escapeHtml(cleanName),
                correo: cleanEmail,
                telefono: escapeHtml(cleanPhone || 'No proporcionado'),
                monto_calculado: escapeHtml(cleanMonto),
                tipo: escapeHtml(cleanTipo),
                fecha: new Date().toLocaleDateString('es-CL')
            }
        };

        if (privateKey) {
            payload.accessToken = privateKey;
        }

        const emailResponse = await fetch('https://api.emailjs.com/api/v1.0/email/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (emailResponse.ok) {
            return res.status(200).json({ success: true });
        }

        const errorText = await emailResponse.text();
        console.error('EmailJS REST error:', errorText);
        return res.status(502).json({ error: 'No se pudo procesar la solicitud.' });

    } catch (error) {
        console.error('Exception inside send-lead api route:', error);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
};
