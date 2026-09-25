"""خروجی استاتیک سایت برای GitHub Pages.

اجرا:  python freeze.py
خروجی: index.html / about.html / portfolio.html / contact.html در ریشه ریپو
"""
import re
from app import app

STATIC_FORM = """<div class="form reveal in">
  <p>📧 برای تماس مستقیم ایمیل بزن:</p>
  <a class="btn primary" href="mailto:nikanazimi1393@gmail.com">✉️ nikanazimi1393@gmail.com</a>
  <p style="margin-top:10px"><a href="https://github.com/nikanazimi1393-design">🔗 گیت‌هاب من</a></p>
</div>"""

ROUTES = {
    "/": "index.html",
    "/about": "about.html",
    "/portfolio": "portfolio.html",
    "/contact": "contact.html",
}

client = app.test_client()
for route, fname in ROUTES.items():
    html = client.get(route).data.decode("utf-8")
    # مسیرهای فلاسک -> مسیر نسبی استاتیک
    html = html.replace('href="/static/', 'href="static/')
    html = html.replace('src="/static/', 'src="static/')
    html = html.replace('href="/"', 'href="index.html"')
    html = html.replace('href="/about"', 'href="about.html"')
    html = html.replace('href="/portfolio"', 'href="portfolio.html"')
    html = html.replace('href="/contact"', 'href="contact.html"')
    html = html.replace('href="/messages"', 'href="https://github.com/nikanazimi1393-design/rozume"')
    if fname == "contact.html":
        html = re.sub(r"<form.*?</form>", STATIC_FORM, html, flags=re.DOTALL)
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname)
