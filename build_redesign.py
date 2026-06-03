import os
import re
import glob
import json

# Paths
SOURCE_DIR = r"c:\Users\Jhon\Desktop\Arreglarpagina"
DEST_DIR = r"c:\Users\Jhon\Desktop\Arreglarpagina\calculolaboral-v2"

if not os.path.exists(DEST_DIR):
    os.makedirs(DEST_DIR)

def generate_seo_tags(filename, title, description, page_type="website"):
    # 1. Canonical URL
    if filename == "index.html":
        canonical_url = "https://calculolaboral.cl/"
    else:
        canonical_url = f"https://calculolaboral.cl/{filename.replace(".html", "")}"
        
    # 2. Open Graph Tags
    og_tags_list = [
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{description}">',
        f'<meta property="og:type" content="{page_type}">',
        f'<meta property="og:url" content="{canonical_url}">',
        '<meta property="og:image" content="https://calculolaboral.cl/assets/og-image.png">',
        '<meta property="og:locale" content="es_CL">',
        '<meta property="og:site_name" content="Cálculo Laboral">'
    ]
    og_tags = "\n    ".join(og_tags_list)
    
    # 3. JSON-LD Structured Data
    if filename == "index.html":
        json_ld_data = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Cálculo Laboral Chile",
            "url": "https://calculolaboral.cl/",
            "description": "Calcula gratis tu sueldo líquido y finiquito en Chile.",
            "potentialAction": {
                "@type": "SearchAction",
                "target": "https://calculolaboral.cl/?q={search_term_string}",
                "query-input": "required name=search_term_string"
            }
        }
    elif filename in ["sueldo_liquido.html", "finiquito_calculator.html"]:
        calc_name = "Calculadora de Sueldo Líquido" if filename == "sueldo_liquido.html" else "Calculadora de Finiquito"
        json_ld_data = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": calc_name,
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "Web",
            "description": description,
            "offers": { "@type": "Offer", "price": "0", "priceCurrency": "CLP" }
        }
    elif page_type == "article":
        json_ld_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title.split("|")[0].strip(),
            "description": description,
            "author": { "@type": "Organization", "name": "Cálculo Laboral" },
            "datePublished": "2026-01-01",
            "dateModified": "2026-06-01"
        }
    else:
        json_ld_data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title.split("|")[0].strip(),
            "description": description,
            "url": canonical_url
        }
        
    json_ld_str = f'<script type="application/ld+json">\n{json.dumps(json_ld_data, indent=4, ensure_ascii=False)}\n</script>'
    
    return canonical_url, og_tags, json_ld_str


# 1. Base Layout Components
HEADER_HTML = """
    <!-- Header -->
    <header class="sticky top-0 w-full z-50 bg-white border-b border-slate-200 shadow-sm transition-all duration-300">
        <div class="max-w-[1200px] mx-auto px-6">
            <div class="flex justify-between items-center h-16">
                <!-- Logo -->
                <a href="./" class="flex-shrink-0 flex items-center gap-2 cursor-pointer hover:opacity-90 transition-opacity">
                    <div class="w-8 h-8 rounded-lg bg-sky-500 flex items-center justify-center shadow-md shadow-sky-500/20 active:scale-95 transition-transform">
                        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="4" y="4" width="16" height="16" rx="2"></rect>
                            <line x1="9" y1="9" x2="15" y2="9"></line>
                            <line x1="9" y1="13" x2="15" y2="13"></line>
                            <line x1="9" y1="17" x2="15" y2="17"></line>
                        </svg>
                    </div>
                    <span class="font-bold text-xl tracking-tight text-slate-900">Cálculo<span class="text-sky-500">Laboral</span></span>
                </a>

                <!-- Desktop Menu -->
                <nav class="hidden md:flex gap-6 items-center">
                    <!-- Dropdown Calculadoras -->
                    <div class="relative group">
                        <button class="flex items-center gap-1 text-sm font-semibold text-slate-600 hover:text-sky-500 transition-colors py-2 outline-none">
                            Calculadoras
                            <span class="material-icons text-xs group-hover:rotate-180 transition-transform">expand_more</span>
                        </button>
                        <div class="absolute left-0 mt-0 w-48 bg-white border border-slate-200 rounded-xl shadow-lg opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-all duration-200 z-50">
                            <div class="p-2 space-y-1">
                                <a href="sueldo_liquido" class="block px-3 py-2 text-xs font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50 rounded-lg transition-colors">Sueldo Líquido</a>
                                <a href="finiquito_calculator" class="block px-3 py-2 text-xs font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50 rounded-lg transition-colors">Finiquito</a>
                            </div>
                        </div>
                    </div>

                    <!-- Dropdown Guías -->
                    <div class="relative group">
                        <button class="flex items-center gap-1 text-sm font-semibold text-slate-600 hover:text-sky-500 transition-colors py-2 outline-none">
                            Guías
                            <span class="material-icons text-xs group-hover:rotate-180 transition-transform">expand_more</span>
                        </button>
                        <div class="absolute left-0 mt-0 w-64 bg-white border border-slate-200 rounded-xl shadow-lg opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-all duration-200 z-50">
                            <div class="p-2 space-y-1 max-h-[300px] overflow-y-auto">
                                <a href="como-calcular-finiquito-chile" class="block px-3 py-2 text-xs font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50 rounded-lg transition-colors">Cómo Calcular Finiquito</a>
                                <a href="como-calcular-sueldo-liquido-paso-a-paso" class="block px-3 py-2 text-xs font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50 rounded-lg transition-colors">Cómo Calcular Sueldo Líquido</a>
                                <a href="como-leer-liquidacion-de-sueldo" class="block px-3 py-2 text-xs font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50 rounded-lg transition-colors">Cómo Leer Liquidación</a>
                                <a href="despido-necesidades-empresa-articulo-161" class="block px-3 py-2 text-xs font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50 rounded-lg transition-colors">Art. 161 Necesidades Empresa</a>
                                <a href="ley-40-horas-chile-2026" class="block px-3 py-2 text-xs font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50 rounded-lg transition-colors">Ley 40 Horas 2026</a>
                                <a href="guia-vacaciones-proporcionales" class="block px-3 py-2 text-xs font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50 rounded-lg transition-colors">Vacaciones Proporcionales</a>
                                <a href="seguro-de-cesantia-chile-como-cobrar" class="block px-3 py-2 text-xs font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50 rounded-lg transition-colors">Cobrar Seguro Cesantía</a>
                                <a href="que-hacer-si-no-te-pagan-el-finiquito" class="block px-3 py-2 text-xs font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50 rounded-lg transition-colors">Si no te Pagan el Finiquito</a>
                                <a href="reclamar-despido-injustificado-chile" class="block px-3 py-2 text-xs font-semibold text-sky-600 bg-sky-50 hover:bg-sky-100 rounded-lg transition-colors">🆕 Despido Injustificado</a>
                            </div>
                        </div>
                    </div>

                    <a href="blog" class="text-sm font-semibold text-slate-600 hover:text-sky-500 transition-colors">Blog</a>
                    <a href="contacto" class="text-sm font-semibold text-slate-600 hover:text-sky-500 transition-colors">Contacto</a>
                </nav>

                <!-- Mobile Menu Button -->
                <div class="flex items-center gap-4">
                    <button id="mobile-menu-btn" aria-label="Abrir menú de navegación" class="md:hidden p-2 rounded-lg text-slate-500 hover:bg-slate-100 transition-colors active:scale-95 duration-100">
                        <span class="material-icons">menu</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Menu (Hidden by default) -->
        <div id="mobile-menu" class="hidden md:hidden bg-white border-t border-slate-200 absolute w-full left-0 z-40 shadow-lg">
            <div class="px-4 py-4 space-y-2">
                <a href="sueldo_liquido" class="block px-3 py-2 rounded-lg text-base font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Sueldo Líquido</a>
                <a href="finiquito_calculator" class="block px-3 py-2 rounded-lg text-base font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Calculadora de Finiquito</a>
                <div class="border-t border-slate-100 my-2"></div>
                <p class="px-3 text-xs font-bold text-slate-500 uppercase tracking-widest">Guías</p>
                <a href="como-calcular-finiquito-chile" class="block px-3 py-2 rounded-lg text-sm font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Cómo Calcular Finiquito</a>
                <a href="como-calcular-sueldo-liquido-paso-a-paso" class="block px-3 py-2 rounded-lg text-sm font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Cómo Calcular Sueldo Líquido</a>
                <a href="como-leer-liquidacion-de-sueldo" class="block px-3 py-2 rounded-lg text-sm font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Cómo Leer Liquidación</a>
                <a href="despido-necesidades-empresa-articulo-161" class="block px-3 py-2 rounded-lg text-sm font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Art. 161 Necesidades Empresa</a>
                <a href="ley-40-horas-chile-2026" class="block px-3 py-2 rounded-lg text-sm font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Ley 40 Horas 2026</a>
                <a href="guia-vacaciones-proporcionales" class="block px-3 py-2 rounded-lg text-sm font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Vacaciones Proporcionales</a>
                <a href="seguro-de-cesantia-chile-como-cobrar" class="block px-3 py-2 rounded-lg text-sm font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Cobrar Seguro Cesantía</a>
                <a href="que-hacer-si-no-te-pagan-el-finiquito" class="block px-3 py-2 rounded-lg text-sm font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Si no te Pagan el Finiquito</a>
                <a href="reclamar-despido-injustificado-chile" class="block px-3 py-2 rounded-lg text-sm font-semibold text-sky-600 bg-sky-50 hover:bg-sky-100">🆕 Despido Injustificado</a>
                <div class="border-t border-slate-100 my-2"></div>
                <a href="blog" class="block px-3 py-2 rounded-lg text-base font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Blog</a>
                <a href="contacto" class="block px-3 py-2 rounded-lg text-base font-semibold text-slate-600 hover:text-sky-500 hover:bg-slate-50">Contacto</a>
            </div>
        </div>
    </header>
"""

FOOTER_HTML = """
    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 pt-16 pb-12 mt-auto">
        <div class="max-w-[1200px] mx-auto px-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
            <!-- Brand Column -->
            <div class="space-y-4">
                <a href="./" class="flex items-center gap-2">
                    <div class="w-8 h-8 rounded-lg bg-sky-500 flex items-center justify-center shadow-md shadow-sky-500/20 active:scale-95 transition-transform">
                        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="4" y="4" width="16" height="16" rx="2"></rect>
                            <line x1="9" y1="9" x2="15" y2="9"></line>
                            <line x1="9" y1="13" x2="15" y2="13"></line>
                            <line x1="9" y1="17" x2="15" y2="17"></line>
                        </svg>
                    </div>
                    <span class="font-bold text-xl tracking-tight text-slate-900">Cálculo<span class="text-sky-500">Laboral</span></span>
                </a>
                <p class="text-sm text-slate-600 leading-relaxed">
                    Herramientas y simuladores gratuitos y actualizados conforme a la legislación laboral chilena vigente en 2026.
                </p>
                <p class="text-xs text-slate-500 font-mono">Versión 2.0.0 (2026)</p>
            </div>

            <!-- Calculadoras Column -->
            <div class="space-y-4">
                <h4 class="text-sm font-bold text-slate-900 uppercase tracking-widest">Calculadoras</h4>
                <ul class="space-y-2">
                    <li><a href="sueldo_liquido" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Sueldo Líquido</a></li>
                    <li><a href="finiquito_calculator" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Calculadora de Finiquito</a></li>
                    <li><a href="./" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium font-semibold">Simulador Integrado</a></li>
                </ul>
            </div>

            <!-- Guías Populares Column -->
            <div class="space-y-4">
                <h4 class="text-sm font-bold text-slate-900 uppercase tracking-widest">Guías Populares</h4>
                <ul class="space-y-2">
                    <li><a href="como-calcular-finiquito-chile" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Cómo Calcular Finiquito</a></li>
                    <li><a href="como-calcular-sueldo-liquido-paso-a-paso" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Cómo Calcular Sueldo Líquido</a></li>
                    <li><a href="guia-vacaciones-proporcionales" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Vacaciones Proporcionales</a></li>
                    <li><a href="ley-40-horas-chile-2026" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Ley de 40 Horas (2026)</a></li>
                </ul>
            </div>

            <!-- Legal Column -->
            <div class="space-y-4">
                <h4 class="text-sm font-bold text-slate-900 uppercase tracking-widest">Sobre el Sitio</h4>
                <ul class="space-y-2">
                    <li><a href="sobre-nosotros" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Sobre Nosotros</a></li>
                    <li><a href="contacto" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Contacto</a></li>
                    <li><a href="terminos" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Términos de Servicio</a></li>
                    <li><a href="privacidad" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Política de Privacidad</a></li>
                    <li><a href="disclaimer" class="text-sm text-slate-600 hover:text-sky-500 transition-colors font-medium">Disclaimer Legal</a></li>
                </ul>
            </div>
        </div>

        <!-- Bottom Footer -->
        <div class="max-w-[1200px] mx-auto px-6 border-t border-slate-200 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-center md:text-left">
            <p class="text-xs text-slate-500">
                &copy; 2026 Cálculo Laboral Chile. Todos los derechos reservados. Todos los cálculos son estimativos y de carácter ilustrativo.
            </p>
            <div class="flex items-center gap-4">
                <span class="text-xs text-slate-500 flex items-center gap-1">
                    <span class="material-icons text-xs text-emerald-500">verified</span>
                    DT Chile Conforme
                </span>
            </div>
        </div>
    </footer>
"""

INDICATOR_BAR_HTML = """
    <!-- Indicators Grid (5 Cards) -->
    <div class="max-w-[1200px] mx-auto px-6 mt-4 mb-8 no-print">
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
            <!-- UF Card -->
            <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm hover:shadow transition-shadow">
                <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">UF (Unidad de Fomento)</span>
                <span class="uf-value text-lg font-extrabold text-slate-900 font-mono">$39.682,99</span>
            </div>
            <!-- UTM Card -->
            <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm hover:shadow transition-shadow">
                <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">UTM Mensual</span>
                <span class="utm-value text-lg font-extrabold text-slate-900 font-mono">$69.611</span>
            </div>
            <!-- Sueldo Mínimo Card -->
            <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm hover:shadow transition-shadow">
                <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">Sueldo Mínimo</span>
                <span class="text-lg font-extrabold text-slate-900 font-mono">$539.000</span>
            </div>
            <!-- Tope AFP Card -->
            <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm hover:shadow transition-shadow">
                <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">Tope Imponible AFP</span>
                <span class="text-lg font-extrabold text-slate-900 font-mono">89.9 UF</span>
            </div>
            <!-- Tope Finiquito Card -->
            <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm hover:shadow transition-shadow">
                <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">Tope Finiquito</span>
                <span class="text-lg font-extrabold text-slate-900 font-mono">90 UF</span>
            </div>
        </div>
        <div class="flex justify-between items-center mt-2.5 px-1 text-[10px] text-slate-500 font-medium">
            <div id="indicators-status" class="flex items-center gap-1">
                <span class="material-icons text-[12px] animate-spin">sync</span> Cargando indicadores del Banco Central...
            </div>
            <a href="#" id="btn-history" class="text-sky-500 hover:text-sky-600 hover:underline flex items-center gap-0.5">
                <span class="material-icons text-[12px]">history</span> Historial de Valores
            </a>
        </div>
    </div>
"""

HISTORY_MODAL_HTML = """
    <!-- History Modal -->
    <div id="history-modal" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 hidden">
        <div class="bg-white rounded-2xl border border-slate-200 w-full max-w-md shadow-2xl p-6 relative overflow-hidden animate-fade-in">
            <div class="flex justify-between items-center border-b border-slate-100 pb-3.5 mb-4">
                <div class="flex items-center gap-2">
                    <span class="material-icons text-sky-500">history</span>
                    <h3 class="text-base font-bold text-slate-900">Historial de Indicadores</h3>
                </div>
                <button id="btn-close-history" aria-label="Cerrar modal" class="text-slate-500 hover:text-slate-700 hover:bg-slate-100 p-1 rounded-full transition-colors active:scale-95 duration-100">
                    <span class="material-icons">close</span>
                </button>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <h4 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2 border-b border-slate-100 pb-1 flex items-center gap-1">
                        <span class="w-1.5 h-1.5 rounded-full bg-sky-500"></span> UF (Últimos 30 días)
                    </h4>
                    <div class="max-h-[250px] overflow-y-auto pr-1">
                        <table class="w-full text-left">
                            <tbody id="uf-history-body">
                                <tr><td class="p-2 text-center text-slate-500 text-xs italic font-medium">Cargando...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div>
                    <h4 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2 border-b border-slate-100 pb-1 flex items-center gap-1">
                        <span class="w-1.5 h-1.5 rounded-full bg-indigo-500"></span> UTM (Últimos 12 meses)
                    </h4>
                    <div class="max-h-[250px] overflow-y-auto pr-1">
                        <table class="w-full text-left">
                            <tbody id="utm-history-body">
                                <tr><td class="p-2 text-center text-slate-500 text-xs italic font-medium">Cargando...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

HTML_LAYOUT = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title}</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{canonical_url}">
    
    <!-- Open Graph Tags -->
    {og_tags}
    
    <!-- Structured Data -->
    {json_ld}
    
    <!-- Fonts and Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Geist:wght@100..900&family=Geist+Mono:wght@100..900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Geist', 'sans-serif'],
                        mono: ['Geist Mono', 'monospace'],
                    }},
                    colors: {{
                        primary: '#0ea5e9',
                    }}
                }}
            }}
        }}
    </script>
    <style>
        .prose-content h2 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            margin-top: 2rem;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }}
        .prose-content h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #1e293b;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            letter-spacing: -0.01em;
        }}
        .prose-content p {{
            margin-bottom: 1.25rem;
            line-height: 1.75;
        }}
        .prose-content ul {{
            list-style-type: disc;
            padding-left: 1.5rem;
            margin-bottom: 1.25rem;
        }}
        .prose-content ol {{
            list-style-type: decimal;
            padding-left: 1.5rem;
            margin-bottom: 1.25rem;
        }}
        .prose-content li {{
            margin-bottom: 0.5rem;
        }}
        .prose-content strong {{
            color: #0f172a;
            font-weight: 600;
        }}
        .prose-content a {{
            color: #0ea5e9;
            text-decoration: underline;
            font-weight: 500;
        }}
        .prose-content a:hover {{
            color: #0284c7;
        }}
        .prose-content a.cta-btn {{
            color: #ffffff !important;
            text-decoration: none !important;
            font-weight: 600 !important;
        }}
        .prose-content a.cta-btn:hover {{
            color: #ffffff !important;
            text-decoration: none !important;
        }}
        .prose-content .callout {{
            background-color: #f0fdf4;
            border-left: 4px solid #22c55e;
            padding: 1rem 1.25rem;
            border-radius: 0.5rem;
            margin: 1.5rem 0;
        }}
        .prose-content .callout-amber {{
            background-color: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 1rem 1.25rem;
            border-radius: 0.5rem;
            margin: 1.5rem 0;
        }}
        .prose-content .formula-box {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin: 1.5rem 0;
            text-align: center;
        }}
        .rubro-card {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 1rem;
            padding: 1rem;
            transition: all 0.2s ease;
        }}
        .rubro-card:hover {{
            border-color: #cbd5e1;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
        }}
        .rubro-label {{
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.125rem 0.5rem;
            border-radius: 9999px;
            display: inline-block;
            flex-shrink: 0;
        }}
        .rubro-imponible {{
            background-color: #f0f9ff;
            color: #0369a1;
            border: 1px solid #e0f2fe;
        }}
        .rubro-no-imponible {{
            background-color: #f0fdf4;
            color: #15803d;
            border: 1px solid #dcfce7;
        }}
        .rubro-descuento {{
            background-color: #fef2f2;
            color: #b91c1c;
            border: 1px solid #fee2e2;
        }}
        .timeline-item {{
            position: relative;
            padding-left: 1.75rem;
            border-left: 2px solid #e2e8f0;
            padding-bottom: 1.5rem;
        }}
        .timeline-item::before {{
            content: "";
            position: absolute;
            left: -5px;
            top: 4px;
            width: 8px;
            height: 8px;
            border-radius: 9999px;
            background-color: #cbd5e1;
            border: 2px solid #ffffff;
            transition: all 0.2s ease;
        }}
        .timeline-item.active {{
            border-left-color: #0ea5e9;
        }}
        .timeline-item.active::before {{
            background-color: #0ea5e9;
            left: -7px;
            top: 2px;
            width: 12px;
            height: 12px;
            box-shadow: 0 0 0 4px rgb(14 165 233 / 0.15);
        }}
        .timeline-item:last-child {{
            padding-bottom: 0;
            border-left-color: transparent;
        }}
        .step-card {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 1rem;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.02);
        }}
        .step-number {{
            width: 2.25rem;
            height: 2.25rem;
            background-color: #e0f2fe;
            color: #0369a1;
            border-radius: 9999px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.875rem;
            flex-shrink: 0;
        }}
        .field-error {{
            color: #ef4444;
            font-size: 0.75rem;
            margin-top: 0.25rem;
        }}
        .print-only {{ display: none !important; }}
        
        @media print {{
            body > *:not(#print-section) {{
                display: none !important;
            }}
            #print-section {{
                display: block !important;
            }}
            html, body {{
                background: #ffffff !important;
                color: #1e293b !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
    {custom_head}
</head>
<body class="bg-slate-50 text-slate-700 min-h-screen flex flex-col font-sans selection:bg-sky-500/20 selection:text-slate-900">

    {header}
    {indicator_bar}

    <!-- Main Content -->
    <main class="flex-grow pt-4 pb-16">
        {content}
    </main>

    {footer}
    {history_modal}

    <!-- Shared Toggle Mobile Menu Script -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const mobileMenuBtn = document.getElementById('mobile-menu-btn');
            const mobileMenu = document.getElementById('mobile-menu');
            if (mobileMenuBtn && mobileMenu) {{
                mobileMenuBtn.addEventListener('click', () => {{
                    mobileMenu.classList.toggle('hidden');
                }});
            }}
        }});
    </script>
    
    <!-- Load shared indicators script -->
    <script src="/js/constants.js"></script>
    <script src="/js/indicators.js"></script>
    <script src="/js/pdf_generator.js"></script>
    <script>
        (function() {{
            emailjs.init("{{HIi9_S1hAf7mWQU_W}}");
        }})();

        function enviarLead() {{
            var nombre = document.getElementById('lead-nombre').value.trim();
            var correo = document.getElementById('lead-correo').value.trim();
            var telefono = document.getElementById('lead-telefono').value.trim();
            var monto = window.resultadoActualMonto || '0';

            if (!nombre || !correo) {{
                alert('Por favor completa nombre y correo.');
                return;
            }}

            emailjs.send("{{service_plsair4}}", "{{template_u1juvx1}}", {{
                nombre: nombre,
                correo: correo,
                telefono: telefono,
                monto_calculado: monto,
                tipo: 'Finiquito',
                fecha: new Date().toLocaleDateString('es-CL')
            }}).then(function() {{
                document.getElementById('lead-form').classList.add('hidden');
                document.getElementById('lead-confirmacion').classList.remove('hidden');
            }}).catch(function() {{
                alert('Error al enviar. Intenta de nuevo.');
            }});
        }}
    </script>
    {custom_scripts}
</body>
</html>
"""


def flexible_replace(text, old_block, new_block):
    # Normalize line endings to \n
    text_norm = text.replace('\r\n', '\n')
    old_norm = old_block.replace('\r\n', '\n')
    
    # Split into lines and strip
    old_lines = [line.strip() for line in old_norm.split('\n') if line.strip()]
    if not old_lines:
        return text
    
    # Escape each line to form regex pattern
    escaped_lines = [re.escape(line) for line in old_lines]
    # Match any leading/trailing horizontal whitespace on lines, and any newlines/indentation between lines
    pattern = r'[ \t]*' + r'[ \t]*\n+[ \t]*'.join(escaped_lines) + r'[ \t]*'
    
    # Perform regex replacement
    new_text, count = re.subn(pattern, lambda m: new_block, text_norm)
    if count > 0:
        return new_text
    else:
        # Fallback to standard replace
        return text.replace(old_block, new_block)

def wrap_images(content):
    def img_replacer(match):
        img_tag = match.group(0)
        if 'bg-slate-100' in img_tag or 'border-slate-200' in img_tag:
            return img_tag
        return f'<div class="bg-slate-100 p-4 border border-slate-200 rounded-xl flex items-center justify-center my-6 max-w-full overflow-hidden shadow-sm">{img_tag}</div>'
    return re.sub(r'<img[^>]+>', img_replacer, content)

def strip_outer_divs(body):
    while True:
        body_stripped = body.strip()
        match = re.match(r'^<div[^>]*>', body_stripped, re.IGNORECASE)
        if not match:
            break
        
        open_tag = match.group(0)
        depth = 0
        div_indices = []
        for m in re.finditer(r'</?div\b[^>]*>', body_stripped, re.IGNORECASE):
            tag = m.group(0)
            start = m.start()
            end = m.end()
            is_close = tag.startswith('</')
            div_indices.append((start, end, is_close))
        
        if not div_indices or div_indices[0][0] != 0:
            break
            
        closing_idx = -1
        depth = 0
        for i, (start, end, is_close) in enumerate(div_indices):
            if is_close:
                depth -= 1
                if depth == 0:
                    closing_idx = i
                    break
            else:
                depth += 1
                
        if closing_idx != -1:
            c_start, c_end, _ = div_indices[closing_idx]
            if c_end == len(body_stripped):
                body = body_stripped[len(open_tag):c_start]
                continue
        break
    return body

def extract_article_info(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 1. Title
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Artículo | Cálculo Laboral Chile"
    
    # 2. Description
    desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="(.*?)"', html, re.IGNORECASE | re.DOTALL)
    if not desc_match:
        desc_match = re.search(r'<meta[^>]*content="(.*?)"[^>]*name="description"', html, re.IGNORECASE | re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else "Guía sobre legislación y cálculos laborales chilenos."
    
    # 3. Scripts / JSON-LD
    ld_scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    custom_head = ""
    for ld in ld_scripts:
        custom_head += f'<script type="application/ld+json">{ld}</script>\n'
        
    # 4. Article content
    article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if article_match:
        body = article_match.group(1)
        body = re.sub(r'<nav[^>]*id="breadcrumb"[^>]*>.*?</nav>', '', body, re.DOTALL | re.IGNORECASE)
        body = re.sub(r'<nav[^>]*class="[^"]*breadcrumb[^"]*"[^>]*>.*?</nav>', '', body, re.DOTALL | re.IGNORECASE)
        body = re.sub(r'<header[^>]*>.*?</header>', '', body, re.DOTALL | re.IGNORECASE)
        
        # Strip any pre-existing nested outer wrappers before performing adjustments
        body = strip_outer_divs(body)
        
        # Call clean_article_body first to let file-specific replacements match original HTML!
        body = clean_article_body(body, os.path.basename(file_path))
        
        body = body.replace('prose-dark', 'prose prose-slate prose-lg max-w-none text-slate-700 leading-relaxed prose-headings:text-slate-900 font-sans prose-headings:font-bold prose-a:text-sky-500 hover:prose-a:text-sky-600 prose-strong:text-slate-900')
        # 1. Capture and style specific CTA buttons FIRST (before generic text-white replacements)
        body = body.replace('class="inline-flex items-center gap-2 px-10 py-4 bg-blue-600 hover:bg-blue-500 text-white font-bold text-lg rounded-xl shadow-lg shadow-blue-500/30 transition-all hover:scale-105"', 'class="cta-btn inline-flex items-center justify-center gap-2 px-6 py-3 bg-sky-500 text-white hover:bg-sky-600 rounded-xl shadow-md shadow-sky-500/10 transition-all hover:scale-[1.01]"')
        body = body.replace('bg-blue-600 hover:bg-blue-500 text-white font-bold', 'bg-sky-500 hover:bg-sky-600 !text-[#ffffff] !no-underline font-bold shadow-sm')
        body = body.replace('bg-blue-600 hover:bg-blue-500 text-white', 'bg-sky-500 hover:bg-sky-600 !text-[#ffffff] !no-underline shadow-sm')
        body = body.replace('bg-blue-600 hover:bg-blue-500 text-slate-800 font-bold', 'bg-sky-500 hover:bg-sky-600 !text-[#ffffff] !no-underline font-bold shadow-sm')
        body = body.replace('bg-blue-600 hover:bg-blue-500 text-slate-800', 'bg-sky-500 hover:bg-sky-600 !text-[#ffffff] !no-underline shadow-sm')
        
        # 2. Deep scrub of dark-themed container boxes and low-contrast text for premium light theme
        body = body.replace('bg-slate-800/40', 'bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all')
        body = body.replace('bg-slate-800/50', 'bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all')
        body = body.replace('bg-slate-800/60', 'bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all')
        body = body.replace('bg-slate-800/30', 'bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all')
        body = body.replace('bg-slate-800/20', 'bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all')
        body = body.replace('bg-slate-800/10', 'bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all')
        body = body.replace('bg-slate-800', 'bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all')
        
        # Gradients
        body = body.replace('bg-gradient-to-r from-blue-900/50 to-purple-900/50', 'bg-gradient-to-br from-sky-50 to-blue-50 border border-sky-100 rounded-2xl p-8 my-6 text-center')
        
        # Borders
        body = body.replace('border-white/10', 'border-slate-200')
        body = body.replace('border-white/5', 'border-slate-100')
        body = body.replace('border-white/20', 'border-slate-200')
        body = body.replace('border-slate-700', 'border-slate-200')
        body = body.replace('border-slate-800', 'border-slate-200')
        body = body.replace('border-red-500/20', 'border-red-200 bg-red-50/40 rounded-2xl p-5 shadow-sm my-6')
        body = body.replace('border-emerald-500/20', 'border-emerald-200 bg-emerald-50/40 rounded-2xl p-5 shadow-sm my-6')
        body = body.replace('border-blue-500/20', 'border-sky-200 bg-sky-50/40 rounded-2xl p-5 shadow-sm my-6')
        
        # Text colors
        body = body.replace('text-slate-300', 'text-slate-600')
        body = body.replace('text-slate-400', 'text-slate-500')
        body = body.replace('text-slate-200', 'text-slate-700')
        body = body.replace('text-blue-300', 'text-sky-700')
        body = body.replace('text-blue-400', 'text-sky-600')
        body = body.replace('text-emerald-300', 'text-emerald-700')
        body = body.replace('text-emerald-400', 'text-emerald-600')
        body = body.replace('text-red-300', 'text-red-700')
        body = body.replace('text-red-400', 'text-red-600')
        body = body.replace('text-purple-300', 'text-purple-700')
        body = body.replace('text-amber-300', 'text-amber-700')
        body = body.replace('text-indigo-300', 'text-indigo-700')
        
        # Badges and metrics
        body = body.replace('bg-blue-500/20', 'bg-sky-100 text-sky-700')
        body = body.replace('bg-blue-500/10', 'bg-sky-50 text-sky-600')
        body = body.replace('bg-blue-500/15', 'bg-sky-100/60 text-sky-600')
        body = body.replace('bg-emerald-500/20', 'bg-emerald-100 text-emerald-700')
        body = body.replace('bg-emerald-500/10', 'bg-emerald-50 text-emerald-600')
        body = body.replace('bg-emerald-500/15', 'bg-emerald-100/60 text-emerald-600')
        body = body.replace('bg-red-500/20', 'bg-red-100 text-red-700')
        body = body.replace('bg-red-500/10', 'bg-red-50 text-red-600')
        body = body.replace('bg-red-500/15', 'bg-red-100/60 text-red-600')
        body = body.replace('bg-slate-900/20', 'bg-slate-100/50')
        body = body.replace('bg-slate-800/80', 'bg-slate-100 text-slate-700 font-semibold')
        body = body.replace('shadow-black/20', 'shadow-sm')
        body = body.replace('shadow-black/40', 'shadow-sm')
        body = body.replace('border-white/5', 'border-slate-100')
        
        # 3. Finally do generic text-white cleanup
        body = body.replace('!text-white', 'text-slate-800 font-semibold')
        body = body.replace('text-white font-bold', 'text-slate-900 font-bold')
        body = body.replace('text-white', 'text-slate-800')
        body = body.replace('hover:text-white', 'hover:text-slate-900')
        body = body.replace('hover:bg-white/5', 'hover:bg-slate-100')
        
        # 4. Cross-link card fixes
        body = body.replace('text-slate-800 hover:text-red-400 font-semibold underline', 'text-sky-600 hover:text-sky-700 font-semibold !no-underline')
        body = body.replace('text-slate-800 font-bold text-lg', 'text-slate-900 font-bold text-lg')
        body = body.replace('hover:border-green-500/30', 'hover:border-green-400 hover:bg-green-50/30')
        body = body.replace('hover:border-blue-500/30', 'hover:border-sky-400 hover:bg-sky-50/30')
        
        # Fix button containers keeping original styles
        body = body.replace('class="!no-underline p-4 rounded-xl bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all', 'class="!no-underline p-4 rounded-xl bg-slate-50 border border-slate-200 hover:shadow-md transition-all')
        
        body = wrap_images(body)
    else:
        body = "<p>Contenido del artículo no encontrado en el archivo de origen.</p>"
        
    return title, description, body, custom_head

def clean_article_body(body, filename):
    # Cover image replacements
    body = body.replace('/assets/img_sueldo_liquido.png', 'assets/guia-sueldo-liquido-cover.png')
    body = body.replace('assets/img_sueldo_liquido.png', 'assets/guia-sueldo-liquido-cover.png')
    body = body.replace('/assets/img_leer_liquidacion.png', 'assets/guia-liquidacion-sueldo-cover.png')
    body = body.replace('assets/img_leer_liquidacion.png', 'assets/guia-liquidacion-sueldo-cover.png')
    body = body.replace('/assets/img_ley_40_horas.png', 'assets/guia-ley-40-horas-chile-cover.png')
    body = body.replace('assets/img_ley_40_horas.png', 'assets/guia-ley-40-horas-chile-cover.png')
    body = body.replace('/assets/img_reclamo_finiquito.png', 'assets/guia-finiquito-no-pago-cover.png')
    body = body.replace('assets/img_reclamo_finiquito.png', 'assets/guia-finiquito-no-pago-cover.png')

    # 1. File-specific manual replacements for unreadable dark infographics, tables, or boxes
    
    if filename == "como-leer-liquidacion-de-sueldo.html":
        # Dark infographic anatomy
        old_infographic = """<!-- Infografía HTML: Anatomía de liquidación de sueldo -->
                <div class="my-8 p-6 rounded-2xl bg-gradient-to-b from-slate-800/60 to-slate-900/60 border border-white/10 shadow-xl">
                    <p class="text-center text-xs font-bold text-slate-400 uppercase tracking-widest mb-5">Anatomía de tu liquidación de sueldo</p>
                    <div class="space-y-3 max-w-md mx-auto">
                        <div class="rounded-lg border border-emerald-500/30 overflow-hidden">
                            <div class="bg-emerald-500/20 px-3 py-1.5"><p class="!text-emerald-400 !text-xs !font-bold !mb-0 !uppercase !tracking-wider">Haberes</p></div>
                            <div class="px-3 py-2 space-y-1">
                                <div class="flex justify-between items-center"><span class="text-slate-300 text-xs">Sueldo Base</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/15 text-blue-400 font-semibold">Imponible</span></div>
                                <div class="flex justify-between items-center"><span class="text-slate-300 text-xs">Gratificación</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/15 text-blue-400 font-semibold">Imponible</span></div>
                                <div class="flex justify-between items-center"><span class="text-slate-300 text-xs">Horas Extra</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/15 text-blue-400 font-semibold">Imponible</span></div>
                                <div class="flex justify-between items-center"><span class="text-slate-300 text-xs">Colación</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400 font-semibold">No Imponible</span></div>
                                <div class="flex justify-between items-center"><span class="text-slate-300 text-xs">Movilización</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400 font-semibold">No Imponible</span></div>
                            </div>
                        </div>
                        <div class="flex justify-center"><span class="material-icons text-slate-600">arrow_downward</span></div>
                        <div class="rounded-lg border border-red-500/30 overflow-hidden">
                            <div class="bg-red-500/20 px-3 py-1.5"><p class="!text-red-400 !text-xs !font-bold !mb-0 !uppercase !tracking-wider">Descuentos</p></div>
                            <div class="px-3 py-2 space-y-1">
                                <div class="flex justify-between items-center"><span class="text-slate-300 text-xs">AFP (10% + comisión)</span><span class="text-rose-400 text-xs font-semibold">−11,27%</span></div>
                                <div class="flex justify-between items-center"><span class="text-slate-300 text-xs">Salud (Fonasa/Isapre)</span><span class="text-rose-400 text-xs font-semibold">−7%</span></div>
                                <div class="flex justify-between items-center"><span class="text-slate-300 text-xs">Seguro de Cesantía</span><span class="text-rose-400 text-xs font-semibold">−0,6%</span></div>
                                <div class="flex justify-between items-center"><span class="text-slate-300 text-xs">Impuesto Único</span><span class="text-rose-400 text-xs font-semibold">Variable</span></div>
                            </div>
                        </div>
                        <div class="flex justify-center"><span class="material-icons text-slate-600">arrow_downward</span></div>
                        <div class="rounded-lg border border-blue-500/40 bg-blue-500/10 px-4 py-3 text-center">
                            <p class="!text-blue-400 !text-sm !font-bold !mb-0">&#128176; SUELDO LÍQUIDO</p>
                            <p class="!text-slate-400 !text-[10px] !mb-0">Lo que recibes en tu cuenta bancaria</p>
                        </div>
                    </div>
                </div>"""
                
        new_infographic = """<!-- Infografía HTML: Anatomía de liquidación de sueldo -->
                <div class="my-8 p-6 rounded-2xl bg-slate-50 border border-slate-200 shadow-sm">
                    <p class="text-center text-xs font-bold text-slate-500 uppercase tracking-widest mb-5">Anatomía de tu liquidación de sueldo</p>
                    <div class="space-y-4 max-w-md mx-auto">
                        <div class="rounded-xl border border-slate-200 overflow-hidden bg-white shadow-sm">
                            <div class="bg-emerald-50 border-b border-emerald-100 px-4 py-2 flex justify-between items-center"><p class="text-emerald-800 text-xs font-bold mb-0 uppercase tracking-wider font-semibold">Haberes</p></div>
                            <div class="px-4 py-3 space-y-2">
                                <div class="flex justify-between items-center text-slate-700 text-sm font-medium"><span>Sueldo Base</span><span class="text-[10px] px-2 py-0.5 rounded bg-sky-50 text-sky-700 border border-sky-100/50 font-semibold">Imponible</span></div>
                                <div class="flex justify-between items-center text-slate-700 text-sm font-medium"><span>Gratificación</span><span class="text-[10px] px-2 py-0.5 rounded bg-sky-50 text-sky-700 border border-sky-100/50 font-semibold">Imponible</span></div>
                                <div class="flex justify-between items-center text-slate-700 text-sm font-medium"><span>Horas Extra</span><span class="text-[10px] px-2 py-0.5 rounded bg-sky-50 text-sky-700 border border-sky-100/50 font-semibold">Imponible</span></div>
                                <div class="flex justify-between items-center text-slate-700 text-sm font-medium"><span>Colación</span><span class="text-[10px] px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-100/50 font-semibold">No Imponible</span></div>
                                <div class="flex justify-between items-center text-slate-700 text-sm font-medium"><span>Movilización</span><span class="text-[10px] px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-100/50 font-semibold">No Imponible</span></div>
                            </div>
                        </div>
                        <div class="flex justify-center"><span class="material-icons text-sky-500 font-bold">arrow_downward</span></div>
                        <div class="rounded-xl border border-slate-200 overflow-hidden bg-white shadow-sm">
                            <div class="bg-rose-50 border-b border-rose-100 px-4 py-2 flex justify-between items-center"><p class="text-rose-800 text-xs font-bold mb-0 uppercase tracking-wider font-semibold">Descuentos</p></div>
                            <div class="px-4 py-3 space-y-2">
                                <div class="flex justify-between items-center text-slate-700 text-sm font-medium"><span>AFP (10% + comisión)</span><span class="text-rose-600 font-bold">−11,27%</span></div>
                                <div class="flex justify-between items-center text-slate-700 text-sm font-medium"><span>Salud (Fonasa/Isapre)</span><span class="text-rose-600 font-bold">−7%</span></div>
                                <div class="flex justify-between items-center text-slate-700 text-sm font-medium"><span>Seguro de Cesantía</span><span class="text-rose-600 font-bold">−0,6%</span></div>
                                <div class="flex justify-between items-center text-slate-700 text-sm font-medium"><span>Impuesto Único</span><span class="text-rose-600 font-bold">Variable</span></div>
                            </div>
                        </div>
                        <div class="flex justify-center"><span class="material-icons text-sky-500 font-bold">arrow_downward</span></div>
                        <div class="rounded-xl border border-sky-200 bg-gradient-to-r from-sky-50 to-blue-50 px-4 py-3 text-center shadow-sm">
                            <p class="text-sky-600 text-sm font-bold mb-0">&#128176; SUELDO LÍQUIDO</p>
                            <p class="text-slate-650 text-[10px] mb-0 font-medium">Lo que recibes en tu cuenta bancaria</p>
                        </div>
                    </div>
                </div>"""
        body = flexible_replace(body, old_infographic, new_infographic)
        
        # Also clean up the CTA card
        old_cta = """<!-- CTA -->
                <div class="mt-10 p-8 rounded-2xl bg-gradient-to-r from-emerald-900/30 to-blue-900/50 border border-emerald-500/20 text-center">
                    <h3 class="!text-white !text-xl !font-bold !mb-3 !mt-0 !border-0 !pb-0">
                        Verifica tu liquidación en segundos
                    </h3>
                    <p class="!text-slate-300 !text-sm !mb-5">
                        Ingresa tu sueldo bruto y nuestra calculadora te mostrará exactamente cuánto deberían ser tus descuentos de AFP, salud, impuesto y tu sueldo líquido final.
                    </p>
                    <a href="/sueldo_liquido"
                        class="inline-flex items-center gap-2 px-10 py-4 bg-blue-600 hover:bg-blue-500 text-white font-bold text-lg rounded-xl shadow-lg shadow-blue-500/30 transition-all hover:scale-105">
                        <span class="material-icons">account_balance_wallet</span>
                        Verificar mi Sueldo Líquido
                    </a>
                </div>"""
        new_cta = """<!-- CTA -->
                <div class="mt-10 p-8 rounded-2xl bg-gradient-to-br from-sky-50 to-blue-50 border border-sky-100 text-center shadow-sm">
                    <h3 class="text-slate-900 text-xl font-bold mb-3 mt-0 border-0 pb-0">
                        Verifica tu liquidación en segundos
                    </h3>
                    <p class="text-slate-600 text-sm mb-5">
                        Ingresa tu sueldo bruto y nuestra calculadora te mostrará exactamente cuánto deberían ser tus descuentos de AFP, salud, impuesto y tu sueldo líquido final.
                    </p>
                    <a href="sueldo_liquido"
                        class="cta-btn inline-flex items-center justify-center gap-2 px-6 py-3 bg-sky-500 text-white hover:bg-sky-600 rounded-xl shadow-md shadow-sky-500/10 transition-all hover:scale-[1.01]">
                        <span class="material-icons">account_balance_wallet</span>
                        Verificar mi Sueldo Líquido
                    </a>
                </div>"""
        body = flexible_replace(body, old_cta, new_cta)
        
        # Legal warning
        old_warning = """<div class="mt-8 p-4 rounded-lg bg-slate-800/30 border border-white/5">
                    <p class="!text-xs !text-slate-500 !mb-0 !leading-relaxed">
                        <strong>Aviso legal:</strong> Esta guía es de carácter informativo. Los porcentajes y topes indicados están actualizados a abril 2026. Para consultas específicas sobre tu situación, contacta al departamento de recursos humanos de tu empresa o a la Dirección del Trabajo.
                    </p>
                </div>"""
        new_warning = """<div class="mt-8 p-4 rounded-lg bg-slate-50 border border-slate-200">
                    <p class="!text-xs !text-slate-600 !mb-0 !leading-relaxed">
                        <strong>Aviso legal:</strong> Esta guía es de carácter informativo. Los porcentajes y topes indicados están actualizados a abril 2026. Para consultas específicas sobre tu situación, contacta al departamento de recursos humanos de tu empresa o a la Dirección del Trabajo.
                    </p>
                </div>"""
        body = flexible_replace(body, old_warning, new_warning)

    elif filename == "como-calcular-sueldo-liquido-paso-a-paso.html":
        # EEAT badge
        old_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-slate-800/40 border border-white/10 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-blue-400">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-white font-semibold m-0">Basado en la normativa local</p>
                        <p class="text-xs text-slate-400 m-0">Alineado a la legislación del SII y la Superintendencia de Pensiones en Chile.</p>
                    </div>
                </div>"""
        new_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-sky-50 border border-sky-100 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-sky-600">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-slate-800 font-semibold m-0">Basado en la normativa local</p>
                        <p class="text-xs text-slate-500 m-0">Alineado a la legislación del SII y la Superintendencia de Pensiones en Chile.</p>
                    </div>
                </div>"""
        body = flexible_replace(body, old_eeat, new_eeat)

        # Flow infographic
        old_flow = """<!-- Infografía HTML: Flujo de cálculo sueldo líquido -->
                <div class="my-8 p-6 rounded-2xl bg-gradient-to-b from-slate-800/60 to-slate-900/60 border border-white/10 shadow-xl">
                    <p class="text-center text-xs font-bold text-slate-400 uppercase tracking-widest mb-5">Del sueldo bruto al sueldo líquido</p>
                    <div class="max-w-xs mx-auto space-y-2">
                        <div class="rounded-lg bg-emerald-500/15 border border-emerald-500/30 px-4 py-3 text-center">
                            <p class="!text-emerald-400 !text-xs !font-bold !mb-0 !uppercase">Sueldo Bruto</p>
                            <p class="!text-white !text-lg !font-bold !mb-0">$1.200.000</p>
                        </div>
                        <div class="flex justify-center"><span class="material-icons text-slate-600 text-sm">arrow_downward</span></div>
                        <div class="rounded-lg bg-red-500/10 border border-red-500/20 px-4 py-2 flex justify-between items-center">
                            <span class="text-slate-300 text-xs">AFP (11,27%)</span>
                            <span class="text-rose-400 text-xs font-bold">−$135.240</span>
                        </div>
                        <div class="rounded-lg bg-red-500/10 border border-red-500/20 px-4 py-2 flex justify-between items-center">
                            <span class="text-slate-300 text-xs">Salud (7%)</span>
                            <span class="text-rose-400 text-xs font-bold">−$84.000</span>
                        </div>
                        <div class="rounded-lg bg-red-500/10 border border-red-500/20 px-4 py-2 flex justify-between items-center">
                            <span class="text-slate-300 text-xs">Cesantía (0,6%)</span>
                            <span class="text-rose-400 text-xs font-bold">−$7.200</span>
                        </div>
                        <div class="rounded-lg bg-amber-500/10 border border-amber-500/20 px-4 py-2 flex justify-between items-center">
                            <span class="text-slate-300 text-xs">Impuesto Único</span>
                            <span class="text-amber-400 text-xs font-bold">−$0 (exento)</span>
                        </div>
                        <div class="flex justify-center"><span class="material-icons text-slate-600 text-sm">arrow_downward</span></div>
                        <div class="rounded-lg bg-blue-500/15 border border-blue-500/40 px-4 py-3 text-center shadow-lg shadow-blue-500/10">
                            <p class="!text-blue-400 !text-xs !font-bold !mb-0 !uppercase">Sueldo Líquido</p>
                            <p class="!text-white !text-lg !font-bold !mb-0">$973.560</p>
                        </div>
                    </div>
                </div>"""
        new_flow = """<!-- Infografía HTML: Flujo de cálculo sueldo líquido -->
                <div class="my-8 p-6 rounded-2xl bg-slate-50 border border-slate-200 shadow-sm">
                    <p class="text-center text-xs font-bold text-slate-500 uppercase tracking-widest mb-5">Del sueldo bruto al sueldo líquido</p>
                    <div class="max-w-xs mx-auto space-y-2">
                        <div class="rounded-lg bg-emerald-50 border border-emerald-200 px-4 py-3 text-center shadow-sm">
                            <p class="text-emerald-700 text-xs font-bold mb-0 uppercase">Sueldo Bruto</p>
                            <p class="text-slate-800 text-lg font-bold mb-0">$1.200.000</p>
                        </div>
                        <div class="flex justify-center"><span class="material-icons text-sky-500 text-sm font-bold">arrow_downward</span></div>
                        <div class="rounded-lg bg-white border border-slate-100 px-4 py-2 flex justify-between items-center shadow-sm">
                            <span class="text-slate-600 text-xs font-medium">AFP (11,27%)</span>
                            <span class="text-rose-600 text-xs font-bold">−$135.240</span>
                        </div>
                        <div class="rounded-lg bg-white border border-slate-100 px-4 py-2 flex justify-between items-center shadow-sm">
                            <span class="text-slate-600 text-xs font-medium">Salud (7%)</span>
                            <span class="text-rose-600 text-xs font-bold">−$84.000</span>
                        </div>
                        <div class="rounded-lg bg-white border border-slate-100 px-4 py-2 flex justify-between items-center shadow-sm">
                            <span class="text-slate-600 text-xs font-medium">Cesantía (0,6%)</span>
                            <span class="text-rose-600 text-xs font-bold">−$7.200</span>
                        </div>
                        <div class="rounded-lg bg-white border border-slate-100 px-4 py-2 flex justify-between items-center shadow-sm">
                            <span class="text-slate-600 text-xs font-medium">Impuesto Único</span>
                            <span class="text-amber-600 text-xs font-bold">−$0 (exento)</span>
                        </div>
                        <div class="flex justify-center"><span class="material-icons text-sky-500 text-sm font-bold">arrow_downward</span></div>
                        <div class="rounded-lg bg-gradient-to-r from-sky-50 to-blue-50 border border-sky-200 px-4 py-3 text-center shadow-sm">
                            <p class="text-sky-600 text-xs font-bold mb-0 uppercase">Sueldo Líquido</p>
                            <p class="text-sky-600 text-lg font-bold mb-0">$973.560</p>
                        </div>
                    </div>
                </div>"""
        body = flexible_replace(body, old_flow, new_flow)

        # Cross links box
        old_cross = """<!-- Callout con enlaces cruzados -->
                <div class="my-6 p-5 rounded-xl bg-slate-800/60 border border-emerald-500/20 shadow-lg">
                    <h4 class="text-emerald-400 font-bold text-sm mb-2 flex items-center gap-2 m-0">
                        <span class="material-icons text-base">info</span> ¿Quieres profundizar en tus haberes y jornada laboral?
                    </h4>
                    <p class="text-xs text-slate-300 mb-3 leading-relaxed">
                        Entender tu liquidación va más allá del cálculo básico de líquido. Te recomendamos leer nuestras guías especializadas:
                    </p>
                    <ul class="text-xs text-slate-400 space-y-2 m-0 pl-4">
                        <li>
                            <a href="/como-leer-liquidacion-de-sueldo" class="text-white hover:text-emerald-400 font-semibold underline transition-colors">
                                Cómo leer tu liquidación de sueldo en Chile
                            </a>: Una explicación rubro por rubro de cada descuento previsional e impuesto.
                        </li>
                        <li>
                            <a href="/ley-40-horas-chile-2026" class="text-white hover:text-emerald-400 font-semibold underline transition-colors">
                                Ley de 40 Horas Chile 2026
                            </a>: Todo sobre la reducción gradual de jornada y cómo afecta el cálculo de tus horas extras.
                        </li>
                    </ul>
                </div>"""
        new_cross = """<!-- Callout con enlaces cruzados -->
                <div class="my-6 p-5 rounded-xl bg-emerald-50/40 border border-emerald-200 shadow-sm">
                    <h4 class="text-emerald-700 font-bold text-sm mb-2 flex items-center gap-2 m-0">
                        <span class="material-icons text-base">info</span> ¿Quieres profundizar en tus haberes y jornada laboral?
                    </h4>
                    <p class="text-xs text-slate-600 mb-3 leading-relaxed">
                        Entender tu liquidación va más allá del cálculo básico de líquido. Te recomendamos leer nuestras guías especializadas:
                    </p>
                    <ul class="text-xs text-slate-600 space-y-2 m-0 pl-4">
                        <li>
                            <a href="como-leer-liquidacion-de-sueldo" class="text-sky-600 hover:text-sky-700 font-semibold transition-colors">
                                Cómo leer tu liquidación de sueldo en Chile
                            </a>: Una explicación rubro por rubro de cada descuento previsional e impuesto.
                        </li>
                        <li>
                            <a href="ley-40-horas-chile-2026" class="text-sky-600 hover:text-sky-700 font-semibold transition-colors">
                                Ley de 40 Horas Chile 2026
                            </a>: Todo sobre la reducción gradual de jornada y cómo afecta el cálculo de tus horas extras.
                        </li>
                    </ul>
                </div>"""
        body = flexible_replace(body, old_cross, new_cross)

        # Simulation details card
        old_sim = """<div class="bg-slate-800/50 rounded-xl p-5 border border-white/10 my-4 shadow-lg shadow-black/20">
                    <ul class="!list-none !p-0">
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2"><span class="text-slate-300">Haberes Imponibles base:</span> <strong class="text-white">$1.200.000</strong></li>
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2 text-rose-300"><span>Cotización AFP (10% + 1,27% = 11,27%):</span> <strong>-$135.240</strong></li>
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2 text-rose-300"><span>Salud Fonasa (7%):</span> <strong>-$84.000</strong></li>
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2 text-rose-300"><span>Cesantía (0,6%):</span> <strong>-$7.200</strong></li>
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2"><span class="text-yellow-100/80">Total Cotizaciones Excluidas:</span> <strong>$226.440</strong></li>
                        <li class="flex justify-between font-bold text-white border-b border-white/5 pb-2 mb-2"><span>Renta Líquida Imponible:</span> <span>$973.560</span></li>
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2 text-rose-300"><span>Impuesto Único retenido (según SII aproximado):</span> <strong>-$1.202</strong></li>
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2 text-emerald-300"><span>Suma de Haberes No Imponibles (Colación/Movilización):</span> <strong>+$50.000</strong></li>
                        <li class="flex justify-between text-lg font-bold text-blue-400 pt-2"><span class="text-white">SUELDO LÍQUIDO FINAL AL BOLSILLO:</span> <span>$1.022.358</span></li>
                    </ul>
                </div>"""
        new_sim = """<div class="bg-white border border-slate-200 rounded-xl p-5 my-4 shadow-sm">
                    <ul class="!list-none !p-0">
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2"><span class="text-slate-600 font-medium">Haberes Imponibles base:</span> <strong class="text-slate-800">$1.200.000</strong></li>
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2 text-rose-600"><span>Cotización AFP (10% + 1,27% = 11,27%):</span> <strong>-$135.240</strong></li>
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2 text-rose-600"><span>Salud Fonasa (7%):</span> <strong>-$84.000</strong></li>
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2 text-rose-600"><span>Cesantía (0,6%):</span> <strong>-$7.200</strong></li>
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2"><span class="text-slate-600 font-medium">Total Cotizaciones Excluidas:</span> <strong class="text-slate-800">$226.440</strong></li>
                        <li class="flex justify-between font-bold text-slate-800 border-b border-slate-100 pb-2 mb-2"><span>Renta Líquida Imponible:</span> <span class="text-slate-900">$973.560</span></li>
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2 text-rose-600"><span>Impuesto Único retenido (según SII aproximado):</span> <strong>-$1.202</strong></li>
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2 text-emerald-600"><span>Suma de Haberes No Imponibles (Colación/Movilización):</span> <strong>+$50.000</strong></li>
                        <li class="flex justify-between text-lg font-bold text-sky-600 pt-2"><span class="text-slate-800">SUELDO LÍQUIDO FINAL AL BOLSILLO:</span> <span>$1.022.358</span></li>
                    </ul>
                </div>"""
        body = flexible_replace(body, old_sim, new_sim)

    elif filename == "ley-40-horas-chile-2026.html":
        # EEAT badge
        old_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-slate-800/40 border border-white/10 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-blue-400">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-white font-semibold m-0">Normativa Ley 21.561</p>
                        <p class="text-xs text-slate-400 m-0">Reducción gradual de jornada ordinaria en Chile.</p>
                    </div>
                </div>"""
        new_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-sky-50 border border-sky-100 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-sky-600">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-slate-800 font-semibold m-0">Normativa Ley 21.561</p>
                        <p class="text-xs text-slate-500 m-0">Reducción gradual de jornada ordinaria en Chile.</p>
                    </div>
                </div>"""
        body = flexible_replace(body, old_eeat, new_eeat)

        # Timeline infographic
        old_timeline = """<!-- Infografía HTML: Timeline Ley 40 Horas -->
                <div class="my-8 p-6 rounded-2xl bg-gradient-to-b from-slate-800/60 to-slate-900/60 border border-white/10 shadow-xl">
                    <p class="text-center text-xs font-bold text-slate-400 uppercase tracking-widest mb-6">Calendario de implementación · Ley 21.561</p>
                    <div class="grid grid-cols-3 gap-3 sm:gap-6 text-center">
                        <div class="opacity-60">
                            <div class="w-12 h-12 sm:w-16 sm:h-16 mx-auto rounded-full bg-slate-700/50 border-2 border-slate-600 flex items-center justify-center mb-2">
                                <span class="text-lg sm:text-2xl font-bold text-slate-400">44</span>
                            </div>
                            <p class="!text-slate-500 !text-xs !mb-0 font-semibold">Abril 2024</p>
                            <p class="!text-slate-600 !text-[10px] !mb-0">Completado ✓</p>
                        </div>
                        <div>
                            <div class="w-12 h-12 sm:w-16 sm:h-16 mx-auto rounded-full bg-blue-500/20 border-2 border-blue-400 flex items-center justify-center mb-2 shadow-lg shadow-blue-500/20 ring-4 ring-blue-500/10">
                                <span class="text-lg sm:text-2xl font-bold text-blue-400">42</span>
                            </div>
                            <p class="!text-blue-400 !text-xs !font-bold !mb-0 font-bold">Abril 2026</p>
                            <p class="!text-blue-300 !text-[10px] !mb-0 font-semibold">← ESTAMOS AQUÍ</p>
                        </div>
                        <div class="opacity-40">
                            <div class="w-12 h-12 sm:w-16 sm:h-16 mx-auto rounded-full bg-slate-700/30 border-2 border-slate-700 border-dashed flex items-center justify-center mb-2">
                                <span class="text-lg sm:text-2xl font-bold text-slate-500">40</span>
                            </div>
                            <p class="!text-slate-500 !text-xs !mb-0 font-semibold">Abril 2028</p>
                            <p class="!text-slate-600 !text-[10px] !mb-0">Meta final</p>
                        </div>
                    </div>
                    <div class="relative mt-4 mb-2 mx-4 sm:mx-8">
                        <div class="h-1 bg-slate-700 rounded-full"></div>
                        <div class="absolute top-0 left-0 h-1 bg-gradient-to-r from-blue-600 to-blue-400 rounded-full" style="width: 50%"></div>
                    </div>
                    <p class="text-center !text-[10px] !text-slate-500 !mb-0 mt-3">Horas semanales máximas de jornada ordinaria</p>
                </div>"""
        new_timeline = """<!-- Infografía HTML: Timeline Ley 40 Horas -->
                <div class="my-8 p-6 rounded-2xl bg-slate-50 border border-slate-200 shadow-sm">
                    <p class="text-center text-xs font-bold text-slate-500 uppercase tracking-widest mb-6">Calendario de implementación · Ley 21.561</p>
                    <div class="grid grid-cols-3 gap-3 sm:gap-6 text-center">
                        <div class="opacity-60">
                            <div class="w-12 h-12 sm:w-16 sm:h-16 mx-auto rounded-full bg-slate-200 border-2 border-slate-300 flex items-center justify-center mb-2">
                                <span class="text-lg sm:text-2xl font-bold text-slate-600">44</span>
                            </div>
                            <p class="text-slate-500 text-xs mb-0 font-semibold">Abril 2024</p>
                            <p class="text-slate-600 text-[10px] mb-0">Completado ✓</p>
                        </div>
                        <div>
                            <div class="w-12 h-12 sm:w-16 sm:h-16 mx-auto rounded-full bg-sky-100 border-2 border-sky-400 flex items-center justify-center mb-2 shadow-sm ring-4 ring-sky-100/50">
                                <span class="text-lg sm:text-2xl font-bold text-sky-600">42</span>
                            </div>
                            <p class="text-sky-600 text-xs mb-0 font-bold">Abril 2026</p>
                            <p class="text-sky-500 text-[10px] mb-0 font-semibold">← ESTAMOS AQUÍ</p>
                        </div>
                        <div class="opacity-40">
                            <div class="w-12 h-12 sm:w-16 sm:h-16 mx-auto rounded-full bg-slate-100 border-2 border-slate-200 border-dashed flex items-center justify-center mb-2">
                                <span class="text-lg sm:text-2xl font-bold text-slate-400">40</span>
                            </div>
                            <p class="text-slate-500 text-xs mb-0 font-semibold">Abril 2028</p>
                            <p class="text-slate-600 text-[10px] mb-0">Meta final</p>
                        </div>
                    </div>
                    <div class="relative mt-4 mb-2 mx-4 sm:mx-8">
                        <div class="h-1 bg-slate-200 rounded-full"></div>
                        <div class="absolute top-0 left-0 h-1 bg-gradient-to-r from-sky-500 to-blue-500 rounded-full" style="width: 50%"></div>
                    </div>
                    <p class="text-center !text-[10px] !text-slate-500 !mb-0 mt-3">Horas semanales máximas de jornada ordinaria</p>
                </div>"""
        body = flexible_replace(body, old_timeline, new_timeline)

        # Timeline list
        old_timeline_list = """<div class="my-8 ml-4">
                    <div class="timeline-item">
                        <p class="!text-slate-400 !text-sm !mb-1"><strong class="text-slate-300">Abril 2024 — Primera reducción</strong></p>
                        <p class="!text-slate-500 !text-sm !mb-0">Jornada máxima baja de 45 a <strong class="text-white">44 horas semanales</strong></p>
                    </div>
                    <div class="timeline-item active">
                        <p class="!text-blue-400 !text-sm !mb-1"><strong>Abril 2026 — Segunda reducción ← ESTAMOS AQUÍ</strong></p>
                        <p class="!text-slate-400 !text-sm !mb-0">Jornada máxima baja de 44 a <strong class="text-white">42 horas semanales</strong></p>
                    </div>
                    <div class="timeline-item future">
                        <p class="!text-slate-400 !text-sm !mb-1"><strong class="text-slate-500">Abril 2028 — Implementación completa</strong></p>
                        <p class="!text-slate-500 !text-sm !mb-0">Jornada máxima baja de 42 a <strong>40 horas semanales</strong></p>
                    </div>
                </div>"""
        new_timeline_list = """<div class="my-8 ml-4 border-l-2 border-slate-200 pl-4 space-y-4">
                    <div class="relative">
                        <div class="absolute -left-[21px] top-1.5 w-2 h-2 rounded-full bg-slate-300"></div>
                        <p class="text-slate-400 text-sm mb-1"><strong>Abril 2024 — Primera reducción</strong></p>
                        <p class="text-slate-500 text-sm mb-0">Jornada máxima baja de 45 a <strong class="text-slate-700 font-semibold">44 horas semanales</strong> (Completado)</p>
                    </div>
                    <div class="relative bg-sky-50/50 border border-sky-100 rounded-xl p-3 -mx-3">
                        <div class="absolute -left-[13px] top-[18px] w-3 h-3 rounded-full bg-sky-500 shadow-sm ring-4 ring-sky-100"></div>
                        <p class="text-sky-600 text-sm mb-1 font-bold">Abril 2026 — Segunda reducción ← ESTAMOS AQUÍ</p>
                        <p class="text-slate-600 text-sm mb-0">Jornada máxima baja de 44 a <strong class="text-slate-800 font-bold">42 horas semanales</strong></p>
                    </div>
                    <div class="relative opacity-60">
                        <div class="absolute -left-[21px] top-1.5 w-2 h-2 rounded-full bg-slate-200"></div>
                        <p class="text-slate-400 text-sm mb-1"><strong>Abril 2028 — Implementación completa</strong></p>
                        <p class="text-slate-500 text-sm mb-0">Jornada máxima baja de 42 a <strong class="text-slate-700 font-semibold">40 horas semanales</strong></p>
                    </div>
                </div>"""
        body = flexible_replace(body, old_timeline_list, new_timeline_list)

        # Minimum wage update
        body = body.replace("el sueldo mínimo es de <strong>$510.000</strong>", "el sueldo mínimo es de <strong>$539.000</strong>")

    elif filename == "que-hacer-si-no-te-pagan-el-finiquito.html":
        # EEAT badge
        old_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-slate-800/40 border border-white/10 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-red-500/20 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-red-400">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-white font-semibold m-0">Información Legal de Confianza</p>
                        <p class="text-xs text-slate-400 m-0">Artículos 163, 168, 169 y 480 del Código del Trabajo de Chile. Información verificada con la Dirección del Trabajo.</p>
                    </div>
                </div>"""
        new_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-sky-50 border border-sky-100 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-sky-600">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-slate-800 font-semibold m-0">Información Legal de Confianza</p>
                        <p class="text-xs text-slate-500 m-0">Artículos 163, 168, 169 y 480 del Código del Trabajo de Chile. Información verificada con la Dirección del Trabajo.</p>
                    </div>
                </div>"""
        body = flexible_replace(body, old_eeat, new_eeat)

        # 5 steps infographic
        old_steps = """<!-- Infografía HTML: 5 Pasos para reclamar finiquito -->
                <div class="my-8 p-6 rounded-2xl bg-gradient-to-b from-slate-800/60 to-slate-900/60 border border-white/10 shadow-xl">
                    <p class="text-center text-xs font-bold text-slate-400 uppercase tracking-widest mb-5">Proceso para reclamar tu finiquito</p>
                    <div class="flex flex-col sm:flex-row items-center justify-between gap-2 sm:gap-1">
                        <div class="flex flex-col items-center text-center flex-1">
                            <div class="w-10 h-10 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center mb-1.5">
                                <span class="material-icons text-blue-400 text-sm">calculate</span>
                            </div>
                            <p class="!text-[10px] sm:!text-xs !text-white !font-semibold !mb-0 !leading-tight">1. Calcula<br>lo adeudado</p>
                        </div>
                        <span class="material-icons text-slate-600 text-sm hidden sm:block">arrow_forward</span>
                        <span class="material-icons text-slate-600 text-sm sm:hidden">arrow_downward</span>
                        <div class="flex flex-col items-center text-center flex-1">
                            <div class="w-10 h-10 rounded-full bg-purple-500/20 border border-purple-500/30 flex items-center justify-center mb-1.5">
                                <span class="material-icons text-purple-400 text-sm">email</span>
                            </div>
                            <p class="!text-[10px] sm:!text-xs !text-white !font-semibold !mb-0 !leading-tight">2. Contacta<br>al empleador</p>
                        </div>
                        <span class="material-icons text-slate-600 text-sm hidden sm:block">arrow_forward</span>
                        <span class="material-icons text-slate-600 text-sm sm:hidden">arrow_downward</span>
                        <div class="flex flex-col items-center text-center flex-1">
                            <div class="w-10 h-10 rounded-full bg-amber-500/20 border border-amber-500/30 flex items-center justify-center mb-1.5">
                                <span class="material-icons text-amber-400 text-sm">account_balance</span>
                            </div>
                            <p class="!text-[10px] sm:!text-xs !text-white !font-semibold !mb-0 !leading-tight">3. Reclama<br>ante la DT</p>
                        </div>
                        <span class="material-icons text-slate-600 text-sm hidden sm:block">arrow_forward</span>
                        <span class="material-icons text-slate-600 text-sm sm:hidden">arrow_downward</span>
                        <div class="flex flex-col items-center text-center flex-1">
                            <div class="w-10 h-10 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center mb-1.5">
                                <span class="material-icons text-emerald-400 text-sm">handshake</span>
                            </div>
                            <p class="!text-[10px] sm:!text-xs !text-white !font-semibold !mb-0 !leading-tight">4. Audiencia<br>conciliación</p>
                        </div>
                        <span class="material-icons text-slate-600 text-sm hidden sm:block">arrow_forward</span>
                        <span class="material-icons text-slate-600 text-sm sm:hidden">arrow_downward</span>
                        <div class="flex flex-col items-center text-center flex-1">
                            <div class="w-10 h-10 rounded-full bg-red-500/20 border border-red-500/30 flex items-center justify-center mb-1.5">
                                <span class="material-icons text-red-400 text-sm">gavel</span>
                            </div>
                            <p class="!text-[10px] sm:!text-xs !text-white !font-semibold !mb-0 !leading-tight">5. Demanda<br>judicial</p>
                        </div>
                    </div>
                </div>"""
        new_steps = """<!-- Infografía HTML: 5 Pasos para reclamar finiquito -->
                <div class="my-8 p-6 rounded-2xl bg-slate-50 border border-slate-200 shadow-sm">
                    <p class="text-center text-xs font-bold text-slate-500 uppercase tracking-widest mb-5">Proceso para reclamar tu finiquito</p>
                    <div class="flex flex-col sm:flex-row items-center justify-between gap-4 sm:gap-1">
                        <div class="flex flex-col items-center text-center flex-1">
                            <div class="w-10 h-10 rounded-full bg-sky-100 border border-sky-200 flex items-center justify-center mb-1.5 shadow-sm">
                                <span class="material-icons text-sky-600 text-sm">calculate</span>
                            </div>
                            <p class="text-[10px] sm:text-xs text-slate-700 font-semibold mb-0 leading-tight">1. Calcula<br>lo adeudado</p>
                        </div>
                        <span class="material-icons text-slate-400 text-sm hidden sm:block">arrow_forward</span>
                        <span class="material-icons text-slate-400 text-sm sm:hidden">arrow_downward</span>
                        <div class="flex flex-col items-center text-center flex-1">
                            <div class="w-10 h-10 rounded-full bg-purple-100 border border-purple-200 flex items-center justify-center mb-1.5 shadow-sm">
                                <span class="material-icons text-purple-600 text-sm">email</span>
                            </div>
                            <p class="text-[10px] sm:text-xs text-slate-700 font-semibold mb-0 leading-tight">2. Contacta<br>al empleador</p>
                        </div>
                        <span class="material-icons text-slate-400 text-sm hidden sm:block">arrow_forward</span>
                        <span class="material-icons text-slate-400 text-sm sm:hidden">arrow_downward</span>
                        <div class="flex flex-col items-center text-center flex-1">
                            <div class="w-10 h-10 rounded-full bg-amber-100 border border-amber-200 flex items-center justify-center mb-1.5 shadow-sm">
                                <span class="material-icons text-amber-600 text-sm">account_balance</span>
                            </div>
                            <p class="text-[10px] sm:text-xs text-slate-700 font-semibold mb-0 leading-tight">3. Reclama<br>ante la DT</p>
                        </div>
                        <span class="material-icons text-slate-400 text-sm hidden sm:block">arrow_forward</span>
                        <span class="material-icons text-slate-400 text-sm sm:hidden">arrow_downward</span>
                        <div class="flex flex-col items-center text-center flex-1">
                            <div class="w-10 h-10 rounded-full bg-emerald-100 border border-emerald-200 flex items-center justify-center mb-1.5 shadow-sm">
                                <span class="material-icons text-emerald-600 text-sm">handshake</span>
                            </div>
                            <p class="text-[10px] sm:text-xs text-slate-700 font-semibold mb-0 leading-tight">4. Audiencia<br>conciliación</p>
                        </div>
                        <span class="material-icons text-slate-400 text-sm hidden sm:block">arrow_forward</span>
                        <span class="material-icons text-slate-400 text-sm sm:hidden">arrow_downward</span>
                        <div class="flex flex-col items-center text-center flex-1">
                            <div class="w-10 h-10 rounded-full bg-red-100 border border-red-200 flex items-center justify-center mb-1.5 shadow-sm">
                                <span class="material-icons text-red-600 text-sm">gavel</span>
                            </div>
                            <p class="text-[10px] sm:text-xs text-slate-700 font-semibold mb-0 leading-tight">5. Demanda<br>judicial</p>
                        </div>
                    </div>
                </div>"""
        body = flexible_replace(body, old_steps, new_steps)

        # Delay consequences
        old_delay = """<div class="bg-slate-800/50 rounded-xl p-5 border border-white/10 my-4 shadow-lg shadow-black/20">
                    <ul class="!list-none !p-0">
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2"><span class="text-slate-300">Reajuste IPC:</span> <strong class="text-amber-400">Las sumas adeudadas se reajustan por inflación</strong></li>
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2"><span class="text-slate-300">Interés máximo convencional:</span> <strong class="text-amber-400">Se acumulan intereses desde el primer día de atraso</strong></li>
                        <li class="flex justify-between text-red-300 pt-1"><span>Recargo legal (Art. 168):</span> <strong>Hasta un 150% de la última remuneración mensual</strong></li>
                    </ul>
                </div>"""
        new_delay = """<div class="bg-white border border-slate-200 rounded-xl p-5 my-4 shadow-sm">
                    <ul class="!list-none !p-0">
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2"><span class="text-slate-600 font-medium">Reajuste IPC:</span> <strong class="text-amber-700">Las sumas adeudadas se reajustan por inflación</strong></li>
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2"><span class="text-slate-600 font-medium">Interés máximo convencional:</span> <strong class="text-amber-700">Se acumulan intereses desde el primer día de atraso</strong></li>
                        <li class="flex justify-between text-rose-600 pt-1"><span>Recargo legal (Art. 168):</span> <strong class="text-rose-700">Hasta un 150% de la última remuneración mensual</strong></li>
                    </ul>
                </div>"""
        body = flexible_replace(body, old_delay, new_delay)

        # Deadlines
        old_deadlines = """<div class="bg-slate-800/50 rounded-xl p-5 border border-white/10 my-4">
                    <ul class="!list-none !p-0">
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2"><span class="text-slate-300">Pago del finiquito:</span> <strong class="text-white">10 días hábiles desde la separación</strong></li>
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2"><span class="text-slate-300">Reclamo ante la DT:</span> <strong class="text-white">Sin plazo definido (pero mejor pronto)</strong></li>
                        <li class="flex justify-between border-b border-white/5 pb-2 mb-2"><span class="text-slate-300">Demanda judicial:</span> <strong class="text-white">60 días hábiles desde el despido</strong></li>
                        <li class="flex justify-between"><span class="text-slate-300">Prescripción de derechos laborales:</span> <strong class="text-white">2 años desde que se hicieron exigibles</strong></li>
                    </ul>
                </div>"""
        new_deadlines = """<div class="bg-white border border-slate-200 rounded-xl p-5 my-4 shadow-sm">
                    <ul class="!list-none !p-0">
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2"><span class="text-slate-600 font-medium">Pago del finiquito:</span> <strong class="text-slate-800">10 días hábiles desde la separación</strong></li>
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2"><span class="text-slate-600 font-medium">Reclamo ante la DT:</span> <strong class="text-slate-800">Sin plazo definido (pero mejor pronto)</strong></li>
                        <li class="flex justify-between border-b border-slate-100 pb-2 mb-2"><span class="text-slate-600 font-medium">Demanda judicial:</span> <strong class="text-slate-800">60 días hábiles desde el despido</strong></li>
                        <li class="flex justify-between"><span class="text-slate-600 font-medium">Prescripción de derechos laborales:</span> <strong class="text-slate-800">2 años desde que se hicieron exigibles</strong></li>
                    </ul>
                </div>"""
        body = flexible_replace(body, old_deadlines, new_deadlines)

    elif filename == "como-calcular-finiquito-chile.html":
        # EEAT badge
        old_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-slate-800/40 border border-white/10 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-blue-400">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-white font-semibold m-0">Base Legal y Normativa 2026</p>
                        <p class="text-xs text-slate-400 m-0">Artículo 177 y siguientes del Código del Trabajo en Chile. Datos actualizados a los topes de UF e IMM de 2026.</p>
                    </div>
                </div>"""
        new_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-sky-50 border border-sky-100 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-sky-600">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-slate-800 font-semibold m-0">Base Legal y Normativa 2026</p>
                        <p class="text-xs text-slate-500 m-0">Artículo 177 y siguientes del Código del Trabajo en Chile. Datos actualizados a los topes de UF e IMM de 2026.</p>
                    </div>
                </div>"""
        body = flexible_replace(body, old_eeat, new_eeat)

        # Warning callout
        old_warning = """<div class="my-6 p-5 rounded-xl bg-slate-800/60 border border-red-500/20 shadow-lg">
                    <h4 class="text-red-400 font-bold text-sm mb-2 flex items-center gap-2 m-0">
                        <span class="material-icons text-base">warning</span> ¿Tu empleador se está retrasando en el pago?
                    </h4>
                    <p class="text-xs text-slate-300 mb-3 leading-relaxed">
                        Por ley, existe un plazo máximo estricto para el pago de tu liquidación final. Te recomendamos leer nuestra guía crítica:
                    </p>
                    <p class="text-xs text-slate-400 m-0">
                        &rarr; <a href="/que-hacer-si-no-te-pagan-el-finiquito" class="text-white hover:text-red-400 font-semibold underline transition-colors">
                            Qué hacer si no te pagan el finiquito a tiempo en Chile
                        </a>: Conoce las multas, el reajuste por IPC y cómo iniciar un reclamo formal ante la Inspección del Trabajo.
                    </p>
                </div>"""
        new_warning = """<div class="my-6 p-5 rounded-xl bg-red-50 border border-red-200 shadow-sm">
                    <h4 class="text-red-700 font-bold text-sm mb-2 flex items-center gap-2 m-0">
                        <span class="material-icons text-base">warning</span> ¿Tu empleador se está retrasando en el pago?
                    </h4>
                    <p class="text-xs text-slate-600 mb-3 leading-relaxed">
                        Por ley, existe un plazo máximo estricto para el pago de tu liquidación final. Te recomendamos leer nuestra guía crítica:
                    </p>
                    <p class="text-xs text-slate-650 m-0 font-medium">
                        &rarr; <a href="que-hacer-si-no-te-pagan-el-finiquito" class="text-sky-600 hover:text-sky-700 font-semibold transition-colors">
                            Qué hacer si no te pagan el finiquito a tiempo en Chile
                        </a>: Conoce las multas, el reajuste por IPC y cómo iniciar un reclamo formal ante la Inspección del Trabajo.
                    </p>
                </div>"""
        body = flexible_replace(body, old_warning, new_warning)

        # Simulation input case card
        old_inputs = """<div class="bg-slate-800/50 rounded-xl p-5 border border-white/10 my-6">
                    <h3 class="!text-white !mt-0 !mb-3 !text-base">📋 Datos del caso</h3>
                    <ul class="!mb-0">
                        <li><strong>Trabajador:</strong> contrato indefinido</li>
                        <li><strong>Sueldo base:</strong> $800.000</li>
                        <li><strong>Gratificación legal:</strong> $200.000</li>
                        <li><strong>Inicio contrato:</strong> 1 de diciembre de 2020</li>
                        <li><strong>Fecha de despido:</strong> 15 de marzo de 2026</li>
                        <li><strong>Causal:</strong> Necesidades de la empresa (Art. 161)</li>
                        <li><strong>Aviso previo:</strong> No se dio con 30 días de anticipación</li>
                        <li><strong>Vacaciones pendientes:</strong> 5 días</li>
                    </ul>
                </div>"""
        new_inputs = """<div class="bg-slate-50 border border-slate-200 rounded-xl p-5 my-6 shadow-sm">
                    <h3 class="text-slate-800 font-bold mt-0 mb-3 text-base">📋 Datos del caso</h3>
                    <ul class="mb-0 text-slate-750 space-y-1 font-medium">
                        <li><strong>Trabajador:</strong> contrato indefinido</li>
                        <li><strong>Sueldo base:</strong> $800.000</li>
                        <li><strong>Gratificación legal:</strong> $200.000</li>
                        <li><strong>Inicio contrato:</strong> 1 de diciembre de 2020</li>
                        <li><strong>Fecha de despido:</strong> 15 de marzo de 2026</li>
                        <li><strong>Causal:</strong> Necesidades de la empresa (Art. 161)</li>
                        <li><strong>Aviso previo:</strong> No se dio con 30 días de anticipación</li>
                        <li><strong>Vacaciones pendientes:</strong> 5 días</li>
                    </ul>
                </div>"""
        body = flexible_replace(body, old_inputs, new_inputs)

    elif filename == "despido-necesidades-empresa-articulo-161.html":
        # EEAT badge
        old_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-slate-800/40 border border-white/10 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-blue-400">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-white font-semibold m-0">Revisado por Equipo Legal</p>
                        <p class="text-xs text-slate-400 m-0">Basado estrictamente en el Código del Trabajo y
                            Jurisprudencia de la Dirección del Trabajo (2026).</p>
                    </div>
                </div>"""
        new_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-sky-50 border border-sky-100 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-sky-600">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-slate-800 font-semibold m-0">Revisado por Equipo Legal</p>
                        <p class="text-xs text-slate-500 m-0">Basado estrictamente en el Código del Trabajo y
                            Jurisprudencia de la Dirección del Trabajo (2026).</p>
                    </div>
                </div>"""
        body = flexible_replace(body, old_eeat, new_eeat)

        # Hero image wrapper
        old_hero_wrap = """<div class="rounded-2xl overflow-hidden border border-white/5 bg-slate-800/20">
                    <img src="assets/guia-despido-necesidades-empresa-161.png"
                        alt="Documento gráfico sobre el Artículo 161 del Código del Trabajo, mostrando causales de despido e indemnizaciones."
                        title="Despido por necesidades de la empresa (Artículo 161)"
                        class="w-full h-auto max-h-[45vh] object-contain" loading="lazy" width="1280" height="720" />
                </div>"""
        new_hero_wrap = """<div class="rounded-2xl overflow-hidden border border-slate-200 bg-slate-50">
                    <img src="assets/guia-despido-necesidades-empresa-161.png"
                        alt="Documento gráfico sobre el Artículo 161 del Código del Trabajo, mostrando causales de despido e indemnizaciones."
                        title="Despido por necesidades de la empresa (Artículo 161)"
                        class="w-full h-auto max-h-[45vh] object-contain" loading="lazy" width="1280" height="720" />
                </div>"""
        body = flexible_replace(body, old_hero_wrap, new_hero_wrap)

        # Simulation card
        old_sim = """<div class="bg-slate-800/50 rounded-xl p-5 border border-white/10 my-6">
                    <h3 class="!text-white !mt-0 !mb-3 !text-base">📋 Datos de la simulación:</h3>
                    <ul class="!mb-0">
                        <li><strong>Sueldo Bruto / Base a calcular:</strong> $1.000.000</li>
                        <li><strong>Años de vinculación laboral:</strong> 4 años y 6 meses.</li>
                        <li><strong>Notificación:</strong> Despido inmediato (sin carta 30 días antes).</li>
                    </ul>
                </div>"""
        new_sim = """<div class="bg-slate-50 border border-slate-200 rounded-xl p-5 my-6 shadow-sm">
                    <h3 class="text-slate-800 font-bold mt-0 mb-3 text-base">📋 Datos de la simulación:</h3>
                    <ul class="mb-0 text-slate-750 space-y-1 font-medium">
                        <li><strong>Sueldo Bruto / Base a calcular:</strong> $1.000.000</li>
                        <li><strong>Años de vinculación laboral:</strong> 4 años y 6 meses.</li>
                        <li><strong>Notificación:</strong> Despido inmediato (sin carta 30 días antes).</li>
                    </ul>
                </div>"""
        body = flexible_replace(body, old_sim, new_sim)

        # Comparison table
        old_table = """<div class="overflow-x-auto my-6">
                    <table
                        class="w-full text-sm border-collapse rounded-xl overflow-hidden border border-white/5 bg-slate-800/20">
                        <thead class="bg-slate-800/80">
                            <tr>
                                <th class="text-left p-4 text-white font-semibold border-b border-white/10">Aspecto</th>
                                <th
                                    class="text-center p-4 text-emerald-400 font-semibold border-b border-white/10 border-l border-white/5">
                                    Artículo 161 (Necesidades de la empresa)</th>
                                <th
                                    class="text-center p-4 text-rose-400 font-semibold border-b border-white/10 border-l border-white/5">
                                    Artículo 160 (Causales y faltas graves)</th>
                            </tr>
                        </thead>
                        <tbody class="text-slate-300 text-center">
                            <tr class="border-b border-white/5">
                                <td class="p-4 text-left font-medium">¿Hay indemnización años servicio?</td>
                                <td class="p-4 border-l border-white/5">Sí, siempre que pase de un año.</td>
                                <td class="p-4 border-l border-white/5">No, bajo ninguna circunstancia inicial.</td>
                            </tr>
                            <tr class="border-b border-white/5">
                                <td class="p-4 text-left font-medium">¿Hay aviso previo?</td>
                                <td class="p-4 border-l border-white/5">Sí, 30 días o el pago sustitutivo a un sueldo.
                                </td>
                                <td class="p-4 border-l border-white/5">No requiere aviso ni mes compensador.</td>
                            </tr>
                            <tr>
                                <td class="p-4 text-left font-medium">¿Puede impugnarse?</td>
                                <td class="p-4 border-l border-white/5">Sí, pidiendo recargos por despido injustificado
                                    (30%).</td>
                                <td class="p-4 border-l border-white/5">Sí, pero peleando despido indebido para
                                    revertirlo a Art. 161.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>"""
        new_table = """<div class="overflow-x-auto my-6 border border-slate-200 rounded-xl shadow-sm">
                    <table class="w-full text-sm border-collapse bg-white">
                        <thead class="bg-slate-50 border-b border-slate-200">
                            <tr>
                                <th class="text-left p-4 text-slate-800 font-semibold">Aspecto</th>
                                <th class="text-center p-4 text-emerald-700 font-semibold border-l border-slate-200">Artículo 161 (Necesidades de la empresa)</th>
                                <th class="text-center p-4 text-rose-700 font-semibold border-l border-slate-200">Artículo 160 (Causales y faltas graves)</th>
                            </tr>
                        </thead>
                        <tbody class="text-slate-600 text-center">
                            <tr class="border-b border-slate-100">
                                <td class="p-4 text-left font-medium text-slate-700">¿Hay indemnización años servicio?</td>
                                <td class="p-4 border-l border-slate-100">Sí, siempre que pase de un año.</td>
                                <td class="p-4 border-l border-slate-100">No, bajo ninguna circunstancia inicial.</td>
                            </tr>
                            <tr class="border-b border-slate-100">
                                <td class="p-4 text-left font-medium text-slate-700">¿Hay aviso previo?</td>
                                <td class="p-4 border-l border-slate-100">Sí, 30 días o el pago sustitutivo a un sueldo.</td>
                                <td class="p-4 border-l border-slate-100">No requiere aviso ni mes compensador.</td>
                            </tr>
                            <tr>
                                <td class="p-4 text-left font-medium text-slate-700">¿Puede impugnarse?</td>
                                <td class="p-4 border-l border-slate-100">Sí, pidiendo recargos por despido injustificado (30%).</td>
                                <td class="p-4 border-l border-slate-100">Sí, pero peleando despido indebido para revertirlo a Art. 161.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>"""
        body = flexible_replace(body, old_table, new_table)

    elif filename == "guia-vacaciones-proporcionales.html":
        # EEAT badge
        old_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-slate-800/40 border border-white/10 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-blue-400">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-white font-semibold m-0">Normativa Artículo 73</p>
                        <p class="text-xs text-slate-400 m-0">Regulado por el Código del Trabajo de Chile. Información sobre cálculo de feriado proporcional e indemnizaciones.</p>
                    </div>
                </div>"""
        new_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-sky-50 border border-sky-100 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-sky-600">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-slate-800 font-semibold m-0">Normativa Artículo 73</p>
                        <p class="text-xs text-slate-500 m-0">Regulado por el Código del Trabajo de Chile. Información sobre cálculo de feriado proporcional e indemnizaciones.</p>
                    </div>
                </div>"""
        body = flexible_replace(body, old_eeat, new_eeat)

        # Formula box
        old_formula = """<div class="bg-slate-800/50 rounded-xl p-5 border border-white/10 font-mono text-sm text-blue-300 my-6">
                    <p class="!text-blue-300 !mb-2">Días proporcionales = 15 × (meses trabajados en el período / 12)
                    </p>
                    <p class="!text-blue-300 !mb-2">Monto = (Sueldo diario) × Días proporcionales</p>
                    <p class="!text-slate-500 !mb-0 text-xs">Donde sueldo diario = Remuneración íntegra ÷ 30</p>
                </div>"""
        new_formula = """<div class="bg-slate-50 border border-slate-200 rounded-xl p-5 font-mono text-sm text-sky-700 my-6 shadow-sm">
                    <p class="text-sky-700 mb-2">Días proporcionales = 15 × (meses trabajados en el período / 12)</p>
                    <p class="text-sky-700 mb-2">Monto = (Sueldo diario) × Días proporcionales</p>
                    <p class="text-slate-500 mb-0 text-xs">Donde sueldo diario = Remuneración íntegra ÷ 30</p>
                </div>"""
        body = flexible_replace(body, old_formula, new_formula)

    elif filename == "seguro-de-cesantia-chile-como-cobrar.html":
        # EEAT badge
        old_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-slate-800/40 border border-white/10 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-blue-400">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-white font-semibold m-0">Normativa Ley 19.728</p>
                        <p class="text-xs text-slate-400 m-0">Regulación legal sobre AFC, cotizaciones y Fondo Solidario en Chile.</p>
                    </div>
                </div>"""
        new_eeat = """<div class="flex items-center gap-4 p-4 rounded-xl bg-sky-50 border border-sky-100 mb-8 mt-2">
                    <div class="w-12 h-12 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-sky-600">gavel</span>
                    </div>
                    <div>
                        <p class="text-sm text-slate-800 font-semibold m-0">Normativa Ley 19.728</p>
                        <p class="text-xs text-slate-500 m-0">Regulación legal sobre AFC, cotizaciones y Fondo Solidario en Chile.</p>
                    </div>
                </div>"""
        body = flexible_replace(body, old_eeat, new_eeat)

        # Infographic banner
        old_banner = """<div class="mb-10 rounded-2xl overflow-hidden border border-white/10 shadow-2xl" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); padding: 40px 30px;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 0; position: relative;">
                    <!-- Connecting line -->
                    <div style="position: absolute; top: 50%; left: 15%; right: 15%; height: 2px; background: linear-gradient(90deg, #10b981, #0ea5e9, #10b981); opacity: 0.3; transform: translateY(-50%); z-index: 0;"></div>
                    
                    <!-- Pillar 1: Protection -->
                    <div style="flex: 1; text-align: center; position: relative; z-index: 1;">
                        <div style="width: 72px; height: 72px; margin: 0 auto 12px; border-radius: 50%; background: rgba(16,185,129,0.12); border: 2px solid rgba(16,185,129,0.25); display: flex; align-items: center; justify-content: center;">
                            <span class="material-icons" style="font-size: 36px; color: #10b981;">shield</span>
                        </div>
                        <h4 style="color: #f1f5f9; font-size: 13px; font-weight: 700; margin: 0 0 4px;">Protección Laboral</h4>
                        <p style="color: #64748b; font-size: 11px; margin: 0; line-height: 1.4; max-width: 160px; margin: 0 auto;">Derecho de seguridad social para todo trabajador en Chile</p>
                    </div>

                    <!-- Arrow 1 -->
                    <div style="color: #334155; font-size: 24px; z-index: 1; margin: 0 -8px;">→</div>

                    <!-- Pillar 2: CIC Account -->
                    <div style="flex: 1; text-align: center; position: relative; z-index: 1;">
                        <div style="width: 72px; height: 72px; margin: 0 auto 12px; border-radius: 50%; background: rgba(14,165,233,0.12); border: 2px solid rgba(14,165,233,0.25); display: flex; align-items: center; justify-content: center;">
                            <span class="material-icons" style="font-size: 36px; color: #0ea5e9;">savings</span>
                        </div>
                        <h4 style="color: #f1f5f9; font-size: 13px; font-weight: 700; margin: 0 0 4px;">Cuenta Individual (CIC)</h4>
                        <p style="color: #64748b; font-size: 11px; margin: 0; line-height: 1.4; max-width: 160px; margin: 0 auto;">Aportes de trabajador (0,6%) y empleador (2,4%)</p>
                    </div>

                    <!-- Arrow 2 -->
                    <div style="color: #334155; font-size: 24px; z-index: 1; margin: 0 -8px;">→</div>

                    <!-- Pillar 3: Benefits -->
                    <div style="flex: 1; text-align: center; position: relative; z-index: 1;">
                        <div style="width: 72px; height: 72px; margin: 0 auto 12px; border-radius: 50%; background: rgba(16,185,129,0.12); border: 2px solid rgba(16,185,129,0.25); display: flex; align-items: center; justify-content: center;">
                            <span class="material-icons" style="font-size: 36px; color: #10b981;">payments</span>
                        </div>
                        <h4 style="color: #f1f5f9; font-size: 13px; font-weight: 700; margin: 0 0 4px;">Beneficio de Cesantía</h4>
                        <p style="color: #64748b; font-size: 11px; margin: 0; line-height: 1.4; max-width: 160px; margin: 0 auto;">Pagos mensuales del 70% al 35% del sueldo</p>
                    </div>
                </div>
            </div>"""
        new_banner = """<div class="mb-10 rounded-2xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm" style="padding: 40px 30px;">
                <div class="flex flex-col md:flex-row items-center justify-center gap-6 md:gap-2 relative">
                    <!-- Connecting line -->
                    <div class="hidden md:block absolute top-[36px] left-[15%] right-[15%] h-[2px] bg-slate-200 z-0"></div>
                    
                    <!-- Pillar 1: Protection -->
                    <div class="flex-1 text-center relative z-10">
                        <div class="w-18 h-18 mx-auto rounded-full bg-emerald-50 border-2 border-emerald-200 flex items-center justify-center mb-3 shadow-sm" style="width: 72px; height: 72px;">
                            <span class="material-icons text-3xl text-emerald-600">shield</span>
                        </div>
                        <h4 class="text-slate-800 text-sm font-bold mb-1">Protección Laboral</h4>
                        <p class="text-slate-500 text-xs max-w-[160px] mx-auto leading-relaxed">Derecho de seguridad social para todo trabajador en Chile</p>
                    </div>

                    <!-- Arrow 1 -->
                    <div class="hidden md:block text-slate-300 text-2xl z-10 font-bold">→</div>

                    <!-- Pillar 2: CIC Account -->
                    <div class="flex-1 text-center relative z-10">
                        <div class="w-18 h-18 mx-auto rounded-full bg-sky-50 border-2 border-sky-200 flex items-center justify-center mb-3 shadow-sm" style="width: 72px; height: 72px;">
                            <span class="material-icons text-3xl text-sky-500">savings</span>
                        </div>
                        <h4 class="text-slate-800 text-sm font-bold mb-1">Cuenta Individual (CIC)</h4>
                        <p class="text-slate-500 text-xs max-w-[160px] mx-auto leading-relaxed">Aportes de trabajador (0,6%) y empleador (2,4%)</p>
                    </div>

                    <!-- Arrow 2 -->
                    <div class="hidden md:block text-slate-300 text-2xl z-10 font-bold">→</div>

                    <!-- Pillar 3: Benefits -->
                    <div class="flex-1 text-center relative z-10">
                        <div class="w-18 h-18 mx-auto rounded-full bg-emerald-50 border-2 border-emerald-200 flex items-center justify-center mb-3 shadow-sm" style="width: 72px; height: 72px;">
                            <span class="material-icons text-3xl text-emerald-600">payments</span>
                        </div>
                        <h4 class="text-slate-800 text-sm font-bold mb-1">Beneficio de Cesantía</h4>
                        <p class="text-slate-500 text-xs max-w-[160px] mx-auto leading-relaxed">Pagos mensuales del 70% al 35% del sueldo</p>
                    </div>
                </div>
            </div>"""
        body = flexible_replace(body, old_banner, new_banner)

        # Warning card
        old_warning = """<div class="my-6 p-5 rounded-xl bg-red-500/10 border border-red-500/20">
                        <h4 class="text-sm font-bold text-white mb-2 flex items-center gap-1.5">
                            <span class="material-icons text-red-400 text-sm">warning</span>
                            ¡Importante sobre el Descuento AFC!
                        </h4>
                        <p class="text-xs text-slate-400 leading-relaxed mb-0">
                            Este descuento solo es legal si la causal aplicada es <strong>Art. 161 (Necesidades de la empresa)</strong>. No aplica en casos de renuncia voluntaria, mutuo acuerdo, vencimiento de plazo o despidos disciplinarios. Además, el descuento solo resta sobre el monto final de la <strong>indemnización por años de servicio</strong>, nunca sobre las vacaciones proporcionales ni sobre las remuneraciones pendientes.
                        </p>
                    </div>"""
        new_warning = """<div class="my-6 p-5 rounded-xl bg-red-50 border border-red-200 shadow-sm">
                        <h4 class="text-sm font-bold text-red-800 mb-2 flex items-center gap-1.5">
                            <span class="material-icons text-red-600 text-sm">warning</span>
                            ¡Importante sobre el Descuento AFC!
                        </h4>
                        <p class="text-xs text-slate-650 leading-relaxed mb-0">
                            Este descuento solo es legal si la causal aplicada es <strong>Art. 161 (Necesidades de la empresa)</strong>. No aplica en casos de renuncia voluntaria, mutuo acuerdo, vencimiento de plazo o despidos disciplinarios. Además, el descuento solo resta sobre el monto final de la <strong>indemnización por años de servicio</strong>, nunca sobre las vacaciones proporcionales ni sobre las remuneraciones pendientes.
                        </p>
                    </div>"""
        body = flexible_replace(body, old_warning, new_warning)

        # AFC table
        old_table = """<div class="overflow-x-auto my-6 border border-white/10 rounded-xl">
                        <table class="w-full text-sm text-left text-slate-400">
                            <thead class="bg-slate-900 text-white text-xs uppercase font-bold border-b border-white/10">
                                <tr>
                                    <th class="px-4 py-3">Giro Mensual</th>
                                    <th class="px-4 py-3 text-right">Porcentaje del Sueldo</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-white/5">
                                <tr>
                                    <td class="px-4 py-3 font-semibold text-white">1° Mes</td>
                                    <td class="px-4 py-3 text-right text-emerald-400 font-mono">70%</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-semibold text-white">2° Mes</td>
                                    <td class="px-4 py-3 text-right text-emerald-400 font-mono">55%</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-semibold text-white">3° Mes</td>
                                    <td class="px-4 py-3 text-right text-emerald-400 font-mono">45%</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-semibold text-white">4° Mes</td>
                                    <td class="px-4 py-3 text-right text-emerald-400 font-mono">40%</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-semibold text-white">5° Mes</td>
                                    <td class="px-4 py-3 text-right text-emerald-400 font-mono">35%</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>"""
        new_table = """<div class="overflow-x-auto my-6 border border-slate-200 rounded-xl shadow-sm">
                        <table class="w-full text-sm text-left text-slate-650 bg-white">
                            <thead class="bg-slate-50 text-slate-700 text-xs uppercase font-bold border-b border-slate-200">
                                <tr>
                                    <th class="px-4 py-3">Giro Mensual</th>
                                    <th class="px-4 py-3 text-right">Porcentaje del Sueldo</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                <tr>
                                    <td class="px-4 py-3 font-semibold text-slate-700">1° Mes</td>
                                    <td class="px-4 py-3 text-right text-emerald-600 font-mono font-bold">70%</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-semibold text-slate-700">2° Mes</td>
                                    <td class="px-4 py-3 text-right text-emerald-600 font-mono font-bold">55%</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-semibold text-slate-700">3° Mes</td>
                                    <td class="px-4 py-3 text-right text-emerald-600 font-mono font-bold">45%</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-semibold text-slate-700">4° Mes</td>
                                    <td class="px-4 py-3 text-right text-emerald-600 font-mono font-bold">40%</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-semibold text-slate-700">5° Mes</td>
                                    <td class="px-4 py-3 text-right text-emerald-600 font-mono font-bold">35%</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>"""
        body = flexible_replace(body, old_table, new_table)

        # Calculator promo card
        old_promo = """<div class="glass-panel p-6 rounded-2xl border border-primary/20 shadow-2xl relative overflow-hidden bg-slate-900/60 backdrop-blur-md">
                        <div class="absolute top-0 right-0 w-24 h-24 bg-primary/10 rounded-full blur-xl -mr-8 -mt-8 pointer-events-none"></div>
                        <h4 class="text-sm font-bold text-primary uppercase tracking-widest mb-2">Simulador de Finiquito</h4>
                        <h3 class="text-lg font-bold text-white mb-3">Revisa tu descuento de la AFC</h3>
                        <p class="text-xs text-slate-400 leading-relaxed mb-5">
                            ¿Te despidieron por necesidades de la empresa? Usa nuestra calculadora gratuita con el descuento legal AFC actualizado a la normativa 2026.
                        </p>
                        <a href="/finiquito_calculator"
                            class="block w-full text-center bg-primary hover:bg-primary-dark text-white font-bold py-3 px-4 rounded-full text-xs transition-all shadow-lg shadow-primary/20 hover:scale-[1.02]">
                            Ir a la Calculadora
                        </a>
                    </div>"""
        new_promo = """<div class="p-6 rounded-2xl border border-slate-200 shadow-sm relative overflow-hidden bg-white">
                        <h4 class="text-sm font-bold text-sky-600 uppercase tracking-widest mb-2">Simulador de Finiquito</h4>
                        <h3 class="text-lg font-bold text-slate-900 mb-3">Revisa tu descuento de la AFC</h3>
                        <p class="text-xs text-slate-655 leading-relaxed mb-5">
                            ¿Te despidieron por necesidades de la empresa? Usa nuestra calculadora gratuita con el descuento legal AFC actualizado a la normativa 2026.
                        </p>
                        <a href="finiquito_calculator"
                            class="block w-full text-center bg-sky-500 hover:bg-sky-600 text-white font-bold py-3 px-4 rounded-xl text-xs transition-all shadow-sm">
                            Ir a la Calculadora
                        </a>
                    </div>"""
        body = flexible_replace(body, old_promo, new_promo)

        # AFC info card
        old_info = """<div class="glass-panel p-6 rounded-2xl border border-white/5 bg-slate-950/30 space-y-4">
                        <h3 class="text-sm font-bold text-white uppercase tracking-wider border-b border-white/5 pb-2">Datos AFC Chile</h3>
                        <ul class="space-y-2.5 text-xs text-slate-400 leading-relaxed">
                            <li class="flex items-start gap-2">
                                <span class="material-icons text-emerald-400 text-sm mt-0.5">location_on</span>
                                <div><strong>Administradora:</strong> AFC Chile S.A.</div>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="material-icons text-emerald-400 text-sm mt-0.5">link</span>
                                <div><strong>Sitio oficial:</strong> <a href="https://www.afc.cl" class="text-primary hover:underline" target="_blank" rel="noopener noreferrer">www.afc.cl</a></div>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="material-icons text-emerald-400 text-sm mt-0.5">phone</span>
                                <div><strong>Call Center:</strong> 600 584 3000</div>
                            </li>
                        </ul>
                    </div>"""
        new_info = """<div class="p-6 rounded-2xl border border-slate-200 bg-slate-50 space-y-4 shadow-sm">
                        <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider border-b border-slate-200 pb-2">Datos AFC Chile</h3>
                        <ul class="space-y-2.5 text-xs text-slate-650 leading-relaxed">
                            <li class="flex items-start gap-2">
                                <span class="material-icons text-emerald-600 text-sm mt-0.5">location_on</span>
                                <div class="text-slate-700"><strong>Administradora:</strong> AFC Chile S.A.</div>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="material-icons text-emerald-600 text-sm mt-0.5">link</span>
                                <div class="text-slate-700"><strong>Sitio oficial:</strong> <a href="https://www.afc.cl" class="text-sky-600 hover:underline" target="_blank" rel="noopener noreferrer">www.afc.cl</a></div>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="material-icons text-emerald-600 text-sm mt-0.5">phone</span>
                                <div class="text-slate-700"><strong>Call Center:</strong> 600 584 3000</div>
                            </li>
                        </ul>
                    </div>"""
        body = flexible_replace(body, old_info, new_info)

    # 2. General Cleanups across all pages (relative paths, stray classes, etc.)
    body = body.replace('href="/sueldo_liquido"', 'href="sueldo_liquido"')
    body = body.replace('href="/finiquito_calculator"', 'href="finiquito_calculator"')
    body = body.replace('href="/como-leer-liquidacion-de-sueldo"', 'href="como-leer-liquidacion-de-sueldo"')
    body = body.replace('href="/ley-40-horas-chile-2026"', 'href="ley-40-horas-chile-2026"')
    body = body.replace('href="/que-hacer-si-no-te-pagan-el-finiquito"', 'href="que-hacer-si-no-te-pagan-el-finiquito"')
    body = body.replace('href="/como-calcular-sueldo-liquido-paso-a-paso"', 'href="como-calcular-sueldo-liquido-paso-a-paso"')
    body = body.replace('href="/como-calcular-finiquito-chile"', 'href="como-calcular-finiquito-chile"')
    body = body.replace('href="/despido-necesidades-empresa-articulo-161"', 'href="despido-necesidades-empresa-articulo-161"')
    body = body.replace('href="/guia-vacaciones-proporcionales"', 'href="guia-vacaciones-proporcionales"')
    body = body.replace('href="/seguro-de-cesantia-chile-como-cobrar"', 'href="seguro-de-cesantia-chile-como-cobrar"')

    # Let's clean some residual text color issues
    body = body.replace('text-rose-300', 'text-rose-700')
    body = body.replace('text-rose-450', 'text-rose-700')
    body = body.replace('text-yellow-100/80', 'text-amber-800')
    body = body.replace('text-emerald-300', 'text-emerald-700')
    body = body.replace('text-green-400', 'text-emerald-600')
    body = body.replace('text-blue-300', 'text-sky-700')
    body = body.replace('text-blue-400', 'text-sky-600')
    
    # Avoid duplicated classes on alert boxes from naive replaces
    body = body.replace('bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all border border-slate-100', 'bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm my-6')
    body = body.replace('bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all border border-slate-200', 'bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm my-6')
    body = body.replace('bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all border border-white/5', 'bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm my-6')
    body = body.replace('bg-slate-50 border border-slate-200/80 rounded-2xl p-5 shadow-sm my-6 transition-all border-white/5', 'bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm my-6')
    
    # Return cleaned body
    return body


# List of articles to build
articles = [
    "como-calcular-finiquito-chile.html",
    "como-calcular-sueldo-liquido-paso-a-paso.html",
    "como-leer-liquidacion-de-sueldo.html",
    "despido-necesidades-empresa-articulo-161.html",
    "ley-40-horas-chile-2026.html",
    "guia-vacaciones-proporcionales.html",
    "seguro-de-cesantia-chile-como-cobrar.html",
    "que-hacer-si-no-te-pagan-el-finiquito.html",
    "reclamar-despido-injustificado-chile.html"
]

print("Starting page migration to light theme...")

for filename in articles:
    source_path = os.path.join(SOURCE_DIR, filename)
    dest_path = os.path.join(DEST_DIR, filename)
    
    if not os.path.exists(source_path):
        print(f"ERROR: Source file {filename} not found.")
        continue
        
    print(f"Processing: {filename}...")
    title, description, body, custom_head = extract_article_info(source_path)
    
    breadcrumbs = f"""
    <nav class="flex items-center gap-2 text-xs text-slate-400 mb-6 max-w-3xl mx-auto">
        <a href="./" class="hover:text-sky-500 transition-colors font-medium">Inicio</a>
        <span class="material-icons text-xs">chevron_right</span>
        <a href="blog" class="hover:text-sky-500 transition-colors font-medium">Blog</a>
        <span class="material-icons text-xs">chevron_right</span>
        <span class="text-slate-600 font-semibold">{title.split("|")[0].strip()}</span>
    </nav>
    """
    
    article_content = f"""
    <div class="max-w-4xl mx-auto px-6 pt-6">
        {breadcrumbs}
        
        <article class="bg-white border border-slate-200 rounded-3xl shadow-sm p-8 sm:p-12 mb-8 relative overflow-hidden">
            <div class="prose-content max-w-none">
                {body}
            </div>
        </article>
    </div>
    """
    
    canonical_url, og_tags, json_ld = generate_seo_tags(filename, title, description, page_type="article")
    
    html_out = HTML_LAYOUT.format(
        title=title,
        description=description,
        canonical_url=canonical_url,
        og_tags=og_tags,
        json_ld=json_ld,
        custom_head="",
        header=HEADER_HTML,
        indicator_bar=INDICATOR_BAR_HTML,
        content=article_content,
        footer=FOOTER_HTML,
        history_modal=HISTORY_MODAL_HTML,
        custom_scripts=""
    )
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_out)

print("Migration of guide articles complete.")

# 2. Simple pages (sobre-nosotros, terminos, privacidad, disclaimer)
simple_pages = {
    "sobre-nosotros.html": ("Sobre Nosotros | Cálculo Laboral Chile", "Conoce quiénes somos, nuestra misión y por qué construimos el mejor simulador de finiquitos y sueldo líquido de Chile."),
    "terminos.html": ("Términos de Servicio | Cálculo Laboral Chile", "Términos y condiciones de uso de la plataforma Cálculo Laboral."),
    "privacidad.html": ("Política de Privacidad | Cálculo Laboral Chile", "Política de privacidad y protección de datos personales de Cálculo Laboral."),
    "disclaimer.html": ("Disclaimer Legal | Cálculo Laboral Chile", "Aviso de responsabilidad legal y limitaciones del simulador Cálculo Laboral.")
}

for filename, (title, desc) in simple_pages.items():
    source_path = os.path.join(SOURCE_DIR, filename)
    dest_path = os.path.join(DEST_DIR, filename)
    
    if os.path.exists(source_path):
        print(f"Processing simple page: {filename}...")
        with open(source_path, "r", encoding="utf-8") as f:
            html = f.read()
        
        body_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
        if not body_match:
            body_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
            
        if body_match:
            body = body_match.group(1)
            body = re.sub(r'<nav[^>]*id="breadcrumb"[^>]*>.*?</nav>', '', body, re.DOTALL | re.IGNORECASE)
            body = re.sub(r'<h1[^>]*>.*?</h1>', '', body, re.DOTALL | re.IGNORECASE)
            body = body.replace('prose-dark', 'prose prose-slate max-w-none text-slate-700 leading-relaxed prose-headings:text-slate-900 font-sans prose-headings:font-bold prose-a:text-sky-500')
            body = clean_article_body(body, filename)
        else:
            body = "<p>Contenido no disponible.</p>"
            
        page_content = f"""
        <div class="max-w-3xl mx-auto px-6 pt-6">
            <h1 class="text-3xl font-extrabold text-slate-900 mb-6 text-center">{title.split("|")[0].strip()}</h1>
            <div class="bg-white border border-slate-200 rounded-3xl shadow-sm p-8 sm:p-12 mb-8 relative overflow-hidden">
                <div class="prose-content max-w-none">
                    {body}
                </div>
            </div>
        </div>
        """
        
        canonical_url, og_tags, json_ld = generate_seo_tags(filename, title, desc, page_type="website")
        
        html_out = HTML_LAYOUT.format(
            title=title,
            description=desc,
            canonical_url=canonical_url,
            og_tags=og_tags,
            json_ld=json_ld,
            custom_head="",
            header=HEADER_HTML,
            indicator_bar=INDICATOR_BAR_HTML,
            content=page_content,
            footer=FOOTER_HTML,
            history_modal=HISTORY_MODAL_HTML,
            custom_scripts=""
        )
        
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(html_out)

print("Simple pages migration complete.")

# 3. Blog List page
blog_title = "Blog Laboral Chile 2026 | Guías y Consejos | Cálculo Laboral"
blog_desc = "Guías detalladas y consejos expertos sobre legislación laboral, contratos, remuneraciones y finiquitos en Chile."

blog_content = """
<div class="max-w-[1200px] mx-auto px-6 pt-6">
    <div class="text-center mb-12">
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight mb-3">Blog Laboral Informativo</h1>
        <p class="text-slate-500 text-base max-w-2xl mx-auto">
            Guías didácticas y actualizadas conforme al Código del Trabajo de Chile para comprender tus liquidaciones, finiquitos y derechos.
        </p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- 1. Sueldo Líquido -->
        <a href="como-calcular-sueldo-liquido-paso-a-paso" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-all">
            <div class="aspect-video bg-slate-100 overflow-hidden relative border-b border-slate-100">
                <img src="assets/guia-sueldo-liquido-cover.png" alt="Guía Sueldo Líquido" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <span class="absolute top-4 left-4 bg-sky-500 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md">Paso a paso</span>
            </div>
            <div class="p-6">
                <h3 class="text-lg font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2">Cómo calcular sueldo líquido paso a paso</h3>
                <p class="text-slate-500 text-xs leading-relaxed mb-4">Aprende a convertir tu sueldo bruto a líquido identificando descuentos e impuestos aplicables.</p>
                <div class="flex justify-between items-center text-[10px] text-slate-400 font-medium">
                    <span>Marzo 2026</span>
                    <span>5 min lectura</span>
                </div>
            </div>
        </a>

        <!-- 2. Vacaciones Proporcionales -->
        <a href="guia-vacaciones-proporcionales" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-all">
            <div class="aspect-video bg-slate-100 overflow-hidden relative border-b border-slate-100">
                <img src="assets/guia-vacaciones-proporcionales-cover.png" alt="Vacaciones Proporcionales" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <span class="absolute top-4 left-4 bg-indigo-500 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md">Cálculo Legal</span>
            </div>
            <div class="p-6">
                <h3 class="text-lg font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2">Cómo calcular vacaciones proporcionales en Chile</h3>
                <p class="text-slate-500 text-xs leading-relaxed mb-4">Fórmulas y ejemplos reales para calcular los días acumulados que te corresponden por ley.</p>
                <div class="flex justify-between items-center text-[10px] text-slate-400 font-medium">
                    <span>Febrero 2026</span>
                    <span>4 min lectura</span>
                </div>
            </div>
        </a>

        <!-- 3. Finiquito paso a paso -->
        <a href="como-calcular-finiquito-chile" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-all">
            <div class="aspect-video bg-slate-100 overflow-hidden relative border-b border-slate-100">
                <img src="assets/guia-calculo-finiquito-chile-2026.png" alt="Cómo Calcular Finiquito" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <span class="absolute top-4 left-4 bg-emerald-500 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md">Completo</span>
            </div>
            <div class="p-6">
                <h3 class="text-lg font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2">Cómo calcular tu finiquito en Chile (Guía 2026)</h3>
                <p class="text-slate-500 text-xs leading-relaxed mb-4">Indemnizaciones por años de servicio, aviso previo, feriado proporcional y desgloses paso a paso.</p>
                <div class="flex justify-between items-center text-[10px] text-slate-400 font-medium">
                    <span>Febrero 2026</span>
                    <span>6 min lectura</span>
                </div>
            </div>
        </a>

        <!-- 4. Cómo leer liquidación -->
        <a href="como-leer-liquidacion-de-sueldo" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-all">
            <div class="aspect-video bg-slate-100 overflow-hidden relative border-b border-slate-100">
                <img src="assets/guia-liquidacion-sueldo-cover.png" alt="Anatomía Liquidación de Sueldo" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <span class="absolute top-4 left-4 bg-slate-500 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md">Anatomía</span>
            </div>
            <div class="p-6">
                <h3 class="text-lg font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2">Cómo leer tu liquidación de sueldo</h3>
                <p class="text-slate-500 text-xs leading-relaxed mb-4">Haberes imponibles, no imponibles, descuentos previsionales, de salud y tributarios de forma simple.</p>
                <div class="flex justify-between items-center text-[10px] text-slate-400 font-medium">
                    <span>Enero 2026</span>
                    <span>5 min lectura</span>
                </div>
            </div>
        </a>

        <!-- 5. Art 161 Despido -->
        <a href="despido-necesidades-empresa-articulo-161" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-all">
            <div class="aspect-video bg-slate-100 overflow-hidden relative border-b border-slate-100">
                <img src="assets/guia-despido-necesidades-empresa-161.png" alt="Despido Necesidades Empresa" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <span class="absolute top-4 left-4 bg-red-500 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md">Legal</span>
            </div>
            <div class="p-6">
                <h3 class="text-lg font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2">Despido por Necesidades de la Empresa (Art 161)</h3>
                <p class="text-slate-500 text-xs leading-relaxed mb-4">Conoce las formalidades, tus derechos, la carta de aviso y la reserva de derechos para reclamar.</p>
                <div class="flex justify-between items-center text-[10px] text-slate-400 font-medium">
                    <span>Enero 2026</span>
                    <span>8 min lectura</span>
                </div>
            </div>
        </a>

        <!-- 6. Ley 40 Horas -->
        <a href="ley-40-horas-chile-2026" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-all">
            <div class="aspect-video bg-slate-100 overflow-hidden relative border-b border-slate-100">
                <img src="assets/guia-ley-40-horas-chile-cover.png" alt="Ley 40 Horas" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <span class="absolute top-4 left-4 bg-amber-500 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md">Novedad</span>
            </div>
            <div class="p-6">
                <h3 class="text-lg font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2">Ley 40 Horas en Chile: Implementación 2026</h3>
                <p class="text-slate-500 text-xs leading-relaxed mb-4">Infografía y cronograma sobre la reducción de jornada laboral y el impacto en tus cálculos diarios.</p>
                <div class="flex justify-between items-center text-[10px] text-slate-400 font-medium">
                    <span>Enero 2026</span>
                    <span>6 min lectura</span>
                </div>
            </div>
        </a>

        <!-- 7. Seguro de Cesantía -->
        <a href="seguro-de-cesantia-chile-como-cobrar" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-all">
            <div class="aspect-video bg-slate-100 overflow-hidden relative border-b border-slate-100">
                <img src="assets/guia-seguro-cesantia-chile.png" alt="Seguro de Cesantía" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <span class="absolute top-4 left-4 bg-teal-500 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md">Seguridad</span>
            </div>
            <div class="p-6">
                <h3 class="text-lg font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2">Seguro de Cesantía: Requisitos y cómo cobrarlo</h3>
                <p class="text-slate-500 text-xs leading-relaxed mb-4">Aprende a tramitar tu seguro ante la AFC, simular giros mensuales y el impacto de los descuentos.</p>
                <div class="flex justify-between items-center text-[10px] text-slate-400 font-medium">
                    <span>Diciembre 2025</span>
                    <span>5 min lectura</span>
                </div>
            </div>
        </a>

        <!-- 8. No te pagan finiquito -->
        <a href="que-hacer-si-no-te-pagan-el-finiquito" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-all">
            <div class="aspect-video bg-slate-100 overflow-hidden relative border-b border-slate-100">
                <img src="assets/guia-finiquito-no-pago-cover.png" alt="No te Pagan Finiquito" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <span class="absolute top-4 left-4 bg-red-600 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md">Alerta</span>
            </div>
            <div class="p-6">
                <h3 class="text-lg font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2">¿Qué hacer si no te pagan el finiquito a tiempo?</h3>
                <p class="text-slate-500 text-xs leading-relaxed mb-4">Conoce los plazos obligatorios de pago (10 días), multas de la DT y cómo interponer un reclamo.</p>
                <div class="flex justify-between items-center text-[10px] text-slate-400 font-medium">
                    <span>Noviembre 2025</span>
                    <span>7 min lectura</span>
                </div>
            </div>
        </a>
    </div>
</div>
"""

canonical_url, og_tags, json_ld = generate_seo_tags("blog.html", blog_title, blog_desc, page_type="website")

html_out = HTML_LAYOUT.format(
    title=blog_title,
    description=blog_desc,
    canonical_url=canonical_url,
    og_tags=og_tags,
    json_ld=json_ld,
    custom_head="",
    header=HEADER_HTML,
    indicator_bar=INDICATOR_BAR_HTML,
    content=blog_content,
    footer=FOOTER_HTML,
    history_modal=HISTORY_MODAL_HTML,
    custom_scripts=""
)

with open(os.path.join(DEST_DIR, "blog.html"), "w", encoding="utf-8") as f:
    f.write(html_out)

print("Blog List page complete.")

# 4. Contact page
contact_content = """
<div class="max-w-[800px] mx-auto px-6">
    <div class="text-center mb-12 animate-fade-in">
        <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight mb-3">Contacto</h1>
        <p class="text-slate-500 text-sm max-w-lg mx-auto">
            Si tienes dudas sobre tus cálculos o la legislación laboral en Chile, escríbenos directamente. Respondemos a todas las consultas de forma gratuita.
        </p>
    </div>

    <!-- Contact Box -->
    <div class="bg-white border border-slate-200 rounded-3xl p-8 sm:p-10 shadow-sm mb-12 relative overflow-hidden">
        <div class="flex flex-col items-center justify-center mb-8 pb-8 border-b border-slate-100">
            <div class="w-12 h-12 rounded-xl bg-sky-50 flex items-center justify-center mb-3">
                <span class="material-icons text-sky-500">mail</span>
            </div>
            <a href="mailto:contacto@calculolaboral.cl" class="text-xl sm:text-2xl font-bold text-slate-900 hover:text-sky-500 transition-colors">
                contacto@calculolaboral.cl
            </a>
            <p class="text-[11px] text-slate-400 font-semibold mt-1">Plazo de respuesta: 24 a 48 horas hábiles</p>
        </div>

        <!-- Success Message (Hidden by default) -->
        <div id="success-message" class="hidden flex flex-col items-center justify-center text-center py-8">
            <div class="w-16 h-16 rounded-full bg-emerald-50 text-emerald-500 flex items-center justify-center mb-4">
                <span class="material-icons text-3xl">check_circle</span>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-1.5">¡Mensaje Enviado!</h3>
            <p class="text-xs text-slate-500 max-w-sm">
                Hemos recibido tu consulta y te responderemos a la brevedad. Gracias por comunicarte con nosotros.
            </p>
            <button id="send-another-btn" class="mt-6 px-4 py-2.5 bg-slate-50 border border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-600 rounded-xl hover:bg-slate-100 transition-colors">
                Enviar otro mensaje
            </button>
        </div>

        <!-- Form -->
        <form id="contact-form" action="https://formsubmit.co/ajax/contacto@calculolaboral.cl" method="POST" class="space-y-4">
            <input type="hidden" name="_subject" value="Nuevo mensaje desde CalculoLaboral.cl">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="true">

            <div class="space-y-1">
                <label for="name" class="block text-xs font-bold text-slate-600 uppercase ml-1">Nombre Completo</label>
                <input type="text" id="name" name="name" required placeholder="Ej. Juan Pérez" class="block w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-medium">
            </div>

            <div class="space-y-1">
                <label for="email" class="block text-xs font-bold text-slate-600 uppercase ml-1">Correo Electrónico</label>
                <input type="email" id="email" name="email" required placeholder="tu@correo.com" class="block w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-medium">
            </div>

            <div class="space-y-1">
                <label for="message" class="block text-xs font-bold text-slate-600 uppercase ml-1">Mensaje o Consulta</label>
                <textarea id="message" name="message" rows="5" required placeholder="Escribe aquí tu consulta en detalle (menciona tu tipo de contrato, sueldo base u otros datos relevantes si deseas una ayuda más precisa)." class="block w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-medium resize-none"></textarea>
            </div>

            <div class="pt-2">
                <button type="submit" id="submit-btn" class="w-full py-4 bg-sky-500 hover:bg-sky-600 text-white font-bold rounded-xl shadow-md shadow-sky-500/10 transition-all hover:scale-[1.01] active:scale-[0.99] duration-100 flex items-center justify-center gap-2">
                    <span class="btn-text">Enviar Mensaje</span>
                    <span class="material-icons text-sm btn-icon">send</span>
                    <svg class="animate-spin h-5 w-5 text-white hidden loading-spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                </button>
            </div>
        </form>
    </div>

    <!-- FAQ Accordions (Contacto) -->
    <div class="max-w-2xl mx-auto mt-16">
        <h2 class="text-xl font-bold text-slate-900 text-center mb-6">Preguntas Frecuentes de Soporte</h2>
        <div class="space-y-4">
            <details class="bg-white border border-slate-200 rounded-2xl group transition-all duration-200 overflow-hidden">
                <summary class="cursor-pointer p-4 font-bold text-xs text-slate-700 flex justify-between items-center uppercase tracking-wider outline-none list-none [&::-webkit-details-marker]:hidden">
                    ¿Son fidedignos los cálculos de este sitio?
                    <span class="material-icons transition-transform group-open:rotate-180 text-sky-500">expand_more</span>
                </summary>
                <div class="px-4 pb-4 pt-1 text-xs text-slate-500 leading-relaxed border-t border-slate-100">
                    Sí, todas nuestras calculadoras están calibradas conforme al Código del Trabajo de Chile y las normativas vigentes del Servicio de Impuestos Internos (SII), Dirección del Trabajo (DT) y AFC para el año 2026. Sin embargo, recuerda que este sitio es una herramienta referencial y no constituye asesoría legal formal.
                </div>
            </details>

            <details class="bg-white border border-slate-200 rounded-2xl group transition-all duration-200 overflow-hidden">
                <summary class="cursor-pointer p-4 font-bold text-xs text-slate-700 flex justify-between items-center uppercase tracking-wider outline-none list-none [&::-webkit-details-marker]:hidden">
                    ¿Tiene algún costo usar los simuladores?
                    <span class="material-icons transition-transform group-open:rotate-180 text-sky-500">expand_more</span>
                </summary>
                <div class="px-4 pb-4 pt-1 text-xs text-slate-500 leading-relaxed border-t border-slate-100">
                    No, todos nuestros servicios, calculadoras, guías paso a paso y artículos informativos son 100% gratuitos y de libre acceso para todos los trabajadores y empleadores de Chile.
                </div>
            </details>

            <details class="bg-white border border-slate-200 rounded-2xl group transition-all duration-200 overflow-hidden">
                <summary class="cursor-pointer p-4 font-bold text-xs text-slate-700 flex justify-between items-center uppercase tracking-wider outline-none list-none [&::-webkit-details-marker]:hidden">
                    ¿Cómo puedo reportar un error en los cálculos?
                    <span class="material-icons transition-transform group-open:rotate-180 text-sky-500">expand_more</span>
                </summary>
                <div class="px-4 pb-4 pt-1 text-xs text-slate-500 leading-relaxed border-t border-slate-100">
                    Si detectas alguna diferencia o anomalía en las fórmulas de liquidación o finiquito, puedes escribirnos describiendo tu caso (con valores de sueldo base, causal y fechas) a nuestro correo oficial <a href="mailto:contacto@calculolaboral.cl" class="text-sky-500 font-bold hover:underline">contacto@calculolaboral.cl</a>. Nuestro equipo técnico lo revisará a la brevedad.
                </div>
            </details>
        </div>
    </div>
</div>
"""

contacto_custom_script = """
    <script>
        const form = document.getElementById('contact-form');
        const successMessage = document.getElementById('success-message');
        const submitBtn = document.getElementById('submit-btn');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnIcon = submitBtn.querySelector('.btn-icon');
        const loadingSpinner = submitBtn.querySelector('.loading-spinner');
        const sendAnotherBtn = document.getElementById('send-another-btn');

        if (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                submitBtn.disabled = true;
                btnText.textContent = 'Enviando...';
                btnIcon.classList.add('hidden');
                loadingSpinner.classList.remove('hidden');

                const formData = new FormData(form);

                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: { 'Accept': 'application/json' }
                })
                .then(response => {
                    if (response.ok) {
                        form.classList.add('hidden');
                        successMessage.classList.remove('hidden');
                        form.reset();
                    } else {
                        alert("Hubo un error al enviar el mensaje. Intente escogiéndonos directamente a contacto@calculolaboral.cl");
                    }
                })
                .catch(error => {
                    alert("Error de conexión. Intente nuevamente.");
                })
                .finally(() => {
                    submitBtn.disabled = false;
                    btnText.textContent = 'Enviar Mensaje';
                    btnIcon.classList.remove('hidden');
                    loadingSpinner.classList.add('hidden');
                });
            });
        }

        if (sendAnotherBtn) {
            sendAnotherBtn.addEventListener('click', () => {
                successMessage.classList.add('hidden');
                form.classList.remove('hidden');
            });
        }
    </script>
"""

canonical_url, og_tags, json_ld = generate_seo_tags("contacto.html", "Contacto | Cálculo Laboral Chile", "Contáctanos ante cualquier duda sobre tus remuneraciones, finiquitos o indemnizaciones laborales en Chile. Respuestas rápidas.", page_type="website")

html_out = HTML_LAYOUT.format(
    title="Contacto | Cálculo Laboral Chile",
    description="Contáctanos ante cualquier duda sobre tus remuneraciones, finiquitos o indemnizaciones laborales en Chile. Respuestas rápidas.",
    canonical_url=canonical_url,
    og_tags=og_tags,
    json_ld=json_ld,
    custom_head="",
    header=HEADER_HTML,
    indicator_bar=INDICATOR_BAR_HTML,
    content=contact_content,
    footer=FOOTER_HTML,
    history_modal=HISTORY_MODAL_HTML,
    custom_scripts=contacto_custom_script
)

with open(os.path.join(DEST_DIR, "contacto.html"), "w", encoding="utf-8") as f:
    f.write(html_out)

print("Contact page complete.")

# 5. Integrated Calculator Page (index.html) Markup
# This page contains both calculators in layout
INDEX_CONTENT = """
<div class="max-w-[1200px] mx-auto px-6">
    <!-- H1 Header Section for SEO -->
    <div class="text-center sm:text-left my-8 max-w-xl mx-auto no-print">
        <h1 class="text-2xl font-bold text-slate-900">
            Calculadoras Laborales Chile 2026
        </h1>
        <p class="text-slate-500 text-sm mt-1">
            Sueldo líquido y finiquito con todas las deducciones legales vigentes.
        </p>
    </div>

    <!-- Tab Controls for Calculator Selection -->
    <div class="flex max-w-xl mx-auto bg-white border border-slate-200 rounded-2xl p-1 mb-8 shadow-sm no-print">
        <button id="tab-btn-finiquito" onclick="switchCalculatorTab('finiquito')" class="flex-1 py-3.5 px-6 rounded-xl text-xs font-bold uppercase tracking-wider transition-all text-white bg-sky-500 shadow-md shadow-sky-500/20 active:scale-[0.98] duration-100">
            Calculadora de Finiquito
        </button>
        <button id="tab-btn-sueldo" onclick="switchCalculatorTab('sueldo')" class="flex-1 py-3.5 px-6 rounded-xl text-xs font-bold uppercase tracking-wider transition-all text-slate-500 hover:text-slate-800 hover:bg-slate-100 active:scale-[0.98] duration-100">
            Sueldo Líquido
        </button>
    </div>

    <!-- ---------------------------------------------------- -->
    <!-- FINIQUITO CALCULATOR CONTAINER                       -->
    <!-- ---------------------------------------------------- -->
    <div id="finiquito-calc-container" class="flex flex-col lg:flex-row gap-8 items-start">
        <!-- Inputs Column (Left, 420px) -->
        <div class="w-full lg:w-[420px] shrink-0 bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm no-print">
            <div class="flex justify-between items-center mb-5 pb-3 border-b border-slate-100">
                <h2 class="text-lg font-bold text-slate-900">Datos Finiquito</h2>
                <div class="flex gap-2">
                    <button id="btnLoadExample" class="px-2.5 py-1 text-[10px] font-bold text-sky-600 bg-sky-50 hover:bg-sky-100 rounded-md transition-colors active:scale-95 duration-100">Ejemplo</button>
                    <button id="btnClear" class="px-2.5 py-1 text-[10px] font-bold text-slate-500 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-md transition-colors active:scale-95 duration-100">Limpiar</button>
                </div>
            </div>

            <!-- Tab bar inner to finiquito script (contrato/ingresos/opciones) -->
            <div class="flex border border-slate-200 p-1 bg-slate-50 rounded-xl mb-6">
                <button type="button" id="tabBtn-contrato" class="flex-1 py-2 px-1 rounded-lg text-[10px] font-bold uppercase tracking-wider transition-all text-white bg-sky-500 shadow-sm active:scale-95 duration-100">Contrato</button>
                <button type="button" id="tabBtn-ingresos" class="flex-1 py-2 px-1 rounded-lg text-[10px] font-bold uppercase tracking-wider transition-all text-slate-500 hover:text-slate-800 hover:bg-slate-200/50 active:scale-95 duration-100">Ingresos</button>
                <button type="button" id="tabBtn-avanzado" class="flex-1 py-2 px-1 rounded-lg text-[10px] font-bold uppercase tracking-wider transition-all text-slate-500 hover:text-slate-800 hover:bg-slate-200/50 active:scale-95 duration-100">Opciones</button>
            </div>

            <!-- Finiquito Tab: Contrato -->
            <div id="tabContent-contrato" class="space-y-4">
                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Fecha de Inicio</label>
                    <input id="startDate" class="block w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-medium" type="date">
                </div>
                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Fecha de Término</label>
                    <input id="endDate" class="block w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-medium" type="date">
                </div>
                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Causal de Término</label>
                    <select id="cause" class="block w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-medium cursor-pointer">
                        <option value="161">Art. 161 - Necesidades de la Empresa</option>
                        <option value="159-1">Art. 159 N°1 - Mutuo Acuerdo</option>
                        <option value="159-2">Art. 159 N°2 - Renuncia Voluntaria</option>
                        <option value="160">Art. 160 - Despido Disciplinario (Sin derecho a indemnización)</option>
                    </select>
                </div>
                <div class="pt-2 flex items-center justify-between">
                    <label class="flex items-center gap-3 cursor-pointer group">
                        <input id="noticeGiven" class="w-4 h-4 rounded border-slate-300 text-sky-500 focus:ring-sky-500/35 cursor-pointer" type="checkbox">
                        <span class="text-xs font-semibold text-slate-500 group-hover:text-slate-800 transition-colors">¿Se avisó con 30 días de anticipación?</span>
                    </label>
                </div>
            </div>

            <!-- Finiquito Tab: Ingresos -->
            <div id="tabContent-ingresos" class="space-y-4 hidden">
                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Sueldo Base Mensual</label>
                    <div class="relative">
                        <span class="absolute left-4 top-3 text-slate-500 font-bold">$</span>
                        <input id="baseSalary" data-type="currency" class="block w-full pl-8 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-mono text-right" placeholder="0">
                    </div>
                </div>
                
                <div class="pt-1">
                    <label class="flex items-center gap-2 cursor-pointer">
                        <input type="checkbox" id="hasVariableSalary" class="w-4 h-4 text-sky-500 bg-white border-slate-200 rounded focus:ring-sky-500">
                        <span class="text-xs font-bold text-slate-600">¿Sueldo Variable / Comisiones?</span>
                    </label>
                </div>

                <!-- Variable Salary Grid (Inputs for 3 months) -->
                <div id="variableSalaryContainer" class="hidden space-y-2.5 p-4 bg-slate-50 border border-slate-200 rounded-xl">
                    <p class="text-[10px] text-slate-500 font-semibold leading-relaxed">Últimos 3 meses imponibles variables:</p>
                    <div class="grid grid-cols-3 gap-2">
                        <div>
                            <label class="text-[9px] font-bold text-slate-500 ml-1">Mes 1</label>
                            <input id="varMonth1" data-type="currency" class="block w-full p-2 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" placeholder="0">
                        </div>
                        <div>
                            <label class="text-[9px] font-bold text-slate-500 ml-1">Mes 2</label>
                            <input id="varMonth2" data-type="currency" class="block w-full p-2 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" placeholder="0">
                        </div>
                        <div>
                            <label class="text-[9px] font-bold text-slate-500 ml-1">Mes 3</label>
                            <input id="varMonth3" data-type="currency" class="block w-full p-2 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" placeholder="0">
                        </div>
                    </div>
                    <div class="flex justify-between items-center pt-2 border-t border-slate-200">
                        <span class="text-[10px] font-bold text-slate-400 uppercase">Promedio</span>
                        <span id="variableAverageOutput" class="text-xs font-bold text-sky-500 font-mono">$0</span>
                    </div>
                </div>

                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Gratificación Mensual</label>
                    <div class="relative">
                        <span class="absolute left-4 top-3 text-slate-500 font-bold">$</span>
                        <input id="gratification" data-type="currency" class="block w-full pl-8 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-mono text-right" placeholder="0">
                    </div>
                </div>

                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Asignaciones Fijas (Colación/Mov)</label>
                    <div class="relative">
                        <span class="absolute left-4 top-3 text-slate-500 font-bold">$</span>
                        <input id="assignments" data-type="currency" class="block w-full pl-8 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-mono text-right" placeholder="0">
                    </div>
                    <div class="pt-1">
                        <label class="flex items-center gap-2 cursor-pointer select-none">
                            <input type="checkbox" id="includeAssignmentsInVacation" class="w-4.5 h-4.5 text-sky-500 border-slate-200 rounded focus:ring-sky-500" checked>
                            <span class="text-[10px] font-semibold text-slate-400">Incluir en Vacaciones (Criterio Judicial)</span>
                        </label>
                    </div>
                </div>

                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Vacaciones Pendientes (Días Hábiles)</label>
                    <div class="flex items-center bg-slate-50 border border-slate-200 rounded-xl p-1 w-full justify-between">
                        <button id="btnVacationMinus" aria-label="Restar día de vacaciones" class="w-8 h-8 rounded-lg bg-white border border-slate-200 text-slate-600 flex items-center justify-center transition-all hover:bg-slate-100 active:scale-90 duration-100" type="button">
                            <span class="material-icons text-sm font-bold">remove</span>
                        </button>
                        <input id="vacationPending" class="w-16 bg-transparent border-none text-center text-slate-800 focus:ring-0 font-bold text-sm" type="text" value="0">
                        <button id="btnVacationPlus" aria-label="Sumar día de vacaciones" class="w-8 h-8 rounded-lg bg-white border border-slate-200 text-slate-600 flex items-center justify-center transition-all hover:bg-slate-100 active:scale-90 duration-100" type="button">
                            <span class="material-icons text-sm font-bold">add</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Finiquito Tab: Opciones -->
            <div id="tabContent-avanzado" class="space-y-3 hidden">
                <p class="text-[10px] text-slate-500 font-bold uppercase mb-2 border-b border-slate-100 pb-1">Conceptos a Incluir</p>
                <div class="space-y-2.5">
                    <!-- Opción 1: Años de Servicio -->
                    <div class="p-3 bg-slate-50 hover:bg-slate-100/70 border border-slate-200/60 rounded-xl transition-all duration-200 flex items-start gap-3">
                        <div class="pt-0.5">
                            <input id="enableIAS" class="w-4 h-4 rounded border-slate-300 text-sky-500 focus:ring-sky-500/35 cursor-pointer transition-transform duration-100 active:scale-90" type="checkbox" checked />
                        </div>
                        <div class="flex-grow select-none">
                            <label for="enableIAS" class="block text-xs font-bold text-slate-800 cursor-pointer hover:text-sky-500 transition-colors">Años de Servicio (IAS)</label>
                            <span class="block text-[10px] text-slate-500 font-medium mt-0.5 leading-relaxed">Suma 1 sueldo mensual por cada año trabajado (tope 11). Requiere contrato mayor a 1 año.</span>
                        </div>
                    </div>

                    <!-- Opción 2: Aviso Previo -->
                    <div class="p-3 bg-slate-50 hover:bg-slate-100/70 border border-slate-200/60 rounded-xl transition-all duration-200 flex items-start gap-3">
                        <div class="pt-0.5">
                            <input id="enableNotice" class="w-4 h-4 rounded border-slate-300 text-sky-500 focus:ring-sky-500/35 cursor-pointer transition-transform duration-100 active:scale-90" type="checkbox" checked />
                        </div>
                        <div class="flex-grow select-none">
                            <label for="enableNotice" class="block text-xs font-bold text-slate-800 cursor-pointer hover:text-sky-500 transition-colors">Indemnización Aviso Previo</label>
                            <span class="block text-[10px] text-slate-500 font-medium mt-0.5 leading-relaxed">Suma 1 sueldo adicional si el empleador no te avisó del despido por escrito con 30 días de anticipación.</span>
                        </div>
                    </div>

                    <!-- Opción 3: Descuento AFC -->
                    <div class="p-3 bg-slate-50 hover:bg-slate-100/70 border border-slate-200/60 rounded-xl transition-all duration-200 flex items-start gap-3">
                        <div class="pt-0.5">
                            <input id="simulateAFC" class="w-4 h-4 rounded border-slate-300 text-sky-500 focus:ring-sky-500/35 cursor-pointer transition-transform duration-100 active:scale-90" type="checkbox" checked />
                        </div>
                        <div class="flex-grow select-none">
                            <label for="simulateAFC" class="block text-xs font-bold text-slate-800 cursor-pointer hover:text-sky-500 transition-colors">Descontar Aporte AFC Empleador</label>
                            <span class="block text-[10px] text-slate-500 font-medium mt-0.5 leading-relaxed">Resta de tu finiquito la parte del seguro de cesantía aportada por el empleador (solo despidos Art. 161).</span>
                        </div>
                    </div>

                    <!-- Opción 4: Remuneración Pendiente -->
                    <div class="p-3 bg-slate-50 hover:bg-slate-100/70 border border-slate-200/60 rounded-xl transition-all duration-200 flex items-start gap-3">
                        <div class="pt-0.5">
                            <input id="enablePending" class="w-4 h-4 rounded border-slate-300 text-sky-500 focus:ring-sky-500/35 cursor-pointer transition-transform duration-100 active:scale-90" type="checkbox" checked />
                        </div>
                        <div class="flex-grow select-none">
                            <label for="enablePending" class="block text-xs font-bold text-slate-800 cursor-pointer hover:text-sky-500 transition-colors">Días Trabajados (Mes en Curso)</label>
                            <span class="block text-[10px] text-slate-500 font-medium mt-0.5 leading-relaxed">Calcula e inyecta la remuneración de los días trabajados en el mes en que finaliza la relación laboral.</span>
                        </div>
                    </div>

                    <!-- Opción 5: Incluir Asignaciones -->
                    <div class="p-3 bg-slate-50 hover:bg-slate-100/70 border border-slate-200/60 rounded-xl transition-all duration-200 flex items-start gap-3">
                        <div class="pt-0.5">
                            <input id="includeAssignmentsInIndemnity" class="w-4 h-4 rounded border-slate-300 text-sky-500 focus:ring-sky-500/35 cursor-pointer transition-transform duration-100 active:scale-90" type="checkbox" checked />
                        </div>
                        <div class="flex-grow select-none">
                            <label for="includeAssignmentsInIndemnity" class="block text-xs font-bold text-slate-800 cursor-pointer hover:text-sky-500 transition-colors">Incluir Asignaciones (Base Diaria)</label>
                            <span class="block text-[10px] text-slate-500 font-medium mt-0.5 leading-relaxed">Suma asignaciones de colación y movilización a la base diaria de cálculo para la indemnización (criterio judicial).</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Results Column (Right, Sticky) -->
        <div class="flex-grow bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm lg:sticky lg:top-24 space-y-6">
            <div class="text-center sm:text-left border-b border-slate-100 pb-5">
                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Monto Total del Finiquito</h3>
                <div class="flex items-baseline gap-2 justify-center sm:justify-start">
                    <span id="totalAmount" class="text-4xl sm:text-5xl font-black text-slate-900 tracking-tight font-mono">$ —</span>
                    <span class="text-sm font-semibold text-slate-400">CLP</span>
                </div>
                <div class="mt-2 text-xs text-slate-400 font-medium flex items-center gap-1 justify-center sm:justify-start">
                    <span class="material-icons text-[12px] text-sky-500">info_outline</span>
                    Desglose detallado referencial
                </div>
            </div>

            <!-- Detailed Breakdown items -->
            <div class="space-y-3.5">
                <!-- IAS Row -->
                <div id="yearsRow" class="flex justify-between items-center text-sm py-1 border-b border-slate-50">
                    <span class="text-slate-600 font-medium flex items-center gap-1">
                        Años de Servicio
                        <span class="material-icons text-[12px] text-slate-400 cursor-help" title="Un mes de remuneración imponible habitual por cada año trabajado (tope 11 años).">help_outline</span>
                    </span>
                    <span id="yearsServiceAmount" class="font-bold text-slate-800 font-mono">$ —</span>
                </div>

                <!-- Notice Row -->
                <div id="noticeRow" class="flex justify-between items-center text-sm py-1 border-b border-slate-50">
                    <span class="text-slate-600 font-medium flex items-center gap-1">
                        Aviso Previo
                        <span class="material-icons text-[12px] text-slate-400 cursor-help" title="Equivale a un mes de remuneración si el empleador no dio el aviso con 30 días de anticipación.">help_outline</span>
                    </span>
                    <span id="noticeAmount" class="font-bold text-slate-800 font-mono">$ —</span>
                </div>

                <!-- Vacación Prop Row -->
                <div class="flex justify-between items-center text-sm py-1 border-b border-slate-50">
                    <span class="text-slate-600 font-medium flex items-center gap-1">
                        Vacaciones Proporcionales
                        <span class="material-icons text-[12px] text-slate-400 cursor-help" title="Pago por los días hábiles acumulados generados durante la fracción del año laboral en curso.">help_outline</span>
                    </span>
                    <span id="vacationPropAmount" class="font-bold text-slate-800 font-mono">$ —</span>
                </div>

                <!-- Vacación Pendiente Row -->
                <div class="flex justify-between items-center text-sm py-1 border-b border-slate-50">
                    <span class="text-slate-600 font-medium flex items-center gap-1">
                        Vacaciones Pendientes
                        <span class="material-icons text-[12px] text-slate-400 cursor-help" title="Pago por días de vacaciones de años anteriores acumulados que no fueron usados por el trabajador.">help_outline</span>
                    </span>
                    <span id="vacationPendingAmount" class="font-bold text-slate-800 font-mono">$ —</span>
                </div>

                <!-- Pending Salary Row -->
                <div class="flex justify-between items-center text-sm py-1 border-b border-slate-50">
                    <span class="text-slate-600 font-medium flex items-center gap-1">
                        Remuneraciones Pendientes
                        <span id="daysWorkedOutput" class="text-[9px] bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded font-bold uppercase font-mono tracking-wider ml-1">— DÍAS</span>
                    </span>
                    <span id="pendingSalaryAmount" class="font-bold text-slate-800 font-mono">$ —</span>
                </div>

                <!-- AFC Deduction Row -->
                <div id="afcRow" class="flex justify-between items-center text-sm py-1 border-b border-slate-50 text-red-500 hidden">
                    <span class="font-medium flex items-center gap-1">
                        Aporte AFC Descontable
                        <span class="material-icons text-[12px] text-slate-400 cursor-help" title="Descuento correspondiente al aporte del empleador a la cuenta individual del seguro de cesantía.">help_outline</span>
                    </span>
                    <span id="afcAmount" class="font-bold font-mono">-$0</span>
                </div>
            </div>

            <!-- Dynamic Non-monetary Data -->
            <div class="p-4 bg-slate-50 border border-slate-200 rounded-2xl grid grid-cols-2 gap-4">
                <div>
                    <span class="block text-[9px] font-bold text-slate-400 uppercase tracking-widest mb-0.5">Antigüedad</span>
                    <span id="antiquityOutput" class="text-xs font-bold text-slate-700 font-mono">— años, — meses</span>
                </div>
                <div>
                    <span class="block text-[9px] font-bold text-slate-400 uppercase tracking-widest mb-0.5">Vacaciones Totales</span>
                    <span id="totalVacationDaysOutput" class="text-xs font-bold text-slate-700 font-mono">— días hábiles</span>
                </div>
            </div>

            <div class="pt-4 border-t border-slate-100 flex flex-col sm:flex-row justify-between text-[10px] text-slate-400 font-medium gap-2">
                <span id="lastUpdateDate">Última actualización legal: Febrero 2026</span>
                <span class="flex items-center gap-0.5">
                    Tope Legal: 
                    <span id="ufCapValue" class="font-bold text-slate-600 font-mono">90 UF</span>
                </span>
            </div>

            <!-- PDF and Lead Capture section -->
            <div id="pdf-section" class="mt-4 hidden no-print">
              <button id="download-pdf-btn" 
                class="flex items-center gap-2 px-4 py-2.5 bg-sky-500 hover:bg-sky-600 text-white text-sm font-semibold rounded-lg transition-colors cursor-pointer">
                📥 Descargar Desglose PDF
              </button>
              <p class="text-xs text-slate-400 mt-1">Descarga instantánea. Sin registro.</p>
            </div>

            <!-- Lead Capture Section (SOLO EN FINIQUITO) -->
            <div id="lead-section" class="mt-3 p-4 bg-amber-50 border border-amber-200 rounded-xl no-print hidden">
              <p class="text-sm font-semibold text-amber-900 mb-2">
                ⚖️ ¿Crees que tu despido fue injustificado?
              </p>
              <p class="text-xs text-amber-700 mb-3">
                Déjanos tu caso y te contactamos.
              </p>
              <form id="lead-form" class="space-y-2">
                <input type="text" id="lead-nombre" placeholder="Tu nombre" required
                  class="w-full px-3 py-2 text-sm border border-amber-300 rounded-lg bg-white outline-none focus:border-amber-500">
                <input type="email" id="lead-correo" placeholder="tu@correo.com" required
                  class="w-full px-3 py-2 text-sm border border-amber-300 rounded-lg bg-white outline-none focus:border-amber-500">
                <input type="tel" id="lead-telefono" placeholder="+56 9 XXXX XXXX"
                  class="w-full px-3 py-2 text-sm border border-amber-300 rounded-lg bg-white outline-none focus:border-amber-500">
                <button type="button" onclick="enviarLead()"
                  class="w-full py-2.5 bg-amber-500 hover:bg-amber-600 text-white text-sm font-semibold rounded-lg transition-colors">
                  Quiero que revisen mi caso →
                </button>
              </form>
              <div id="lead-confirmacion" class="hidden mt-3 p-3 bg-green-50 border border-green-200 rounded-lg text-sm text-green-800 text-center">
                ✅ Recibimos tu caso. Te contactaremos pronto.
              </div>
              <p class="text-xs text-amber-600 mt-2 text-center">
                Sin costo. Solo para determinar si tu despido califica.
              </p>
            </div>
        </div>
    </div>

    <!-- ---------------------------------------------------- -->
    <!-- SUELDO LIQUIDO CALCULATOR CONTAINER                  -->
    <!-- ---------------------------------------------------- -->
    <div id="sueldo-calc-container" class="flex flex-col lg:flex-row gap-8 items-start hidden">
        <!-- Inputs Column (Left, 420px) -->
        <div class="w-full lg:w-[420px] shrink-0 bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm space-y-6 no-print">
            <div class="flex justify-between items-center mb-5 pb-3 border-b border-slate-100">
                <h2 class="text-lg font-bold text-slate-900">Datos Remuneración</h2>
                <span class="px-2.5 py-1 text-[10px] font-bold text-sky-600 bg-sky-50 border border-sky-100 rounded-md">Real-time</span>
            </div>

            <!-- Base & Overtime -->
            <div class="space-y-4">
                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1" for="salary">Sueldo Base Mensual</label>
                    <div class="relative">
                        <span class="absolute left-4 top-3 text-slate-500 font-bold">$</span>
                        <input id="salary" name="salary" placeholder="539.000" type="text" value="539.000" class="block w-full pl-8 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 font-bold focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-right font-mono" />
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-1">
                        <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Horas Extras</label>
                        <input id="overtime" type="number" placeholder="0" min="0" class="block w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-semibold text-right" />
                    </div>
                    <div class="space-y-1">
                        <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Bonos / Comisiones</label>
                        <div class="relative">
                            <span class="absolute left-3 top-3 text-slate-500 font-bold text-xs">$</span>
                            <input id="bonuses" type="text" placeholder="0" class="block w-full pl-7 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-semibold text-right font-mono" />
                        </div>
                    </div>
                </div>
            </div>

            <!-- Gratificación & Contrato -->
            <div class="space-y-4 pt-4 border-t border-slate-100">
                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Gratificación Legal</label>
                    <select id="gratificationType" class="block w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-semibold cursor-pointer">
                        <option value="legal_tope">Tope Legal (25% / 4.75 IMM)</option>
                        <option value="manual">Monto Fijo Manual</option>
                        <option value="none">Sin Gratificación</option>
                    </select>
                    <!-- Manual input container (hidden on load) -->
                    <div id="manualGratInput" class="hidden relative pt-2">
                        <span class="absolute left-4 top-5 text-slate-400 font-bold">$</span>
                        <input id="gratificationManual" type="text" placeholder="Monto fijo" class="block w-full pl-8 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-mono text-right" />
                    </div>
                </div>

                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Tipo de Contrato</label>
                    <div class="flex p-1 bg-slate-100 rounded-xl border border-slate-200">
                        <button id="btn-indefinido" class="flex-1 py-2 px-3 rounded-lg bg-sky-500 text-white text-xs font-bold uppercase tracking-wider shadow-sm transition-all outline-none">Indefinido</button>
                        <button id="btn-plazo" class="flex-1 py-2 px-3 rounded-lg text-slate-400 hover:text-slate-700 text-xs font-bold uppercase tracking-wider transition-colors outline-none">Plazo Fijo</button>
                    </div>
                </div>
            </div>

            <!-- AFP & Salud -->
            <div class="space-y-4 pt-4 border-t border-slate-100">
                <div class="space-y-1">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">AFP (Administradora)</label>
                    <select id="afpSelect" class="block w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-slate-800 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all outline-none text-sm font-semibold cursor-pointer">
                        <option value="Capital">Capital (11,44%)</option>
                        <option value="Cuprum">Cuprum (11,44%)</option>
                        <option value="Habitat">Habitat (11,27%)</option>
                        <option value="Modelo" selected>Modelo (10,58%)</option>
                        <option value="Planvital">Planvital (11,16%)</option>
                        <option value="Provida">Provida (11,45%)</option>
                        <option value="Uno">Uno (10,69%)</option>
                    </select>
                </div>

                <div class="space-y-2">
                    <label class="block text-xs font-bold text-slate-600 uppercase ml-1">Previsión de Salud</label>
                    <div class="flex items-center gap-6">
                        <label class="flex items-center cursor-pointer group text-sm text-slate-600 font-semibold select-none">
                            <input class="form-radio text-sky-500 focus:ring-sky-500/35 border-slate-300 h-4.5 w-4.5 cursor-pointer mr-2" name="salud" type="radio" value="fonasa" checked />
                            Fonasa (7%)
                        </label>
                        <label class="flex items-center cursor-pointer group text-sm text-slate-600 font-semibold select-none">
                            <input class="form-radio text-sky-500 focus:ring-sky-500/35 border-slate-300 h-4.5 w-4.5 cursor-pointer mr-2" name="salud" type="radio" value="isapre" />
                            Isapre
                        </label>
                    </div>
                    <!-- Isapre Input (hidden on load) -->
                    <div id="isapreInput" class="hidden relative pt-2">
                        <div class="flex border border-slate-200 rounded-xl overflow-hidden focus-within:ring-2 focus-within:ring-sky-500/20 focus-within:border-sky-500 transition-all bg-white">
                            <input id="isapreValue" class="border-none bg-transparent text-slate-800 w-full pl-4 py-2.5 outline-none text-sm font-semibold text-right" placeholder="Cotización pactada (Ej: 2.5)" />
                            <div class="bg-slate-100 border-l border-slate-200 px-4 flex items-center justify-center">
                                <span class="text-xs font-bold text-slate-600">UF</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Non-Taxable Incomes -->
            <div class="space-y-4 pt-4 border-t border-slate-100">
                <h4 class="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1">
                    <span class="material-icons text-sm text-sky-500">payments</span>
                    Haberes No Imponibles
                </h4>
                <div class="grid grid-cols-3 gap-2">
                    <div>
                        <label class="text-[9px] font-bold text-slate-500 ml-1">Colación</label>
                        <div class="relative">
                            <span class="absolute left-2.5 top-2.5 text-slate-500 text-xs">$</span>
                            <input id="colacion" type="text" placeholder="0" class="block w-full pl-5 pr-2 py-2 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" />
                        </div>
                    </div>
                    <div>
                        <label class="text-[9px] font-bold text-slate-500 ml-1">Movilización</label>
                        <div class="relative">
                            <span class="absolute left-2.5 top-2.5 text-slate-500 text-xs">$</span>
                            <input id="movilizacion" type="text" placeholder="0" class="block w-full pl-5 pr-2 py-2 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" />
                        </div>
                    </div>
                    <div>
                        <label class="text-[9px] font-bold text-slate-500 ml-1">Viáticos</label>
                        <div class="relative">
                            <span class="absolute left-2.5 top-2.5 text-slate-500 text-xs">$</span>
                            <input id="viaticos" type="text" placeholder="0" class="block w-full pl-5 pr-2 py-2 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" />
                        </div>
                    </div>
                </div>
            </div>

            <!-- Accordion Discounts -->
            <details class="p-1 bg-slate-50 border border-slate-200 rounded-2xl transition-colors">
                <summary class="cursor-pointer p-3.5 font-bold text-xs text-slate-500 hover:text-slate-800 uppercase tracking-widest flex items-center justify-between outline-none list-none [&::-webkit-details-marker]:hidden">
                    <div class="flex items-center gap-1.5">
                        <span class="material-icons text-sky-500 text-sm">playlist_add</span>
                        Descuentos Opcionales
                    </div>
                    <span class="material-icons text-sky-500">expand_more</span>
                </summary>
                <div class="px-3 pb-3.5 pt-2 border-t border-slate-200 grid grid-cols-2 gap-3">
                    <div>
                        <label class="text-[9px] font-bold text-slate-500 uppercase ml-1">CCAF (Imponible)</label>
                        <div class="relative">
                            <span class="absolute left-2.5 top-2 text-slate-500 text-xs">$</span>
                            <input id="ccaf" type="text" placeholder="0" class="block w-full pl-5 pr-2 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" />
                        </div>
                    </div>
                    <div>
                        <label class="text-[9px] font-bold text-slate-500 uppercase ml-1">APV (Imponible)</label>
                        <div class="relative">
                            <span class="absolute left-2.5 top-2 text-slate-500 text-xs">$</span>
                            <input id="apv" type="text" placeholder="0" class="block w-full pl-5 pr-2 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" />
                        </div>
                    </div>
                    <div>
                        <label class="text-[9px] font-bold text-slate-500 uppercase ml-1">Préstamos</label>
                        <div class="relative">
                            <span class="absolute left-2.5 top-2 text-slate-500 text-xs">$</span>
                            <input id="prestamos" type="text" placeholder="0" class="block w-full pl-5 pr-2 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" />
                        </div>
                    </div>
                    <div>
                        <label class="text-[9px] font-bold text-slate-500 uppercase ml-1">Pensión Alimenticia</label>
                        <div class="relative">
                            <span class="absolute left-2.5 top-2 text-slate-500 text-xs">$</span>
                            <input id="pension" type="text" placeholder="0" class="block w-full pl-5 pr-2 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" />
                        </div>
                    </div>
                    <div>
                        <label class="text-[9px] font-bold text-slate-500 uppercase ml-1">Sindicato</label>
                        <div class="relative">
                            <span class="absolute left-2.5 top-2 text-slate-500 text-xs">$</span>
                            <input id="sindicato" type="text" placeholder="0" class="block w-full pl-5 pr-2 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" />
                        </div>
                    </div>
                    <div>
                        <label class="text-[9px] font-bold text-slate-500 uppercase ml-1">Otros Descuentos</label>
                        <div class="relative">
                            <span class="absolute left-2.5 top-2 text-slate-500 text-xs">$</span>
                            <input id="otrosDescuentos" type="text" placeholder="0" class="block w-full pl-5 pr-2 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-mono text-right" />
                        </div>
                    </div>
                    <div class="col-span-2 pt-2 border-t border-slate-100 flex items-center">
                        <label class="flex items-center gap-2 cursor-pointer">
                            <input id="toggleReduceSS" type="checkbox" class="w-4 h-4 rounded border-slate-300 text-sky-500 focus:ring-sky-500/35 cursor-pointer">
                            <span class="text-[10px] text-slate-500 font-semibold">CCAF/APV reduce base de AFP/Salud</span>
                        </label>
                    </div>
                </div>
            </details>
        </div>

        <!-- Results Column (Right, Sticky) -->
        <div class="flex-grow bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm lg:sticky lg:top-24 space-y-6">
            <div class="text-center sm:text-left border-b border-slate-100 pb-5 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Tu Sueldo Líquido Estimado</h3>
                    <div class="flex items-baseline gap-2 justify-center sm:justify-start">
                        <span id="headerNetSalary" class="text-4xl sm:text-5xl font-black text-slate-900 tracking-tight font-mono">$ —</span>
                        <span id="headerPercentage" class="text-sm font-bold text-slate-400">0%</span>
                    </div>
                </div>
                <div class="text-right">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block">Total Descuentos</span>
                    <span id="headerTotalDiscounts" class="text-lg font-bold text-red-500 font-mono">-$ —</span>
                </div>
            </div>

            <!-- Interactive Donut Chart Segment -->
            <div class="flex flex-col sm:flex-row gap-6 items-center justify-center border-b border-slate-100 pb-6">
                <!-- Conic styled div chart -->
                <div id="distribution-chart" class="w-44 h-44 rounded-full border border-slate-100 flex items-center justify-center relative shadow-inner shrink-0" style="background: conic-gradient(#10b981 0% 100%);">
                    <div class="w-32 h-32 rounded-full bg-white flex flex-col items-center justify-center z-10 shadow-sm">
                        <span id="chart-liquid-percent" class="text-3xl font-extrabold text-slate-800 font-mono">—</span>
                        <span class="text-[9px] text-slate-500 font-bold uppercase tracking-wider mt-0.5">Líquido</span>
                    </div>
                </div>

                <!-- Custom Dynamic Legend -->
                <div class="space-y-2.5 flex-grow w-full max-w-[220px]">
                    <div class="flex items-center justify-between text-xs font-medium">
                        <div class="flex items-center gap-2">
                            <span class="w-3 h-3 rounded bg-emerald-500 shrink-0"></span>
                            <span class="text-slate-500">Sueldo Líquido</span>
                        </div>
                        <span id="legend-liquido-percent" class="font-bold text-slate-800 font-mono">0%</span>
                    </div>
                    <div class="flex items-center justify-between text-xs font-medium">
                        <div class="flex items-center gap-2">
                            <span class="w-3 h-3 rounded bg-blue-500 shrink-0"></span>
                            <span class="text-slate-500">AFP + AFC</span>
                        </div>
                        <span id="legend-afp-percent" class="font-bold text-slate-800 font-mono">0%</span>
                    </div>
                    <div class="flex items-center justify-between text-xs font-medium">
                        <div class="flex items-center gap-2">
                            <span class="w-3 h-3 rounded bg-rose-500 shrink-0"></span>
                            <span class="text-slate-500">Previsión Salud</span>
                        </div>
                        <span id="legend-health-percent" class="font-bold text-slate-800 font-mono">0%</span>
                    </div>
                    <div class="flex items-center justify-between text-xs font-medium">
                        <div class="flex items-center gap-2">
                            <span class="w-3 h-3 rounded bg-purple-500 shrink-0"></span>
                            <span class="text-slate-500">Impuesto SII</span>
                        </div>
                        <span id="legend-tax-percent" class="font-bold text-slate-800 font-mono">0%</span>
                    </div>
                    <div id="legend-otros-container" class="flex items-center justify-between text-xs font-medium hidden">
                        <div class="flex items-center gap-2">
                            <span class="w-3 h-3 rounded bg-orange-500 shrink-0"></span>
                            <span class="text-slate-500">Otros Descuentos</span>
                        </div>
                        <span id="legend-otros-percent" class="font-bold text-slate-800 font-mono">0%</span>
                    </div>
                </div>
            </div>

            <!-- Detailed Breakdown values -->
            <div class="space-y-3 pt-2">
                <div class="flex justify-between items-center text-sm py-1 border-b border-slate-50">
                    <span class="text-slate-600 font-semibold" id="labelAFP">AFP</span>
                    <span id="resultAFP" class="font-bold text-slate-800 font-mono">$0</span>
                </div>
                <div class="flex justify-between items-center text-sm py-1 border-b border-slate-50">
                    <span class="text-slate-600 font-semibold" id="labelHealth">Salud</span>
                    <span id="resultHealth" class="font-bold text-slate-800 font-mono">$0</span>
                </div>
                <div class="flex justify-between items-center text-sm py-1 border-b border-slate-50">
                    <span class="text-slate-600 font-semibold">Seguro Cesantía (AFC)</span>
                    <span id="resultAFC" class="font-bold text-slate-800 font-mono">$0</span>
                </div>
                <div class="flex justify-between items-center text-sm py-1 border-b border-slate-50">
                    <span class="text-slate-600 font-semibold">Impuesto Único (Segunda Categoría)</span>
                    <span id="resultTax" class="font-bold text-slate-800 font-mono">$0</span>
                </div>

                <!-- CCAF / APV Breakdown Container -->
                <div id="section-imponibles" class="bg-amber-600/5 border border-amber-600/10 rounded-2xl p-3 hidden space-y-2 mt-2">
                    <div class="flex justify-between items-center text-xs font-semibold text-amber-800">
                        <span>CCAF Descontado</span>
                        <span id="resultCCAF" class="font-mono">$0</span>
                    </div>
                    <div class="flex justify-between items-center text-xs font-semibold text-amber-800">
                        <span>APV Descontado</span>
                        <span id="resultAPV" class="font-mono">$0</span>
                    </div>
                </div>

                <!-- Non-imponibles and cash deductions container -->
                <div id="section-no-imponibles" class="bg-slate-50 border border-slate-100 rounded-2xl p-3 hidden space-y-2 mt-2 text-xs font-medium text-slate-600">
                    <div class="flex justify-between items-center">
                        <span>Préstamos</span>
                        <span id="resultPrestamos" class="font-mono">$0</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span>Pensión Alimenticia</span>
                        <span id="resultPension" class="font-mono">$0</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span>Sindicato</span>
                        <span id="resultSindicato" class="font-mono">$0</span>
                    </div>
                    <div class="flex justify-between items-center text-slate-700 font-bold">
                        <span>Otros</span>
                        <span id="resultOtros" class="font-mono">$0</span>
                    </div>
                </div>
            </div>

            <!-- Inline Alert Box -->
            <div id="global-notifications" class="hidden space-y-2 pt-2">
                <!-- Alerts are injected dynamically by salary_ui.js -->
            </div>

            <!-- PDF section -->
            <div id="pdf-section" class="mt-4 hidden no-print">
              <button id="download-pdf-btn-sueldo" 
                class="flex items-center gap-2 px-4 py-2.5 bg-sky-500 hover:bg-sky-600 text-white text-sm font-semibold rounded-lg transition-colors cursor-pointer">
                📥 Descargar Desglose PDF
              </button>
              <p class="text-xs text-slate-400 mt-1">Descarga instantánea. Sin registro.</p>
            </div>
        </div>
    </div>

    <!-- Mobile Result Bar shared at the bottom -->
    <div id="mobile-result-bar" class="lg:hidden fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-slate-200 px-6 py-4 flex items-center justify-between shadow-2xl translate-y-full transition-transform duration-300 no-print">
        <div>
            <span class="block text-[9px] font-bold text-slate-400 uppercase tracking-widest">Líquido a pago</span>
            <div class="flex items-baseline gap-1.5">
                <span id="mobile-result-value" class="text-2xl font-black text-slate-900 tracking-tight font-mono">$0</span>
                <span id="mobile-result-percentage" class="text-xs font-bold text-slate-400">0%</span>
            </div>
        </div>
        <button onclick="window.scrollTo({top: 0, behavior: 'smooth'})" class="px-4 py-2.5 bg-sky-500 hover:bg-sky-600 text-white text-xs font-bold uppercase tracking-wider rounded-xl shadow-md shadow-sky-500/10">Ver desglose</button>
    </div>

    <!-- ---------------------------------------------------- -->
    <!-- EDUCATIONAL ACCORDIONS (Below the fold)              -->
    <!-- ---------------------------------------------------- -->
    <div class="max-w-3xl mx-auto mt-20 no-print">
        <h2 class="text-2xl font-bold text-slate-900 text-center mb-8">Información y Preguntas Frecuentes</h2>
        <div class="space-y-4">
            <details class="bg-white border border-slate-200 rounded-2xl group transition-all duration-200 overflow-hidden">
                <summary class="cursor-pointer p-5 font-bold text-sm text-slate-800 flex justify-between items-center outline-none list-none [&::-webkit-details-marker]:hidden">
                    ¿Cómo se calcula el sueldo líquido en Chile?
                    <span class="material-icons transition-transform group-open:rotate-180 text-sky-500">expand_more</span>
                </summary>
                <div class="px-5 pb-5 pt-1 text-sm text-slate-500 leading-relaxed border-t border-slate-100">
                    El sueldo líquido (o sueldo a pago) se obtiene restando del Sueldo Bruto los descuentos obligatorios fijados por ley: la cotización para tu fondo de pensiones en la AFP (que oscila entre 10.58% y 11.45% según la entidad), la cotización de salud legal (7% para Fonasa o el monto pactado en tu Isapre), y tu parte del seguro de cesantía en AFC (0.6% si tu contrato es de tipo indefinido). De exceder las 13.5 UTM imponibles, se aplica de forma progresiva el impuesto de segunda categoría.
                </div>
            </details>

            <details class="bg-white border border-slate-200 rounded-2xl group transition-all duration-200 overflow-hidden">
                <summary class="cursor-pointer p-5 font-bold text-sm text-slate-800 flex justify-between items-center outline-none list-none [&::-webkit-details-marker]:hidden">
                    ¿Qué conceptos integra un finiquito laboral?
                    <span class="material-icons transition-transform group-open:rotate-180 text-sky-500">expand_more</span>
                </summary>
                <div class="px-5 pb-5 pt-1 text-sm text-slate-500 leading-relaxed border-t border-slate-100">
                    Un finiquito de trabajo contempla fundamentalmente cuatro haberes a liquidar: las remuneraciones pendientes por los días laborados durante el último mes, la indemnización por vacaciones proporcionales y pendientes no gozadas, la indemnización por años de servicio (un mes de remuneración computable por cada año completo, si la causal es necesidades de la empresa u otra idónea), y la indemnización sustitutiva de aviso previo (un mes adicional, si el despido fue de forma inmediata).
                </div>
            </details>

            <details class="bg-white border border-slate-200 rounded-2xl group transition-all duration-200 overflow-hidden">
                <summary class="cursor-pointer p-5 font-bold text-sm text-slate-800 flex justify-between items-center outline-none list-none [&::-webkit-details-marker]:hidden">
                    ¿Cómo funciona la indemnización por años de servicio?
                    <span class="material-icons transition-transform group-open:rotate-180 text-sky-500">expand_more</span>
                </summary>
                <div class="px-5 pb-5 pt-1 text-sm text-slate-500 leading-relaxed border-t border-slate-100">
                    Acorde al artículo 163 del Código del Trabajo, si el contrato es indefinido y termina por Necesidades de la Empresa (Art. 161), el empleador debe abonar una indemnización equivalente a un mes de la última remuneración imponible por cada año completo de servicio continuado. Las fracciones iguales o superiores a 6 meses se computan como un año completo adicional. Existe un tope legal de 11 años computables, y una limitación económica mensual máxima de 90 UF.
                </div>
            </details>

            <details class="bg-white border border-slate-200 rounded-2xl group transition-all duration-200 overflow-hidden">
                <summary class="cursor-pointer p-5 font-bold text-sm text-slate-800 flex justify-between items-center outline-none list-none [&::-webkit-details-marker]:hidden">
                    ¿Cómo se calculan las vacaciones proporcionales en el finiquito?
                    <span class="material-icons transition-transform group-open:rotate-180 text-sky-500">expand_more</span>
                </summary>
                <div class="px-5 pb-5 pt-1 text-sm text-slate-500 leading-relaxed border-t border-slate-100">
                    Todo trabajador acumula por ley 1.25 días hábiles de feriado por cada mes completo trabajado (15 días hábiles anuales). Al desvincularse, el empleador debe compensar monetariamente los días de vacaciones proporcionales generados en el año actual que no alcanzaron a gozarse. Para valorizarlos, se proyectan los días hábiles sobre el calendario corrido incluyendo fines de semana y feriados, multiplicando dichos días calendario por la remuneración diaria del trabajador.
                </div>
            </details>

            <details class="bg-white border border-slate-200 rounded-2xl group transition-all duration-200 overflow-hidden">
                <summary class="cursor-pointer p-5 font-bold text-sm text-slate-800 flex justify-between items-center outline-none list-none [&::-webkit-details-marker]:hidden">
                    ¿Cuál es el plazo legal de pago de un finiquito?
                    <span class="material-icons transition-transform group-open:rotate-180 text-sky-500">expand_more</span>
                </summary>
                <div class="px-5 pb-5 pt-1 text-sm text-slate-500 leading-relaxed border-t border-slate-100">
                    De conformidad con el artículo 177 del Código del Trabajo, el empleador dispone de un plazo máximo improrrogable de 10 días hábiles (contados de lunes a sábado, sin incluir domingos ni festivos) a partir del término efectivo del contrato de trabajo para confeccionar el documento de finiquito y poner a disposición del trabajador los montos resultantes. El no pago oportuno faculta a demandar con reajustes por IPC y multas de hasta 150%.
                </div>
            </details>
        </div>
    </div>

    <!-- ---------------------------------------------------- -->
    <!-- RELATED GUIDES SECTION (6 Cards)                     -->
    <!-- ---------------------------------------------------- -->
    <div class="max-w-[1200px] mx-auto mt-24 no-print">
        <h2 class="text-2xl font-bold text-slate-900 text-center mb-10">Guías Prácticas de Utilidad</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Card 1 -->
            <a href="como-calcular-sueldo-liquido-paso-a-paso" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] transition-all duration-300">
                <div class="aspect-video bg-slate-100 overflow-hidden relative">
                    <img src="assets/guia-sueldo-liquido-cover.png" alt="Calcular sueldo líquido" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                </div>
                <div class="p-5">
                    <h3 class="font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2 text-sm">Cómo Calcular Sueldo Líquido Paso a Paso</h3>
                    <p class="text-slate-500 text-[11px] leading-relaxed line-clamp-2">Entiende al detalle cómo pasar tu renta bruta mensual a líquida restando las retenciones obligatorias de AFP, Fonasa o Isapre.</p>
                </div>
            </a>
            <!-- Card 2 -->
            <a href="guia-vacaciones-proporcionales" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] transition-all duration-300">
                <div class="aspect-video bg-slate-100 overflow-hidden relative">
                    <img src="assets/guia-vacaciones-proporcionales-cover.png" alt="Vacaciones Proporcionales" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                </div>
                <div class="p-5">
                    <h3 class="font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2 text-sm">Cálculo de Vacaciones Proporcionales</h3>
                    <p class="text-slate-500 text-[11px] leading-relaxed line-clamp-2">Aprende la fórmula del feriado proporcional y comprende por qué a veces aparece valorizado en $0 en tu liquidación de término.</p>
                </div>
            </a>
            <!-- Card 3 -->
            <a href="como-calcular-finiquito-chile" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] transition-all duration-300">
                <div class="aspect-video bg-slate-100 overflow-hidden relative">
                    <img src="assets/guia-calculo-finiquito-chile-2026.png" alt="Cálculo de Finiquito" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                </div>
                <div class="p-5">
                    <h3 class="font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2 text-sm">Cómo Calcular tu Finiquito en Chile</h3>
                    <p class="text-slate-500 text-[11px] leading-relaxed line-clamp-2">Guía didáctica completa con fórmulas, indemnización por años de servicio, aviso previo y un ejemplo práctico resuelto.</p>
                </div>
            </a>
            <!-- Card 4 -->
            <a href="despido-necesidades-empresa-articulo-161" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] transition-all duration-300">
                <div class="aspect-video bg-slate-100 overflow-hidden relative">
                    <img src="assets/guia-despido-necesidades-empresa-161.png" alt="Artículo 161" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                </div>
                <div class="p-5">
                    <h3 class="font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2 text-sm">Despido por Necesidades de la Empresa</h3>
                    <p class="text-slate-500 text-[11px] leading-relaxed line-clamp-2">Conoce qué causales se consideran válidas en el Artículo 161 y qué hacer si consideras que tu despido es injustificado.</p>
                </div>
            </a>
            <!-- Card 5 -->
            <a href="ley-40-horas-chile-2026" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] transition-all duration-300">
                <div class="aspect-video bg-slate-100 overflow-hidden relative">
                    <img src="assets/guia-ley-40-horas-chile-cover.png" alt="Ley 40 Horas" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                </div>
                <div class="p-5">
                    <h3 class="font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2 text-sm">Implementación de la Ley de 40 Horas</h3>
                    <p class="text-slate-500 text-[11px] leading-relaxed line-clamp-2">Infografía detallada y cronograma legal sobre la reducción paulatina de la jornada ordinaria en Chile en 2026.</p>
                </div>
            </a>
            <!-- Card 6 -->
            <a href="que-hacer-si-no-te-pagan-el-finiquito" class="group block bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] transition-all duration-300">
                <div class="aspect-video bg-slate-100 overflow-hidden relative">
                    <img src="assets/guia-finiquito-no-pago-cover.png" alt="No pago de finiquito" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                </div>
                <div class="p-5">
                    <h3 class="font-bold text-slate-900 group-hover:text-sky-500 transition-colors mb-2 text-sm">¿Qué hacer si no te pagan a tiempo?</h3>
                    <p class="text-slate-500 text-[11px] leading-relaxed line-clamp-2">Conoce las multas aplicables a los empleadores que exceden el plazo reglamentario de 10 días para liquidar tu contrato.</p>
                </div>
            </a>
        </div>
    </div>

    <!-- ---------------------------------------------------- -->
    <!-- PRINT-ONLY TEMPLATES FOR PROFESSIONAL PDF            -->
    <!-- ---------------------------------------------------- -->
    
    <!-- Finiquito Print Template -->
    <div id="print-template-finiquito" class="print-only hidden font-sans text-slate-800 p-8 max-w-4xl mx-auto">
      <!-- Header with Logo and Brand -->
      <div class="flex justify-between items-center border-b-2 border-slate-200 pb-6 mb-6">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-sky-500 flex items-center justify-center shadow-md shadow-sky-500/20">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="4" y="4" width="16" height="16" rx="2"></rect>
              <line x1="9" y1="9" x2="15" y2="9"></line>
              <line x1="9" y1="13" x2="15" y2="13"></line>
              <line x1="9" y1="17" x2="15" y2="17"></line>
            </svg>
          </div>
          <div>
            <span class="font-bold text-xl tracking-tight text-slate-900">Cálculo<span class="text-sky-500">Laboral</span></span>
            <span class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider">Simulación Legal de Finiquito</span>
          </div>
        </div>
        <div class="text-right">
          <h2 class="text-base font-bold text-slate-800 uppercase tracking-wider">Reporte de Finiquito</h2>
          <p class="text-[10px] text-slate-400 font-semibold mt-0.5">Fecha de emisión: <span id="print-date-finiquito" class="font-mono">—</span></p>
        </div>
      </div>

      <!-- Summary of Inputs -->
      <div class="bg-slate-50 rounded-2xl p-5 border border-slate-200/80 mb-6">
        <h3 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Parámetros de la Simulación</h3>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Fecha de Inicio:</span>
            <span id="print-input-start-date" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Fecha de Término:</span>
            <span id="print-input-end-date" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Antigüedad:</span>
            <span id="print-input-antiquity" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Causal de Término:</span>
            <span id="print-input-cause" class="font-bold text-slate-700">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Sueldo Base:</span>
            <span id="print-input-base-salary" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Gratificación:</span>
            <span id="print-input-gratification" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Asignaciones Fijas:</span>
            <span id="print-input-assignments" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Vac. Pendientes:</span>
            <span id="print-input-vacation-pending" class="font-bold text-slate-700 font-mono">—</span>
          </div>
        </div>
      </div>

      <!-- Main Breakdown Table -->
      <div class="border border-slate-200 rounded-2xl overflow-hidden mb-6">
        <table class="w-full border-collapse text-left text-xs">
          <thead>
            <tr class="bg-slate-100 border-b border-slate-200 text-slate-600 font-bold uppercase tracking-wider">
              <th class="py-3 px-4">Concepto Liquidado</th>
              <th class="py-3 px-4 text-right">Monto CLP</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-slate-700">
            <tr>
              <td class="py-3.5 px-4 font-semibold text-slate-700">Indemnización por Años de Servicio (IAS)</td>
              <td id="print-row-ias" class="py-3.5 px-4 text-right font-mono font-bold">$ —</td>
            </tr>
            <tr>
              <td class="py-3.5 px-4 font-semibold text-slate-700">Indemnización Sustitutiva de Aviso Previo</td>
              <td id="print-row-notice" class="py-3.5 px-4 text-right font-mono font-bold">$ —</td>
            </tr>
            <tr>
              <td class="py-3.5 px-4 font-semibold text-slate-700">Vacaciones Proporcionales</td>
              <td id="print-row-vacation-prop" class="py-3.5 px-4 text-right font-mono font-bold">$ —</td>
            </tr>
            <tr>
              <td class="py-3.5 px-4 font-semibold text-slate-700">Vacaciones Pendientes</td>
              <td id="print-row-vacation-pending" class="py-3.5 px-4 text-right font-mono font-bold">$ —</td>
            </tr>
            <tr>
              <td class="py-3.5 px-4 font-semibold text-slate-700">Remuneraciones Pendientes (Días del Mes)</td>
              <td id="print-row-pending-salary" class="py-3.5 px-4 text-right font-mono font-bold">$ —</td>
            </tr>
            <tr id="print-row-afc-container" class="text-red-600 bg-red-500/5">
              <td class="py-3.5 px-4 font-semibold">Descuento AFC Aporte Empleador</td>
              <td id="print-row-afc" class="py-3.5 px-4 text-right font-mono font-bold">-$ —</td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="bg-slate-900 text-white font-bold text-sm">
              <td class="py-4 px-4 rounded-bl-2xl">Total Neto del Finiquito Estimado</td>
              <td id="print-row-total" class="py-4 px-4 text-right font-mono rounded-br-2xl text-base">$ —</td>
            </tr>
          </tfoot>
        </table>
      </div>

      <!-- Footer Disclaimer -->
      <div class="text-[9px] text-slate-400 space-y-2 mt-8 leading-relaxed border-t border-slate-100 pt-4">
        <p><strong>Nota legal explicativa:</strong> Esta simulación de finiquito es de carácter meramente ilustrativo e informativo y no constituye asesoría legal ni vinculante para ninguna de las partes. El cálculo ha sido efectuado de acuerdo con las normativas legales de la Dirección del Trabajo (DT) vigentes en la República de Chile para el año 2026. Los valores definitivos pueden variar dependiendo de la revisión detallada de liquidaciones históricas y variables específicas de la relación laboral.</p>
        <p>© 2026 Cálculo Laboral Chile (calculolaboral.cl) — Herramientas gratuitas para el trabajador.</p>
      </div>
    </div>

    <!-- Sueldo Liquido Print Template -->
    <div id="print-template-sueldo" class="print-only hidden font-sans text-slate-800 p-8 max-w-4xl mx-auto">
      <!-- Header with Logo and Brand -->
      <div class="flex justify-between items-center border-b-2 border-slate-200 pb-6 mb-6">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-sky-500 flex items-center justify-center shadow-md shadow-sky-500/20">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="4" y="4" width="16" height="16" rx="2"></rect>
              <line x1="9" y1="9" x2="15" y2="9"></line>
              <line x1="9" y1="13" x2="15" y2="13"></line>
              <line x1="9" y1="17" x2="15" y2="17"></line>
            </svg>
          </div>
          <div>
            <span class="font-bold text-xl tracking-tight text-slate-900">Cálculo<span class="text-sky-500">Laboral</span></span>
            <span class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider">Simulación Legal de Sueldo Líquido</span>
          </div>
        </div>
        <div class="text-right">
          <h2 class="text-base font-bold text-slate-800 uppercase tracking-wider">Detalle de Liquidación</h2>
          <p class="text-[10px] text-slate-400 font-semibold mt-0.5">Fecha de emisión: <span id="print-date-sueldo" class="font-mono">—</span></p>
        </div>
      </div>

      <!-- Summary of Inputs -->
      <div class="bg-slate-50 rounded-2xl p-5 border border-slate-200/80 mb-6">
        <h3 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Haberes e Ingresos</h3>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Sueldo Base Mensual:</span>
            <span id="print-input-salary-base" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Horas Extraordinarias:</span>
            <span id="print-input-salary-ot" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Gratificación Legal:</span>
            <span id="print-input-salary-grat" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Bonos Imponibles:</span>
            <span id="print-input-salary-bonuses" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Asignación Colación:</span>
            <span id="print-input-salary-colacion" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Asignación Movilización:</span>
            <span id="print-input-salary-movilizacion" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">Viáticos / Otros No Imp:</span>
            <span id="print-input-salary-viaticos" class="font-bold text-slate-700 font-mono">—</span>
          </div>
          <div>
            <span class="block text-slate-400 font-semibold mb-0.5">AFP Seleccionada:</span>
            <span id="print-input-salary-afp-name" class="font-bold text-slate-700">—</span>
          </div>
        </div>
      </div>

      <!-- Main Breakdown Table -->
      <div class="border border-slate-200 rounded-2xl overflow-hidden mb-6">
        <table class="w-full border-collapse text-left text-xs">
          <thead>
            <tr class="bg-slate-100 border-b border-slate-200 text-slate-600 font-bold uppercase tracking-wider">
              <th class="py-3 px-4">Concepto Descontado / Liquidado</th>
              <th class="py-3 px-4 text-right">Monto CLP</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-slate-700">
            <tr>
              <td class="py-3 px-4 font-semibold text-slate-700">Cotización Previsional Obligatoria (AFP)</td>
              <td id="print-row-salary-afp" class="py-3 px-4 text-right font-mono font-bold text-red-600">-$ —</td>
            </tr>
            <tr>
              <td class="py-3 px-4 font-semibold text-slate-700">Cotización Legal de Salud (7% Fonasa / Isapre)</td>
              <td id="print-row-salary-health" class="py-3 px-4 text-right font-mono font-bold text-red-600">-$ —</td>
            </tr>
            <tr>
              <td class="py-3 px-4 font-semibold text-slate-700">Seguro de Cesantía (AFC Trabajador)</td>
              <td id="print-row-salary-afc" class="py-3 px-4 text-right font-mono font-bold text-red-600">-$ —</td>
            </tr>
            <tr>
              <td class="py-3 px-4 font-semibold text-slate-700">Impuesto de Segunda Categoría (SII)</td>
              <td id="print-row-salary-tax" class="py-3 px-4 text-right font-mono font-bold text-red-600">-$ —</td>
            </tr>
            <tr id="print-row-salary-ccaf-container" class="hidden bg-red-500/5">
              <td class="py-3 px-4 font-semibold text-slate-700">Descuento CCAF (Caja de Compensación)</td>
              <td id="print-row-salary-ccaf" class="py-3 px-4 text-right font-mono font-bold text-red-600">-$ —</td>
            </tr>
            <tr id="print-row-salary-apv-container" class="hidden bg-red-500/5">
              <td class="py-3 px-4 font-semibold text-slate-700">Descuento APV (Ahorro Previsional Voluntario)</td>
              <td id="print-row-salary-apv" class="py-3 px-4 text-right font-mono font-bold text-red-600">-$ —</td>
            </tr>
            <tr id="print-row-salary-loans-container" class="hidden bg-red-500/5">
              <td class="py-3 px-4 font-semibold text-slate-700">Descuento por Préstamos / Mutuales</td>
              <td id="print-row-salary-loans" class="py-3 px-4 text-right font-mono font-bold text-red-600">-$ —</td>
            </tr>
            <tr id="print-row-salary-pension-container" class="hidden bg-red-500/5">
              <td class="py-3 px-4 font-semibold text-slate-700">Descuento por Pensión Alimenticia</td>
              <td id="print-row-salary-pension" class="py-3 px-4 text-right font-mono font-bold text-red-600">-$ —</td>
            </tr>
            <tr id="print-row-salary-sindicato-container" class="hidden bg-red-500/5">
              <td class="py-3 px-4 font-semibold text-slate-700">Cuota Sindical</td>
              <td id="print-row-salary-sindicato" class="py-3 px-4 text-right font-mono font-bold text-red-600">-$ —</td>
            </tr>
            <tr id="print-row-salary-other-container" class="hidden bg-red-500/5">
              <td class="py-3 px-4 font-semibold text-slate-700">Otros Descuentos Autorizados</td>
              <td id="print-row-salary-other" class="py-3 px-4 text-right font-mono font-bold text-red-600">-$ —</td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="bg-slate-900 text-white font-bold text-sm">
              <td class="py-4 px-4 rounded-bl-2xl">Sueldo Líquido Final Estimado (Líquido a Pago)</td>
              <td id="print-row-salary-net" class="py-4 px-4 text-right font-mono rounded-br-2xl text-base">$ —</td>
            </tr>
          </tfoot>
        </table>
      </div>

      <!-- Footer Disclaimer -->
      <div class="text-[9px] text-slate-400 space-y-2 mt-8 leading-relaxed border-t border-slate-100 pt-4">
        <p><strong>Nota legal explicativa:</strong> Este cálculo de sueldo líquido es referencial e ilustrativo y se ha elaborado conforme a los topes imponibles y tasas previsionales vigentes para el año 2026 en Chile. Las liquidaciones definitivas extendidas por el empleador pueden tener variaciones específicas derivadas de comisiones exactas de AFP, tramos de seguro de cesantía o descuentos particulares pactados colectivamente.</p>
        <p>© 2026 Cálculo Laboral Chile (calculolaboral.cl) — Herramientas gratuitas para el trabajador.</p>
      </div>
    </div>
</div>
"""

INDEX_SCRIPTS = """
    <!-- Calculator Scripts -->
    <script src="/js/salary_logic.js"></script>
    <script src="/js/salary_ui.js"></script>
    <script src="/js/logic.js"></script>
    <script src="/js/ui.js"></script>
    <script src="/js/validation.js"></script>
    <script>
        // High-end tab system switching between both calculators
        function switchCalculatorTab(tab) {
            const btnFiniquito = document.getElementById('tab-btn-finiquito');
            const btnSueldo = document.getElementById('tab-btn-sueldo');
            const containerFiniquito = document.getElementById('finiquito-calc-container');
            const containerSueldo = document.getElementById('sueldo-calc-container');

            if (tab === 'finiquito') {
                containerFiniquito.classList.remove('hidden');
                containerSueldo.classList.add('hidden');
                btnFiniquito.className = "flex-1 py-3.5 px-6 rounded-xl text-xs font-bold uppercase tracking-wider transition-all text-white bg-sky-500 shadow-md shadow-sky-500/20 outline-none";
                btnSueldo.className = "flex-1 py-3.5 px-6 rounded-xl text-xs font-bold uppercase tracking-wider transition-all text-slate-500 hover:text-slate-800 hover:bg-slate-100 outline-none";
                
                // Hide sueldo mobile bar and trigger calculations for finiquito
                document.getElementById('mobile-result-bar').classList.add('translate-y-full');
                if (typeof updateCalculations === 'function') updateCalculations();
            } else {
                containerFiniquito.classList.add('hidden');
                containerSueldo.classList.remove('hidden');
                btnSueldo.className = "flex-1 py-3.5 px-6 rounded-xl text-xs font-bold uppercase tracking-wider transition-all text-white bg-sky-500 shadow-md shadow-sky-500/20 outline-none";
                btnFiniquito.className = "flex-1 py-3.5 px-6 rounded-xl text-xs font-bold uppercase tracking-wider transition-all text-slate-500 hover:text-slate-800 hover:bg-slate-100 outline-none";
                
                // Trigger sueldo calculations
                const salaryInput = document.getElementById('salary');
                if (salaryInput) salaryInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
        
        // Tab routing support
        document.addEventListener('DOMContentLoaded', () => {
            const hash = window.location.hash || '';
            const path = window.location.pathname || '';
            
            if (hash === '#sueldo' || path.includes('sueldo_liquido')) {
                switchCalculatorTab('sueldo');
            } else {
                switchCalculatorTab('finiquito');
            }
        });
    </script>
"""

# Generate index.html
print("Generating: index.html...")
canonical_url, og_tags, json_ld = generate_seo_tags("index.html", "Cálculo Laboral Chile 2026 | Finiquito y Sueldo Líquido", "Calcula gratis tu sueldo líquido y finiquito en Chile. Herramientas oficiales actualizadas a 2026 con las leyes de la Dirección del Trabajo. Sin registro.", page_type="website")
index_html_out = HTML_LAYOUT.format(
    title="Cálculo Laboral Chile 2026 | Finiquito y Sueldo Líquido",
    description="Calcula gratis tu sueldo líquido y finiquito en Chile. Herramientas oficiales actualizadas a 2026 con las leyes de la Dirección del Trabajo. Sin registro.",
    canonical_url=canonical_url,
    og_tags=og_tags,
    json_ld=json_ld,
    custom_head="",
    header=HEADER_HTML,
    indicator_bar=INDICATOR_BAR_HTML,
    content=INDEX_CONTENT,
    footer=FOOTER_HTML,
    history_modal=HISTORY_MODAL_HTML,
    custom_scripts=INDEX_SCRIPTS
)
with open(os.path.join(DEST_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html_out)

# Generate sueldo_liquido.html (Redirects tab on load)
print("Generating: sueldo_liquido.html...")
canonical_url, og_tags, json_ld = generate_seo_tags("sueldo_liquido.html", "Calculadora de Sueldo Líquido Chile 2026 | Pasar de Bruto a Neto Exacto", "Pasa tu sueldo bruto a líquido exacto. Incluye descuentos vigentes de AFP, Salud (Fonasa/Isapre) e Impuestos. Herramienta 100% gratis.", page_type="website")
sueldo_html_out = HTML_LAYOUT.format(
    title="Calculadora de Sueldo Líquido Chile 2026 | Pasar de Bruto a Neto Exacto",
    description="Pasa tu sueldo bruto a líquido exacto. Incluye descuentos vigentes de AFP, Salud (Fonasa/Isapre) e Impuestos. Herramienta 100% gratis.",
    canonical_url=canonical_url,
    og_tags=og_tags,
    json_ld=json_ld,
    custom_head="",
    header=HEADER_HTML,
    indicator_bar=INDICATOR_BAR_HTML,
    content=INDEX_CONTENT,
    footer=FOOTER_HTML,
    history_modal=HISTORY_MODAL_HTML,
    custom_scripts=INDEX_SCRIPTS + """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            switchCalculatorTab('sueldo');
        });
    </script>
    """
)
with open(os.path.join(DEST_DIR, "sueldo_liquido.html"), "w", encoding="utf-8") as f:
    f.write(sueldo_html_out)

# Generate finiquito_calculator.html (Redirects tab on load)
print("Generating: finiquito_calculator.html...")
canonical_url, og_tags, json_ld = generate_seo_tags("finiquito_calculator.html", "Calculadora de Finiquito Chile 2026 (Formato Oficial) | Simulador Exacto", "Calcula tu finiquito online en segundos con el formato oficial de la DT. Incluye indemnización por años de servicio, vacaciones y aviso previo.", page_type="website")
finiquito_html_out = HTML_LAYOUT.format(
    title="Calculadora de Finiquito Chile 2026 (Formato Oficial) | Simulador Exacto",
    description="Calcula tu finiquito online en segundos con el formato oficial de la DT. Incluye indemnización por años de servicio, vacaciones y aviso previo.",
    canonical_url=canonical_url,
    og_tags=og_tags,
    json_ld=json_ld,
    custom_head="",
    header=HEADER_HTML,
    indicator_bar=INDICATOR_BAR_HTML,
    content=INDEX_CONTENT,
    footer=FOOTER_HTML,
    history_modal=HISTORY_MODAL_HTML,
    custom_scripts=INDEX_SCRIPTS + """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            switchCalculatorTab('finiquito');
        });
    </script>
    """
)
with open(os.path.join(DEST_DIR, "finiquito_calculator.html"), "w", encoding="utf-8") as f:
    f.write(finiquito_html_out)

# Generate vercel.json in DEST_DIR and in root directory
print("Generating: vercel.json...")
vercel_json_content = """{
  "redirects": [
    { "source": "/finiquito_calculator", "destination": "/finiquito_calculator.html", "permanent": true },
    { "source": "/sueldo_liquido", "destination": "/sueldo_liquido.html", "permanent": true },
    { "source": "/guia-vacaciones-proporcionales", "destination": "/guia-vacaciones-proporcionales.html", "permanent": true },
    { "source": "/como-calcular-finiquito-chile", "destination": "/como-calcular-finiquito-chile.html", "permanent": true },
    { "source": "/como-calcular-sueldo-liquido-paso-a-paso", "destination": "/como-calcular-sueldo-liquido-paso-a-paso.html", "permanent": true },
    { "source": "/como-leer-liquidacion-de-sueldo", "destination": "/como-leer-liquidacion-de-sueldo.html", "permanent": true },
    { "source": "/despido-necesidades-empresa-articulo-161", "destination": "/despido-necesidades-empresa-articulo-161.html", "permanent": true },
    { "source": "/ley-40-horas-chile-2026", "destination": "/ley-40-horas-chile-2026.html", "permanent": true },
    { "source": "/que-hacer-si-no-te-pagan-el-finiquito", "destination": "/que-hacer-si-no-te-pagan-el-finiquito.html", "permanent": true },
    { "source": "/seguro-de-cesantia-chile-como-cobrar", "destination": "/seguro-de-cesantia-chile-como-cobrar.html", "permanent": true },
    { "source": "/reclamar-despido-injustificado-chile", "destination": "/reclamar-despido-injustificado-chile.html", "permanent": true },
    { "source": "/contacto", "destination": "/contacto.html", "permanent": true },
    { "source": "/blog", "destination": "/blog.html", "permanent": true },
    { "source": "/privacidad", "destination": "/privacidad.html", "permanent": true },
    { "source": "/terminos", "destination": "/terminos.html", "permanent": true },
    { "source": "/disclaimer", "destination": "/disclaimer.html", "permanent": true },
    { "source": "/sobre-nosotros", "destination": "/sobre-nosotros.html", "permanent": true }
  ]
}"""

with open(os.path.join(DEST_DIR, "vercel.json"), "w", encoding="utf-8") as f:
    f.write(vercel_json_content)

with open(os.path.join(os.path.dirname(DEST_DIR), "vercel.json"), "w", encoding="utf-8") as f:
    f.write(vercel_json_content)

print("Redesign complete! All 17 HTML files have been beautifully generated under calculolaboral-v2.")
