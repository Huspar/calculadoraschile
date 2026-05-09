import os
import sys
import json
import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    OrderBy,
    Filter,
    FilterExpression,
)
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'credentials.json'
GA4_PROPERTY_ID = '525092126'
GSC_SITE_URL = 'sc-domain:calculolaboral.cl'

def get_credentials():
    scopes = [
        'https://www.googleapis.com/auth/analytics.readonly',
        'https://www.googleapis.com/auth/webmasters.readonly'
    ]
    return service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=scopes)

# ──────────────────────────────────────
#  SECTION 1: GA4 - Pages (last 28 days)
# ──────────────────────────────────────
def ga4_pages(client):
    print("\n" + "="*80)
    print("  GA4 - RENDIMIENTO POR PÁGINA (últimos 28 días)")
    print("="*80)
    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="newUsers"),
        ],
        date_ranges=[DateRange(start_date="28daysAgo", end_date="yesterday")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=25,
    )
    response = client.run_report(request)

    print(f"{'Página':<45} {'Sesiones':>8} {'Vistas':>8} {'Rebote':>8} {'Duración':>10} {'Nuevos':>8}")
    print("-" * 95)
    for row in response.rows:
        path = row.dimension_values[0].value
        sessions = row.metric_values[0].value
        views = row.metric_values[1].value
        bounce = f"{float(row.metric_values[2].value)*100:.1f}%"
        duration = f"{float(row.metric_values[3].value):.0f}s"
        new_users = row.metric_values[4].value
        print(f"{path:<45} {sessions:>8} {views:>8} {bounce:>8} {duration:>10} {new_users:>8}")

# ──────────────────────────────────────
#  SECTION 2: GA4 - Traffic Sources
# ──────────────────────────────────────
def ga4_sources(client):
    print("\n" + "="*80)
    print("  GA4 - FUENTES DE TRÁFICO (últimos 28 días)")
    print("="*80)
    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=[Dimension(name="sessionSource"), Dimension(name="sessionMedium")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="newUsers"),
            Metric(name="bounceRate"),
        ],
        date_ranges=[DateRange(start_date="28daysAgo", end_date="yesterday")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=15,
    )
    response = client.run_report(request)
    print(f"{'Fuente':<25} {'Medio':<15} {'Sesiones':>10} {'Nuevos':>10} {'Rebote':>10}")
    print("-" * 75)
    for row in response.rows:
        source = row.dimension_values[0].value
        medium = row.dimension_values[1].value
        sessions = row.metric_values[0].value
        new_users = row.metric_values[1].value
        bounce = f"{float(row.metric_values[2].value)*100:.1f}%"
        print(f"{source:<25} {medium:<15} {sessions:>10} {new_users:>10} {bounce:>10}")

# ──────────────────────────────────────
#  SECTION 3: GA4 - Device & Country
# ──────────────────────────────────────
def ga4_devices(client):
    print("\n" + "="*80)
    print("  GA4 - DISPOSITIVOS (últimos 28 días)")
    print("="*80)
    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=[Dimension(name="deviceCategory")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
        ],
        date_ranges=[DateRange(start_date="28daysAgo", end_date="yesterday")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
    )
    response = client.run_report(request)
    print(f"{'Dispositivo':<20} {'Sesiones':>10} {'Rebote':>10} {'Duración':>10}")
    print("-" * 55)
    for row in response.rows:
        print(f"{row.dimension_values[0].value:<20} {row.metric_values[0].value:>10} {float(row.metric_values[1].value)*100:.1f}%{'':<3} {float(row.metric_values[2].value):.0f}s")

def ga4_countries(client):
    print("\n" + "="*80)
    print("  GA4 - PAÍSES TOP (últimos 28 días)")
    print("="*80)
    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=[Dimension(name="country")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="newUsers"),
        ],
        date_ranges=[DateRange(start_date="28daysAgo", end_date="yesterday")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=10,
    )
    response = client.run_report(request)
    print(f"{'País':<25} {'Sesiones':>10} {'Nuevos':>10}")
    print("-" * 48)
    for row in response.rows:
        print(f"{row.dimension_values[0].value:<25} {row.metric_values[0].value:>10} {row.metric_values[1].value:>10}")

# ──────────────────────────────────────
#  SECTION 4: GA4 - Total Summary
# ──────────────────────────────────────
def ga4_totals(client):
    print("\n" + "="*80)
    print("  GA4 - RESUMEN GENERAL (últimos 28 días vs 28 días anteriores)")
    print("="*80)
    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        metrics=[
            Metric(name="sessions"),
            Metric(name="totalUsers"),
            Metric(name="newUsers"),
            Metric(name="screenPageViews"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="sessionsPerUser"),
        ],
        date_ranges=[
            DateRange(start_date="28daysAgo", end_date="yesterday"),
            DateRange(start_date="56daysAgo", end_date="29daysAgo"),
        ],
    )
    response = client.run_report(request)
    metric_names = ["Sesiones", "Usuarios Totales", "Usuarios Nuevos", "Vistas de Página", "Tasa de Rebote", "Duración Prom.", "Sesiones/Usuario"]
    
    print(f"{'Métrica':<25} {'Actual':>12} {'Anterior':>12} {'Cambio':>12}")
    print("-" * 65)
    for i, row in enumerate(response.rows):
        for j, name in enumerate(metric_names):
            curr = float(row.metric_values[j].value) if row == response.rows[0] else 0
            prev_row = response.rows[1] if len(response.rows) > 1 else None
            if row == response.rows[0]:
                curr_val = float(row.metric_values[j].value)
                prev_val = float(prev_row.metric_values[j].value) if prev_row else 0
                
                if j == 4:  # bounce rate
                    curr_str = f"{curr_val*100:.1f}%"
                    prev_str = f"{prev_val*100:.1f}%"
                    change = (curr_val - prev_val) * 100
                    change_str = f"{change:+.1f}pp"
                elif j == 5:  # duration
                    curr_str = f"{curr_val:.0f}s"
                    prev_str = f"{prev_val:.0f}s"
                    change = ((curr_val - prev_val) / prev_val * 100) if prev_val else 0
                    change_str = f"{change:+.1f}%"
                elif j == 6:  # sessions per user
                    curr_str = f"{curr_val:.2f}"
                    prev_str = f"{prev_val:.2f}"
                    change = ((curr_val - prev_val) / prev_val * 100) if prev_val else 0
                    change_str = f"{change:+.1f}%"
                else:
                    curr_str = f"{int(curr_val)}"
                    prev_str = f"{int(prev_val)}"
                    change = ((curr_val - prev_val) / prev_val * 100) if prev_val else 0
                    change_str = f"{change:+.1f}%"
                
                print(f"{name:<25} {curr_str:>12} {prev_str:>12} {change_str:>12}")
        break  # only process first row (current period)

# ──────────────────────────────────────
#  SECTION 5: GSC - Top Queries
# ──────────────────────────────────────
def gsc_queries(service):
    print("\n" + "="*80)
    print("  GSC - TOP CONSULTAS DE BÚSQUEDA (últimos 28 días)")
    print("="*80)
    end_date = datetime.date.today() - datetime.timedelta(days=2)
    start_date = end_date - datetime.timedelta(days=28)
    
    req = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'dimensions': ['query'],
        'rowLimit': 25,
        'aggregationType': 'auto'
    }
    
    response = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=req).execute()
    rows = response.get('rows', [])
    
    print(f"{'Consulta':<50} {'Clicks':>8} {'Impr.':>8} {'CTR':>8} {'Pos.':>8}")
    print("-" * 86)
    total_clicks = 0
    total_impressions = 0
    for row in rows:
        query = row['keys'][0]
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0)
        pos = row.get('position', 0)
        total_clicks += clicks
        total_impressions += impressions
        print(f"{query:<50} {clicks:>8} {impressions:>8} {ctr*100:>7.2f}% {pos:>7.1f}")
    
    print("-" * 86)
    total_ctr = (total_clicks / total_impressions * 100) if total_impressions else 0
    print(f"{'TOTAL':<50} {total_clicks:>8} {total_impressions:>8} {total_ctr:>7.2f}%")

# ──────────────────────────────────────
#  SECTION 6: GSC - Top Pages
# ──────────────────────────────────────
def gsc_pages(service):
    print("\n" + "="*80)
    print("  GSC - TOP PÁGINAS EN BÚSQUEDA (últimos 28 días)")
    print("="*80)
    end_date = datetime.date.today() - datetime.timedelta(days=2)
    start_date = end_date - datetime.timedelta(days=28)
    
    req = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'dimensions': ['page'],
        'rowLimit': 20
    }
    
    response = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=req).execute()
    rows = response.get('rows', [])
    
    print(f"{'Página':<55} {'Clicks':>8} {'Impr.':>8} {'CTR':>8} {'Pos.':>8}")
    print("-" * 91)
    for row in rows:
        page = row['keys'][0].replace('https://calculolaboral.cl', '')
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0)
        pos = row.get('position', 0)
        print(f"{page:<55} {clicks:>8} {impressions:>8} {ctr*100:>7.2f}% {pos:>7.1f}")

# ──────────────────────────────────────
#  SECTION 7: GSC - Pages + Queries combo
# ──────────────────────────────────────
def gsc_page_query(service):
    print("\n" + "="*80)
    print("  GSC - CONSULTAS POR PÁGINA (Top 30)")
    print("="*80)
    end_date = datetime.date.today() - datetime.timedelta(days=2)
    start_date = end_date - datetime.timedelta(days=28)
    
    req = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'dimensions': ['page', 'query'],
        'rowLimit': 30
    }
    
    response = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=req).execute()
    rows = response.get('rows', [])
    
    print(f"{'Página':<35} {'Consulta':<35} {'Clicks':>7} {'Impr.':>7} {'CTR':>7} {'Pos.':>6}")
    print("-" * 100)
    for row in rows:
        page = row['keys'][0].replace('https://calculolaboral.cl', '')[:34]
        query = row['keys'][1][:34]
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0)
        pos = row.get('position', 0)
        print(f"{page:<35} {query:<35} {clicks:>7} {impressions:>7} {ctr*100:>6.2f}% {pos:>5.1f}")

# ──────────────────────────────────────
#  SECTION 8: GSC - Device breakdown
# ──────────────────────────────────────
def gsc_devices(service):
    print("\n" + "="*80)
    print("  GSC - RENDIMIENTO POR DISPOSITIVO (últimos 28 días)")
    print("="*80)
    end_date = datetime.date.today() - datetime.timedelta(days=2)
    start_date = end_date - datetime.timedelta(days=28)
    
    req = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'dimensions': ['device'],
        'rowLimit': 5
    }
    
    response = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=req).execute()
    rows = response.get('rows', [])
    
    print(f"{'Dispositivo':<20} {'Clicks':>10} {'Impr.':>10} {'CTR':>10} {'Pos.':>10}")
    print("-" * 65)
    for row in rows:
        device = row['keys'][0]
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0)
        pos = row.get('position', 0)
        print(f"{device:<20} {clicks:>10} {impressions:>10} {ctr*100:>9.2f}% {pos:>9.1f}")

# ──────────────────────────────────────
#  SECTION 9: GSC - Country breakdown
# ──────────────────────────────────────
def gsc_countries(service):
    print("\n" + "="*80)
    print("  GSC - RENDIMIENTO POR PAÍS (últimos 28 días)")
    print("="*80)
    end_date = datetime.date.today() - datetime.timedelta(days=2)
    start_date = end_date - datetime.timedelta(days=28)
    
    req = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'dimensions': ['country'],
        'rowLimit': 10
    }
    
    response = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=req).execute()
    rows = response.get('rows', [])
    
    print(f"{'País':<25} {'Clicks':>10} {'Impr.':>10} {'CTR':>10} {'Pos.':>10}")
    print("-" * 68)
    for row in rows:
        country = row['keys'][0]
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0)
        pos = row.get('position', 0)
        print(f"{country:<25} {clicks:>10} {impressions:>10} {ctr*100:>9.2f}% {pos:>9.1f}")

# ──────────────────────────────────────
#  SECTION 10: GSC - URL Inspection
# ──────────────────────────────────────
def gsc_url_inspection(service, credentials):
    print("\n" + "="*80)
    print("  GSC - ESTADO DE INDEXACIÓN DE URLS")
    print("="*80)
    import xml.etree.ElementTree as ET
    
    sitemap_path = 'sitemap.xml'
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = []
    for url_tag in root.findall('ns:url', namespace):
        loc = url_tag.find('ns:loc', namespace).text
        urls.append(loc)
    
    print(f"Inspeccionando {len(urls)} URLs del sitemap...\n")
    
    url_inspection = service.urlInspection().index()
    
    print(f"{'URL':<55} {'Veredicto':<15} {'Estado':<25} {'Rastreo':<15}")
    print("-" * 110)
    
    for url in urls:
        try:
            request = {
                'inspectionUrl': url,
                'siteUrl': GSC_SITE_URL,
                'languageCode': 'es-CL'
            }
            response = url_inspection.inspect(body=request).execute()
            result = response.get('inspectionResult', {})
            index_status = result.get('indexStatusResult', {})
            verdict = index_status.get('verdict', 'UNKNOWN')
            coverage = index_status.get('coverageState', 'UNKNOWN')
            crawled = index_status.get('lastCrawlTime', 'Never')[:10] if index_status.get('lastCrawlTime') else 'Never'
            
            short_url = url.replace('https://calculolaboral.cl', '')
            if not short_url:
                short_url = '/'
            print(f"{short_url:<55} {verdict:<15} {coverage:<25} {crawled:<15}")
        except Exception as e:
            short_url = url.replace('https://calculolaboral.cl', '')
            print(f"{short_url:<55} ERROR: {str(e)[:50]}")

# ──────────────────────────────────────
#  MAIN
# ──────────────────────────────────────
if __name__ == '__main__':
    creds = get_credentials()
    
    # GA4 reports
    ga4_client = BetaAnalyticsDataClient(credentials=creds)
    
    try:
        ga4_totals(ga4_client)
    except Exception as e:
        print(f"Error GA4 totals: {e}")
    
    try:
        ga4_pages(ga4_client)
    except Exception as e:
        print(f"Error GA4 pages: {e}")
    
    try:
        ga4_sources(ga4_client)
    except Exception as e:
        print(f"Error GA4 sources: {e}")
    
    try:
        ga4_devices(ga4_client)
    except Exception as e:
        print(f"Error GA4 devices: {e}")
    
    try:
        ga4_countries(ga4_client)
    except Exception as e:
        print(f"Error GA4 countries: {e}")
    
    # GSC reports
    gsc_service = build('searchconsole', 'v1', credentials=creds)
    
    try:
        gsc_queries(gsc_service)
    except Exception as e:
        print(f"Error GSC queries: {e}")
    
    try:
        gsc_pages(gsc_service)
    except Exception as e:
        print(f"Error GSC pages: {e}")
    
    try:
        gsc_page_query(gsc_service)
    except Exception as e:
        print(f"Error GSC page_query: {e}")
    
    try:
        gsc_devices(gsc_service)
    except Exception as e:
        print(f"Error GSC devices: {e}")
    
    try:
        gsc_countries(gsc_service)
    except Exception as e:
        print(f"Error GSC countries: {e}")
    
    try:
        gsc_url_inspection(gsc_service, creds)
    except Exception as e:
        print(f"Error GSC URL inspection: {e}")
    
    print("\n" + "="*80)
    print("  AUDITORÍA COMPLETADA")
    print("="*80)
