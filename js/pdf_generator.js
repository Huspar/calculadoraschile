/**
 * PDF Report Generator & Lead Capture System - Cálculo Laboral (2026)
 * Handles modal injection, email capture (opt-in), leads backup in localStorage,
 * and compiles pixel-perfect print sheets for native browser PDF export.
 */

(function () {
    // 1. INJECT MODAL HTML AND CSS ON PAGE LOAD
    window.addEventListener('DOMContentLoaded', () => {
        injectModalHTML();
        injectPrintStyles();
        setupEventListeners();
    });

    // 2. MODAL HTML TEMPLATE
    function injectModalHTML() {
        if (document.getElementById('pdf-email-modal')) return;

        const modalDiv = document.createElement('div');
        modalDiv.id = 'pdf-email-modal';
        modalDiv.className = 'fixed inset-0 z-[100] hidden items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4';
        modalDiv.innerHTML = `
            <div class="w-full max-w-md rounded-2xl p-6 shadow-2xl relative overflow-hidden border border-white/10 bg-[#1e293b] text-white" style="background: #1e293b; border-radius: 1rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">
                <!-- Decorative Top Bar -->
                <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-emerald-500 to-blue-600"></div>
                
                <!-- Header -->
                <div class="flex justify-between items-start mb-4 mt-2">
                    <div class="flex items-center gap-2">
                        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-blue-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
                            <span class="material-icons text-white text-sm">picture_as_pdf</span>
                        </div>
                        <h3 class="text-lg font-bold text-white">Descargar Reporte PDF</h3>
                    </div>
                    <button id="close-pdf-modal-btn" class="p-1 rounded-lg text-slate-400 hover:bg-white/5 hover:text-white transition-colors cursor-pointer" type="button">
                        <span class="material-icons">close</span>
                    </button>
                </div>
                
                <!-- Description -->
                <p class="text-sm text-slate-300 mb-5 leading-relaxed">
                    Ingresa tu correo electrónico para descargar al instante un informe estructurado con todo el desglose matemático y legal de tu simulación.
                </p>
                
                <!-- Form -->
                <form id="pdf-email-form" class="space-y-4">
                    <div>
                        <label for="pdf-email" class="block text-xs font-semibold text-slate-400 mb-2 ml-1">Correo Electrónico</label>
                        <input type="email" id="pdf-email" required
                            class="w-full px-4 py-3 bg-[#0f172a] border border-white/10 rounded-full text-white placeholder-slate-600 focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-sm transition-all"
                            placeholder="tu@correo.com" style="background-color: #0f172a; color: #ffffff;" />
                        <div id="pdf-email-error" class="hidden text-xs text-rose-400 mt-2 ml-2 font-medium"></div>
                    </div>
                    
                    <!-- Opt-in Checkbox -->
                    <label class="flex items-start gap-3 cursor-pointer group mt-4">
                        <input type="checkbox" id="pdf-marketing-optin" required
                            class="w-4 h-4 mt-0.5 rounded border-slate-700 bg-slate-950 text-emerald-500 focus:ring-emerald-500/50 cursor-pointer" />
                        <span class="text-xs text-slate-400 group-hover:text-slate-300 transition-colors leading-relaxed select-none">
                            Acepto recibir guías, ebooks y novedades sobre derechos laborales en Chile de acuerdo con la <a href="/privacidad" target="_blank" class="text-emerald-400 hover:underline font-semibold">Política de Privacidad</a>.
                        </span>
                    </label>
                    
                    <!-- Submit Button -->
                    <button type="submit"
                        class="w-full bg-gradient-to-r from-emerald-500 to-blue-600 hover:opacity-95 text-white font-bold py-3.5 px-6 rounded-full shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-2 cursor-pointer mt-6">
                        <span class="material-icons text-sm">download</span>
                        Generar y Descargar PDF
                    </button>
                </form>
            </div>
        `;
        document.body.appendChild(modalDiv);
    }

    // 3. INJECT PRINT STYLES (Strictly optimized for A4/Letter 1-page budget limits)
    function injectPrintStyles() {
        if (document.getElementById('pdf-print-styles')) return;

        const style = document.createElement('style');
        style.id = 'pdf-print-styles';
        style.innerHTML = `
            @media print {
                /* Set A4/Letter margins at the page level and force portrait orientation */
                @page {
                    size: portrait;
                    margin: 6mm 10mm 6mm 10mm !important;
                }
                /* Hide everything except print-section */
                body > *:not(#print-section) {
                    display: none !important;
                }
                /* Format printed page - restrict heights strictly to 1 page */
                html, body {
                    background: #ffffff !important;
                    color: #000000 !important;
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
                    font-size: 8pt !important;
                    line-height: 1.2 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    height: 100% !important;
                    max-height: 100% !important;
                    overflow: hidden !important;
                    page-break-after: avoid !important;
                    page-break-before: avoid !important;
                }
                #print-section {
                    display: block !important;
                    width: 100% !important;
                    height: 100% !important;
                    max-height: 100% !important;
                    overflow: hidden !important;
                    padding: 0 !important; /* Zero padding since page margin handles spacing */
                    background: #ffffff !important;
                    color: #000000 !important;
                    box-sizing: border-box !important;
                }
                .print-header {
                    border-bottom: 1.2px solid #0f172a !important;
                    padding-bottom: 4px !important;
                    margin-bottom: 8px !important;
                    display: flex !important;
                    justify-content: space-between !important;
                    align-items: flex-end !important;
                }
                .print-title {
                    font-size: 11pt !important;
                    font-weight: bold !important;
                    text-transform: uppercase !important;
                    margin-top: 0px !important;
                    margin-bottom: 2px !important;
                    color: #0f172a !important;
                }
                .print-section-title {
                    background: #f8fafc !important;
                    padding: 3px 6px !important;
                    font-size: 8.5pt !important;
                    font-weight: bold !important;
                    text-transform: uppercase !important;
                    border-left: 3px solid #10b981 !important;
                    margin-top: 8px !important;
                    margin-bottom: 4px !important;
                    color: #0f172a !important;
                }
                .print-table {
                    width: 100% !important;
                    border-collapse: collapse !important;
                    margin-bottom: 8px !important;
                }
                .print-table th {
                    text-align: left !important;
                    padding: 3px 5px !important;
                    font-size: 7.5pt !important;
                    border-bottom: 1px solid #cbd5e1 !important;
                    color: #475569 !important;
                }
                .print-table td {
                    padding: 3px 5px !important;
                    font-size: 8pt !important;
                    border-bottom: 1px solid #f1f5f9 !important;
                }
                .print-total-box {
                    border: 1.5px solid #10b981 !important;
                    background: #f0fdf4 !important;
                    padding: 6px 10px !important;
                    border-radius: 4px !important;
                    margin-top: 8px !important;
                    margin-bottom: 8px !important;
                    text-align: right !important;
                    page-break-inside: avoid !important;
                }
                .print-total-amount {
                    font-size: 14pt !important;
                    font-weight: 800 !important;
                    color: #15803d !important;
                }
                .print-disclaimer {
                    font-size: 6.8pt !important;
                    color: #64748b !important;
                    line-height: 1.2 !important;
                    border-top: 1px solid #cbd5e1 !important;
                    padding-top: 4px !important;
                    margin-top: 8px !important;
                    text-align: justify !important;
                    page-break-inside: avoid !important;
                }
                /* Prevent page-break on table rows and content blocks */
                tr, td, th, table, div, p {
                    page-break-inside: avoid !important;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // 4. SETUP EVENT LISTENERS
    function setupEventListeners() {
        const downloadBtn = document.getElementById('download-pdf-btn');
        const closeBtn = document.getElementById('close-pdf-modal-btn');
        const modal = document.getElementById('pdf-email-modal');
        const form = document.getElementById('pdf-email-form');
        const emailInput = document.getElementById('pdf-email');
        const emailError = document.getElementById('pdf-email-error');

        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => {
                // Verify that calculator is calculated
                if (!isCalculated()) {
                    alert("Por favor, realiza una simulación primero ingresando tus datos para generar el reporte.");
                    return;
                }
                modal.classList.remove('hidden');
                modal.classList.add('flex');
            });
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
                if (emailError) emailError.classList.add('hidden');
                if (emailInput) {
                    emailInput.classList.remove('border-rose-500', 'focus:ring-rose-500');
                    emailInput.classList.add('border-white/10', 'focus:ring-emerald-500');
                }
            });
        }

        // Clear errors as soon as user types
        if (emailInput && emailError) {
            emailInput.addEventListener('input', () => {
                emailError.classList.add('hidden');
                emailError.textContent = '';
                emailInput.classList.remove('border-rose-500', 'focus:ring-rose-500');
                emailInput.classList.add('border-white/10', 'focus:ring-emerald-500');
            });
        }

        // Close when clicking outside content card
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.add('hidden');
                    modal.classList.remove('flex');
                    if (emailError) emailError.classList.add('hidden');
                    if (emailInput) {
                        emailInput.classList.remove('border-rose-500', 'focus:ring-rose-500');
                        emailInput.classList.add('border-white/10', 'focus:ring-emerald-500');
                    }
                }
            });
        }

        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const email = emailInput ? emailInput.value.trim() : '';
                const optin = document.getElementById('pdf-marketing-optin').checked;

                if (email) {
                    const validation = isValidRealEmail(email);
                    if (!validation.valid) {
                        if (emailError && emailInput) {
                            emailError.textContent = validation.message;
                            emailError.classList.remove('hidden');
                            emailInput.classList.remove('border-white/10', 'focus:ring-emerald-500');
                            emailInput.classList.add('border-rose-500', 'focus:ring-rose-500');
                            emailInput.focus();
                        }
                        return;
                    }

                    if (optin) {
                        // Save lead to local database (localStorage)
                        saveLead(email);
                        
                        // Generate report print
                        generatePDFReport();

                        // Close modal and reset form
                        modal.classList.add('hidden');
                        modal.classList.remove('flex');
                        form.reset();
                        if (emailError) emailError.classList.add('hidden');
                        if (emailInput) {
                            emailInput.classList.remove('border-rose-500', 'focus:ring-rose-500');
                            emailInput.classList.add('border-white/10', 'focus:ring-emerald-500');
                        }
                    }
                }
            });
        }
    }

    // 5. HELPER: STRICT EMAIL VALIDATION (Blocks fake, temp, and test emails)
    function isValidRealEmail(email) {
        email = email.trim().toLowerCase();
        
        // 5.1 Basic Syntax Check with a strict regex
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailRegex.test(email)) {
            return { valid: false, message: "Por favor, ingresa una dirección de correo válida." };
        }

        const [localPart, domain] = email.split('@');

        // 5.2 Block obvious test/fake local parts or domains
        const blockedLocalParts = [
            'test', 'testing', 'prueba', 'pruebas', 'correo', 'email', 'asdf', 'qwer', 'zxcv', 
            'abc', 'admin', 'soporte', 'support', 'info', 'no-reply', 'noreply', 'asd', '123',
            '1234', '12345', 'ninguno', 'dummy', 'fake', 'user', 'usuario', 'a', 'b', 'c', 'x'
        ];
        
        const blockedDomains = [
            'test.com', 'test.cl', 'example.com', 'example.org', 'example.net', 
            'correo.com', 'correo.cl', 'prueba.com', 'prueba.cl', 'email.com', 'email.cl',
            'asd.com', 'asdf.com', 'xyz.com', 'abc.com', '123.com', '123.cl', 
            'none.com', 'no.com', 'domain.com', 'domain.cl', 'mail.com'
        ];

        if (blockedLocalParts.includes(localPart) || localPart.length < 3) {
            return { valid: false, message: "Por favor, ingresa un correo personal o laboral real." };
        }

        if (blockedDomains.includes(domain)) {
            return { valid: false, message: "Este dominio de correo no parece ser válido o real." };
        }

        // 5.3 Block disposable/temporary email domains
        const disposableDomains = [
            'yopmail.com', 'yopmail.fr', 'yopmail.net', 'tempmail.com', 'tempmailo.com', 
            '10minutemail.com', 'guerrillamail.com', 'trashmail.com', 'sharklasers.com', 
            'mailinator.com', 'getairmail.com', 'dispostable.com', 'burnermail.io', 
            'maildrop.cc', 'temp-mail.org', 'fakemailgenerator.com', 'throwawaymail.com', 
            'emailondeck.com', 'crazymailing.com', 'boun.cr', 'jetable.org', 'tempail.com',
            'mohmal.com', 'guerrillamailblock.com', 'guerrillamail.net', 'guerrillamail.org',
            'guerrillamail.biz', 'grr.la', 'pokemail.net', 'torbox.com'
        ];

        if (disposableDomains.some(disposable => domain === disposable || domain.endsWith('.' + disposable))) {
            return { valid: false, message: "No se permiten correos electrónicos temporales o desechables." };
        }

        return { valid: true };
    }

    // 6. HELPER: CHECK IF CALCULATOR IS GENUINELY CALCULATED WITH REAL INPUTS
    function isCalculated() {
        // For Finiquito
        const totalFiniElement = document.getElementById('totalAmount');
        if (totalFiniElement) {
            const startDate = document.getElementById('startDate')?.value;
            const endDate = document.getElementById('endDate')?.value;
            const baseSalary = document.getElementById('baseSalary')?.value;
            
            // If main inputs are completely empty or negative, it's not calculated
            if (!startDate || !endDate || !baseSalary || parseFloat(baseSalary) <= 0) {
                return false;
            }
            
            const val = totalFiniElement.textContent.trim();
            // Should not be the default placeholder value, error, or empty reset states
            return val !== '' && val !== '$6.850.250' && val !== '$ — CLP' && !val.includes('Error');
        }

        // For Sueldo Liquido
        const netSalElement = document.getElementById('headerNetSalary');
        if (netSalElement) {
            const salary = document.getElementById('salary')?.value;
            
            // If main input is empty or negative/zero, it's not calculated
            if (!salary || parseFloat(salary) <= 0) {
                return false;
            }
            
            const val = netSalElement.textContent.trim();
            // Should not be the default zero placeholder or error states
            return val !== '' && val !== '$0' && val !== '$ --' && !val.includes('Error');
        }

        return false;
    }

    // 6. HELPER: SAVE EMAIL LEAD TO LOCAL STORAGE DATABASE
    function saveLead(email) {
        try {
            const leads = JSON.parse(localStorage.getItem('pdf_leads') || '[]');
            const pageType = window.location.pathname.includes('sueldo') ? 'sueldo_liquido' : 'finiquito';
            
            // Avoid duplicates
            if (!leads.some(l => l.email === email && l.type === pageType)) {
                leads.push({
                    email: email,
                    date: new Date().toISOString(),
                    type: pageType
                });
                localStorage.setItem('pdf_leads', JSON.stringify(leads));
                console.log("Lead guardado localmente:", email);
            }
            
            // Here you could send the lead to a Google Sheet Webhook if configured:
            // fetch('YOUR_APPS_SCRIPT_WEBHOOK_URL', {
            //     method: 'POST',
            //     body: JSON.stringify({ email: email, type: pageType })
            // });
        } catch (e) {
            console.error("Error al guardar lead:", e);
        }
    }

    // 7. MAIN FUNCTION: GENERATE PRINT REPORT AND TRIGGER WINDOW.PRINT
    function generatePDFReport() {
        const isSueldoPage = window.location.pathname.includes('sueldo');
        
        // Remove existing print section
        const oldSection = document.getElementById('print-section');
        if (oldSection) oldSection.remove();

        const printSection = document.createElement('div');
        printSection.id = 'print-section';
        printSection.style.display = 'none';

        const currentDate = new Date().toLocaleDateString('es-CL', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });

        let htmlContent = '';

        if (isSueldoPage) {
            htmlContent = compileSueldoReport(currentDate);
        } else {
            htmlContent = compileFiniquitoReport(currentDate);
        }

        printSection.innerHTML = htmlContent;
        document.body.appendChild(printSection);

        // Wait a tiny bit for render, then print
        setTimeout(() => {
            window.print();
            // Clean up print section after dialog close
            setTimeout(() => {
                const sec = document.getElementById('print-section');
                if (sec) sec.remove();
            }, 1000);
        }, 100);
    }

    // 8. COMPILE FINIQUITO REPORT
    function compileFiniquitoReport(dateString) {
        // Query results safely from DOM
        const total = document.getElementById('totalAmount')?.textContent || '$0';
        const antiquity = document.getElementById('antiquityOutput')?.textContent || 'No especificada';
        const vacationDays = document.getElementById('totalVacationDaysOutput')?.textContent || '0 días';
        
        const yearsService = document.getElementById('yearsServiceAmount')?.textContent || '$0';
        const noticeAmount = document.getElementById('noticeAmount')?.textContent || '$0';
        const pendingSalary = document.getElementById('pendingSalaryAmount')?.textContent || '$0';
        const vacationProp = document.getElementById('vacationPropAmount')?.textContent || '$0';
        const vacationPending = document.getElementById('vacationPendingAmount')?.textContent || '$0';
        
        // AFC Deduction (if displayed or not hidden)
        const afcRow = document.getElementById('afcRow');
        const afcAmount = (afcRow && !afcRow.classList.contains('hidden')) 
            ? document.getElementById('afcAmount')?.textContent 
            : '$0';

        // Query input values for general details
        const startDateVal = document.getElementById('startDate')?.value || '--';
        const endDateVal = document.getElementById('endDate')?.value || '--';
        const baseSalary = document.getElementById('baseSalary')?.value || '0';
        const assignments = document.getElementById('assignments')?.value || '0';
        
        const causeSelect = document.getElementById('cause');
        const cause = causeSelect ? causeSelect.options[causeSelect.selectedIndex]?.text : 'No especificada';
        
        const noticeCheckbox = document.getElementById('noticeGiven');
        const noticeText = (noticeCheckbox && noticeCheckbox.checked) ? 'Sí' : 'No';

        return `
            <div class="print-header">
                <div>
                    <h2 style="margin: 0; font-size: 13pt; font-weight: bold; color: #0f172a;">CÁLCULO LABORAL</h2>
                    <span style="font-size: 7.5pt; color: #64748b;">www.calculolaboral.cl</span>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 8.5pt; font-weight: bold; color: #64748b;">SIMULACIÓN DE FINIQUITO</span><br>
                    <span style="font-size: 7.5pt; color: #94a3b8;">Fecha: ${dateString}</span>
                </div>
            </div>

            <div class="print-title">Reporte de Simulación de Finiquito</div>
            <p style="font-size: 8pt; color: #64748b; margin-top: 0; margin-bottom: 8px;">
                Este documento muestra el desglose del finiquito laboral estimado según la legislación chilena vigente.
            </p>

            <!-- Column Layout: Resumen del Contrato and Bases de Cálculo side by side -->
            <div style="display: flex; gap: 15px; margin-bottom: 5px; width: 100%;">
                <div style="flex: 1; min-width: 0;">
                    <div class="print-section-title" style="margin-top: 0; margin-bottom: 4px;">1. Resumen del Contrato</div>
                    <table class="print-table">
                        <tr>
                            <td style="font-weight: bold; width: 45%;">Inicio:</td>
                            <td>${formatInputDate(startDateVal)}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: bold;">Término:</td>
                            <td>${formatInputDate(endDateVal)}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: bold;">Antigüedad:</td>
                            <td>${antiquity}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: bold;">Causal:</td>
                            <td>${cause}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: bold;">¿Aviso previo?:</td>
                            <td>${noticeText}</td>
                        </tr>
                    </table>
                </div>
                <div style="width: 42%; min-width: 0;">
                    <div class="print-section-title" style="margin-top: 0; margin-bottom: 4px;">2. Bases de Cálculo</div>
                    <table class="print-table">
                        <tr>
                            <td style="font-weight: bold; width: 50%;">Sueldo Base:</td>
                            <td>$${formatNumber(parseInt(baseSalary || 0))} CLP</td>
                        </tr>
                        <tr>
                            <td style="font-weight: bold;">Haberes no Imp.:</td>
                            <td>$${formatNumber(parseInt(assignments || 0))} CLP</td>
                        </tr>
                    </table>
                </div>
            </div>

            <div class="print-section-title" style="margin-top: 4px; margin-bottom: 4px;">3. Detalle de Indemnizaciones y Haberes a Pagar</div>
            <table class="print-table" style="margin-bottom: 6px;">
                <thead>
                    <tr>
                        <th style="width: 70%; padding: 2px 5px !important;">Concepto</th>
                        <th style="text-align: right; padding: 2px 5px !important;">Monto Estimado</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 2px 5px !important;">Indemnización por Años de Servicio</td>
                        <td style="text-align: right; font-weight: 500; padding: 2px 5px !important;">${yearsService}</td>
                    </tr>
                    <tr>
                        <td style="padding: 2px 5px !important;">Indemnización Sustitutiva del Aviso Previo (Mes de Aviso)</td>
                        <td style="text-align: right; font-weight: 500; padding: 2px 5px !important;">${noticeAmount}</td>
                    </tr>
                    <tr>
                        <td style="padding: 2px 5px !important;">Feriado Proporcional (Vacaciones Acumuladas: ${vacationDays})</td>
                        <td style="text-align: right; font-weight: 500; padding: 2px 5px !important;">${vacationProp}</td>
                    </tr>
                    <tr>
                        <td style="padding: 2px 5px !important;">Feriado Legal Pendiente (Vacaciones anteriores)</td>
                        <td style="text-align: right; font-weight: 500; padding: 2px 5px !important;">${vacationPending}</td>
                    </tr>
                    <tr>
                        <td style="padding: 2px 5px !important;">Remuneraciones del Mes Pendientes (Días Trabajados)</td>
                        <td style="text-align: right; font-weight: 500; padding: 2px 5px !important;">${pendingSalary}</td>
                    </tr>
                    ${afcAmount !== '$0' && afcAmount !== '0' && afcAmount !== '' ? `
                    <tr style="color: #b91c1c;">
                        <td style="padding: 2px 5px !important;">Descuento Aporte AFC Empleador (Art. 13 Ley 19.728)</td>
                        <td style="text-align: right; font-weight: 500; padding: 2px 5px !important;">-${afcAmount}</td>
                    </tr>
                    ` : ''}
                </tbody>
            </table>

            <div class="print-total-box" style="margin-top: 4px; margin-bottom: 6px; padding: 5px 10px !important;">
                <span style="font-size: 8.5pt; font-weight: bold; text-transform: uppercase; color: #475569; display: block; margin-bottom: 2px;">Monto Total Neto Estimado</span>
                <span class="print-total-amount" style="font-size: 13.5pt !important;">${total}</span> <span style="font-size: 10pt; font-weight: bold; color: #15803d;">CLP</span>
            </div>

            <div class="print-disclaimer" style="margin-top: 4px; padding-top: 4px; font-size: 6.5pt !important; line-height: 1.15 !important;">
                <strong>NOTA DE CARÁCTER INFORMATIVO:</strong> Este documento representa una simulación matemática basada en los datos ingresados voluntariamente por el usuario y los parámetros regulatorios vigentes en Chile. No tiene validez legal oficial ante juzgados o notarías, ni constituye un finiquito oficial.<br>
                <strong>DESCARGO DE RESPONSABILIDAD:</strong> Esta simulación se ofrece de manera gratuita y con propósitos educativos. Los cálculos de finiquitos reales están condicionados por elementos particulares (créditos sociales vigentes, cotizaciones adeudadas, cláusulas específicas del contrato, etc.). Cálculo Laboral no asume responsabilidad alguna por interpretaciones o decisiones basadas en esta simulación. Se sugiere validar el borrador con la Inspección del Trabajo o un abogado laboral.
            </div>
        `;
    }

    // 9. COMPILE SUELDO REPORT
    function compileSueldoReport(dateString) {
        // Query results safely from DOM
        const netSalary = document.getElementById('headerNetSalary')?.textContent || '$0';
        const totalDiscounts = document.getElementById('headerTotalDiscounts')?.textContent || '$0';
        
        const afp = document.getElementById('resultAFP')?.textContent || '$0';
        const health = document.getElementById('resultHealth')?.textContent || '$0';
        const afc = document.getElementById('resultAFC')?.textContent || '$0';
        const tax = document.getElementById('resultTax')?.textContent || '$0';

        const labelAFP = document.getElementById('labelAFP')?.textContent || 'Modelo';
        const labelHealth = document.getElementById('labelHealth')?.textContent || '7%';

        // Input values
        const baseSalary = document.getElementById('salary')?.value || '0';
        const overtimeHours = document.getElementById('overtime')?.value || '0';
        const bonuses = document.getElementById('bonuses')?.value || '0';
        
        const colacion = document.getElementById('colacion')?.value || '0';
        const movilizacion = document.getElementById('movilizacion')?.value || '0';
        const viaticos = document.getElementById('viaticos')?.value || '0';

        // Additional discounts
        const ccaf = document.getElementById('ccaf')?.value || '0';
        const apv = document.getElementById('apv')?.value || '0';
        const prestamos = document.getElementById('prestamos')?.value || '0';
        const pension = document.getElementById('pension')?.value || '0';
        const sindicato = document.getElementById('sindicato')?.value || '0';
        const otrosDescuentos = document.getElementById('otrosDescuentos')?.value || '0';

        return `
            <div class="print-header">
                <div>
                    <h2 style="margin: 0; font-size: 13pt; font-weight: bold; color: #0f172a;">CÁLCULO LABORAL</h2>
                    <span style="font-size: 7.5pt; color: #64748b;">www.calculolaboral.cl</span>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 8.5pt; font-weight: bold; color: #64748b;">SIMULACIÓN DE SUELDO LÍQUIDO</span><br>
                    <span style="font-size: 7.5pt; color: #94a3b8;">Fecha: ${dateString}</span>
                </div>
            </div>

            <div class="print-title">Reporte de Simulación de Sueldo Líquido</div>
            <p style="font-size: 8pt; color: #64748b; margin-top: 0; margin-bottom: 8px;">
                Este documento muestra el desglose del sueldo bruto imponible, no imponible y descuentos previsionales aplicados.
            </p>

            <!-- Column Layout: Haberes and Descuentos Previsionales side by side -->
            <div style="display: flex; gap: 15px; margin-bottom: 5px; width: 100%;">
                <div style="flex: 1; min-width: 0;">
                    <div class="print-section-title" style="margin-top: 0; margin-bottom: 4px;">1. Haberes (Ingresos)</div>
                    <table class="print-table">
                        <thead>
                            <tr>
                                <th style="width: 60%; padding: 2px 5px !important;">Concepto</th>
                                <th style="text-align: right; padding: 2px 5px !important;">Monto</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="padding: 2px 5px !important;">Sueldo Base Mensual</td>
                                <td style="text-align: right; font-weight: 500; padding: 2px 5px !important;">$${formatNumber(parseInt(baseSalary || 0))} CLP</td>
                            </tr>
                            <tr>
                                <td style="padding: 2px 5px !important;">Horas Extras (${overtimeHours} horas)</td>
                                <td style="text-align: right; font-weight: 500; padding: 2px 5px !important;">(Incluidas en liquidación)</td>
                            </tr>
                            ${bonuses !== '0' && bonuses !== '' ? `
                            <tr>
                                <td style="padding: 2px 5px !important;">Bonos e Imponibles</td>
                                <td style="text-align: right; font-weight: 500; padding: 2px 5px !important;">$${formatNumber(parseInt(bonuses || 0))} CLP</td>
                            </tr>
                            ` : ''}
                            <tr>
                                <td style="font-weight: bold; background-color: #f8fafc; padding: 2px 5px !important;">Haberes No Imponibles</td>
                                <td style="text-align: right; font-weight: bold; background-color: #f8fafc; padding: 2px 5px !important;">$${formatNumber(parseInt(colacion || 0) + parseInt(movilizacion || 0) + parseInt(viaticos || 0))} CLP</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div style="flex: 1; min-width: 0;">
                    <div class="print-section-title" style="margin-top: 0; margin-bottom: 4px;">2. Descuentos Previsionales</div>
                    <table class="print-table">
                        <thead>
                            <tr>
                                <th style="width: 60%; padding: 2px 5px !important;">Descuento Obligatorio</th>
                                <th style="text-align: right; padding: 2px 5px !important;">Monto Retenido</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="padding: 2px 5px !important;">AFP (Tasa ${labelAFP})</td>
                                <td style="text-align: right; font-weight: 500; color: #b91c1c; padding: 2px 5px !important;">-${afp}</td>
                            </tr>
                            <tr>
                                <td style="padding: 2px 5px !important;">Salud (${labelHealth})</td>
                                <td style="text-align: right; font-weight: 500; color: #b91c1c; padding: 2px 5px !important;">-${health}</td>
                            </tr>
                            <tr>
                                <td style="padding: 2px 5px !important;">Seguro de Cesantía AFC</td>
                                <td style="text-align: right; font-weight: 500; color: #b91c1c; padding: 2px 5px !important;">-${afc}</td>
                            </tr>
                            <tr>
                                <td style="padding: 2px 5px !important;">Impuesto 2ª Categoría</td>
                                <td style="text-align: right; font-weight: 500; color: #b91c1c; padding: 2px 5px !important;">-${tax}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            ${ccaf !== '0' || apv !== '0' || prestamos !== '0' || pension !== '0' || sindicato !== '0' || otrosDescuentos !== '0' ? `
            <div class="print-section-title" style="margin-top: 4px; margin-bottom: 4px;">3. Otros Descuentos Aplicados (Adicionales)</div>
            <table class="print-table" style="margin-bottom: 6px;">
                <thead>
                    <tr>
                        <th style="width: 70%; padding: 2px 5px !important;">Descuento Adicional</th>
                        <th style="text-align: right; padding: 2px 5px !important;">Monto</th>
                    </tr>
                </thead>
                <tbody>
                    ${ccaf !== '0' && ccaf !== '' ? `<tr><td style="padding: 2px 5px !important;">Caja Compensación (CCAF)</td><td style="text-align: right; color: #b91c1c; padding: 2px 5px !important;">-$${formatNumber(parseInt(ccaf || 0))} CLP</td></tr>` : ''}
                    ${apv !== '0' && apv !== '' ? `<tr><td style="padding: 2px 5px !important;">APV (Ahorro Previsional Voluntario)</td><td style="text-align: right; color: #b91c1c; padding: 2px 5px !important;">-$${formatNumber(parseInt(apv || 0))} CLP</td></tr>` : ''}
                    ${prestamos !== '0' && prestamos !== '' ? `<tr><td style="padding: 2px 5px !important;">Préstamos de la Empresa</td><td style="text-align: right; color: #b91c1c; padding: 2px 5px !important;">-$${formatNumber(parseInt(prestamos || 0))} CLP</td></tr>` : ''}
                    ${pension !== '0' && pension !== '' ? `<tr><td style="padding: 2px 5px !important;">Pensión Alimenticia</td><td style="text-align: right; color: #b91c1c; padding: 2px 5px !important;">-$${formatNumber(parseInt(pension || 0))} CLP</td></tr>` : ''}
                    ${sindicato !== '0' && sindicato !== '' ? `<tr><td style="padding: 2px 5px !important;">Cuota Sindical</td><td style="text-align: right; color: #b91c1c; padding: 2px 5px !important;">-$${formatNumber(parseInt(sindicato || 0))} CLP</td></tr>` : ''}
                    ${otrosDescuentos !== '0' && otrosDescuentos !== '' ? `<tr><td style="padding: 2px 5px !important;">Otros Descuentos Diversos</td><td style="text-align: right; color: #b91c1c; padding: 2px 5px !important;">-$${formatNumber(parseInt(otrosDescuentos || 0))} CLP</td></tr>` : ''}
                </tbody>
            </table>
            ` : ''}

            <div class="print-total-box" style="margin-top: 4px; margin-bottom: 6px; padding: 5px 10px !important;">
                <span style="font-size: 8.5pt; font-weight: bold; text-transform: uppercase; color: #475569; display: block; margin-bottom: 2px;">Sueldo Líquido Estimado a Recibir</span>
                <span class="print-total-amount" style="font-size: 13.5pt !important;">${netSalary}</span> <span style="font-size: 10pt; font-weight: bold; color: #15803d;">CLP</span>
                <div style="font-size: 7.5pt; color: #64748b; margin-top: 1px;">Total descuentos descontados de la liquidación: ${totalDiscounts}</div>
            </div>

            <div class="print-disclaimer" style="margin-top: 4px; padding-top: 4px; font-size: 6.5pt !important; line-height: 1.15 !important;">
                <strong>NOTA DE CARÁCTER INFORMATIVO:</strong> Este documento representa una simulación matemática basada en los datos ingresados voluntariamente por el usuario y los parámetros regulatorios vigentes en Chile. No tiene validez legal oficial ante el empleador, la Inspección del Trabajo o tribunales de justicia.<br>
                <strong>DESCARGO DE RESPONSABILIDAD:</strong> Esta simulación se ofrece de manera gratuita y con propósitos informativos generales. Los cálculos definitivos de remuneraciones están supeditados a regulaciones contractuales individuales, días de inasistencia, licencias médicas, y otros haberes variables del mes. Cálculo Laboral no asume responsabilidad alguna por interpretaciones o decisiones basadas en esta simulación.
            </div>
        `;
    }

    // 10. FORMAT HELPERS
    function formatInputDate(dateStr) {
        if (!dateStr || dateStr === '--') return '--';
        const parts = dateStr.split('-');
        if (parts.length === 3) {
            return `${parts[2]}/${parts[1]}/${parts[0]}`;
        }
        return dateStr;
    }

    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }
})();
