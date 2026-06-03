#!/usr/bin/env python3
"""
Rebuild all calculolaboral content pages with the new light theme design.
Extracts core content from old pages and wraps them in the new consistent design.
"""
import re, sys
from pathlib import Path

REPO = Path("/opt/data/repos/calculolaboral")

# ─── Shared page template ───────────────────────────────────────────
PAGE_START = '''<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="application-version" content="2.0.0">
    <meta name="description" content="{meta_desc}">
    <title>{title}</title>
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="es-CL" href="{canonical}">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:locale" content="es_CL">
    <meta property="og:site_name" content="Cálculo Laboral">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{ sans: ['Inter', 'system-ui', 'sans-serif'] }},
                    colors: {{ blue: {{ DEFAULT: '#0ea5e9', dark: '#0284c7', light: '#e0f2fe' }} }}
                }}
            }}
        }}
    </script>
    <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased">

<header class="sticky top-0 z-50 bg-white border-b border-slate-200">
    <div class="max-w-5xl mx-auto px-4 md:px-6 h-14 flex items-center justify-between">
        <a href="/" class="flex items-center gap-2.5 no-underline flex-shrink-0">
            <div class="w-8 h-8 bg-sky-500 rounded-lg flex items-center justify-center text-white font-bold text-sm">CL</div>
            <span class="text-[15px] font-semibold text-slate-900">Cálculo<span class="text-sky-500">Laboral</span>.cl</span>
        </a>
        <nav class="hidden md:flex items-center gap-1">
            <a href="/" class="px-3 py-2 text-[13px] font-medium text-slate-500 hover:text-sky-600 rounded-md">Calculadoras</a>
            <div class="relative group">
                <span class="px-3 py-2 text-[13px] font-medium text-slate-500 hover:text-slate-700 rounded-md cursor-pointer">Guías ▾</span>
                <div class="absolute top-full right-0 mt-1 w-64 bg-white border border-slate-200 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-150 z-50">
                    <a href="/como-calcular-finiquito-chile.html" class="block px-4 py-2.5 text-[13px] text-slate-600 hover:bg-slate-50 hover:text-sky-600 rounded-t-lg">📋 Cómo calcular tu finiquito</a>
                    <a href="/como-calcular-sueldo-liquido-paso-a-paso.html" class="block px-4 py-2.5 text-[13px] text-slate-600 hover:bg-slate-50 hover:text-sky-600">💼 Cómo calcular sueldo líquido</a>
                    <a href="/despido-necesidades-empresa-articulo-161.html" class="block px-4 py-2.5 text-[13px] text-slate-600 hover:bg-slate-50 hover:text-sky-600">⚖️ Despido Art. 161</a>
                    <a href="/ley-40-horas-chile-2026.html" class="block px-4 py-2.5 text-[13px] text-slate-600 hover:bg-slate-50 hover:text-sky-600">🕐 Ley 40 Horas</a>
                    <a href="/guia-vacaciones-proporcionales.html" class="block px-4 py-2.5 text-[13px] text-slate-600 hover:bg-slate-50 hover:text-sky-600">🏖️ Vacaciones proporcionales</a>
                    <a href="/seguro-de-cesantia-chile-como-cobrar.html" class="block px-4 py-2.5 text-[13px] text-slate-600 hover:bg-slate-50 hover:text-sky-600">🛡️ Seguro de Cesantía</a>
                    <a href="/que-hacer-si-no-te-pagan-el-finiquito.html" class="block px-4 py-2.5 text-[13px] text-slate-600 hover:bg-slate-50 hover:text-sky-600 rounded-b-lg">❗ No te pagaron el finiquito</a>
                </div>
            </div>
            <a href="/blog.html" class="px-3 py-2 text-[13px] font-medium text-slate-500 hover:text-slate-700 rounded-md">Blog</a>
            <a href="/contacto.html" class="px-3 py-2 text-[13px] font-medium text-slate-500 hover:text-slate-700 rounded-md">Contacto</a>
        </nav>
    </div>
</header>

<main class="max-w-3xl mx-auto px-4 md:px-6 py-8 md:py-10 pb-16">

    <!-- Article Header -->
    <div class="mb-8">
        <h1 class="text-2xl md:text-3xl font-extrabold text-slate-900 leading-tight mb-4">{h1}</h1>
    </div>

    <!-- Article Content -->
    <article class="prose-custom">
'''

PAGE_END = '''
    </article>

</main>

<!-- Related Guides -->
<section class="max-w-5xl mx-auto px-4 md:px-6 pb-10">
    <h2 class="text-lg font-extrabold text-slate-900 mb-4">📖 Guías Relacionadas</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <a href="/como-calcular-finiquito-chile.html" class="bg-white border border-slate-200 rounded-[10px] p-4 hover:border-sky-300 hover:shadow-sm transition-all duration-150 no-underline group">
            <span class="text-lg">📋</span>
            <h3 class="text-sm font-semibold text-slate-800 mt-2 group-hover:text-sky-600">Cómo calcular tu finiquito en Chile (2026)</h3>
            <p class="text-[12px] text-slate-400 mt-1">Guía paso a paso con ejemplos reales según el Código del Trabajo.</p>
        </a>
        <a href="/como-calcular-sueldo-liquido-paso-a-paso.html" class="bg-white border border-slate-200 rounded-[10px] p-4 hover:border-sky-300 hover:shadow-sm transition-all duration-150 no-underline group">
            <span class="text-lg">💼</span>
            <h3 class="text-sm font-semibold text-slate-800 mt-2 group-hover:text-sky-600">Cómo calcular el sueldo líquido paso a paso</h3>
            <p class="text-[12px] text-slate-400 mt-1">AFP, salud, impuesto único y todas las deducciones explicadas.</p>
        </a>
        <a href="/despido-necesidades-empresa-articulo-161.html" class="bg-white border border-slate-200 rounded-[10px] p-4 hover:border-sky-300 hover:shadow-sm transition-all duration-150 no-underline group">
            <span class="text-lg">⚖️</span>
            <h3 class="text-sm font-semibold text-slate-800 mt-2 group-hover:text-sky-600">Despido por necesidades de la empresa (Art. 161)</h3>
            <p class="text-[12px] text-slate-400 mt-1">Cuándo aplica, cuánto te corresponde y cómo reclamar.</p>
        </a>
        <a href="/ley-40-horas-chile-2026.html" class="bg-white border border-slate-200 rounded-[10px] p-4 hover:border-sky-300 hover:shadow-sm transition-all duration-150 no-underline group">
            <span class="text-lg">🕐</span>
            <h3 class="text-sm font-semibold text-slate-800 mt-2 group-hover:text-sky-600">Ley de 40 Horas en Chile (2026)</h3>
            <p class="text-[12px] text-slate-400 mt-1">Todo lo que necesitas saber sobre la reducción de jornada laboral.</p>
        </a>
    </div>
</section>

<footer class="border-t border-slate-200 mt-14">
    <div class="max-w-5xl mx-auto px-4 md:px-6 py-10">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
                <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Calculadoras</span>
                <div class="mt-3 space-y-2">
                    <a href="/" class="block text-[13px] text-slate-500 hover:text-sky-600">Finiquito</a>
                    <a href="/" class="block text-[13px] text-slate-500 hover:text-sky-600">Sueldo Líquido</a>
                </div>
            </div>
            <div>
                <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Guías</span>
                <div class="mt-3 space-y-2">
                    <a href="/como-calcular-finiquito-chile.html" class="block text-[13px] text-slate-500 hover:text-sky-600">Calcular Finiquito</a>
                    <a href="/como-calcular-sueldo-liquido-paso-a-paso.html" class="block text-[13px] text-slate-500 hover:text-sky-600">Sueldo Líquido</a>
                    <a href="/despido-necesidades-empresa-articulo-161.html" class="block text-[13px] text-slate-500 hover:text-sky-600">Despido Art. 161</a>
                    <a href="/guia-vacaciones-proporcionales.html" class="block text-[13px] text-slate-500 hover:text-sky-600">Vacaciones</a>
                </div>
            </div>
            <div>
                <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Legal</span>
                <div class="mt-3 space-y-2">
                    <a href="/ley-40-horas-chile-2026.html" class="block text-[13px] text-slate-500 hover:text-sky-600">Ley 40 Horas</a>
                    <a href="/seguro-de-cesantia-chile-como-cobrar.html" class="block text-[13px] text-slate-500 hover:text-sky-600">Seguro de Cesantía</a>
                    <a href="/que-hacer-si-no-te-pagan-el-finiquito.html" class="block text-[13px] text-slate-500 hover:text-sky-600">No te pagaron finiquito</a>
                </div>
            </div>
            <div>
                <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Sitio</span>
                <div class="mt-3 space-y-2">
                    <a href="/blog.html" class="block text-[13px] text-slate-500 hover:text-sky-600">Blog</a>
                    <a href="/contacto.html" class="block text-[13px] text-slate-500 hover:text-sky-600">Contacto</a>
                    <a href="/sobre-nosotros.html" class="block text-[13px] text-slate-500 hover:text-sky-600">Sobre Nosotros</a>
                    <a href="/privacidad.html" class="block text-[13px] text-slate-500 hover:text-sky-600">Privacidad</a>
                </div>
            </div>
        </div>
        <div class="border-t border-slate-100 mt-8 pt-6 text-center text-xs text-slate-400">
            <p>© 2026 CalculoLaboral.cl — Información referencial. Consulta siempre con un especialista laboral.</p>
            <p class="mt-1">Valores actualizados a Febrero 2026</p>
        </div>
    </div>
</footer>

<script src="/js/constants.js"></script>
<script src="/js/indicators.js"></script>

</body>
</html>'''

ARTICLE_CSS_START = '''    <style>
        .prose-custom { line-height: 1.75; color: #334155; }
        .prose-custom h2 { font-size: 1.35rem; font-weight: 700; color: #0f172a; margin: 2rem 0 0.75rem; padding-bottom: 0.5rem; border-bottom: 2px solid #e2e8f0; }
        .prose-custom h3 { font-size: 1.1rem; font-weight: 600; color: #1e293b; margin: 1.5rem 0 0.5rem; }
        .prose-custom h4 { font-size: 1rem; font-weight: 600; color: #334155; margin: 1.25rem 0 0.4rem; }
        .prose-custom p { margin-bottom: 1rem; }
        .prose-custom ul, .prose-custom ol { margin: 0.75rem 0; padding-left: 1.5rem; }
        .prose-custom li { margin-bottom: 0.4rem; }
        .prose-custom strong { color: #0f172a; font-weight: 600; }
        .prose-custom a { color: #0ea5e9; text-decoration: underline; text-underline-offset: 2px; }
        .prose-custom a:hover { color: #0284c7; }
        .prose-custom .callout { background: #f0f9ff; border-left: 4px solid #0ea5e9; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 8px 8px 0; }
        .prose-custom .callout-warning { background: #fffbeb; border-left-color: #f59e0b; }
        .prose-custom .callout-danger { background: #fef2f2; border-left-color: #ef4444; }
        .prose-custom .table-wrap { overflow-x: auto; margin: 1.5rem 0; }
        .prose-custom table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
        .prose-custom th { background: #f8fafc; text-align: left; padding: 0.6rem 0.9rem; font-weight: 600; color: #475569; border-bottom: 2px solid #e2e8f0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.03em; }
        .prose-custom td { padding: 0.6rem 0.9rem; border-bottom: 1px solid #f1f5f9; }
        .prose-custom tr:last-child td { border-bottom: none; }
        .prose-custom img { max-width: 100%; border-radius: 8px; margin: 1.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .prose-custom blockquote { border-left: 3px solid #cbd5e1; padding: 0.5rem 1rem; margin: 1.25rem 0; color: #64748b; font-style: italic; }
        .prose-custom .lead { font-size: 1.05rem; color: #475569; margin-bottom: 1.5rem; line-height: 1.7; }
    </style>
'''


def extract_content(html):
    """Extract the main article content from the old page HTML."""
    # Try to find content between specific markers
    # Most pages have content in a specific pattern: after certain markers

    # Remove everything before the main content starts
    # Find the first <h1> or the main article section
    h1_match = re.search(r'<h1[^>]*>.*?</h1>', html, re.DOTALL)

    # Try to find content section: look for patterns like "<!-- Content -->" or after specific classes
    # First, try finding a main/article tag
    main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)

    if article_match:
        content = article_match.group(1)
    elif main_match:
        content = main_match.group(1)
    else:
        # Fallback: take everything after the first meaningful section
        # Find where the real content begins (after nav/header stuff)
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
        if body_match:
            body = body_match.group(1)
            # Try to find the point where content starts
            # Look for the first <h1> or first large text block
            content = body

    if not content:
        return "<p>Contenido no disponible</p>"

    # Clean up: remove script tags, Tailwind CDN references, old CSS
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<link[^>]*tailwind[^>]*>', '', content, flags=re.DOTALL)
    content = re.sub(r'<link[^>]*googleapis[^>]*>', '', content, flags=re.DOTALL)
    content = re.sub(r'<link[^>]*gstatic[^>]*>', '', content, flags=re.DOTALL)
    content = re.sub(r'<link[^>]*fonts\.googleapis[^>]*>', '', content, flags=re.DOTALL)

    # Remove old dark theme indicators
    content = content.replace('text-white', 'text-slate-800')
    content = content.replace('text-slate-200', 'text-slate-600')
    content = content.replace('text-slate-300', 'text-slate-500')
    content = content.replace('bg-[#070a13]', 'bg-slate-50')
    content = content.replace('#F8FAFC', '#0f172a')
    content = content.replace('#94A3B8', '#475569')
    content = content.replace('text-gray-400', 'text-slate-500')
    content = content.replace('text-gray-300', 'text-slate-400')
    content = content.replace('text-gray-200', 'text-slate-300')

    # Remove old header/footer patterns
    content = re.sub(r'<!--\s*HEADER.*?-->(.*?)<!--\s*FIN HEADER.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'<!--\s*FOOTER.*?-->(.*?)<!--\s*FIN FOOTER.*?-->', '', content, flags=re.DOTALL)

    # Remove nav elements from extracted content
    content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
    content = re.sub(r'<header[^>]*>.*?</header>', '', content, flags=re.DOTALL)
    content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL)

    # Remove mobile menu, glass divs, etc.
    content = re.sub(r'class="[^"]*glass[^"]*"[^>]*>.*?</div>', '', content, flags=re.DOTALL)

    # Clean up excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)

    return content.strip()


def extract_meta(html, page_name):
    """Extract title, description, H1 from old page."""
    title_match = re.search(r'<title>(.*?)</title>', html)
    title = title_match.group(1) if title_match else page_name.replace('-', ' ').title()

    desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html)
    meta_desc = desc_match.group(1) if desc_match else ""

    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else title

    return {
        'title': title,
        'meta_desc': meta_desc[:160] if meta_desc else title[:160],
        'og_title': title,
        'h1': h1,
        'canonical': f"https://calculolaboral.cl/{page_name}"
    }


def rebuild_page(page_name):
    """Rebuild a single page with the new design."""
    path = REPO / page_name
    if not path.exists():
        print(f"  SKIP: {page_name} (not found)")
        return False

    html = path.read_text(encoding='utf-8', errors='replace')
    meta = extract_meta(html, page_name)
    content = extract_content(html)

    # Deduplicate: if content already starts with h1, remove it from content
    # since PAGE_START already has the h1
    h1_clean = re.sub(r'<[^>]+>', '', meta['h1']).strip()
    content_h1 = re.search(r'<h1[^>]*>', content)
    if content_h1:
        content = re.sub(r'<h1[^>]*>.*?</h1>\s*', '', content, count=1, flags=re.DOTALL)

    # Build new page
    # Format the template with metadata
    start = PAGE_START.format(**meta)

    new_html = start + ARTICLE_CSS_START + '\n\n' + content + '\n\n' + PAGE_END

    # Write backup
    backup_path = path.with_suffix('.html.bak')
    if not backup_path.exists():
        path.rename(backup_path)

    # Write new page
    path.write_text(new_html, encoding='utf-8')
    print(f"  ✅ {page_name} ({len(new_html)} bytes)")
    return True


# ─── MAIN ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    PAGES = [
        "blog.html",
        "como-calcular-finiquito-chile.html",
        "como-calcular-sueldo-liquido-paso-a-paso.html",
        "como-leer-liquidacion-de-sueldo.html",
        "contacto.html",
        "despido-necesidades-empresa-articulo-161.html",
        "guia-vacaciones-proporcionales.html",
        "ley-40-horas-chile-2026.html",
        "que-hacer-si-no-te-pagan-el-finiquito.html",
        "seguro-de-cesantia-chile-como-cobrar.html",
    ]

    print(f"Rebuilding {len(PAGES)} pages with new design...\n")
    success = 0
    for p in PAGES:
        if rebuild_page(p):
            success += 1

    print(f"\nDone: {success}/{len(PAGES)} pages rebuilt successfully")
    print("Original files backed up as .html.bak")
