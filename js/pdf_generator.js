/**
 * PDF Report Generator & Lead Capture System - Cálculo Laboral (2026)
 * Handles modal injection, email capture (opt-in), leads backup in localStorage,
 * and compiles pixel-perfect print sheets for native browser PDF export.
 */

(function () {
    // CONFIGURACIÓN DE LEADS: Reemplaza con la URL de tu Google Apps Script desplegado
    const WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycby81-BL0hip010mshIYnpCwTMHKJYEcyNVrZyKZeoRJDi3_MQ4UWEC7gf2HxhcJ4iL1Ug/exec';

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

    // 3. INJECT PRINT STYLES (Premium A4 single-page design)
    function injectPrintStyles() {
        if (document.getElementById('pdf-print-styles')) return;

        const style = document.createElement('style');
        style.id = 'pdf-print-styles';
        style.innerHTML = `
            @media print {
                @page {
                    size: portrait;
                    margin: 8mm 12mm 8mm 12mm !important;
                }
                body > *:not(#print-section) {
                    display: none !important;
                }
                html, body {
                    background: #ffffff !important;
                    color: #1e293b !important;
                    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
                    font-size: 8.5pt !important;
                    line-height: 1.35 !important;
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
                    padding: 0 !important;
                    background: #ffffff !important;
                    color: #1e293b !important;
                    box-sizing: border-box !important;
                }
                .print-header {
                    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%) !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    color: #ffffff !important;
                    padding: 12px 16px !important;
                    border-radius: 6px !important;
                    margin-bottom: 10px !important;
                    display: flex !important;
                    justify-content: space-between !important;
                    align-items: center !important;
                    position: relative !important;
                    overflow: hidden !important;
                }
                .print-header::after {
                    content: '' !important;
                    position: absolute !important;
                    top: 0 !important;
                    right: 0 !important;
                    width: 120px !important;
                    height: 100% !important;
                    background: linear-gradient(135deg, transparent 0%, rgba(16,185,129,0.15) 100%) !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
                .print-title {
                    font-size: 11pt !important;
                    font-weight: 700 !important;
                    text-transform: uppercase !important;
                    letter-spacing: 0.3px !important;
                    margin-top: 0px !important;
                    margin-bottom: 3px !important;
                    color: #0f172a !important;
                }
                .print-section-title {
                    background: linear-gradient(90deg, #f0fdf4 0%, #f8fafc 100%) !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    padding: 4px 8px !important;
                    font-size: 8pt !important;
                    font-weight: 700 !important;
                    text-transform: uppercase !important;
                    letter-spacing: 0.5px !important;
                    border-left: 3px solid #10b981 !important;
                    border-bottom: 1px solid #e2e8f0 !important;
                    margin-top: 8px !important;
                    margin-bottom: 5px !important;
                    color: #0f172a !important;
                }
                .print-table {
                    width: 100% !important;
                    border-collapse: collapse !important;
                    margin-bottom: 8px !important;
                }
                .print-table th {
                    text-align: left !important;
                    padding: 4px 8px !important;
                    font-size: 7.5pt !important;
                    font-weight: 600 !important;
                    text-transform: uppercase !important;
                    letter-spacing: 0.3px !important;
                    border-bottom: 2px solid #10b981 !important;
                    color: #475569 !important;
                    background: #f8fafc !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
                .print-table td {
                    padding: 4px 8px !important;
                    font-size: 8pt !important;
                    border-bottom: 1px solid #e2e8f0 !important;
                }
                .print-table tr:nth-child(even) td {
                    background: #f8fafc !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
                .print-total-box {
                    border: 2px solid #10b981 !important;
                    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 50%, #d1fae5 100%) !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    padding: 8px 14px !important;
                    border-radius: 6px !important;
                    margin-top: 8px !important;
                    margin-bottom: 8px !important;
                    text-align: right !important;
                    page-break-inside: avoid !important;
                }
                .print-total-amount {
                    font-size: 16pt !important;
                    font-weight: 800 !important;
                    color: #047857 !important;
                    letter-spacing: -0.5px !important;
                }
                .print-disclaimer {
                    font-size: 6.5pt !important;
                    color: #94a3b8 !important;
                    line-height: 1.25 !important;
                    border-top: 1px solid #e2e8f0 !important;
                    padding-top: 5px !important;
                    margin-top: 6px !important;
                    text-align: justify !important;
                    page-break-inside: avoid !important;
                }
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
            const leadData = {
                email: email,
                date: new Date().toISOString(),
                type: pageType,
                userAgent: navigator.userAgent
            };
            
            // Avoid duplicates
            if (!leads.some(l => l.email === email && l.type === pageType)) {
                leads.push(leadData);
                localStorage.setItem('pdf_leads', JSON.stringify(leads));
                console.log("Lead guardado localmente:", email);
            }
            
            // Envío asíncrono al Webhook de Google Sheets si está configurado
            if (WEBHOOK_URL && WEBHOOK_URL.trim() !== '') {
                fetch(WEBHOOK_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'text/plain;charset=utf-8'
                    },
                    body: JSON.stringify(leadData),
                    redirect: 'follow'
                })
                .then(response => response.text())
                .then(result => {
                    console.log("Lead sincronizado con Google Sheets:", result);
                })
                .catch(err => {
                    console.warn("No se pudo sincronizar el lead con Google Sheets:", err);
                });
            }
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
        // Generate unique folio: YYYYMMDD-XXXXX
        const now = new Date();
        const folioDate = now.getFullYear().toString() + String(now.getMonth() + 1).padStart(2, '0') + String(now.getDate()).padStart(2, '0');
        const folioRandom = Math.random().toString(36).substring(2, 7).toUpperCase();
        const folio = `FIN-${folioDate}-${folioRandom}`;

        // Economic indicators from CONSTANTS (global)
        const uf = (typeof CONSTANTS !== 'undefined' && CONSTANTS.UF) ? CONSTANTS.UF : '--';
        const utm = (typeof CONSTANTS !== 'undefined' && CONSTANTS.UTM) ? CONSTANTS.UTM : '--';
        const imm = (typeof CONSTANTS !== 'undefined' && CONSTANTS.IMM) ? CONSTANTS.IMM : '--';

        // Query results safely from DOM
        const total = document.getElementById('totalAmount')?.textContent || '$0';
        const antiquity = document.getElementById('antiquityOutput')?.textContent || 'No especificada';
        const vacationDays = document.getElementById('totalVacationDaysOutput')?.textContent || '0 días';
        
        const yearsService = document.getElementById('yearsServiceAmount')?.textContent || '$0';
        const noticeAmount = document.getElementById('noticeAmount')?.textContent || '$0';
        const pendingSalary = document.getElementById('pendingSalaryAmount')?.textContent || '$0';
        const vacationProp = document.getElementById('vacationPropAmount')?.textContent || '$0';
        const vacationPendingAmt = document.getElementById('vacationPendingAmount')?.textContent || '$0';
        
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

        // --- NEW: Income tab fields ---
        const hasVariableSalary = document.getElementById('hasVariableSalary')?.checked || false;
        const varMonth1 = document.getElementById('varMonth1')?.value || '0';
        const varMonth2 = document.getElementById('varMonth2')?.value || '0';
        const varMonth3 = document.getElementById('varMonth3')?.value || '0';
        const variableAverage = document.getElementById('variableAverageOutput')?.textContent || '$0';

        const gratification = document.getElementById('gratification')?.value || '0';
        const vacPendingDays = document.getElementById('vacationPending')?.value || '0';
        const includeAssignInVac = document.getElementById('includeAssignmentsInVacation')?.checked || false;

        // --- NEW: Advanced options tab fields ---
        const enableIAS = document.getElementById('enableIAS')?.checked ?? true;
        const enableNotice = document.getElementById('enableNotice')?.checked ?? true;
        const simulateAFC = document.getElementById('simulateAFC')?.checked || false;
        const enablePending = document.getElementById('enablePending')?.checked ?? true;
        const includeAssignInIndem = document.getElementById('includeAssignmentsInIndemnity')?.checked || false;

        // Helper: build variable salary rows for Bases de Cálculo
        let variableSalaryRows = '';
        if (hasVariableSalary) {
            variableSalaryRows = `
                        <tr>
                            <td style="font-weight: bold;">Sueldo Variable:</td>
                            <td>Sí (prom. ${variableAverage})</td>
                        </tr>`;
        }

        // Helper: gratification row
        let gratificationRow = '';
        const gratVal = parseInt(gratification || 0);
        if (gratVal > 0) {
            gratificationRow = `
                        <tr>
                            <td style="font-weight: bold;">Gratificación Art. 50:</td>
                            <td>$${formatNumber(gratVal)} CLP</td>
                        </tr>`;
        }

        // Helper: vacation pending days row
        let vacPendingRow = '';
        const vacPDays = parseInt(vacPendingDays || 0);
        if (vacPDays > 0) {
            vacPendingRow = `
                        <tr>
                            <td style="font-weight: bold;">Vac. pendientes ant.:</td>
                            <td>${vacPDays} días</td>
                        </tr>`;
        }

        // Build options checkmarks (compact single line per option)
        const checkIcon = '☑';
        const uncheckIcon = '☐';
        const optionsItems = [
            { label: 'Indemn. Años Serv.', active: enableIAS },
            { label: 'Aviso Previo', active: enableNotice },
            { label: 'Desc. AFC', active: simulateAFC },
            { label: 'Sueldo Pendiente', active: enablePending },
            { label: 'Asign. en IAS', active: includeAssignInIndem },
            { label: 'Asign. en Vac.', active: includeAssignInVac }
        ];
        const optionsLine = optionsItems.map(o => `${o.active ? checkIcon : uncheckIcon} ${o.label}`).join('&nbsp;&nbsp;│&nbsp;&nbsp;');

        return `
            <!-- Premium Branded Header -->
            <div style="background-color: #0f172a !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; color-adjust: exact !important; color: #ffffff; padding: 14px 18px; border-radius: 6px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 32px; height: 32px; border-radius: 8px; background-color: #10b981 !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; color-adjust: exact !important; display: flex; align-items: center; justify-content: center;">
                        <span style="color: #ffffff; font-size: 16pt; font-weight: 900; line-height: 1;">C</span>
                    </div>
                    <div>
                        <h2 style="margin: 0; font-size: 14pt; font-weight: 800; color: #ffffff; letter-spacing: 0.5px;">CÁLCULO LABORAL</h2>
                        <span style="font-size: 7.5pt; color: #94a3b8; letter-spacing: 0.3px;">www.calculolaboral.cl</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 9pt; font-weight: 700; color: #34d399; letter-spacing: 0.5px;">SIMULACIÓN DE FINIQUITO</span><br>
                    <span style="font-size: 7pt; color: #cbd5e1;">${dateString}</span><br>
                    <span style="font-size: 6.5pt; color: #94a3b8; font-family: 'Courier New', monospace; letter-spacing: 0.5px;">${folio}</span>
                </div>
            </div>

            <!-- Economic Indicators Chips -->
            <div style="display: flex; gap: 6px; margin-bottom: 8px; font-size: 7pt;">
                <div style="flex: 1; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 3px 8px; text-align: center; -webkit-print-color-adjust: exact; print-color-adjust: exact;">
                    <span style="color: #64748b;">UF</span>&nbsp;&nbsp;<strong style="color: #047857;">$${typeof uf === 'number' ? formatNumber(uf) : uf}</strong>
                </div>
                <div style="flex: 1; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 4px; padding: 3px 8px; text-align: center; -webkit-print-color-adjust: exact; print-color-adjust: exact;">
                    <span style="color: #64748b;">UTM</span>&nbsp;&nbsp;<strong style="color: #1d4ed8;">$${typeof utm === 'number' ? formatNumber(utm) : utm}</strong>
                </div>
                <div style="flex: 1; background: #faf5ff; border: 1px solid #e9d5ff; border-radius: 4px; padding: 3px 8px; text-align: center; -webkit-print-color-adjust: exact; print-color-adjust: exact;">
                    <span style="color: #64748b;">IMM</span>&nbsp;&nbsp;<strong style="color: #7c3aed;">$${typeof imm === 'number' ? formatNumber(imm) : imm}</strong>
                </div>
            </div>

            <div class="print-title">Reporte de Simulación de Finiquito</div>
            <p style="font-size: 7.5pt; color: #64748b; margin-top: 0; margin-bottom: 8px;">
                Desglose del finiquito laboral estimado según la legislación chilena vigente (Código del Trabajo).
            </p>

            <!-- Column Layout: Resumen del Contrato and Bases de Cálculo side by side -->
            <div style="display: flex; gap: 12px; margin-bottom: 5px; width: 100%;">
                <div style="flex: 1; min-width: 0;">
                    <div class="print-section-title" style="margin-top: 0; margin-bottom: 4px;">1. Resumen del Contrato</div>
                    <table class="print-table">
                        <tr>
                            <td style="font-weight: 600; width: 42%; color: #475569;">Inicio:</td>
                            <td>${formatInputDate(startDateVal)}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: 600; color: #475569;">Término:</td>
                            <td>${formatInputDate(endDateVal)}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: 600; color: #475569;">Antigüedad:</td>
                            <td style="font-weight: 600; color: #0f172a;">${antiquity}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: 600; color: #475569;">Causal:</td>
                            <td style="font-size: 7.5pt;">${cause}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: 600; color: #475569;">¿Aviso previo?:</td>
                            <td>${noticeText}</td>
                        </tr>
                    </table>
                </div>
                <div style="width: 44%; min-width: 0;">
                    <div class="print-section-title" style="margin-top: 0; margin-bottom: 4px;">2. Bases de Cálculo</div>
                    <table class="print-table">
                        <tr>
                            <td style="font-weight: 600; width: 50%; color: #475569;">Sueldo Base:</td>
                            <td style="font-weight: 600;">$${formatNumber(parseInt(baseSalary || 0))}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: 600; color: #475569;">Haberes no Imp.:</td>
                            <td>$${formatNumber(parseInt(assignments || 0))}</td>
                        </tr>
                        ${gratificationRow}
                        ${variableSalaryRows}
                        ${vacPendingRow}
                    </table>
                </div>
            </div>

            <div class="print-section-title" style="margin-top: 4px; margin-bottom: 4px;">3. Detalle de Indemnizaciones y Haberes</div>
            <table class="print-table" style="margin-bottom: 6px;">
                <thead>
                    <tr>
                        <th style="width: 70%;">Concepto</th>
                        <th style="text-align: right;">Monto Estimado</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Indemnización por Años de Servicio</td>
                        <td style="text-align: right; font-weight: 600;">${yearsService}</td>
                    </tr>
                    <tr>
                        <td>Indemnización Sustitutiva del Aviso Previo</td>
                        <td style="text-align: right; font-weight: 600;">${noticeAmount}</td>
                    </tr>
                    <tr>
                        <td>Feriado Proporcional (${vacationDays})</td>
                        <td style="text-align: right; font-weight: 600;">${vacationProp}</td>
                    </tr>
                    <tr>
                        <td>Feriado Legal Pendiente</td>
                        <td style="text-align: right; font-weight: 600;">${vacationPendingAmt}</td>
                    </tr>
                    <tr>
                        <td>Remuneraciones Pendientes (Días Trabajados)</td>
                        <td style="text-align: right; font-weight: 600;">${pendingSalary}</td>
                    </tr>
                    ${afcAmount !== '$0' && afcAmount !== '0' && afcAmount !== '' ? `
                    <tr>
                        <td style="color: #b91c1c;">Descuento Aporte AFC Empleador (Art. 13)</td>
                        <td style="text-align: right; font-weight: 600; color: #b91c1c;">-${afcAmount}</td>
                    </tr>
                    ` : ''}
                </tbody>
            </table>

            <!-- Premium Total Box -->
            <div style="border: 2px solid #10b981; background-color: #ecfdf5 !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; color-adjust: exact !important; padding: 10px 16px; border-radius: 6px; margin-top: 6px; margin-bottom: 8px; text-align: right;">
                <span style="font-size: 7.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #047857; display: block; margin-bottom: 3px;">Monto Total Neto Estimado</span>
                <span style="font-size: 18pt; font-weight: 800; color: #047857; letter-spacing: -0.5px;">${total}</span> <span style="font-size: 11pt; font-weight: 700; color: #047857;">CLP</span>
            </div>

            <!-- Parameters Badges -->
            <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 6px;">
                ${optionsItems.map(o => `<span style="font-size: 6.5pt; padding: 2px 6px; border-radius: 3px; border: 1px solid ${o.active ? '#bbf7d0' : '#e2e8f0'}; background-color: ${o.active ? '#f0fdf4' : '#f8fafc'} !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; color-adjust: exact !important; color: ${o.active ? '#047857' : '#94a3b8'};">${o.active ? '✓' : '✗'} ${o.label}</span>`).join('')}
            </div>

            <!-- Footer Disclaimer -->
            <div class="print-disclaimer">
                <strong>NOTA INFORMATIVA:</strong> Simulación matemática basada en datos del usuario y normativa vigente. No constituye documento legal ni finiquito oficial.<br>
                <strong>DESCARGO:</strong> Cálculo Laboral no asume responsabilidad por decisiones basadas en esta simulación. Valide con la Inspección del Trabajo o un abogado laboral.
            </div>

            <!-- Footer Bar -->
            <div style="margin-top: 4px; text-align: center; font-size: 6pt; color: #cbd5e1;">
                www.calculolaboral.cl — Simulador de Finiquito Chile ${new Date().getFullYear()} — Generado automáticamente
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
