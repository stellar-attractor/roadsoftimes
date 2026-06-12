#!/usr/bin/env python3
"""
Строим roadsoftimes.xml из GameTown XML (хирургическая замена).
Все Blogger-виджеты берутся из GameTown как есть — только CSS,
заголовок сайта, слайдер, шаблон карточки и футер заменяются.
"""
import re, subprocess

SRC  = "GameTown Blogger Template/GameTown Blogger Template.xml"
DEST = "template/roadsoftimes.xml"

# ════════════════════════════════════════════════════════════════════
# ФОТО — Blogger CDN URLs (обновлять здесь при замене картинок)
# ════════════════════════════════════════════════════════════════════
IMG_PANZER    = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjbsy8z3wff5_j9tPETK3zwahsqLASMPsKRbryw2-8OoaPkETCWeb4j5M3-5BX9yCBjAeMtiwUnflD4AFTVgzrsceThG-2AZXt6YMd1hq7PzAPmf6NIlLsgieCrMW0HOMVMnIjxGfAbUR00v2hkKL34aKDS6ffdgIvXZPLiHTlID3xC1TCcdrtFy-6OhBQ/s2304/IMG_20260601_104857761_HDR.jpg"
IMG_PEENEMUENDE = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiwR9h5lwJJTESgPqxEIafbK_sg8rm5TV20-MtcGM_M-3daAmdC1IN9T9mfvWePo8BXWb4kVWrrN61Bs4AqFqXSoQ84u4TsXh-xaJe4oGzNvkish7V0Lu4vLyp9-Y5vkwZhKwBGN5PocQlPs9XpxmeAR5kil6Z9cQRoXWsiQSGx4_W_Eepyuu6RifYphBw/s2304/IMG_20260515_125042651%20(1).jpg"
IMG_MARINE     = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhspFLh3AHnHE4HlQQuwTeziyodYv-0LEZ8t3_JuR4SdrmU2wewzA2XsrO9VcZ7Y1k4sbjbXVyI8fIYbacVLftPIVfa_xYKeS9ayJ1nUNWKrm4JWzOhHSvMRa6_w2R2ChAbF3gI45ZA8sKyrUUd-gZ1GCwGstZvMoAEmOWL0r9NouuGw8SkYIe6niehzDs/s2304/IMG_20260604_113633685.jpg"
# Слайд 1 = Панцер; он же используется в блоке "Рекомендуемый музей"
IMG_MARINE2   = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjEl3grJ3JUlUFHB2TcpSimiHBVhvjIIccNILr4M3z9Ra3BfPZgwWWOuuU_wuNNeUQ_znWt6vSJY-WqxPUEf8GRviQ6aGHgV_WP21rrv-fvehIGF93uY0D7ARkdugotefIcizwX4rcP4AQnoK9_odL_WD-iH_kdmCHRMbOgPyGXttJ8XS5C67bn0Sh3uvI/s2304/IMG_20260604_110416067.jpg"
IMG_LOGO      = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjsQcep8gmOfKRF1NmcGFx0SPlX7hyUdSaAmzCArAvDFvGBImpQEpFi22bU1Tcc8w-SJB5C72eVajNJcCEhu1ERTon2sVV7xbBgpPU0A5JGs30uT_TdCyfAYV_crV0qWJqkVHWjH1_c6uFF4Ji-wH5RBAlM7yrBLVfJJ-EOS54MNeRCkfMPxL88QSqH_Lc/s200/logo-200.png"

IMG_SLIDE1    = IMG_PANZER
IMG_SLIDE2    = IMG_PEENEMUENDE
IMG_SLIDE3    = IMG_MARINE

with open(SRC, encoding="utf-8") as f:
    src = f.read()

# ════════════════════════════════════════════════════════════════════
# 1. GOOGLE FONTS + FAVICON
# ════════════════════════════════════════════════════════════════════
# Blogger не хранит ICO — используем PNG (все современные браузеры поддерживают)
# logo-200.png уже на Blogger CDN, берём размер s64 для иконки
FAVICON_URL = IMG_LOGO.replace('/s200/', '/s64/')

src = src.replace(
    "<link href='http://fonts.googleapis.com/css?family=PT+Sans:400,700' rel='stylesheet' type='text/css'/>\n"
    "<link href='http://fonts.googleapis.com/css?family=Oswald' rel='stylesheet' type='text/css'/>",
    "<link href='https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700"
    "&amp;family=PT+Sans:ital,wght@0,400;0,700;1,400&amp;family=PT+Mono&amp;display=swap'"
    " rel='stylesheet' type='text/css'/>"
)

# ════════════════════════════════════════════════════════════════════
# 2. CSS  (полностью заменяем <b:skin>)
# ════════════════════════════════════════════════════════════════════
NEW_CSS = """\
/* ДОРОГИ ВРЕМЁН — Blogger Theme (based on GameTown by Lasantha Bandara) */

/* ── Body layout editor overrides ──────────────────────────────── */
body#layout .rot-header{display:none}
body#layout .rot-hero{display:none}
body#layout .rot-featured-museum{display:none}
body#layout .rot-choose-path{display:none}
body#layout .rot-footer-top{display:none}
body#layout #outer-wrapper{width:auto;background:none}
.widget.Attribution{display:none!important}

/* ── Reset ─────────────────────────────────────────────────────── */
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f0e09;color:#c8c0a8;font-family:'PT Sans',Arial,sans-serif;font-size:14px;line-height:1.6}
a{color:#c9a84c;text-decoration:none}
a:hover{color:#e2c06a}
a img{border:0}
img{max-width:100%;height:auto}

/* ── Hide GameTown original header/nav ─────────────────────────── */
#body-wrapper > #outer-wrapper > #wrap2 > .span-24,
#body-wrapper > #outer-wrapper > #wrap2 > .span-8{display:none}
.menu-secondary-container,.menu-secondary,.menus{display:none!important}
#header-wrapper{display:none!important}
#outer-wrapper{width:100%!important;margin:0!important;padding:0!important;background:none!important;text-align:left}
#wrap2{width:100%}

/* ── HEADER ─────────────────────────────────────────────────────── */
.rot-header{background:#1e1d14;border-bottom:2px solid #8a6f2e;position:sticky;top:0;z-index:1000}
.rot-header-inner{display:flex;align-items:center;height:60px;gap:24px;max-width:1100px;margin:0 auto;padding:0 15px}
.rot-logo{display:flex;align-items:center;gap:10px;text-decoration:none;flex-shrink:0}
.rot-logo-emblem{width:46px;height:46px;border-radius:50%;overflow:hidden;flex-shrink:0;display:block}
.rot-logo-emblem img{width:100%;height:100%;object-fit:cover;display:block}
.rot-logo-title{font-family:'Oswald',sans-serif;font-size:15px;font-weight:600;color:#e2c06a;letter-spacing:1px;text-transform:uppercase;display:block}
.rot-logo-sub{font-size:9px;color:#7a7060;letter-spacing:2px;text-transform:uppercase;font-family:'PT Mono',monospace;display:block}
.rot-nav{flex:1}
.rot-nav ul{display:flex;list-style:none;gap:2px;margin:0;padding:0}
.rot-nav a{display:block;padding:8px 13px;font-family:'Oswald',sans-serif;font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:#c8c0a8;border-bottom:2px solid transparent;transition:color .2s,border-color .2s}
.rot-nav a:hover,.rot-nav-active a{color:#c9a84c;border-bottom-color:#c9a84c}
/* ── FLOATING WIDGETS HOLDER (за экраном, JS переставляет содержимое) ── */
#floating-widgets{position:absolute;left:-9999px;top:-9999px;width:1px;height:1px;overflow:hidden}
/* В Layout-редакторе — показываем нормально, чтобы виджеты были видны */
body#layout #floating-widgets{position:static;left:auto;top:auto;width:auto;height:auto;overflow:visible}
body#layout #toolbar1,body#layout #toolbar1 .section,body#layout #toolbar1 .widget,body#layout #toolbar1 .widget-content{display:block!important;margin:0!important;padding:0!important}
body#layout #newsfeed1{position:static!important;width:auto!important;display:block!important}
body#layout #dropmenu1{position:static!important;left:auto!important;top:auto!important;width:auto!important;height:auto!important;overflow:visible!important}
/* ── HEADER TOOLBAR ─────────────────────────────────────────────── */
#rot-toolbar-target{display:flex;align-items:center;flex-shrink:0}
#toolbar1,#toolbar1 .section,#toolbar1 .widget,#toolbar1 .widget-content{margin:0!important;padding:0!important;background:none!important;border:none!important;display:contents}
#toolbar1 h2.title{display:none!important}
.rot-toolbar{display:flex;align-items:center;gap:4px}
.rot-toolbar a{display:flex;align-items:center;justify-content:center;width:28px;height:28px;opacity:.45;transition:opacity .2s,filter .2s;filter:grayscale(40%)}
.rot-toolbar a:hover{opacity:1;filter:none}
.rot-toolbar a img{width:24px;height:24px;display:block}
/* ── HERO NEWSFEED ──────────────────────────────────────────────── */
#newsfeed1{position:absolute;bottom:0;left:0;right:0;z-index:20;display:block!important}
#newsfeed1 .section,#newsfeed1 .widget,#newsfeed1 .widget-content{margin:0!important;padding:0!important;background:none!important;border:none!important}
#newsfeed1 .rot-newsfeed-scroll{width:340px}
#newsfeed1 h2.title{display:none!important}
.rot-newsfeed{background:transparent;border:none;overflow:hidden;height:120px}
.rot-newsfeed-label{display:none}
.rot-newsfeed-scroll{animation:rotNFScroll 24s linear infinite}
.rot-newsfeed-scroll:hover{animation-play-state:paused}
@keyframes rotNFScroll{0%{transform:translateY(0)}100%{transform:translateY(-50%)}}
.rot-newsfeed-scroll a{display:block;padding:5px 10px;font-family:'PT Mono',monospace;font-size:12px;color:#c8c0a8;text-decoration:none;line-height:1.4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-shadow:0 1px 3px rgba(0,0,0,.8)}
.rot-newsfeed-scroll a:hover{color:#c9a84c}

/* ── HERO SLIDER ─────────────────────────────────────────────────── */
.rot-hero{position:relative;width:100%;height:480px;overflow:hidden;background:#000}
.rot-slides{position:relative;width:100%;height:100%}
.rot-slide{position:absolute;top:0;left:0;right:0;bottom:0;opacity:0;transition:opacity .8s ease}
.rot-slide.active{opacity:1}
.rot-slide img{display:block;width:100%;height:100%;object-fit:cover;object-position:center 40%;filter:brightness(.95)}
.rot-slide::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:linear-gradient(to right,rgba(10,9,5,.92) 0%,rgba(10,9,5,.62) 38%,rgba(10,9,5,.18) 62%,rgba(10,9,5,0) 100%)}
.rot-hero-content{position:absolute;top:50%;left:0;transform:translateY(-50%);width:100%;z-index:10}
.rot-hero-inner{max-width:1100px;margin:0 auto;padding:0 15px 0 75px}
.rot-hero-eyebrow{font-family:'PT Mono',monospace;font-size:13px;letter-spacing:3px;text-transform:uppercase;color:#8a6f2e;margin-bottom:8px}
.rot-hero-title{font-family:'Oswald',sans-serif;font-size:64px;font-weight:700;line-height:1.0;color:#e8e0cc;text-transform:uppercase;letter-spacing:2px;margin-bottom:14px;max-width:580px;text-shadow:0 2px 20px rgba(0,0,0,.8)}
.rot-hero-desc{font-size:18px;color:#c8c0a8;max-width:460px;line-height:1.65;margin-bottom:28px}
.rot-hero-buttons{display:flex;gap:12px;flex-wrap:wrap}
.rot-btn{display:inline-block;padding:10px 22px;font-family:'Oswald',sans-serif;font-size:13px;letter-spacing:1.5px;text-transform:uppercase;border:1px solid;cursor:pointer;transition:all .2s;text-decoration:none}
.rot-btn-primary{background:#c9a84c;border-color:#c9a84c;color:#0f0e09;font-weight:600}
.rot-btn-primary:hover{background:#e2c06a;border-color:#e2c06a;color:#0f0e09}
.rot-btn-outline{background:transparent;border-color:#7a7060;color:#c8c0a8}
.rot-btn-outline:hover{border-color:#8a6f2e;color:#c9a84c}
.rot-hero-geo{position:absolute;bottom:18px;right:20px;z-index:10;font-family:'PT Mono',monospace;font-size:10px;letter-spacing:1px;color:#7a7060;background:rgba(10,9,5,.7);padding:5px 10px;border:1px solid #252418}
.rot-pager{position:absolute;bottom:22px;left:50%;transform:translateX(-50%);z-index:10;display:flex;gap:8px}
.rot-pager span{width:28px;height:3px;background:rgba(201,168,76,.3);cursor:pointer;transition:background .2s;display:inline-block}
.rot-pager span.active{background:#c9a84c}
.rot-arrow{position:absolute;top:50%;transform:translateY(-50%);z-index:10;background:rgba(10,9,5,.6);border:1px solid #3a3520;color:#7a7060;width:40px;height:40px;line-height:40px;text-align:center;cursor:pointer;font-size:20px;transition:all .2s;user-select:none}
.rot-arrow:hover{background:rgba(201,168,76,.15);border-color:#8a6f2e;color:#c9a84c}
.rot-arrow-prev{left:20px}
.rot-arrow-next{right:20px}

/* ── MAIN LAYOUT ─────────────────────────────────────────────────── */
/* content-wrapper — grid-контейнер. Строки и колонки:
   1) .rot-hero        → col 1/-1, row 1 — полная ширина
   2) #main-wrapper    → col 1,    row 2 — посты
   3) #museum-wrapper  → col 1,    row 3 — музей (под постами)
   4) #rsidebar-wrapper→ col 2,    row 2/span 2 — сайдбар (оба ряда)
   5) #crosscol-wrapper→ display:none */
#content-wrapper{max-width:1100px!important;margin:24px auto 0!important;padding:0 15px!important;display:grid!important;grid-template-columns:1fr 300px!important;grid-template-rows:auto auto auto!important;gap:0 24px!important;align-items:start!important;background:none!important}
.rot-hero{grid-column:1/-1!important;grid-row:1!important;margin:0 -15px!important;width:calc(100% + 30px)!important}
#crosscol-wrapper{display:none!important}
#main-wrapper{grid-column:1!important;grid-row:2!important;width:auto!important;float:none!important;min-width:0;padding-top:24px}
#museum-wrapper{grid-column:1!important;grid-row:3!important;width:auto!important;float:none!important;min-width:0;padding-top:0}
#rsidebar-wrapper{grid-column:2!important;grid-row:2/span 2!important;width:auto!important;float:none!important;min-width:0;padding-top:24px}

/* ── VIEW SWITCHER ──────────────────────────────────────────────── */
.rot-view-switcher{display:flex;gap:4px;align-items:center}
.rot-view-btn{background:none;border:1px solid #252418;padding:5px 10px;cursor:pointer;color:#7a7060;font-family:'Oswald',sans-serif;font-size:11px;letter-spacing:1px;text-transform:uppercase;transition:color .2s,border-color .2s;line-height:1}
.rot-view-btn svg{display:block}
.rot-view-btn:hover{color:#c9a84c;border-color:#8a6f2e}
.rot-view-btn.active{color:#c9a84c;border-color:#8a6f2e;background:#1a1a0e}

/* ── POST CARDS ─────────────────────────────────────────────────── */
.rot-section-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid #3a3520}
.rot-section-title{font-family:'Oswald',sans-serif;font-size:16px;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:#e8e0cc;display:flex;align-items:center;gap:8px}
.rot-section-title::before{content:'';display:inline-block;width:3px;height:16px;background:#c9a84c}
.rot-section-link{font-family:'PT Mono',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#7a7060;border:1px solid #252418;padding:4px 10px;transition:color .2s,border-color .2s}
.rot-section-link:hover{color:#c9a84c;border-color:#8a6f2e}
/* ── Сетка карточек постов ──────────────────────────────────────── */
/* Грид вешаем на .blog-posts.hfeed — это ближайший надёжный контейнер
   до date-outer/date-posts/post-outer. Промежуточные #main и .widget.Blog
   — обычные блоки, не трогаем их display чтобы не конфликтовать с GameTown */
.rot-posts-grid{display:block!important}
.rot-posts-grid .blog-posts.hfeed{display:grid!important;grid-template-columns:repeat(3,1fr)!important;gap:16px!important;padding:0!important}
.rot-posts-grid .date-outer,
.rot-posts-grid .date-posts,
.rot-posts-grid .post-outer{display:contents!important}
/* Скрываем лишние grid-items от Blogger */
.rot-posts-grid .inline-ad,
.rot-posts-grid .date-header,
.rot-posts-grid h2.title,
.rot-posts-grid .widget-title,
.rot-posts-grid ins,
.rot-posts-grid .adsbygoogle{display:none!important}
/* Пагинация вытаскивается отдельно поверх сетки */
.rot-posts-grid .blog-pager{grid-column:1/-1}
/* ── FEED VIEW ──────────────────────────────────────────────────── */
.rot-posts-grid.view-feed .blog-posts.hfeed{display:flex!important;flex-direction:column!important;gap:0!important}
.rot-posts-grid.view-feed .date-outer,
.rot-posts-grid.view-feed .date-posts,
.rot-posts-grid.view-feed .post-outer{display:contents!important}
.rot-posts-grid.view-feed .rot-post-card{flex-direction:row!important;border:none!important;border-bottom:1px solid #252418!important;border-radius:0!important;gap:0;padding:14px 0}
.rot-posts-grid.view-feed .rot-post-card:hover{border-color:#252418!important;background:none!important}
.rot-posts-grid.view-feed .rot-card-thumb{width:130px!important;min-width:130px!important;height:86px!important;flex-shrink:0;margin-right:16px;overflow:hidden}
.rot-posts-grid.view-feed .rot-card-thumb img{width:100%;height:100%;object-fit:cover}
.rot-posts-grid.view-feed .rot-card-body{padding:0!important;display:flex;flex-direction:column;justify-content:center;gap:4px}
.rot-posts-grid.view-feed .rot-card-title{font-size:15px!important;margin:0 0 4px!important}
.rot-posts-grid.view-feed .rot-card-excerpt{font-size:13px!important;-webkit-line-clamp:2!important;display:-webkit-box!important;-webkit-box-orient:vertical!important;overflow:hidden!important}
.rot-posts-grid.view-feed .blog-pager{margin-top:10px;border-top:1px solid #3a3520}
/* Blogger label-filter banner — скрываем дефолтный, показываем наш */
.status-msg-wrap,.status-msg-body,.status-msg-border{display:none!important}
.rot-label-banner{display:none;grid-column:1/-1;padding:10px 16px;background:#1a1a0e;border:1px solid #3a3520;border-left:3px solid #c9a84c;font-family:'Oswald',sans-serif;font-size:13px;letter-spacing:1px;text-transform:uppercase;color:#7a7060;margin-bottom:4px;align-self:start}
.rot-label-banner span{color:#c9a84c}
.rot-post-card{background:#1a1a0e;border:1px solid #252418;overflow:hidden;transition:border-color .2s;display:flex;flex-direction:column;position:relative}
.rot-post-card:hover{border-color:#8a6f2e}
/* Вся карточка кликабельна через ::after на ссылке заголовка */
.rot-card-link::after{content:'';position:absolute;inset:0;z-index:1}
/* Метки и другие ссылки остаются кликабельными поверх */
.rot-card-labels a,.rot-tag{position:relative;z-index:2}
.rot-card-thumb{position:relative;height:160px;overflow:hidden;flex-shrink:0;background:#232318}
.rot-card-thumb img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .4s ease}
.rot-post-card:hover .rot-card-thumb img{transform:scale(1.05)}
.rot-tag{position:absolute;top:10px;left:10px;font-family:'PT Mono',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;padding:3px 8px;z-index:2;background:#2a0f0f;color:#ae6a5a;border:1px solid #ae6a5a}
.rot-card-body{padding:14px;flex:1;display:flex;flex-direction:column}
.rot-card-title{font-family:'Oswald',sans-serif;font-size:16px;font-weight:500;color:#e8e0cc;line-height:1.25;margin-bottom:8px}
.rot-card-title a{color:inherit;transition:color .2s}
.rot-card-title a:hover{color:#c9a84c}
.rot-card-excerpt{font-size:12px;color:#7a7060;line-height:1.55;margin-bottom:12px;overflow:hidden;max-height:72px}
.rot-card-excerpt img,.rot-card-excerpt table,.rot-card-excerpt iframe,.rot-card-excerpt figure{display:none!important}
.rot-card-meta{display:flex;align-items:center;gap:12px;font-family:'PT Mono',monospace;font-size:10px;color:#7a7060;border-top:1px solid #252418;padding-top:10px;flex-wrap:wrap}
.rot-card-labels a{font-family:'PT Mono',monospace;font-size:9px;text-transform:uppercase;letter-spacing:1px;padding:2px 7px;border:1px solid #3a3520;color:#8a6f2e;margin-right:4px}
.rot-card-labels a:hover{color:#c9a84c;border-color:#8a6f2e}

/* ── СТРАНИЦА ПОСТА ──────────────────────────────────────────────── */
/* Пост занимает всю ширину грида (3 колонки → одна на всю ширину) */
.rot-single-post{padding:28px 0 0;min-width:0;grid-column:1/-1!important}
.rot-single-labels{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}
.rot-single-header{margin-bottom:28px;padding-bottom:20px;border-bottom:1px solid #252418}
.rot-single-title{font-family:'Oswald',sans-serif;font-size:32px;font-weight:600;color:#e8e0cc;line-height:1.15;margin-bottom:12px}
/* Круглый аватар — добавить класс rot-avatar на <img> в посте */
.rot-avatar{border-radius:50%!important;object-fit:cover!important;width:260px!important;height:260px!important;float:left!important;margin:0 24px 16px 0!important;shape-outside:circle()}
.rot-avatar-wrap{display:block!important;float:left!important;margin:0 24px 16px 0!important;border-radius:50%;overflow:hidden;width:260px;height:260px;flex-shrink:0}
.rot-avatar-wrap img{width:100%!important;height:100%!important;object-fit:cover!important;display:block!important}
.rot-single-meta{font-family:'PT Mono',monospace;font-size:10px;color:#7a7060;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.rot-single-meta .rot-meta-labels{display:flex;flex-wrap:wrap;gap:5px;margin-left:4px}
.rot-single-meta .rot-meta-labels a{font-family:'PT Mono',monospace;font-size:9px;text-transform:uppercase;letter-spacing:1px;padding:2px 7px;border:1px solid #3a3520;color:#8a6f2e;text-decoration:none}
.rot-single-meta .rot-meta-labels a:hover{color:#c9a84c;border-color:#8a6f2e}
.rot-single-body{font-size:15px;color:#c8c0a8;line-height:1.8;max-width:720px}
.rot-single-body h2,.rot-single-body h3{font-family:'Oswald',sans-serif;color:#e8e0cc;margin:28px 0 10px}
.rot-single-body h2{font-size:22px}.rot-single-body h3{font-size:18px}
.rot-single-body p{margin-bottom:16px}
.rot-single-body img{max-width:100%;height:auto;display:block;margin:20px 0;border:1px solid #252418}
.rot-single-body a{color:#c9a84c;border-bottom:1px solid rgba(201,168,76,.3);transition:border-color .2s}
.rot-single-body a:hover{border-color:#c9a84c}
.rot-single-body blockquote{border-left:3px solid #8a6f2e;margin:20px 0;padding:8px 0 8px 18px;color:#a09880;font-style:italic}
.rot-single-footer{margin-top:36px;padding-top:20px;border-top:1px solid #252418}

/* ── КОММЕНТАРИИ ─────────────────────────────────────────────────── */
#comments{margin-top:36px;padding-top:24px;border-top:2px solid #3a3520;color:#c8c0a8}
/* Заголовки "N comments:" и "Post a Comment" */
#comments>h4,#comments h4{font-family:'Oswald',sans-serif;font-size:13px;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:#c9a84c;margin-bottom:20px;background:none;border:none;padding:0}
#comment-post-message{font-family:'Oswald',sans-serif;font-size:13px;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:#c9a84c;margin:24px 0 12px}
/* Список — Blogger использует dl/dt/dd */
#comments-block{margin:0;padding:0}
.comment-author{font-family:'PT Mono',monospace;font-size:10px;letter-spacing:1px;text-transform:uppercase;color:#8a6f2e;margin-bottom:4px}
.comment-author a{color:#8a6f2e}
.comment-body{margin:0 0 4px;padding:0}
.comment-body p{font-size:13px;color:#c8c0a8;line-height:1.7;margin:0 0 6px}
.comment-footer{font-family:'PT Mono',monospace;font-size:9px;color:#7a7060;margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid #252418}
.comment-footer a{color:#7a7060}.comment-footer a:hover{color:#c9a84c}
.avatar-image-container img{width:32px;height:32px;border:1px solid #3a3520;vertical-align:middle;margin-right:8px}
/* Подписка на комментарии */
.comment-footer>a[href*="atom"]{font-size:9px;color:#3a3520!important}
/* Контейнер iframe-формы — инвертируем цвета чтобы вписать в тёмную тему */
#comment-form,#comment-editor-container{width:100%!important;max-width:none!important;box-sizing:border-box!important}
#comment-editor-container{background:#0e0e08;border:1px solid #3a3520;margin-top:8px;overflow:hidden}
/* Все div-потомки контейнера — ломаем фиксированные px-ширины */
#comment-editor-container div{width:100%!important;max-width:100%!important;min-width:0!important;box-sizing:border-box!important}
#comment-editor{border:none!important;display:block!important;
  filter:invert(1) hue-rotate(180deg) brightness(.9) contrast(.95)}
/* На странице поста грид не нужен — отключаем */
/* Статические страницы, одиночные посты и 404: скрыть grid-header, показать полный контент */
body.rot-page-static_page .rot-section-header,
body.rot-page-item .rot-section-header,
body.rot-page-error_page .rot-section-header{display:none!important}
body.rot-page-static_page .rot-posts-grid .blog-posts.hfeed,
body.rot-page-item .rot-posts-grid .blog-posts.hfeed,
body.rot-page-error_page .rot-posts-grid .blog-posts.hfeed{display:block!important;padding:0!important}
body.rot-page-static_page .rot-posts-grid .date-outer,
body.rot-page-static_page .rot-posts-grid .date-posts,
body.rot-page-static_page .rot-posts-grid .post-outer,
body.rot-page-item .rot-posts-grid .date-outer,
body.rot-page-item .rot-posts-grid .date-posts,
body.rot-page-item .rot-posts-grid .post-outer,
body.rot-page-error_page .rot-posts-grid .date-outer,
body.rot-page-error_page .rot-posts-grid .date-posts,
body.rot-page-error_page .rot-posts-grid .post-outer{display:block!important}
body.rot-page-static_page .rot-post-card,
body.rot-page-item .rot-post-card,
body.rot-page-error_page .rot-post-card{display:block!important;background:none!important;border:none!important;border-radius:0!important;padding:0!important}
body.rot-page-static_page .rot-card-img,
body.rot-page-item .rot-card-img,
body.rot-page-error_page .rot-card-img{display:none!important}
body.rot-page-static_page .rot-card-body,
body.rot-page-item .rot-card-body,
body.rot-page-error_page .rot-card-body{padding:0!important}
body.rot-page-static_page .rot-card-title,
body.rot-page-item .rot-card-title,
body.rot-page-error_page .rot-card-title{font-size:28px!important;margin-bottom:16px!important}
body.rot-page-static_page .rot-card-excerpt,
body.rot-page-item .rot-card-excerpt,
body.rot-page-error_page .rot-card-excerpt{display:none!important}
body.rot-page-static_page .rot-single-body,
body.rot-page-item .rot-single-body,
body.rot-page-error_page .rot-single-body{display:block!important}

/* Blog pager */
.blog-pager{display:flex;justify-content:space-between;align-items:center;padding:16px 0;border-top:1px solid #3a3520;margin-top:10px;background:none}
.blog-pager a,.blog-pager-newer-link,.blog-pager-older-link{font-family:'Oswald',sans-serif;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#7a7060;border:1px solid #252418;padding:6px 14px;transition:color .2s,border-color .2s}
.blog-pager a:hover{color:#c9a84c;border-color:#8a6f2e}
.blog-posts.hfeed{padding:0}

/* ── Контейнер под grid (Featured Museum + Choose Path) ─────────── */
.rot-below-grid{max-width:1100px;margin:24px auto 0;padding:0 15px}

/* ── FEATURED MUSEUM ────────────────────────────────────────────── */
.rot-featured-museum{margin-bottom:28px;background:#1a1a0e;border:1px solid #252418;overflow:hidden;clear:both;position:relative;transition:border-color .2s}
.rot-featured-museum:hover{border-color:#8a6f2e}
.rot-museum-link::after{content:'';position:absolute;inset:0;z-index:1}
.rot-block-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#232318;border-bottom:1px solid #3a3520}
.rot-museum-inner{display:grid;grid-template-columns:320px 1fr}
.rot-museum-photo{height:220px;overflow:hidden}
.rot-museum-photo img{display:block;width:100%;height:100%;object-fit:cover}
.rot-museum-body{padding:20px 22px;display:flex;flex-direction:column;justify-content:space-between}
.rot-museum-label{font-family:'PT Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#8a6f2e;margin-bottom:6px}
.rot-museum-title{font-family:'Oswald',sans-serif;font-size:21px;font-weight:600;color:#e8e0cc;margin-bottom:10px;line-height:1.2}
.rot-museum-desc{font-size:13px;color:#c8c0a8;line-height:1.65;margin-bottom:14px}
.rot-museum-stats{display:flex;gap:20px;margin-bottom:16px}
.rot-stat{display:flex;flex-direction:column;align-items:center;gap:3px}
.rot-stat-icon{font-size:17px;opacity:.7}
.rot-stat-val{font-family:'Oswald',sans-serif;font-size:12px;color:#c9a84c}
.rot-stat-label{font-size:9px;color:#7a7060;letter-spacing:1px;text-transform:uppercase;font-family:'PT Mono',monospace}

/* ── MUSEUM WIDGET — внутри main-wrapper ────────────────────────── */
/* Обнуляем обёртку Blogger-виджета, чтобы не ломать дизайн блока */
#museum-wrapper{padding-top:28px}
#museum1>.widget{background:none!important;border:none!important;margin:0!important;overflow:visible!important}
#museum1>.widget>.widget-content{padding:0!important}

/* ── CHOOSE PATH ────────────────────────────────────────────────── */
.rot-choose-path{margin-bottom:28px;clear:both}
.rot-path-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.rot-path-card{background:#1a1a0e;border:1px solid #252418;padding:20px 14px;text-align:center;transition:border-color .2s,background .2s;text-decoration:none;display:block}
.rot-path-card:hover{border-color:#8a6f2e;background:#232318}
.rot-path-icon{font-size:26px;margin-bottom:10px;display:block}
.rot-path-title{font-family:'Oswald',sans-serif;font-size:13px;font-weight:500;text-transform:uppercase;letter-spacing:1.5px;color:#e8e0cc;margin-bottom:5px}
.rot-path-desc{font-size:11px;color:#7a7060;line-height:1.4}

/* ── GameTown tab-блок: скрываем nav и tab1, tabviewsection открыт ── */
#rsidebar-wrapper .tabs-widget,
#sidebartab1{display:none!important}
/* Search box — растянуть на всю ширину сайдбара */
#search{overflow:hidden;margin-bottom:16px}
#searchform{display:flex;width:100%}
#s{flex:1;width:100%!important;background:#232318;border:1px solid #3a3520;border-right:none;color:#c8c0a8;padding:7px 10px;font-family:'PT Mono',monospace;font-size:12px;outline:none;box-sizing:border-box}
#s:focus{border-color:#8a6f2e}
/* tabviewsection и widget-container — убираем отступы GameTown */
#rsidebar-wrapper .tabviewsection,
#rsidebar-wrapper .widget-container{padding:0!important;margin:0!important;background:none!important;border:none!important}
/* sidebartab2/3 скрываются через JS после инициализации Blogger */
/* ── SIDEBAR ─────────────────────────────────────────────────────── */
#rsidebar-wrapper .section{display:flex;flex-direction:column}
#rsidebar-wrapper .widget{background:#1a1a0e;border:1px solid #252418;overflow:hidden;margin-bottom:16px;min-width:0;max-width:100%}
#rsidebar-wrapper .widget:last-child{margin-bottom:0}
#rsidebar-wrapper h2{background:#232318;border-bottom:1px solid #3a3520;padding:10px 14px;font-family:'Oswald',sans-serif;font-size:13px;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:#c9a84c;margin:0}
#rsidebar-wrapper .widget-content{padding:12px 14px;font-size:12px;color:#c8c0a8}
#rsidebar-wrapper .widget-content a{color:#c8c0a8;transition:color .2s}
#rsidebar-wrapper .widget-content a:hover{color:#c9a84c}
#rsidebar-wrapper .widget-content ul{list-style:none;padding:0;margin:0}
#rsidebar-wrapper .widget-content li{padding:5px 0;border-bottom:1px solid #252418;display:flex;justify-content:space-between;align-items:center;font-size:12px}
#rsidebar-wrapper .widget-content li:last-child{border-bottom:none}
#rsidebar-wrapper .widget-content li span{font-family:'PT Mono',monospace;font-size:10px;color:#7a7060;background:#232318;padding:1px 7px;border-radius:2px}
/* Archive */
#BlogArchive1 .widget-content{padding:0}
/* Search */
#BlogSearch1 .widget-content{padding:10px 14px}
#BlogSearch1 input{width:100%;background:#232318;border:1px solid #3a3520;color:#c8c0a8;padding:7px 10px;font-family:'PT Sans',sans-serif;font-size:12px;outline:none}
#BlogSearch1 input:focus{border-color:#8a6f2e}

/* ── САЙДБАР — статичные виджеты ─────────────────────────────── */
.rot-sw{background:#1a1a0e;border:1px solid #252418;overflow:hidden;margin-bottom:16px}
.rot-sw-head{background:#232318;border-bottom:1px solid #3a3520;padding:10px 14px;font-family:'Oswald',sans-serif;font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:2.5px;color:#c9a84c;margin:0;display:flex;align-items:center;gap:8px}
.rot-sw-head-icon{font-size:13px;opacity:.85}
.rot-sw-body{padding:14px}

/* В пути */
.rot-onroad-status{display:inline-flex;align-items:center;gap:6px;font-family:'PT Mono',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:#5a8a5a;margin-bottom:12px}
.rot-onroad-dot{width:7px;height:7px;border-radius:50%;background:#5a8a5a;box-shadow:0 0 6px #5a8a5a;animation:rot-pulse 2s ease-in-out infinite}
@keyframes rot-pulse{0%,100%{opacity:1}50%{opacity:.4}}
.rot-onroad-dest{font-family:'Oswald',sans-serif;font-size:18px;font-weight:600;color:#e8e0cc;line-height:1.1;margin-bottom:4px}
.rot-onroad-country{font-family:'PT Mono',monospace;font-size:10px;color:#8a6f2e;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px}
.rot-onroad-route{font-size:12px;color:#c8c0a8;line-height:1.6;border-left:2px solid #3a3520;padding-left:10px;margin-bottom:10px}
.rot-onroad-dates{font-family:'PT Mono',monospace;font-size:10px;color:#7a7060;display:flex;align-items:center;gap:6px}
.rot-onroad-dates::before{content:'';display:inline-block;width:12px;height:1px;background:#3a3520}

/* Цитата */
.rot-quote-body{position:relative;padding:4px 0 4px 18px;border-left:3px solid #8a6f2e}
.rot-quote-mark{font-family:Georgia,serif;font-size:42px;line-height:.6;color:#8a6f2e;opacity:.5;position:absolute;left:-2px;top:6px}
.rot-quote-text{font-size:13px;color:#c8c0a8;line-height:1.7;font-style:italic;margin:0 0 10px}
.rot-quote-author{font-family:'PT Mono',monospace;font-size:10px;color:#7a7060;letter-spacing:1px}

/* ── Наш таб-виджет Метки/Архив ────────────────────────────────── */
.rot-tabs-widget{background:#1a1a0e;border:1px solid #252418;overflow:hidden;margin-bottom:16px}
.rot-tabs-nav{display:flex;border-bottom:1px solid #3a3520}
.rot-tabs-nav button{flex:1;background:none;border:none;border-bottom:2px solid transparent;padding:10px 8px;font-family:'Oswald',sans-serif;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:#7a7060;cursor:pointer;transition:color .2s,border-color .2s;margin-bottom:-1px}
.rot-tabs-nav button:hover{color:#c9a84c}
.rot-tabs-nav button.rot-tab-active{color:#c9a84c;border-bottom-color:#c9a84c;background:#232318}
.rot-tab-panel{display:none}
.rot-tab-panel.rot-tab-active{display:block}
/* ── Облако меток ───────────────────────────────────────────────── */
#rsidebar-wrapper .Label .widget-content{padding:12px 14px;display:flex;flex-wrap:wrap;gap:6px}
#rsidebar-wrapper .Label .widget-content a,
#rsidebar-wrapper .Label .widget-content span{display:inline-block;font-family:'PT Mono',monospace;text-transform:uppercase;letter-spacing:.5px;color:#7a7060;background:#232318;border:1px solid #2e2d20;padding:3px 8px;transition:color .2s,border-color .2s,background .2s;text-decoration:none;line-height:1.5}
#rsidebar-wrapper .Label .widget-content a:hover{color:#c9a84c;border-color:#8a6f2e;background:#1a1a0e}
/* label-size-* от Blogger: 1(редко)→5(часто) — меняем размер шрифта */
.label-size-1{font-size:9px!important}
.label-size-2{font-size:10px!important}
.label-size-3{font-size:11px!important;color:#c8c0a8!important}
.label-size-4{font-size:12px!important;color:#c8c0a8!important;border-color:#3a3520!important}
.label-size-5{font-size:13px!important;color:#c9a84c!important;border-color:#8a6f2e!important;background:#1a1a0e!important}
.label-count{display:none}
/* ── Архив — иерархия с тогглами ───────────────────────────────── */
#rsidebar-wrapper .BlogArchive .widget-content{padding:0}
/* Сброс ВСЕХ отступов и float внутри архива */
#rsidebar-wrapper .BlogArchive .widget-content *{
  float:none!important;
  margin-left:0!important;
  padding-left:0!important;
  box-sizing:border-box!important}
#rsidebar-wrapper .BlogArchive ul,
#rsidebar-wrapper .BlogArchive li,
#rsidebar-wrapper .BlogArchive .archivedate,
#rsidebar-wrapper .BlogArchive .items,
#rsidebar-wrapper .BlogArchive #ArchiveList,
#rsidebar-wrapper .BlogArchive #ArchiveList > div{
  display:block!important;width:100%!important;
  margin:0!important;padding:0!important;
  border:none!important;list-style:none!important}
/* Класс для сворачивания — перебивает display:block!important выше */
#rsidebar-wrapper .BlogArchive ul.rot-collapsed,
#rsidebar-wrapper .BlogArchive ul.hierarchy.rot-collapsed,
#rsidebar-wrapper .BlogArchive ul.posts.rot-collapsed{display:none!important}
/* Скрываем счётчики */
#rsidebar-wrapper .BlogArchive span.post-count{display:none!important}
/* Тоггл-стрелка */
#rsidebar-wrapper .BlogArchive a.toggle{display:inline!important;font-size:10px;color:#8a6f2e;text-decoration:none;padding-right:4px!important}
#rsidebar-wrapper .BlogArchive a.toggle .zippy{font-style:normal;display:inline!important}
/* Год — строка заголовка */
#rsidebar-wrapper .BlogArchive ul > li.archivedate > a.post-count-link{
  display:inline!important;font-family:'Oswald',sans-serif;font-size:12px;
  letter-spacing:1.5px;text-transform:uppercase;color:#c9a84c;text-decoration:none}
#rsidebar-wrapper .BlogArchive ul > li.archivedate{
  padding:7px 18px!important;background:#232318;border-bottom:1px solid #3a3520}
/* Месяц — строка */
#rsidebar-wrapper .BlogArchive ul.items > li.archivedate > a.post-count-link{
  display:inline!important;font-size:11px;color:#c8c0a8;text-decoration:none;
  letter-spacing:.5px;text-transform:none;transition:color .2s}
#rsidebar-wrapper .BlogArchive ul.items > li.archivedate{
  padding:5px 14px 5px 20px!important;border-bottom:1px solid #252418}
#rsidebar-wrapper .BlogArchive ul.items > li.archivedate > a.post-count-link:hover{color:#c9a84c}
/* Посты */
#rsidebar-wrapper .BlogArchive .items .items li{
  padding:4px 14px 4px 32px!important;border-bottom:1px solid #1a1a0e}
#rsidebar-wrapper .BlogArchive .items .items li a{
  display:inline!important;font-size:11px;color:#7a7060;text-decoration:none;transition:color .2s}
#rsidebar-wrapper .BlogArchive .items .items li a:hover{color:#c9a84c}
#rsidebar-wrapper .BlogArchive .items .items li:last-child{border-bottom:none}

/* ── FOOTER ──────────────────────────────────────────────────────── */
#footer-widgets-container{display:none}
.footer-widget-box{display:none!important}
#footer-container{background:#1e1d14;border-top:2px solid #3a3520;margin-top:48px;padding:36px 15px 0}
.rot-footer-top{max-width:1100px;margin:0 auto;padding-bottom:28px;display:grid;grid-template-columns:240px 1fr 1fr 1fr;gap:32px}
.rot-footer-logo-title{font-family:'Oswald',sans-serif;font-size:15px;font-weight:600;color:#e2c06a;letter-spacing:1px;text-transform:uppercase;display:block}
.rot-footer-logo-sub{font-size:9px;color:#7a7060;letter-spacing:2px;text-transform:uppercase;font-family:'PT Mono',monospace;display:block;margin-top:2px}
.rot-footer-desc{font-size:12px;color:#7a7060;line-height:1.65;margin-top:12px}
.rot-footer-col-title{font-family:'Oswald',sans-serif;font-size:12px;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:#8a6f2e;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #252418}
.rot-footer-links{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:7px}
.rot-footer-links a{font-size:12px;color:#7a7060;transition:color .2s}
.rot-footer-links a:hover{color:#c9a84c}
.rot-footer-bottom-bar{border-top:1px solid #252418;padding:14px 15px}
.rot-footer-bottom{max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;font-family:'PT Mono',monospace;font-size:10px;color:#7a7060}
#footer{padding:0;background:none;border:none}
#copyrights,#credits{display:none}

/* ── DROPDOWN MENU (dropmenu1) ──────────────────────────────────── */
#dropmenu1{position:relative;z-index:500;background:#141309;border-bottom:1px solid #3a3520}
#dropmenu1 .section,#dropmenu1 .widget,#dropmenu1 .widget-content{margin:0!important;padding:0!important;background:none!important;border:none!important}
#dropmenu1 h2.title{display:none!important}
#cssmenu{max-width:1100px;margin:0 auto;padding:0 15px}
#css3menu1{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:stretch}
#css3menu1 > li{position:relative}
#css3menu1 > li > a{display:flex;align-items:center;gap:6px;padding:9px 14px;font-family:'Oswald',sans-serif;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:#c8c0a8;white-space:nowrap;border-right:1px solid #252418;transition:color .2s,background .2s;text-decoration:none}
#css3menu1 > li > a:hover{color:#c9a84c;background:#1a1a0e}
#css3menu1 > li > a span{display:inline}
#css3menu1 > li > a img{width:20px;height:20px;vertical-align:middle;object-fit:contain;opacity:.65;flex-shrink:0}
#css3menu1 > li > a:hover img{opacity:1}
#css3menu1 > li.topmenu > a::after,
#css3menu1 > li.toplast > a::after{content:' \\25BE';font-size:10px;opacity:.5}
#css3menu1 > li > ul{display:none;position:absolute;top:100%;left:0;min-width:210px;background:#1a1a0e;border:1px solid #3a3520;border-top:2px solid #c9a84c;z-index:1000;list-style:none;margin:0;padding:4px 0;box-shadow:0 8px 24px rgba(0,0,0,.7)}
#css3menu1 > li:hover > ul{display:block}
#css3menu1 > li > ul > li > a{display:flex;align-items:center;gap:8px;padding:7px 14px;font-family:'PT Sans',sans-serif;font-size:13px;color:#c8c0a8;white-space:nowrap;transition:color .2s,background .2s;text-decoration:none}
#css3menu1 > li > ul > li > a:hover{color:#c9a84c;background:#252418}
#css3menu1 > li > ul > li > a img{width:20px;height:20px;object-fit:contain;opacity:.65;flex-shrink:0}
#css3menu1 > li > ul > li > a:hover img{opacity:1}
#css3menu1 li > a > span:only-child,#css3menu1 li > span{display:block;font-size:0;height:1px;background:#3a3520;margin:4px 0;overflow:hidden}
#css3menu1 li > a > span:not(:only-child){font-size:inherit}
#css3menu1 li span.divider{display:block;font-size:0;height:1px;background:#3a3520;margin:4px 0}
#css3menu1 li > ul > li{position:relative}
#css3menu1 li > ul > li > ul{display:none;position:absolute;top:0;left:100%;min-width:210px;background:#1a1a0e;border:1px solid #3a3520;border-top:2px solid #8a6f2e;z-index:1001;list-style:none;margin:0;padding:4px 0;box-shadow:4px 4px 16px rgba(0,0,0,.6)}
#css3menu1 li > ul > li:hover > ul{display:block}
#css3menu1 li > ul > li > ul > li > a{display:flex;align-items:center;gap:8px;padding:7px 14px;font-family:'PT Sans',sans-serif;font-size:13px;color:#c8c0a8;white-space:nowrap;transition:color .2s,background .2s;text-decoration:none}
#css3menu1 li > ul > li > ul > li > a:hover{color:#c9a84c;background:#252418}
#css3menu1 li > ul > li > ul > li > a img{width:20px;height:20px;object-fit:contain;opacity:.65;flex-shrink:0}

/* ══════════════════════════════════════════════════════════════════
   АДАПТИВ — три точки перелома:
   1) ≤1024px  планшет горизонтальный: боковая колонка чуть уже
   2) ≤768px   планшет / крупный телефон: основные переключения
   3) ≤480px   телефон: финальные упрощения
══════════════════════════════════════════════════════════════════ */

@media(max-width:1024px){
  #content-wrapper{grid-template-columns:1fr 260px!important}
  .rot-hero-title{font-size:42px}
  .rot-footer-top{grid-template-columns:200px 1fr 1fr 1fr;gap:20px}
}

@media(max-width:768px){
  /* ── Шапка: скрыть навигацию, оставить логотип + кнопки ── */
  .rot-nav{display:none!important}
  .rot-header-inner{flex-wrap:wrap;justify-content:space-between}

  /* ── Герой ── */
  .rot-hero{height:320px!important}
  .rot-hero-title{font-size:34px;max-width:100%}
  .rot-hero-desc{display:none}
  .rot-hero-buttons a:last-child{display:none}

  /* ── Двухколоночный основной грид → один столбец ── */
  #content-wrapper{grid-template-columns:1fr!important;grid-template-rows:auto!important;gap:0!important}
  #main-wrapper{grid-column:1!important;grid-row:auto!important}
  #museum-wrapper{grid-column:1!important;grid-row:auto!important}
  /* Боковая колонка едет под музей */
  #rsidebar-wrapper{grid-column:1!important;grid-row:auto!important;order:2;width:100%!important;max-width:100%!important;border-left:none!important;border-top:1px solid #252418;padding-top:24px!important;margin-top:32px}

  /* ── Карточки постов: 2 колонки ── */
  .rot-posts-grid{grid-template-columns:repeat(2,1fr)!important}

  /* ── Блок «Музей»: фото сверху, текст снизу ── */
  .rot-museum-inner{grid-template-columns:1fr!important}
  .rot-museum-photo{height:200px}

  /* ── Выбери маршрут: 2×2 ── */
  .rot-path-grid{grid-template-columns:repeat(2,1fr)!important}

  /* ── Футер: одна колонка ── */
  .rot-footer-top{grid-template-columns:1fr!important;gap:20px}
  .rot-footer-bottom{flex-direction:column;gap:8px;text-align:center}
}

@media(max-width:480px){
  /* ── Герой ── */
  .rot-hero{height:260px!important}
  .rot-hero-title{font-size:28px;letter-spacing:1px}
  .rot-hero-eyebrow{display:none}
  .rot-hero-geo{display:none}

  /* ── Одна колонка постов ── */
  .rot-posts-grid{grid-template-columns:1fr!important}

  /* ── Раздел posts-section: убрать боковые отступы ── */
  .rot-section-header{padding-left:4px}

  /* ── Карточки: изображение короче ── */
  .rot-card-thumb{height:160px!important}

  /* ── Выбери маршрут: 1 колонка на совсем маленьком ── */
  .rot-path-grid{grid-template-columns:1fr!important}

  /* ── Шапка — сжать логотип ── */
  .rot-logo-title{font-size:15px!important}
  .rot-logo-sub{display:none}
}
"""

skin_re = re.compile(r'<b:skin><!\[CDATA\[.*?\]\]></b:skin>', re.DOTALL)
_new_skin = '<b:skin><![CDATA[\n' + NEW_CSS + '\n]]></b:skin>'
src = skin_re.sub(lambda m: _new_skin, src)

# ════════════════════════════════════════════════════════════════════
# 2b. Favicon — заменяем плейсхолдер на Blogger-переменную
# ════════════════════════════════════════════════════════════════════
src = src.replace(
    "<link href='YOUR-FAVICON-URL' rel='shortcut icon' type='image/vnd.microsoft.icon'/>",
    "<b:if cond='data:blog.faviconUrl'><link expr:href='data:blog.faviconUrl' rel='shortcut icon' type='image/x-icon'/></b:if>"
)

# ════════════════════════════════════════════════════════════════════
# 3. Summary JS helper — ЗАМЕНЯЕМ GameTown-версию функции прямо в теле
#    (вставка в <head> бесполезна: GameTown переопределяет функцию позже)
# ════════════════════════════════════════════════════════════════════
GAMETOWN_SUMMARY_OLD = """\
function createSummaryAndThumb(pID){
\tvar div = document.getElementById(pID);
\tvar imgtag = "";
\tvar img = div.getElementsByTagName("img");
\tvar summ = summary_noimg;
\tif(img.length>=1) {\t
\t\timgtag = '<img src="'+img[0].src+'" class="pbtthumbimg"/>';
\t\tsumm = summary_img;
\t}
\t
\tvar summary = imgtag + '<div>' + removeHtmlTag(div.innerHTML,summ) + '</div>';
\tdiv.innerHTML = summary;
}"""

GAMETOWN_SUMMARY_NEW = """\
function createSummaryAndThumb(id){
  var d=document.getElementById(id);
  var imgs=d.getElementsByTagName("img");
  var imgSrc=imgs.length>=1?imgs[0].src:null;
  d.innerHTML="<span>"+removeHtmlTag(d.innerHTML,imgSrc?summary_img:summary_noimg)+"</span>";
  if(imgSrc){
    var card=d.closest?d.closest(".rot-post-card"):null;
    if(card){
      var thumb=card.querySelector(".rot-card-thumb");
      if(thumb){
        var existing=thumb.querySelector("img");
        if(existing){
          existing.src=imgSrc; /* перезаписываем thumbnailUrl полноразмерным */
        } else {
          var el=document.createElement("img");el.src=imgSrc;el.alt="";
          thumb.appendChild(el);
        }
      }
    }
  }
}"""

assert GAMETOWN_SUMMARY_OLD in src, "GameTown createSummaryAndThumb not found — check source"
src = src.replace(GAMETOWN_SUMMARY_OLD, GAMETOWN_SUMMARY_NEW)

# Заодно уменьшаем длину анонсов до 200 символов (GameTown ставит 550/450)
src = src.replace('summary_noimg = 550;\nsummary_img = 450;',
                  'summary_noimg = 200;\nsummary_img = 200;')

# ════════════════════════════════════════════════════════════════════
# 4. Вставляем наш HEADER после <body> и перед <div id='body-wrapper'>
#    Завершённый блок — никаких висящих div
# ════════════════════════════════════════════════════════════════════
OUR_HEADER = """
<!-- ═══ ДОРОГИ ВРЕМЁН: HEADER ════════════════════════════════════ -->
<div class='rot-header'>
  <div class='rot-header-inner'>
    <a class='rot-logo' expr:href='data:blog.homepageUrl'>
      <div class='rot-logo-emblem'><img src='{IMG_LOGO}' alt='&#1044;&#1086;&#1088;&#1086;&#1075;&#1080; &#1042;&#1088;&#1077;&#1084;&#1105;&#1085;'/></div>
      <div>
        <span class='rot-logo-title'>&#1044;&#1086;&#1088;&#1086;&#1075;&#1080; &#1042;&#1088;&#1077;&#1084;&#1105;&#1085;</span>
        <span class='rot-logo-sub'>&#1055;&#1091;&#1090;&#1077;&#1096;&#1077;&#1089;&#1090;&#1074;&#1080;&#1103; &#183; &#1052;&#1091;&#1079;&#1077;&#1080; &#183; &#1048;&#1089;&#1090;&#1086;&#1088;&#1080;&#1103;</span>
      </div>
    </a>
    <nav class='rot-nav'>
      <ul>
        <li id='rot-nav-home'><a expr:href='data:blog.homepageUrl'>&#1043;&#1083;&#1072;&#1074;&#1085;&#1072;&#1103;</a></li>
        <li id='rot-nav-dorogi'><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%94%D0%BE%D1%80%D0%BE%D0%B3%D0%B8&quot;'>&#1044;&#1086;&#1088;&#1086;&#1075;&#1080;</a></li>
        <li id='rot-nav-vremena'><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%92%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%B0&quot;'>&#1042;&#1088;&#1077;&#1084;&#1077;&#1085;&#1072;</a></li>
        <li id='rot-nav-goroda'><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0&quot;'>&#1043;&#1086;&#1088;&#1086;&#1076;&#1072;</a></li>
        <li id='rot-nav-muzei'><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%9C%D1%83%D0%B7%D0%B5%D0%B8&quot;'>&#1052;&#1091;&#1079;&#1077;&#1080;</a></li>
        <li id='rot-nav-ekspona'><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%AD%D0%BA%D1%81%D0%BF%D0%BE%D0%BD%D0%B0%D1%82%D1%8B&quot;'>&#1069;&#1082;&#1089;&#1087;&#1086;&#1085;&#1072;&#1090;&#1099;</a></li>
      </ul>
    </nav>
    <div class='rot-header-icons' id='rot-toolbar-target'></div>
  </div>
</div>
<!-- ═══ END HEADER ═══════════════════════════════════════════════ -->
"""
PAGE_TYPE_JS = "<script>document.body.className+=' rot-page-<data:blog.pageType/>';</script>\n"
src = src.replace('<body>\n\n<div id=\'body-wrapper\'>', '<body>\n' + PAGE_TYPE_JS + OUR_HEADER.format(IMG_LOGO=IMG_LOGO) + '\n<div id=\'body-wrapper\'>')

# ════════════════════════════════════════════════════════════════════
# 5. Заменяем СЛАЙДЕР GameTown на наш HERO
#    (тот же <b:if> wrapper — уже валидный XML)
# ════════════════════════════════════════════════════════════════════
OLD_SLIDER_START = "<!-- Featured Content Slider Started -->"
OLD_SLIDER_END   = "<!-- Featured Content Slider End -->"

old_slider_match = re.search(
    re.escape(OLD_SLIDER_START) + r'.*?' + re.escape(OLD_SLIDER_END),
    src, re.DOTALL
)

NEW_HERO = """\
<!-- ═══ ДОРОГИ ВРЕМЁН: HERO SLIDER ══════════════════════════════ -->
<b:if cond='data:blog.pageType != &quot;static_page&quot;'>
<b:if cond='data:blog.pageType != &quot;item&quot;'>
<div class='rot-hero'>
  <div class='rot-slides'>
    <div class='rot-slide active' data-geo='Deutsches Panzermuseum, &#1052;&#1102;&#1085;&#1089;&#1090;&#1077;&#1088;'>
      <img alt='Panzer 38(t)' src='{IMG_SLIDE1}'/>
    </div>
    <div class='rot-slide' data-geo='&#1052;&#1091;&#1079;&#1077;&#1081;-&#1079;&#1072;&#1074;&#1086;&#1076; &#1055;&#1077;&#1085;&#1077;&#1084;&#1102;&#1085;&#1076;&#1077;, &#1043;&#1077;&#1088;&#1084;&#1072;&#1085;&#1080;&#1103;'>
      <img alt='&#1056;&#1072;&#1082;&#1077;&#1090;&#1072; V-2' src='{IMG_SLIDE2}'/>
    </div>
    <div class='rot-slide' data-geo='&#1052;&#1086;&#1088;&#1089;&#1082;&#1086;&#1081; &#1084;&#1091;&#1079;&#1077;&#1081;, &#1042;&#1080;&#1083;&#1100;&#1075;&#1077;&#1083;&#1100;&#1084;&#1089;&#1093;&#1072;&#1092;&#1077;&#1085;'>
      <img alt='&#1054;&#1088;&#1091;&#1076;&#1080;&#1081;&#1085;&#1072;&#1103; &#1073;&#1072;&#1096;&#1085;&#1103;' src='{IMG_SLIDE3}'/>
    </div>
  </div>
  <div class='rot-hero-content'>
    <div class='rot-hero-inner'>
      <p class='rot-hero-eyebrow'>&#1040;&#1074;&#1090;&#1086;&#1088;&#1089;&#1082;&#1080;&#1081; &#1073;&#1083;&#1086;&#1075; &#1086;&#1073; &#1080;&#1089;&#1090;&#1086;&#1088;&#1080;&#1080; &#1045;&#1074;&#1088;&#1086;&#1087;&#1099;</p>
      <h1 class='rot-hero-title'>&#1044;&#1086;&#1088;&#1086;&#1075;&#1080; &#1042;&#1088;&#1077;&#1084;&#1105;&#1085;</h1>
      <p class='rot-hero-desc'>&#1052;&#1077;&#1089;&#1090;&#1086;, &#1075;&#1076;&#1077; &#1080;&#1089;&#1090;&#1086;&#1088;&#1080;&#1103; &#1086;&#1078;&#1080;&#1074;&#1072;&#1077;&#1090;</p>
      <div class='rot-hero-buttons'>
        <a class='rot-btn rot-btn-primary' id='rot-btn-read' expr:href='data:blog.homepageUrl'>&#1063;&#1080;&#1090;&#1072;&#1090;&#1100; &#8250;</a>
        <a class='rot-btn rot-btn-outline' href='/p/blog-page.html'>&#1054; &#1087;&#1088;&#1086;&#1077;&#1082;&#1090;&#1077;</a>
      </div>
    </div>
  </div>
  <div class='rot-hero-geo' id='rot-hero-geo'>Deutsches Panzermuseum, &#1052;&#1102;&#1085;&#1089;&#1090;&#1077;&#1088;</div>
  <div class='rot-arrow rot-arrow-prev' id='rot-prev'>&#8249;</div>
  <div class='rot-arrow rot-arrow-next' id='rot-next'>&#8250;</div>
  <div class='rot-pager' id='rot-pager'><span class='active'>&#160;</span><span>&#160;</span><span>&#160;</span></div>
</div>
</b:if>
</b:if>
<!-- ═══ END HERO ═════════════════════════════════════════════════ -->"""

if old_slider_match:
    src = src[:old_slider_match.start()] + NEW_HERO.format(
        IMG_SLIDE1=IMG_SLIDE1, IMG_SLIDE2=IMG_SLIDE2, IMG_SLIDE3=IMG_SLIDE3
    ) + src[old_slider_match.end():]

# ════════════════════════════════════════════════════════════════════
# 6. Section header + rot-posts-grid внутри main-wrapper
#    Никаких новых HTML-обёрток — только CSS делает grid
# ════════════════════════════════════════════════════════════════════

OLD_MAIN_SECTION = "<b:section class='main' id='main' showaddelement='no'>"
NEW_MAIN_SECTION = """\
<div class='rot-section-header'>
  <h2 class='rot-section-title'>&#1055;&#1091;&#1073;&#1083;&#1080;&#1082;&#1072;&#1094;&#1080;&#1080;</h2>
  <div class='rot-view-switcher'>
    <button class='rot-view-btn active' id='btn-cards' onclick='rotSetView(&quot;cards&quot;)' title='&#1050;&#1072;&#1088;&#1090;&#1086;&#1095;&#1082;&#1080;'>
      <svg width='16' height='16' viewBox='0 0 16 16' fill='currentColor'><rect x='1' y='1' width='6' height='6'/><rect x='9' y='1' width='6' height='6'/><rect x='1' y='9' width='6' height='6'/><rect x='9' y='9' width='6' height='6'/></svg>
    </button>
    <button class='rot-view-btn' id='btn-feed' onclick='rotSetView(&quot;feed&quot;)' title='&#1051;&#1077;&#1085;&#1090;&#1072;'>
      <svg width='16' height='16' viewBox='0 0 16 16' fill='currentColor'><rect x='5' y='1' width='10' height='2'/><rect x='1' y='1' width='3' height='2'/><rect x='5' y='5' width='10' height='2'/><rect x='1' y='5' width='3' height='2'/><rect x='5' y='9' width='10' height='2'/><rect x='1' y='9' width='3' height='2'/><rect x='5' y='13' width='10' height='2'/><rect x='1' y='13' width='3' height='2'/></svg>
    </button>
  </div>
</div>
<div class='rot-posts-grid'>
<b:section class='main' id='main' showaddelement='no'>"""
src = src.replace(OLD_MAIN_SECTION, NEW_MAIN_SECTION)

# ════════════════════════════════════════════════════════════════════
# 6b. Сайдбар — фиксируем id виджетов, чтобы контент выживал после
#     повторной загрузки темы в Blogger.
#     Blogger сохраняет данные виджета если его id есть в XML.
#     HTML2  = «Маршрут»   HTML_QUOTE = «Цитата»
#     Оба прописаны явно → контент не теряется при апдейте темы.
# ════════════════════════════════════════════════════════════════════
WIDGET_INCLUDABLE = """\
    <b:includable id='main'>
  <b:if cond='data:title != &quot;&quot;'>
    <h2 class='title'><data:title/></h2>
  </b:if>
  <div class='widget-content'>
    <data:content/>
  </div>
  <b:include name='quickedit'/>
</b:includable>"""

OLD_SIDEBAR_SECTION = """\
<b:section class='sidebar' id='rsidebartop' showaddelement='yes'>
  <b:widget id='HTML2' locked='false' title='' type='HTML'>
    <b:includable id='main'>
  <!-- only display title if it's non-empty -->
  <b:if cond='data:title != &quot;&quot;'>
    <h2 class='title'><data:title/></h2>
  </b:if>
  <div class='widget-content'>
    <data:content/>
  </div>

  <b:include name='quickedit'/>
</b:includable>
  </b:widget>
</b:section>"""

NEW_SIDEBAR_SECTION = (
    "<b:section class='sidebar' id='rsidebartop' showaddelement='yes'>\n"
    "  <b:widget id='HTML2' locked='false' title='Маршрут' type='HTML'>\n"
    + WIDGET_INCLUDABLE + "\n"
    "  </b:widget>\n"
    "  <b:widget id='HTML8' locked='false' title='&#1062;&#1080;&#1090;&#1072;&#1090;&#1072;' type='HTML'>\n"
    + WIDGET_INCLUDABLE + "\n"
    "  </b:widget>\n"
    "  <b:widget id='HTML10' locked='false' title='' type='HTML'>\n"
    + WIDGET_INCLUDABLE + "\n"
    "  </b:widget>\n"
    "</b:section>"
)

assert OLD_SIDEBAR_SECTION in src, "rsidebartop section not found — GameTown template changed?"
src = src.replace(OLD_SIDEBAR_SECTION, NEW_SIDEBAR_SECTION)

# Закрываем rot-posts-grid, вставляем секцию музея, закрываем main-wrapper
MUSEUM_SECTION = (
    "<b:section class='museum-section' id='museum1' showaddelement='no'>\n"
    "  <b:widget id='HTML9' locked='false' title='&#1056;&#1077;&#1082;&#1086;&#1084;&#1077;&#1085;&#1076;&#1091;&#1102; &#1084;&#1091;&#1079;&#1077;&#1081;' type='HTML'>\n"
    "    <b:includable id='main'>\n"
    "  <div class='widget-content'>\n"
    "    <data:content/>\n"
    "  </div>\n"
    "  <b:include name='quickedit'/>\n"
    "</b:includable>\n"
    "  </b:widget>\n"
    "</b:section>"
)
TOOLBAR_SECTION = (
    "<b:section class='header-toolbar' id='toolbar1' showaddelement='no'>\n"
    "  <b:widget id='HTML11' locked='false' title='Тулбар' type='HTML'>\n"
    + WIDGET_INCLUDABLE + "\n"
    "  </b:widget>\n"
    "</b:section>"
)

NEWSFEED_SECTION = (
    "<b:section class='hero-newsfeed' id='newsfeed1' showaddelement='no'>\n"
    "  <b:widget id='HTML12' locked='false' title='Newsfeed' type='HTML'>\n"
    + WIDGET_INCLUDABLE + "\n"
    "  </b:widget>\n"
    "</b:section>"
)

DROPMENU_SECTION = (
    "<b:section class='drop-menu' id='dropmenu1' showaddelement='no'>\n"
    "  <b:widget id='HTML13' locked='false' title='&#1052;&#1077;&#1085;&#1102;' type='HTML'>\n"
    + WIDGET_INCLUDABLE + "\n"
    "  </b:widget>\n"
    "</b:section>"
)

src = src.replace(
    "        </b:section>\n      </div>\n\n<div id='rsidebar-wrapper'>",
    "        </b:section>\n</div><!-- /.rot-posts-grid -->\n"
    + "      </div><!-- /#main-wrapper -->\n\n"
    + "<div id='museum-wrapper'>\n" + MUSEUM_SECTION + "\n</div><!-- /#museum-wrapper -->\n\n"
    + "<!-- Toolbar и Newsfeed: Layout видит здесь, JS переставляет их на место -->\n"
    + "<div id='floating-widgets'>\n"
    + TOOLBAR_SECTION + "\n"
    + NEWSFEED_SECTION + "\n"
    + DROPMENU_SECTION + "\n"
    + "</div><!-- /#floating-widgets -->\n\n"
    + "<div id='rsidebar-wrapper'>"
)

# ════════════════════════════════════════════════════════════════════
# 6c. Сайдбар — удаляем ненужные виджеты GameTown из sidebarright
#     (Recent Posts / Unordered List / Download) и переименовываем
#     табы Popular→убираем, Tags→Метки, Blog Archives→Архив
# ════════════════════════════════════════════════════════════════════

# Удаляем три виджета из sidebarright (HTML1, HTML5, HTML3)
src = src.replace(
    "          <b:widget id='HTML1' locked='false' title='Recent Posts' type='HTML'>\n"
    "            <b:includable id='main'>\n"
    "  <!-- only display title if it's non-empty -->\n"
    "  <b:if cond='data:title != &quot;&quot;'>\n"
    "    <h2 class='title'><data:title/></h2>\n"
    "  </b:if>\n"
    "  <div class='widget-content'>\n"
    "    <data:content/>\n"
    "  </div>\n\n"
    "  <b:include name='quickedit'/>\n"
    "</b:includable>\n"
    "          </b:widget>\n"
    "          <b:widget id='HTML5' locked='false' title='Unordered List' type='HTML'>\n"
    "            <b:includable id='main'>\n"
    "  <!-- only display title if it's non-empty -->\n"
    "  <b:if cond='data:title != &quot;&quot;'>\n"
    "    <h2 class='title'><data:title/></h2>\n"
    "  </b:if>\n"
    "  <div class='widget-content'>\n"
    "    <data:content/>\n"
    "  </div>\n\n"
    "  <b:include name='quickedit'/>\n"
    "</b:includable>\n"
    "          </b:widget>\n"
    "          <b:widget id='HTML3' locked='false' title='Download' type='HTML'>\n"
    "            <b:includable id='main'>\n"
    "  <!-- only display title if it's non-empty -->\n"
    "  <b:if cond='data:title != &quot;&quot;'>\n"
    "    <h2 class='title'><data:title/></h2>\n"
    "  </b:if>\n"
    "  <div class='widget-content'>\n"
    "    <data:content/>\n"
    "  </div>\n\n"
    "</b:includable>\n"
    "          </b:widget>",
    ""
)

# Убираем GameTown jQuery-инициализацию табов (она скрывает sidebartab2/3)
src = src.replace(
    "            jQuery(document).ready(function($){\n"
    "                $(&quot;.tabs-widget-content-widget-themater_tabs-1432447472-id&quot;).hide();\n"
    "            \t$(&quot;ul.tabs-widget-widget-themater_tabs-1432447472-id li:first a&quot;).addClass(&quot;tabs-widget-current&quot;).show();\n"
    "            \t$(&quot;.tabs-widget-content-widget-themater_tabs-1432447472-id:first&quot;).show();",
    "            jQuery(document).ready(function($){\n"
    "                /* GameTown tab init disabled — managed by rot-tabs widget */"
)

# Убираем обёртки tabs-widget-content вокруг sidebartab2 и sidebartab3
import re
src = re.sub(
    r"<div class='tabs-widget-content tabs-widget-content-widget-themater_tabs-1432447472-id' id='widget-themater_tabs-1432447472-id(2|3)'>\n",
    "",
    src
)
# Закрывающий </div> после каждой секции (sidebartab2 и sidebartab3)
# Заменяем "</div>\s*\n\s*\n" после </b:section> для id2 и id3
src = re.sub(
    r"(</b:section>\s*\n)(</div>[ \t]*\n[ \t]*\n)(?=\s*<b:section[^>]+id='sidebartab[23]'|$|\s*</div>[ \t]*\n[ \t]*\n\s*</div>)",
    r"\1\n",
    src
)

# ════════════════════════════════════════════════════════════════════
# 7. Featured Museum + Choose Path — вставляем ПОСЛЕ content-wrapper
#    (не внутри grid), перед footer-widgets-container.
#    Оборачиваем в rot-below-grid с max-width 1100px.
# ════════════════════════════════════════════════════════════════════
EXTRA_BLOCKS = """\

<!-- ═══ CHOOSE PATH (вне grid, полная ширина) ═══════════════════ -->
<div class='rot-below-grid'>

<div class='rot-choose-path'>
  <div class='rot-section-header'>
    <h2 class='rot-section-title'>&#1042;&#1099;&#1073;&#1077;&#1088;&#1080;&#1090;&#1077; &#1089;&#1074;&#1086;&#1081; &#1087;&#1091;&#1090;&#1100;</h2>
  </div>
  <div class='rot-path-grid'>
    <a class='rot-path-card' expr:href='data:blog.homepageUrl + &quot;search/label/%D0%94%D0%BE%D1%80%D0%BE%D0%B3%D0%B8&quot;'>
      <span class='rot-path-icon'>&#129517;</span>
      <div class='rot-path-title'>&#1044;&#1086;&#1088;&#1086;&#1075;&#1080;</div>
      <p class='rot-path-desc'>&#1052;&#1072;&#1088;&#1096;&#1088;&#1091;&#1090;&#1099; &#1080; &#1087;&#1086;&#1077;&#1079;&#1076;&#1082;&#1080;</p>
    </a>
    <a class='rot-path-card' expr:href='data:blog.homepageUrl + &quot;search/label/%D0%92%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%B0&quot;'>
      <span class='rot-path-icon'>&#128220;</span>
      <div class='rot-path-title'>&#1042;&#1088;&#1077;&#1084;&#1077;&#1085;&#1072;</div>
      <p class='rot-path-desc'>&#1048;&#1089;&#1090;&#1086;&#1088;&#1080;&#1103; &#1080; &#1089;&#1086;&#1073;&#1099;&#1090;&#1080;&#1103;</p>
    </a>
    <a class='rot-path-card' expr:href='data:blog.homepageUrl + &quot;search/label/%D0%9C%D1%83%D0%B7%D0%B5%D0%B8&quot;'>
      <span class='rot-path-icon'>&#127963;&#65039;</span>
      <div class='rot-path-title'>&#1052;&#1091;&#1079;&#1077;&#1080;</div>
      <p class='rot-path-desc'>&#1050;&#1086;&#1083;&#1083;&#1077;&#1082;&#1094;&#1080;&#1080; &#1080; &#1074;&#1099;&#1089;&#1090;&#1072;&#1074;&#1082;&#1080;</p>
    </a>
    <a class='rot-path-card' expr:href='data:blog.homepageUrl + &quot;search/label/%D0%AD%D0%BA%D1%81%D0%BF%D0%BE%D0%BD%D0%B0%D1%82%D1%8B&quot;'>
      <span class='rot-path-icon'>&#9881;&#65039;</span>
      <div class='rot-path-title'>&#1069;&#1082;&#1089;&#1087;&#1086;&#1085;&#1072;&#1090;&#1099;</div>
      <p class='rot-path-desc'>&#1058;&#1077;&#1093;&#1085;&#1080;&#1082;&#1072; &#1080; &#1072;&#1088;&#1090;&#1077;&#1092;&#1072;&#1082;&#1090;&#1099;</p>
    </a>
  </div>
</div>

</div><!-- /.rot-below-grid -->
<!-- ═══ END EXTRA BLOCKS ══════════════════════════════════════════ -->
"""

# Вставляем после content-wrapper, перед footer-widgets-container
src = src.replace(
    "<div style='clear:both;'/>\n<div id='footer-widgets-container'>",
    EXTRA_BLOCKS
    + "<div style='clear:both;'/>\n<div id='footer-widgets-container'>"
)

# ════════════════════════════════════════════════════════════════════
# 8. Шаблон карточки поста (Blog1 -> post includable)
# ════════════════════════════════════════════════════════════════════
old_post_inc = re.search(
    r"<b:includable id='post' var='post'>.*?</b:includable>",
    src, re.DOTALL
)
if old_post_inc:
    NEW_POST_INC = """\
<b:includable id='post' var='post'>
<b:if cond='data:blog.pageType == &quot;item&quot; or data:blog.pageType == &quot;static_page&quot; or data:blog.pageType == &quot;error_page&quot;'>

  <!-- ═══ СТРАНИЦА ПОСТА ═══════════════════════════════════════════ -->
  <article class='rot-single-post'>
    <header class='rot-single-header'>
      <h1 class='rot-single-title'><data:post.title/></h1>
      <div class='rot-single-meta'>
        <span>&#128197; <data:post.timestamp/></span>
        <b:if cond='data:post.allowComments'>
          <span>&#128172; <data:post.numComments/></span>
        </b:if>
        <b:if cond='data:post.labels'>
          <span class='rot-meta-labels'>
            <b:loop values='data:post.labels' var='label'>
              <a expr:href='data:label.url'><data:label.name/></a>
            </b:loop>
          </span>
        </b:if>
      </div>
    </header>
    <div class='rot-single-body'>
      <data:post.body/>
    </div>
  </article>

<b:else/>

  <!-- ═══ КАРТОЧКА (главная / архив / метка) ══════════════════════ -->
  <article class='rot-post-card'>
    <div class='rot-card-thumb'>
      <b:if cond='data:post.labels'>
        <b:loop values='data:post.labels' var='label'>
          <b:if cond='data:label.isFirst == &quot;true&quot;'>
            <span class='rot-tag'><data:label.name/></span>
          </b:if>
        </b:loop>
      </b:if>
      <b:if cond='data:post.thumbnailUrl'>
        <img alt='' expr:src='data:post.thumbnailUrl'/>
      </b:if>
    </div>
    <div class='rot-card-body'>
      <h3 class='rot-card-title'><a class='rot-card-link' expr:href='data:post.url'><data:post.title/></a></h3>
      <div class='rot-card-excerpt'>
        <div expr:id='&quot;summary&quot; + data:post.id'><data:post.body/></div>
        <script type='text/javascript'>createSummaryAndThumb(&quot;summary<data:post.id/>&quot;);</script>
      </div>
      <div class='rot-card-meta'>
        <span>&#128197; <data:post.timestamp/></span>
        <b:if cond='data:post.allowComments'>
          <span>&#128172; <data:post.numComments/></span>
        </b:if>
        <b:if cond='data:post.labels'>
          <span class='rot-card-labels'>
            <b:loop values='data:post.labels' var='label'>
              <a expr:href='data:label.url'><data:label.name/></a>
            </b:loop>
          </span>
        </b:if>
      </div>
    </div>
  </article>

</b:if>
</b:includable>"""
    src = src[:old_post_inc.start()] + NEW_POST_INC + src[old_post_inc.end():]

# ════════════════════════════════════════════════════════════════════
# 9. Заменяем контент внутри #footer-container
# ════════════════════════════════════════════════════════════════════
OLD_FOOTER_CONTENT = re.search(
    r"<div id='footer-container'>.*?</div><!-- #footer -->\n</div>",
    src, re.DOTALL
)
NEW_FOOTER_CONTENT = """\
<div id='footer-container'>
<div class='rot-footer-top'>
  <div>
    <span class='rot-footer-logo-title'>&#1044;&#1086;&#1088;&#1086;&#1075;&#1080; &#1042;&#1088;&#1077;&#1084;&#1105;&#1085;</span>
    <span class='rot-footer-logo-sub'>&#1055;&#1091;&#1090;&#1077;&#1096;&#1077;&#1089;&#1090;&#1074;&#1080;&#1103; &#183; &#1052;&#1091;&#1079;&#1077;&#1080; &#183; &#1048;&#1089;&#1090;&#1086;&#1088;&#1080;&#1103;</span>
    <p class='rot-footer-desc'>&#1040;&#1074;&#1090;&#1086;&#1088;&#1089;&#1082;&#1080;&#1081; &#1087;&#1088;&#1086;&#1077;&#1082;&#1090; &#1086; &#1074;&#1086;&#1077;&#1085;&#1085;&#1086;&#1081; &#1080;&#1089;&#1090;&#1086;&#1088;&#1080;&#1080;, &#1084;&#1091;&#1079;&#1077;&#1103;&#1093; &#1080; &#1087;&#1091;&#1090;&#1077;&#1096;&#1077;&#1089;&#1090;&#1074;&#1080;&#1103;&#1093; &#1087;&#1086; &#1045;&#1074;&#1088;&#1086;&#1087;&#1077;.</p>
  </div>
  <div>
    <p class='rot-footer-col-title'>&#1053;&#1072;&#1074;&#1080;&#1075;&#1072;&#1094;&#1080;&#1103;</p>
    <ul class='rot-footer-links'>
      <li><a expr:href='data:blog.homepageUrl'>&#1043;&#1083;&#1072;&#1074;&#1085;&#1072;&#1103;</a></li>
      <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%94%D0%BE%D1%80%D0%BE%D0%B3%D0%B8&quot;'>&#1044;&#1086;&#1088;&#1086;&#1075;&#1080;</a></li>
      <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%92%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%B0&quot;'>&#1042;&#1088;&#1077;&#1084;&#1077;&#1085;&#1072;</a></li>
      <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0&quot;'>&#1043;&#1086;&#1088;&#1086;&#1076;&#1072;</a></li>
      <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%9C%D1%83%D0%B7%D0%B5%D0%B8&quot;'>&#1052;&#1091;&#1079;&#1077;&#1080;</a></li>
      <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%AD%D0%BA%D1%81%D0%BF%D0%BE%D0%BD%D0%B0%D1%82%D1%8B&quot;'>&#1069;&#1082;&#1089;&#1087;&#1086;&#1085;&#1072;&#1090;&#1099;</a></li>
    </ul>
  </div>
  <div>
    <p class='rot-footer-col-title'>&#1048;&#1085;&#1092;&#1086;&#1088;&#1084;&#1072;&#1094;&#1080;&#1103;</p>
    <ul class='rot-footer-links'>
      <li><a href='https://roadsoftimes.blogspot.com/p/blog-page.html'>&#1054; &#1087;&#1088;&#1086;&#1077;&#1082;&#1090;&#1077;</a></li>
      <li><a href='https://roadsoftimes.blogspot.com/p/blog-page_11.html'>&#1050;&#1086;&#1085;&#1090;&#1072;&#1082;&#1090;&#1099;</a></li>
      <li><a expr:href='data:blog.homepageUrl + &quot;feeds/posts/default&quot;'>RSS</a></li>
    </ul>
  </div>
  <div>
    <p class='rot-footer-col-title'>&#1057;&#1083;&#1077;&#1076;&#1080;&#1090;&#1077; &#1079;&#1072; &#1085;&#1072;&#1084;&#1080;</p>
    <ul class='rot-footer-links'>
      <li><a href='https://vk.com/roadsoftimes' target='_blank'>VK</a></li>
      <li><a href='https://t.me/roadsoftimes' target='_blank'>Telegram</a></li>
      <li><a href='#'>YouTube</a></li>
    </ul>
  </div>
</div>
<div class='rot-footer-bottom-bar'>
  <div class='rot-footer-bottom'>
    <span>&#169; 2026 &#1044;&#1086;&#1088;&#1086;&#1075;&#1080; &#1042;&#1088;&#1077;&#1084;&#1105;&#1085;</span>
    <div><a href='https://vk.com/roadsoftimes' target='_blank' style='color:#7a7060;margin-right:10px'>VK</a><a href='https://t.me/roadsoftimes' target='_blank' style='color:#7a7060;margin-right:10px'>TG</a><a href='#' style='color:#7a7060'>YT</a></div>
  </div>
</div>
<div id='footer'><div id='copyrights'>&#160;</div></div><!-- #footer -->
</div>"""
if OLD_FOOTER_CONTENT:
    src = src[:OLD_FOOTER_CONTENT.start()] + NEW_FOOTER_CONTENT + src[OLD_FOOTER_CONTENT.end():]

# ════════════════════════════════════════════════════════════════════
# 10. Слайдер JS  (перед </body>)
# ════════════════════════════════════════════════════════════════════
SLIDER_JS = """
<script type='text/javascript'>
//<![CDATA[
(function(){
  var slides=document.querySelectorAll('.rot-slide');
  var dots=document.querySelectorAll('#rot-pager span');
  var geo=document.getElementById('rot-hero-geo');
  if(!slides.length)return;
  var cur=0,total=slides.length,timer;
  function goTo(n){
    slides[cur].classList.remove('active');
    if(dots[cur])dots[cur].classList.remove('active');
    cur=(n+total)%total;
    slides[cur].classList.add('active');
    if(dots[cur])dots[cur].classList.add('active');
    if(geo)geo.textContent=slides[cur].getAttribute('data-geo')||'';
  }
  function start(){timer=setInterval(function(){goTo(cur+1);},5000);}
  function stop(){clearInterval(timer);}
  var p=document.getElementById('rot-prev');
  var n=document.getElementById('rot-next');
  if(p)p.onclick=function(){goTo(cur-1);stop();start();};
  if(n)n.onclick=function(){goTo(cur+1);stop();start();};
  dots.forEach(function(d,i){d.onclick=function(){goTo(i);stop();start();};});
  start();
})();
//]]>
</script>
"""
COMMENT_FIX_JS = """
<script type='text/javascript'>
//<![CDATA[
(function(){
  function fixAll(){
    var sel = ['#comment-form','#comment-editor-container','#comment-editor'];
    sel.forEach(function(s){
      var el = document.querySelector(s);
      if(el){
        el.removeAttribute('width');
        el.style.setProperty('width','100%','important');
        el.style.setProperty('max-width','none','important');
        el.style.setProperty('min-width','0','important');
      }
    });
    // Все потомки контейнера с жёстко прописанной шириной
    var container = document.getElementById('comment-editor-container');
    if(container){
      container.querySelectorAll('*').forEach(function(el){
        var w = el.getAttribute('width');
        if(w) el.removeAttribute('width');
        var sw = el.style.width;
        if(sw && sw.indexOf('px') !== -1){
          el.style.setProperty('width','100%','important');
          el.style.setProperty('max-width','none','important');
        }
      });
    }
  }
  var obs = new MutationObserver(fixAll);
  obs.observe(document.body, {childList:true, subtree:true, attributes:true, attributeFilter:['width','style']});
  fixAll();
})();
//]]>
</script>
"""
VIEW_SWITCHER_JS = """
<script>
function rotSetView(v){
  var grid = document.querySelector('.rot-posts-grid');
  var btnCards = document.getElementById('btn-cards');
  var btnFeed  = document.getElementById('btn-feed');
  if(!grid) return;
  if(v === 'feed'){
    grid.classList.add('view-feed');
    if(btnCards) btnCards.classList.remove('active');
    if(btnFeed)  btnFeed.classList.add('active');
  } else {
    grid.classList.remove('view-feed');
    if(btnCards) btnCards.classList.add('active');
    if(btnFeed)  btnFeed.classList.remove('active');
  }
  try{ localStorage.setItem('rot-view', v); } catch(e){}
}
(function(){
  var saved;
  try{ saved = localStorage.getItem('rot-view'); } catch(e){}
  if(saved) rotSetView(saved);
})();
</script>
"""
LABEL_BANNER_JS = """
<script>
(function(){
  var m = location.pathname.match(/\\/search\\/label\\/([^?#\\/]+)/);
  if(!m) return;
  var label = decodeURIComponent(m[1]);
  if(!label) return;
  var grid = document.querySelector('.rot-posts-grid .blog-posts.hfeed');
  if(!grid) return;
  var banner = document.createElement('div');
  banner.className = 'rot-label-banner';
  banner.innerHTML = '\\u0420\\u0430\\u0437\\u0434\\u0435\\u043b: <span>' + label + '</span>';
  banner.style.display = 'block';
  grid.insertBefore(banner, grid.firstChild);
})();
</script>
"""
NAV_ACTIVE_JS = """
<script>
(function(){
  var path = location.pathname + location.search;
  var map = [
    ['rot-nav-dorogi',  'Дороги'],
    ['rot-nav-vremena', 'Времена'],
    ['rot-nav-goroda',  'Города'],
    ['rot-nav-muzei',   'Музеи'],
    ['rot-nav-ekspona', 'Экспонаты']
  ];
  var matched = false;
  map.forEach(function(pair){
    var label = encodeURIComponent(pair[1]);
    if(path.indexOf(label) !== -1 || path.indexOf(pair[1]) !== -1){
      var el = document.getElementById(pair[0]);
      if(el){ el.classList.add('rot-nav-active'); matched = true; }
    }
  });
  // Главная — только если это реально главная или архив, не статические страницы /p/
  if(!matched){
    if(path.indexOf('/p/') === -1){
      var home = document.getElementById('rot-nav-home');
      if(home) home.classList.add('rot-nav-active');
    }
  }
})();
</script>
"""
WIDGET_PLACEMENT_JS = """
<script>
(function(){
  // Переставляем toolbar в хедер, newsfeed в hero, dropmenu под хедер
  function placeWidgets(){
    var toolbar = document.getElementById('toolbar1');
    var target  = document.getElementById('rot-toolbar-target');
    if(toolbar){ if(target) target.appendChild(toolbar); }

    var newsfeed = document.getElementById('newsfeed1');
    var hero     = document.querySelector('.rot-hero');
    if(newsfeed){ if(hero){
      hero.insertBefore(newsfeed, hero.firstChild);
    }}

    var dropmenu = document.getElementById('dropmenu1');
    var header   = document.querySelector('.rot-header');
    if(dropmenu){ if(header){ if(header.parentNode){
      header.parentNode.insertBefore(dropmenu, header.nextSibling);
    }}}
  }
  function alignNewsfeed(){
    var hero     = document.querySelector('.rot-hero');
    var newsfeed = document.getElementById('newsfeed1');
    if(!hero){ return; } if(!newsfeed){ return; }
    var btn = hero.querySelector('.rot-hero-buttons a');
    if(!btn){ return; }
    var heroRect = hero.getBoundingClientRect();
    var btnRect  = btn.getBoundingClientRect();
    var scrollEl = newsfeed.querySelector('.rot-newsfeed-scroll');
    if(scrollEl){ scrollEl.style.marginLeft = (btnRect.left - heroRect.left - 10) + 'px'; }
  }
  function initWidgets(){
    placeWidgets();
    requestAnimationFrame(function(){ requestAnimationFrame(alignNewsfeed); });
  }
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initWidgets);
  } else {
    initWidgets();
  }
  window.addEventListener('resize', alignNewsfeed);
})();
</script>
"""
LATEST_POST_JS = """
<script>
(function(){
  var btn = document.getElementById('rot-btn-read');
  if(!btn){ return; }
  fetch('/feeds/posts/default?alt=json&amp;max-results=1')
    .then(function(r){ return r.json(); })
    .then(function(data){
      var entries = data.feed.entry;
      if(!entries || !entries.length){ return; }
      var links = entries[0].link || [];
      links.forEach(function(l){
        if(l.rel === 'alternate'){ btn.href = l.href; }
      });
    })
    .catch(function(){});
})();
</script>
"""
src = src.replace('</body>', SLIDER_JS + COMMENT_FIX_JS + VIEW_SWITCHER_JS + LABEL_BANNER_JS + NAV_ACTIVE_JS + WIDGET_PLACEMENT_JS + LATEST_POST_JS + '</body>')

# ════════════════════════════════════════════════════════════════════
# Убираем все AdSense-заглушки — они рендерятся как пустые <div>
# и вылетают в grid как первый пустой элемент на label-страницах
# ════════════════════════════════════════════════════════════════════
# Убираем все AdSense-блоки точными заменами
src = src.replace("      <data:defaultAdStart/>\n", "")
# <div style='clear:both'/> после status-msg-wrap — рендерится на label-страницах
# как пустой grid-item без класса (не ловится CSS-селектором)
src = src.replace("  <div style='clear: both;'/>\n", "")
src = src.replace(
    "        <b:if cond='data:post.includeAd'>\n"
    "          <b:if cond='data:post.isFirstPost'>\n"
    "            <data:defaultAdEnd/>\n"
    "          <b:else/>\n"
    "            <data:adEnd/>\n"
    "          </b:if>\n"
    "          <div class='inline-ad'>\n"
    "            <data:adCode/>\n"
    "          </div>\n"
    "          <data:adStart/>\n"
    "        </b:if>\n",
    ""
)
src = src.replace("      <data:adEnd/>\n", "")

# ════════════════════════════════════════════════════════════════════
# SAVE + VALIDATE
# ════════════════════════════════════════════════════════════════════
with open(DEST, 'w', encoding='utf-8') as f:
    f.write(src)

print("Saved:", DEST)
result = subprocess.run(['xmllint', '--noout', DEST], capture_output=True, text=True)
lines = [l for l in result.stderr.splitlines() if l.strip()]
if lines:
    print("XML issues:")
    for l in lines[:20]: print(" ", l)
else:
    print("XML: VALID ✓")
