from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from datetime import datetime

router = APIRouter()

@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    """Правила для поисковых роботов"""
    content = """User-agent: *
Allow: /auth
Allow: /$
Disallow: /profile
Disallow: /admin
Disallow: /api/

Sitemap: https://yourdomain.com/sitemap.xml
"""
    return content

@router.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap():
    """Динамическая карта сайта"""
    # В реальном проекте здесь можно брать маршруты из конфига
    base_url = "https://yourdomain.com"  # заменить на VITE_SITE_URL из env
    urls = [
        {"loc": "/", "changefreq": "weekly", "priority": "0.8"},
        {"loc": "/auth", "changefreq": "monthly", "priority": "0.9"},
    ]
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml += f"""  <url>
    <loc>{base_url}{url["loc"]}</loc>
    <lastmod>{datetime.now().isoformat()}</lastmod>
    <changefreq>{url["changefreq"]}</changefreq>
    <priority>{url["priority"]}</priority>
  </url>\n"""
    
    xml += '</urlset>'
    return xml