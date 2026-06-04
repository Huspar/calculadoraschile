/**
 * Vercel Serverless Function: send-lead
 * Intermediates between Cálculo Laboral client forms and EmailJS API.
 * Keeps EmailJS credentials secure and supports server-side private tokens.
 */
module.exports = async (req, res) => {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader(
        'Access-Control-Allow-Headers',
        'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
    );

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        res.setHeader('Allow', ['POST']);
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { nombre, correo, telefono, monto_calculado, tipo } = req.body;

        if (!nombre || !correo) {
            return res.status(400).json({ error: 'Nombre y correo son obligatorios.' });
        }

        // EmailJS credentials from environment variables with fallbacks
        const serviceId = process.env.EMAILJS_SERVICE_ID || 'service_plsair4';
        const templateId = process.env.EMAILJS_TEMPLATE_ID || 'template_u1juvx1';
        const publicKey = process.env.EMAILJS_PUBLIC_KEY || 'HIi9_S1hAf7mWQU_W';
        const privateKey = process.env.EMAILJS_PRIVATE_KEY; // Safer token validation

        // EmailJS REST API payload format
        const payload = {
            service_id: serviceId,
            template_id: templateId,
            user_id: publicKey,
            template_params: {
                nombre: nombre,
                correo: correo,
                telefono: telefono || 'No proporcionado',
                monto_calculado: monto_calculado || '0',
                tipo: tipo || 'Finiquito',
                fecha: new Date().toLocaleDateString('es-CL')
            }
        };

        if (privateKey) {
            payload.accessToken = privateKey;
        }

        // Native Node fetch call
        const emailResponse = await fetch('https://api.emailjs.com/api/v1.0/email/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (emailResponse.ok) {
            return res.status(200).json({ success: true });
        } else {
            const errorText = await emailResponse.text();
            console.error('EmailJS REST error details:', errorText);
            return res.status(500).json({ error: 'Error al enviar lead a EmailJS.', details: errorText });
        }

    } catch (error) {
        console.error('Exception inside send-lead api route:', error);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
};
