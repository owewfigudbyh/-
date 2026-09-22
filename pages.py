# -*- coding: utf-8 -*-
"""Собирает страницы услуг: шапка, подвал и блок контактов берутся из index.html."""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(BASE, 'index.html'), encoding='utf-8').read()


def cut(start, end):
    i = src.index(start)
    j = src.index(end, i) + len(end)
    return src[i:j]


SPRITE = cut('<!-- ============ SVG sprite ============ -->', '</defs>\n</svg>')
HEADER = cut('<!-- ============ HEADER ============ -->', '</header>')
CONTACT = cut('<!-- ============ CONTACT ============ -->', '</section>')
FOOTER = cut('<!-- ============ FOOTER ============ -->', '</footer>')

PAGES = [
    {
        'file': 'obmen-rub-uah.html',
        'title': 'Обмен RUB ⇄ UAH — Атлант Сервис Обмен',
        'desc': 'Обмен российских рублей на украинские гривны и обратно. Условия уточняются индивидуально.',
        'h1': 'Обмен RUB ⇄ UAH',
        'lead': 'Обмен российских рублей на украинские гривны и обратно. Вы сообщаете сумму и направление '
                'обмена, после чего получаете актуальные условия и дальнейшие инструкции.',
        'extra': '',
        'img': 'exchange.webp',
        'alt': 'Монета с символом рубля и монета с флагом Украины',
        'nav': 'obmen-rub-uah.html',
    },
    {
        'file': 'perestanovka-nalichnyh.html',
        'title': 'Перестановка наличных по всему миру — Атлант Сервис Обмен',
        'desc': 'Организация передачи наличных между городами и странами. Направления и условия уточняются индивидуально.',
        'h1': 'Перестановка наличных<br>по всему миру',
        'lead': 'Передача наличных между странами и городами. Вы сообщаете сумму, место отправления и место '
                'получения, а затем получаете информацию по доступности направления и условиям операции.',
        'img': 'map-card.svg',
        'alt': 'Карта направлений переводов',
        'nav': 'perestanovka-nalichnyh.html',
    },
]

TPL = '''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<meta name="theme-color" content="#0c2340">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Атлант Сервис Обмен">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="img/og-cover.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>

{sprite}

{header}

<main class="wrap" id="top">

  <nav class="crumbs">
    <a href="index.html">Главная</a><span>›</span><span>{crumb}</span>
  </nav>

  <!-- ============ ШАПКА СТРАНИЦЫ ============ -->
  <section class="page-head">
    <div>
      <p class="eyebrow">Услуга</p>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="hero-btns">
        <a class="btn btn-pri" href="#contacts">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.4 3.1 2.6 10.6c-.8.3-.8 1.5.1 1.7l4.9 1.4 1.8 5.5c.2.8 1.3 1 1.8.3l2.3-2.7 4.6 3.4c.6.5 1.6.2 1.8-.7l3-14.6c.2-.9-.6-1.7-1.5-1.3z"/></svg>
          Связаться с нами
        </a>
        <a class="btn btn-ghost" href="index.html">На главную <span style="color:#9fb1c5">›</span></a>
      </div>
    </div>

    <div class="page-head-pic">
      <img src="img/{img}" width="1400" height="1032" alt="{alt}" decoding="async">
    </div>
  </section>

  <!-- ============ ТЕКСТ СТРАНИЦЫ ============ -->
  <section class="article">

    <!-- ===== НАЧАЛО КОНТЕНТА: замените блок ниже своим текстом ===== -->

    <div class="placeholder">
      <h2>Здесь будет описание услуги</h2>
      <p>Место под текст: порядок работы, доступные направления, сроки, условия и всё, что важно
      рассказать клиенту. Удалите этот блок и вставьте свои заголовки и абзацы.</p>
    </div>

    <!-- Пример структуры:
      <h2>Заголовок раздела</h2>
      <p>Абзац текста.</p>
      <ul>
        <li>Пункт списка</li>
        <li>Ещё пункт</li>
      </ul>
    -->

    <!-- ===== КОНЕЦ КОНТЕНТА ===== -->

  </section>
{extra}
{contact}
</main>

{footer}

</body>
</html>
'''

PAGES[1]['extra'] = ''

for p in PAGES:
    header = HEADER.replace('<a class="on" href="index.html">', '<a href="index.html">')
    header = header.replace('<a href="%s">' % p['nav'], '<a class="on" href="%s">' % p['nav'])
    contact = CONTACT.replace('<!-- ============ CONTACT ============ -->',
                              '<!-- ============ КОНТАКТЫ ============ -->')
    html = TPL.format(title=p['title'], desc=p['desc'], sprite=SPRITE, header=header,
                      crumb=p['h1'].replace('<br>', ' '), h1=p['h1'], lead=p['lead'],
                      img=p['img'], alt=p['alt'], extra=p.get('extra', ''), contact=contact, footer=FOOTER)
    out = os.path.join(BASE, p['file'])
    io.open(out, 'w', encoding='utf-8').write(html)
    print(p['file'], round(os.path.getsize(out) / 1024, 1), 'KB')


# ---------- страница 404 ----------
NOT_FOUND = '''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Страница не найдена — Атлант Сервис Обмен</title>
<meta name="robots" content="noindex">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<meta name="theme-color" content="#0c2340">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>

{sprite}

{header}

<main class="wrap" id="top">
  <section class="page-head" style="grid-template-columns:1fr">
    <div>
      <p class="eyebrow">Ошибка 404</p>
      <h1>Такой страницы нет</h1>
      <p class="lead">Возможно, адрес набран с опечаткой или страница была удалена.
      Вернитесь на главную или напишите нам — подскажем, где искать.</p>
      <div class="hero-btns">
        <a class="btn btn-pri" href="index.html">На главную</a>
        <a class="btn btn-ghost" href="index.html#contacts">Связаться <span style="color:#9fb1c5">&#8250;</span></a>
      </div>
    </div>
  </section>
{extra}
{contact}
</main>

{footer}

</body>
</html>
'''

NOT_FOUND = NOT_FOUND.replace('{extra}', '')
nf = NOT_FOUND.replace('{sprite}', SPRITE).replace('{header}', HEADER.replace('<a class="on" href="index.html">', '<a href="index.html">'))
nf = nf.replace('{contact}', CONTACT).replace('{footer}', FOOTER)
io.open(os.path.join(BASE, '404.html'), 'w', encoding='utf-8').write(nf)
print('404.html', round(os.path.getsize(os.path.join(BASE, '404.html')) / 1024, 1), 'KB')
