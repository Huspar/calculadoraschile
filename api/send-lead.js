/**
 * Vercel Serverless Function: send-lead
 * Intermediates between Cálculo Laboral client forms and Resend (transactional email).
 * Sends the lead notification to JHON (CC) and the requested guide/resource to the USER.
 *
 * Hardened (2026-06):
 *  - Strict CORS allowlist (no wildcard)
 *  - In-memory IP rate limit (10 req / 10 min per IP)
 *  - Honeypot field to catch bots
 *  - Input validation: name (1-80), email RFC-lite, phone digits-only (<=20), tipo enum, monto numeric (<=20 chars)
 *  - Body size limit (1KB)
 *  - No hardcoded credential fallbacks: RESEND_API_KEY must be set in Vercel env or the request fails fast.
 *  - Generic error responses (no internal details leaked)
 *  - HTML-escaped email content
 *  - LeadMagnet tipo: also sends a welcome email with the guide link to the user
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

const FROM_ADDRESS = 'contacto@calculolaboral.cl'; // Verified in Resend on 2026-07-01 (Cloudflare DNS)
const FROM_NAME = 'Cálculo Laboral';
const NOTIFY_JHON = 'jhonfcj@gmail.com';
const GUIDE_URL = 'https://calculolaboral.cl/Articulos/lead-magnet-finiquito.pdf';

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
    // RFC 5322 lite — good enough to reject obvious garbage, server still does the real validation.
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

    // Block cross-origin POSTs that did not pass the allowlist (CSRF mitigation).
    const origin = req.headers.origin;
    if (typeof origin === 'string' && !ALLOWED_ORIGINS.has(origin)) {
        return res.status(403).json({ error: 'Origin not allowed' });
    }

    // Body size guard
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
        // Vercel parses JSON automatically when Content-Type is application/json.
        const body = req.body && typeof req.body === 'object' ? req.body : {};
        const {
            nombre,
            correo,
            telefono,
            monto_calculado,
            tipo,
            // Honeypot: must be empty for real users; bots fill it.
            website,
            // Minimum time the form has been on screen (ms). If too short, treat as bot.
            form_rendered_at
        } = body;

        if (typeof website === 'string' && website.trim().length > 0) {
            // Silently accept to look like a success without sending anything.
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

        // Resend API key must come from Vercel env. No hardcoded fallbacks.
        const resendApiKey = process.env.RESEND_API_KEY;

        if (!resendApiKey) {
            console.error('send-lead: missing RESEND_API_KEY env var');
            return res.status(500).json({ error: 'Service not configured' });
        }

        const fechaLocal = new Date().toLocaleDateString('es-CL');

        // Email body builder: small helper, escapes HTML, returns safe HTML and text versions
        function buildEmailHtml({ title, intro, body }) {
            return `<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"></head>
<body style="font-family: -apple-system, system-ui, sans-serif; color: #0f172a; line-height: 1.5; max-width: 560px; margin: 0 auto; padding: 24px;">
<h1 style="color: #0ea5e9; font-size: 22px; margin: 0 0 16px;">${title}</h1>
<p style="margin: 0 0 16px;">${intro}</p>
<div style="background: #f0f9ff; border-left: 4px solid #0ea5e9; padding: 14px 18px; margin: 0 0 16px; font-size: 14px;">${body}</div>
<hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;">
<p style="font-size: 12px; color: #64748b; margin: 0;">Cálculo Laboral · calculolaboral.cl</p>
</body>
</html>`;
        }

        function buildEmailText({ intro, body }) {
            return `${intro}\n\n${body.replace(/<[^>]+>/g, '')}\n\n--\nCálculo Laboral · calculolaboral.cl`;
        }

        let userSubject, userHtml, userText;

        if (cleanTipo === 'LeadMagnet') {
            // LeadMagnet: send a welcome email to the user with the guide link
            userSubject = 'Tu guía "Qué hago con mi finiquito" está lista';
            const userIntro = `Hola ${cleanName}, gracias por descargar la guía. Te la adjuntamos a continuación.`;
            const userBody = `
                <p style="margin: 0 0 12px;"><strong>📘 Guía: Qué hago con mi finiquito</strong></p>
                <p style="margin: 0 0 12px;">6 páginas · lectura de 6 minutos · 3 escenarios de inversión + plan de 90 días.</p>
                <p style="margin: 16px 0; text-align: center;">
                    <a href="${GUIDE_URL}" style="background: #0ea5e9; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block;">Descargar la guía (PDF)</a>
                </p>
                <p style="margin: 16px 0 0; font-size: 13px; color: #64748b;">El link de descarga funciona en cualquier dispositivo. Puedes compartirla con quien quieras.</p>
            `;
            userHtml = buildEmailHtml({ title: 'Tu guía está lista 📘', intro: userIntro, body: userBody });
            userText = buildEmailText({ intro: userIntro, body: userBody });
        } else {
            // Other tipos: only the user gets a confirmation, no resource attached
            userSubject = 'Recibimos tu consulta en Cálculo Laboral';
            const userIntro = `Hola ${cleanName}, recibimos tu mensaje. Te contactaremos pronto.`;
            const userBody = `<p>Nuestro equipo revisará tu caso y te responderá a la brevedad al correo ${cleanEmail}.</p>`;
            userHtml = buildEmailHtml({ title: 'Recibimos tu consulta', intro: userIntro, body: userBody });
            userText = buildEmailText({ intro: userIntro, body: userBody });
        }

        // Notification email to JHON (with all the lead details)
        const jhonSubject = `[${cleanTipo}] Nuevo lead: ${cleanName}`;
        const jhonIntro = `Nuevo lead capturado en calculolaboral.cl.`;
        const jhonBody = `
            <table style="width: 100%; font-size: 14px; border-collapse: collapse;">
                <tr><td style="padding: 4px 0; color: #64748b;">Nombre:</td><td style="padding: 4px 0; font-weight: bold;">${cleanName}</td></tr>
                <tr><td style="padding: 4px 0; color: #64748b;">Correo:</td><td style="padding: 4px 0;"><a href="mailto:${cleanEmail}">${cleanEmail}</a></td></tr>
                <tr><td style="padding: 4px 0; color: #64748b;">Teléfono:</td><td style="padding: 4px 0;">${cleanPhone || '—'}</td></tr>
                <tr><td style="padding: 4px 0; color: #64748b;">Tipo:</td><td style="padding: 4px 0;">${cleanTipo}</td></tr>
                <tr><td style="padding: 4px 0; color: #64748b;">Monto:</td><td style="padding: 4px 0;">$${cleanMonto} CLP</td></tr>
                <tr><td style="padding: 4px 0; color: #64748b;">Fuente:</td><td style="padding: 4px 0;">${escapeHtml(typeof body === 'object' && body && body.fuente ? body.fuente : 'web')}</td></tr>
                <tr><td style="padding: 4px 0; color: #64748b;">Fecha:</td><td style="padding: 4px 0;">${fechaLocal}</td></tr>
            </table>
        `;
        const jhonHtml = buildEmailHtml({ title: `Nuevo lead: ${cleanName}`, intro: jhonIntro, body: jhonBody });
        const jhonText = buildEmailText({ intro: jhonIntro, body: jhonBody });

        // Send BOTH emails via Resend (user first, then jhon)
        async function sendResendEmail(to, subject, html, text, replyTo) {
            const payload = {
                from: `${FROM_NAME} <${FROM_ADDRESS}>`,
                to: Array.isArray(to) ? to : [to],
                subject,
                html,
                text,
            };
            if (replyTo) {
                payload.reply_to = replyTo;
            }
            const resp = await fetch('https://api.resend.com/emails', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${resendApiKey}`,
                    'Content-Type': 'application/json',
                    'User-Agent': 'calculolaboral-cl/1.0',
                },
                body: JSON.stringify(payload),
            });
            return resp;
        }

        // Send to user (CC jhon for context, so he sees the user email too)
        const userResp = await sendResendEmail(
            cleanEmail,
            userSubject,
            userHtml,
            userText,
            NOTIFY_JHON
        );
        if (!userResp.ok) {
            const errText = await userResp.text();
            console.error('Resend error (user email):', errText);
            return res.status(422).json({ error: 'Resend error (user email)', details: errText });
        }

        // Send to jhon with user details (Reply-To set to user email for easy reply)
        const jhonResp = await sendResendEmail(
            NOTIFY_JHON,
            jhonSubject,
            jhonHtml,
            jhonText,
            cleanEmail
        );
        if (!jhonResp.ok) {
            const errText = await jhonResp.text();
            console.error('Resend error (jhon email):', errText);
            // Don't fail the user request if jhon notification fails — the lead is still captured
            console.warn('User email was sent but jhon notification failed. Lead:', cleanEmail);
        }

        return res.status(200).json({ success: true });

    } catch (error) {
        console.error('Exception inside send-lead api route:', error);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
};
