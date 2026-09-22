# -*- coding: utf-8 -*-
"""Финальная сборка под домен.

Запуск:  python deploy.py atlant-obmen.com

Что делает:
  1. прописывает абсолютные адреса в og:image, og:url и canonical;
  2. создаёт robots.txt и sitemap.xml;
  3. собирает папку dist и архив atlant-site.zip для загрузки на хостинг.
"""
import io, os, re, shutil, sys
from datetime import date

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
PAGES = ['index.html', 'obmen-rub-uah.html', 'perestanovka-nalichnyh.html', '404.html']
ASSETS = ['styles.css', 'favicon.ico', '.htaccess', 'robots.txt', 'sitemap.xml']

domain = (sys.argv[1] if len(sys.argv) > 1 else '').strip().lower()
domain = re.sub(r'^https?://', '', domain).strip('/')
if not domain:
    sys.exit('Укажите домен:  python deploy.py ваш-домен.ru')
site = 'https://' + domain

# ---------- 1. абсолютные адреса в мета-тегах ----------
for name in PAGES:
    path = os.path.join(BASE, name)
    s = io.open(path, encoding='utf-8').read()
    s = re.sub(r'<meta property="og:image" content="[^"]*">',
               '<meta property="og:image" content="%s/img/og-cover.jpg">' % site, s)
    s = re.sub(r'\s*<meta property="og:url" content="[^"]*">', '', s)
    s = re.sub(r'\s*<link rel="canonical" href="[^"]*">', '', s)
    page_url = site + '/' + ('' if name == 'index.html' else name)
    if name != '404.html':
        add = ('\n<link rel="canonical" href="%s">'
               '\n<meta property="og:url" content="%s">' % (page_url, page_url))
        s = s.replace('<meta name="theme-color" content="#0c2340">',
                      '<meta name="theme-color" content="#0c2340">' + add)
    io.open(path, 'w', encoding='utf-8').write(s)

# ---------- 2. robots.txt и sitemap.xml ----------
io.open(os.path.join(BASE, 'robots.txt'), 'w', encoding='utf-8').write(
    'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % site)

today = date.today().isoformat()
urls = ''.join(
    '  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <priority>%s</priority>\n  </url>\n'
    % (site + '/' + ('' if n == 'index.html' else n), today, '1.0' if n == 'index.html' else '0.8')
    for n in PAGES if n != '404.html')
io.open(os.path.join(BASE, 'sitemap.xml'), 'w', encoding='utf-8').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)

# ---------- 3. dist + zip ----------
dist = os.path.join(BASE, 'dist')
shutil.rmtree(dist, ignore_errors=True)
os.makedirs(dist)
for name in PAGES + ASSETS:
    src = os.path.join(BASE, name)
    if os.path.exists(src):
        shutil.copy2(src, dist)
shutil.copytree(os.path.join(BASE, 'img'), os.path.join(dist, 'img'))

zip_path = os.path.join(BASE, 'atlant-site')
if os.path.exists(zip_path + '.zip'):
    os.remove(zip_path + '.zip')
shutil.make_archive(zip_path, 'zip', dist)

total = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(dist) for f in fs)
print('домен:      ', site)
print('файлов:     ', sum(len(fs) for _, _, fs in os.walk(dist)))
print('размер:     ', round(total / 1024, 1), 'KB')
print('архив:      ', zip_path + '.zip')
