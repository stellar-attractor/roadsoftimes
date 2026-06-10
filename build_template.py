#!/usr/bin/env python3
"""
Строим roadsoftimes.xml из GameTown XML (хирургическая замена).
Все Blogger-виджеты берутся из GameTown как есть — только CSS,
заголовок сайта, слайдер, шаблон карточки и футер заменяются.
"""
import re, subprocess

SRC  = "GameTown Blogger Template/GameTown Blogger Template.xml"
DEST = "template/roadsoftimes.xml"

with open(SRC, encoding="utf-8") as f:
    src = f.read()

# ════════════════════════════════════════════════════════════════════
# 1. GOOGLE FONTS
# ════════════════════════════════════════════════════════════════════
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
#outer-wrapper{width:100%!important;margin:0!important;padding:0!important;background:none!important;text-align:left}
#wrap2{width:100%}

/* ── HEADER ─────────────────────────────────────────────────────── */
.rot-header{background:#1e1d14;border-bottom:2px solid #8a6f2e;position:sticky;top:0;z-index:1000}
.rot-header-inner{display:flex;align-items:center;height:60px;gap:24px;max-width:1100px;margin:0 auto;padding:0 15px}
.rot-logo{display:flex;align-items:center;gap:10px;text-decoration:none;flex-shrink:0}
.rot-logo-emblem{width:36px;height:36px;border:2px solid #c9a84c;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;color:#c9a84c;font-family:'PT Mono',monospace;flex-shrink:0}
.rot-logo-title{font-family:'Oswald',sans-serif;font-size:15px;font-weight:600;color:#e2c06a;letter-spacing:1px;text-transform:uppercase;display:block}
.rot-logo-sub{font-size:9px;color:#7a7060;letter-spacing:2px;text-transform:uppercase;font-family:'PT Mono',monospace;display:block}
.rot-nav{flex:1}
.rot-nav ul{display:flex;list-style:none;gap:2px;margin:0;padding:0}
.rot-nav a{display:block;padding:8px 13px;font-family:'Oswald',sans-serif;font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:#c8c0a8;border-bottom:2px solid transparent;transition:color .2s,border-color .2s}
.rot-nav a:hover,.rot-nav-active a{color:#c9a84c;border-bottom-color:#c9a84c}
.rot-header-icons{display:flex;align-items:center;gap:10px;flex-shrink:0}
.rot-icon-btn{background:none;border:1px solid #3a3520;color:#7a7060;width:32px;height:32px;border-radius:3px;cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;transition:color .2s,border-color .2s}
.rot-icon-btn:hover{color:#c9a84c;border-color:#8a6f2e}

/* ── HERO SLIDER ─────────────────────────────────────────────────── */
.rot-hero{position:relative;width:100%;height:480px;overflow:hidden;background:#000}
.rot-slides{position:relative;width:100%;height:100%}
.rot-slide{position:absolute;top:0;left:0;right:0;bottom:0;opacity:0;transition:opacity .8s ease}
.rot-slide.active{opacity:1}
.rot-slide img{display:block;width:100%;height:100%;object-fit:cover;object-position:center 40%;filter:brightness(.42)}
.rot-slide::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:linear-gradient(to right,rgba(10,9,5,.93) 0%,rgba(10,9,5,.58) 45%,rgba(10,9,5,.08) 100%)}
.rot-hero-content{position:absolute;top:50%;left:0;transform:translateY(-50%);width:100%;z-index:10}
.rot-hero-inner{max-width:1100px;margin:0 auto;padding:0 15px}
.rot-hero-eyebrow{font-family:'PT Mono',monospace;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#8a6f2e;margin-bottom:8px}
.rot-hero-title{font-family:'Oswald',sans-serif;font-size:52px;font-weight:700;line-height:1.0;color:#e8e0cc;text-transform:uppercase;letter-spacing:2px;margin-bottom:14px;max-width:540px;text-shadow:0 2px 20px rgba(0,0,0,.8)}
.rot-hero-desc{font-size:14px;color:#c8c0a8;max-width:420px;line-height:1.65;margin-bottom:28px}
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
/* content-wrapper — grid-контейнер. Дочерние элементы:
   1) .rot-hero  → grid-column:1/-1 → полная ширина, строка 1
   2) #crosscol-wrapper → display:none, не grid-item
   3) #main-wrapper → колонка 1fr, строка 2
   4) #rsidebar-wrapper → колонка 300px, строка 2 */
#content-wrapper{max-width:1100px!important;margin:24px auto 0!important;padding:0 15px!important;display:grid!important;grid-template-columns:1fr 300px!important;gap:0 24px!important;align-items:start!important;background:none!important}
/* Герой: растягиваем на обе колонки и убираем боковые отступы */
.rot-hero{grid-column:1/-1!important;margin:0 -15px!important;width:calc(100% + 30px)!important}
#crosscol-wrapper{display:none!important}
#main-wrapper{width:auto!important;float:none!important;min-width:0;padding-top:24px}
#rsidebar-wrapper{width:auto!important;float:none!important;min-width:0;padding-top:24px}

/* ── POST CARDS ─────────────────────────────────────────────────── */
.rot-section-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid #3a3520}
.rot-section-title{font-family:'Oswald',sans-serif;font-size:16px;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:#e8e0cc;display:flex;align-items:center;gap:8px}
.rot-section-title::before{content:'';display:inline-block;width:3px;height:16px;background:#c9a84c}
.rot-section-link{font-family:'PT Mono',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#7a7060;border:1px solid #252418;padding:4px 10px;transition:color .2s,border-color .2s}
.rot-section-link:hover{color:#c9a84c;border-color:#8a6f2e}
/* ── Сетка карточек постов ──────────────────────────────────────── */
/* Между .rot-posts-grid и <article> есть куча обёрток Blogger:
   .widget.Blog > .blog-posts.hfeed > .date-outer > .date-posts > .post-outer > article
   Делаем все промежуточные слои прозрачными через display:contents,
   тогда article.rot-post-card становятся прямыми grid-items */
.rot-posts-grid{display:grid!important;grid-template-columns:repeat(3,1fr)!important;gap:16px!important}
.rot-posts-grid .widget.Blog,
.rot-posts-grid .blog-posts.hfeed,
.rot-posts-grid .date-outer,
.rot-posts-grid .date-posts,
.rot-posts-grid .post-outer{display:contents!important}
/* Скрываем заголовки дат — они не нужны в карточечной сетке */
.rot-posts-grid .date-header{display:none!important}
/* Пагинация вытаскивается отдельно поверх сетки */
.rot-posts-grid .blog-pager{grid-column:1/-1}
.rot-post-card{background:#1a1a0e;border:1px solid #252418;overflow:hidden;transition:border-color .2s;display:flex;flex-direction:column}
.rot-post-card:hover{border-color:#8a6f2e}
.rot-card-thumb{position:relative;height:160px;overflow:hidden;flex-shrink:0;background:#232318}
.rot-card-thumb img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .4s ease}
.rot-post-card:hover .rot-card-thumb img{transform:scale(1.05)}
.rot-tag{position:absolute;top:10px;left:10px;font-family:'PT Mono',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;padding:3px 8px;z-index:2;background:#2a0f0f;color:#ae6a5a;border:1px solid #ae6a5a}
.rot-card-body{padding:14px;flex:1;display:flex;flex-direction:column}
.rot-card-title{font-family:'Oswald',sans-serif;font-size:16px;font-weight:500;color:#e8e0cc;line-height:1.25;margin-bottom:8px}
.rot-card-title a{color:inherit;transition:color .2s}
.rot-card-title a:hover{color:#c9a84c}
.rot-card-excerpt{font-size:12px;color:#7a7060;line-height:1.55;margin-bottom:12px;flex:1}
.rot-card-excerpt img{display:none}
.rot-card-meta{display:flex;align-items:center;gap:12px;font-family:'PT Mono',monospace;font-size:10px;color:#7a7060;border-top:1px solid #252418;padding-top:10px;flex-wrap:wrap}
.rot-card-labels a{font-family:'PT Mono',monospace;font-size:9px;text-transform:uppercase;letter-spacing:1px;padding:2px 7px;border:1px solid #3a3520;color:#8a6f2e;margin-right:4px}
.rot-card-labels a:hover{color:#c9a84c;border-color:#8a6f2e}
/* Blog pager */
.blog-pager{display:flex;justify-content:space-between;align-items:center;padding:16px 0;border-top:1px solid #3a3520;margin-top:10px;background:none}
.blog-pager a,.blog-pager-newer-link,.blog-pager-older-link{font-family:'Oswald',sans-serif;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#7a7060;border:1px solid #252418;padding:6px 14px;transition:color .2s,border-color .2s}
.blog-pager a:hover{color:#c9a84c;border-color:#8a6f2e}
.blog-posts.hfeed{padding:0}

/* ── Контейнер под grid (Featured Museum + Choose Path) ─────────── */
.rot-below-grid{max-width:1100px;margin:24px auto 0;padding:0 15px}

/* ── FEATURED MUSEUM ────────────────────────────────────────────── */
.rot-featured-museum{margin-bottom:28px;background:#1a1a0e;border:1px solid #252418;overflow:hidden;clear:both}
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

/* ── CHOOSE PATH ────────────────────────────────────────────────── */
.rot-choose-path{margin-bottom:28px;clear:both}
.rot-path-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.rot-path-card{background:#1a1a0e;border:1px solid #252418;padding:20px 14px;text-align:center;transition:border-color .2s,background .2s;text-decoration:none;display:block}
.rot-path-card:hover{border-color:#8a6f2e;background:#232318}
.rot-path-icon{font-size:26px;margin-bottom:10px;display:block}
.rot-path-title{font-family:'Oswald',sans-serif;font-size:13px;font-weight:500;text-transform:uppercase;letter-spacing:1.5px;color:#e8e0cc;margin-bottom:5px}
.rot-path-desc{font-size:11px;color:#7a7060;line-height:1.4}

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

/* ── FOOTER ──────────────────────────────────────────────────────── */
#footer-widgets-container{display:none}
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
"""

skin_re = re.compile(r'<b:skin><!\[CDATA\[.*?\]\]></b:skin>', re.DOTALL)
src = skin_re.sub('<b:skin><![CDATA[\n' + NEW_CSS + '\n]]></b:skin>', src)

# ════════════════════════════════════════════════════════════════════
# 3. Summary JS helper  (добавляем перед </head>)
# ════════════════════════════════════════════════════════════════════
SUMMARY_JS = """<script type='text/javascript'>
//<![CDATA[
var summary_noimg=200,summary_img=200;
function removeHtmlTag(s,n){var a=s.split("<");for(var i=0;i<a.length;i++){a[i]=a[i].substring(a[i].indexOf(">")+1);}s=a.join("");return s.substring(0,n-3)+"...";}
function createSummaryAndThumb(id){
  var d=document.getElementById(id);
  var img=d.getElementsByTagName("img");
  var t=img.length>=1?'<img src="'+img[0].src+'" style="display:none"/>':'';
  d.innerHTML=t+"<span>"+removeHtmlTag(d.innerHTML,img.length>=1?summary_img:summary_noimg)+"</span>";
}
//]]>
</script>
"""
src = src.replace('</head>', SUMMARY_JS + '</head>')

# ════════════════════════════════════════════════════════════════════
# 4. Вставляем наш HEADER после <body> и перед <div id='body-wrapper'>
#    Завершённый блок — никаких висящих div
# ════════════════════════════════════════════════════════════════════
OUR_HEADER = """
<!-- ═══ ДОРОГИ ВРЕМЁН: HEADER ════════════════════════════════════ -->
<div class='rot-header'>
  <div class='rot-header-inner'>
    <a class='rot-logo' expr:href='data:blog.homepageUrl'>
      <div class='rot-logo-emblem'>&#8853;</div>
      <div>
        <span class='rot-logo-title'>&#1044;&#1086;&#1088;&#1086;&#1075;&#1080; &#1042;&#1088;&#1077;&#1084;&#1105;&#1085;</span>
        <span class='rot-logo-sub'>&#1055;&#1091;&#1090;&#1077;&#1096;&#1077;&#1089;&#1090;&#1074;&#1080;&#1103; &#183; &#1052;&#1091;&#1079;&#1077;&#1080; &#183; &#1048;&#1089;&#1090;&#1086;&#1088;&#1080;&#1103;</span>
      </div>
    </a>
    <nav class='rot-nav'>
      <ul>
        <li class='rot-nav-active'><a expr:href='data:blog.homepageUrl'>&#1043;&#1083;&#1072;&#1074;&#1085;&#1072;&#1103;</a></li>
        <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%AD%D0%BA%D1%81%D0%BF%D0%B5%D0%B4%D0%B8%D1%86%D0%B8%D0%B8&quot;'>&#1069;&#1082;&#1089;&#1087;&#1077;&#1076;&#1080;&#1094;&#1080;&#1080;</a></li>
        <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%9C%D1%83%D0%B7%D0%B5%D0%B8&quot;'>&#1052;&#1091;&#1079;&#1077;&#1080;</a></li>
        <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%90%D1%80%D1%82%D0%B5%D1%84%D0%B0%D0%BA%D1%82%D1%8B&quot;'>&#1040;&#1088;&#1090;&#1077;&#1092;&#1072;&#1082;&#1090;&#1099;</a></li>
        <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F&quot;'>&#1048;&#1089;&#1090;&#1086;&#1088;&#1080;&#1103;</a></li>
      </ul>
    </nav>
    <div class='rot-header-icons'>
      <button class='rot-icon-btn' onclick='javascript:void(0)'>&#128269;</button>
    </div>
  </div>
</div>
<!-- ═══ END HEADER ═══════════════════════════════════════════════ -->
"""
src = src.replace('<body>\n\n<div id=\'body-wrapper\'>', '<body>\n' + OUR_HEADER + '\n<div id=\'body-wrapper\'>')

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
      <img alt='Panzer 38(t)' src='SLIDE-1-IMAGE-URL-HERE'/>
    </div>
    <div class='rot-slide' data-geo='&#1052;&#1091;&#1079;&#1077;&#1081;-&#1079;&#1072;&#1074;&#1086;&#1076; &#1055;&#1077;&#1085;&#1077;&#1084;&#1102;&#1085;&#1076;&#1077;, &#1043;&#1077;&#1088;&#1084;&#1072;&#1085;&#1080;&#1103;'>
      <img alt='&#1056;&#1072;&#1082;&#1077;&#1090;&#1072; V-2' src='SLIDE-2-IMAGE-URL-HERE'/>
    </div>
    <div class='rot-slide' data-geo='&#1052;&#1086;&#1088;&#1089;&#1082;&#1086;&#1081; &#1084;&#1091;&#1079;&#1077;&#1081;, &#1042;&#1080;&#1083;&#1100;&#1075;&#1077;&#1083;&#1100;&#1084;&#1089;&#1093;&#1072;&#1092;&#1077;&#1085;'>
      <img alt='&#1054;&#1088;&#1091;&#1076;&#1080;&#1081;&#1085;&#1072;&#1103; &#1073;&#1072;&#1096;&#1085;&#1103;' src='SLIDE-3-IMAGE-URL-HERE'/>
    </div>
  </div>
  <div class='rot-hero-content'>
    <div class='rot-hero-inner'>
      <p class='rot-hero-eyebrow'>&#1040;&#1074;&#1090;&#1086;&#1088;&#1089;&#1082;&#1080;&#1081; &#1073;&#1083;&#1086;&#1075; &#1086; &#1074;&#1086;&#1077;&#1085;&#1085;&#1086;&#1081; &#1080;&#1089;&#1090;&#1086;&#1088;&#1080;&#1080;</p>
      <h1 class='rot-hero-title'>&#1044;&#1086;&#1088;&#1086;&#1075;&#1080; &#1042;&#1088;&#1077;&#1084;&#1105;&#1085;</h1>
      <p class='rot-hero-desc'>&#1055;&#1091;&#1090;&#1077;&#1096;&#1077;&#1089;&#1090;&#1074;&#1080;&#1103; &#1087;&#1086; &#1084;&#1077;&#1089;&#1090;&#1072;&#1084;, &#1075;&#1076;&#1077; &#1080;&#1089;&#1090;&#1086;&#1088;&#1080;&#1103; &#1086;&#1078;&#1080;&#1074;&#1072;&#1077;&#1090;. &#1052;&#1091;&#1079;&#1077;&#1080;, &#1072;&#1088;&#1090;&#1077;&#1092;&#1072;&#1082;&#1090;&#1099;, &#1089;&#1091;&#1076;&#1100;&#1073;&#1099;.</p>
      <div class='rot-hero-buttons'>
        <a class='rot-btn rot-btn-primary' expr:href='data:blog.homepageUrl'>&#1063;&#1080;&#1090;&#1072;&#1090;&#1100; &#8250;</a>
        <a class='rot-btn rot-btn-outline' href='/p/about.html'>&#1054; &#1087;&#1088;&#1086;&#1077;&#1082;&#1090;&#1077;</a>
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
    src = src[:old_slider_match.start()] + NEW_HERO + src[old_slider_match.end():]

# ════════════════════════════════════════════════════════════════════
# 6. Section header + rot-posts-grid внутри main-wrapper
#    Никаких новых HTML-обёрток — только CSS делает grid
# ════════════════════════════════════════════════════════════════════

OLD_MAIN_SECTION = "<b:section class='main' id='main' showaddelement='no'>"
NEW_MAIN_SECTION = """\
<div class='rot-section-header'>
  <h2 class='rot-section-title'>&#1055;&#1086;&#1089;&#1083;&#1077;&#1076;&#1085;&#1080;&#1077; &#1087;&#1091;&#1073;&#1083;&#1080;&#1082;&#1072;&#1094;&#1080;&#1080;</h2>
  <a class='rot-section-link' expr:href='data:blog.homepageUrl'>&#1042;&#1089;&#1077; &#8594;</a>
</div>
<div class='rot-posts-grid'>
<b:section class='main' id='main' showaddelement='no'>"""
src = src.replace(OLD_MAIN_SECTION, NEW_MAIN_SECTION)

# Закрываем rot-posts-grid — оригинальный </div> GameTown закрывает main-wrapper,
# поэтому нам нужен дополнительный </div> перед ним
src = src.replace(
    "        </b:section>\n      </div>\n\n<div id='rsidebar-wrapper'>",
    "        </b:section>\n</div><!-- /.rot-posts-grid -->\n      </div><!-- /#main-wrapper -->\n\n<div id='rsidebar-wrapper'>"
)

# ════════════════════════════════════════════════════════════════════
# 7. Featured Museum + Choose Path — вставляем ПОСЛЕ content-wrapper
#    (не внутри grid), перед footer-widgets-container.
#    Оборачиваем в rot-below-grid с max-width 1100px.
# ════════════════════════════════════════════════════════════════════
EXTRA_BLOCKS = """\

<!-- ═══ FEATURED MUSEUM + CHOOSE PATH (вне grid) ════════════════ -->
<div class='rot-below-grid'>

<div class='rot-featured-museum'>
  <div class='rot-block-header'>
    <span class='rot-section-title' style='font-size:13px'>&#1056;&#1077;&#1082;&#1086;&#1084;&#1077;&#1085;&#1076;&#1091;&#1077;&#1084;&#1099;&#1081; &#1084;&#1091;&#1079;&#1077;&#1081;</span>
    <a class='rot-section-link' href='#'>&#1042;&#1089;&#1077; &#1084;&#1091;&#1079;&#1077;&#1080; &#8594;</a>
  </div>
  <div class='rot-museum-inner'>
    <div class='rot-museum-photo'><img alt='Museum' src='MUSEUM-IMAGE-URL-HERE'/></div>
    <div class='rot-museum-body'>
      <div>
        <p class='rot-museum-label'>&#128205; &#1052;&#1102;&#1085;&#1089;&#1090;&#1077;&#1088;, &#1043;&#1077;&#1088;&#1084;&#1072;&#1085;&#1080;&#1103;</p>
        <h3 class='rot-museum-title'>Deutsches Panzermuseum Munster</h3>
        <p class='rot-museum-desc'>&#1054;&#1076;&#1085;&#1086; &#1080;&#1079; &#1082;&#1088;&#1091;&#1087;&#1085;&#1077;&#1081;&#1096;&#1080;&#1093; &#1090;&#1072;&#1085;&#1082;&#1086;&#1074;&#1099;&#1093; &#1084;&#1091;&#1079;&#1077;&#1077;&#1074; &#1084;&#1080;&#1088;&#1072;. &#1041;&#1086;&#1083;&#1077;&#1077; 300 &#1077;&#1076;&#1080;&#1085;&#1080;&#1094; &#1090;&#1077;&#1093;&#1085;&#1080;&#1082;&#1080;.</p>
      </div>
      <div>
        <div class='rot-museum-stats'>
          <div class='rot-stat'><span class='rot-stat-icon'>&#128710;</span><span class='rot-stat-val'>&#1073;&#1077;&#1089;&#1087;&#1083;&#1072;&#1090;&#1085;&#1086;</span><span class='rot-stat-label'>&#1074;&#1093;&#1086;&#1076;</span></div>
          <div class='rot-stat'><span class='rot-stat-icon'>&#128336;</span><span class='rot-stat-val'>10:00&#8211;18:00</span><span class='rot-stat-label'>&#1095;&#1072;&#1089;&#1099;</span></div>
          <div class='rot-stat'><span class='rot-stat-icon'>&#128197;</span><span class='rot-stat-val'>1971</span><span class='rot-stat-label'>&#1086;&#1089;&#1085;&#1086;&#1074;&#1072;&#1085;</span></div>
        </div>
        <a class='rot-btn rot-btn-outline' href='#' style='font-size:12px;padding:8px 18px'>&#1055;&#1086;&#1076;&#1088;&#1086;&#1073;&#1085;&#1077;&#1077; &#8250;</a>
      </div>
    </div>
  </div>
</div>

<div class='rot-choose-path'>
  <div class='rot-section-header'>
    <h2 class='rot-section-title'>&#1042;&#1099;&#1073;&#1077;&#1088;&#1080;&#1090;&#1077; &#1089;&#1074;&#1086;&#1081; &#1087;&#1091;&#1090;&#1100;</h2>
  </div>
  <div class='rot-path-grid'>
    <a class='rot-path-card' expr:href='data:blog.homepageUrl + &quot;search/label/%D0%AD%D0%BA%D1%81%D0%BF%D0%B5%D0%B4%D0%B8%D1%86%D0%B8%D0%B8&quot;'>
      <span class='rot-path-icon'>&#9876;&#65039;</span>
      <div class='rot-path-title'>&#1069;&#1082;&#1089;&#1087;&#1077;&#1076;&#1080;&#1094;&#1080;&#1080;</div>
      <p class='rot-path-desc'>&#1055;&#1086;&#1083;&#1077;&#1074;&#1099;&#1077; &#1088;&#1077;&#1087;&#1086;&#1088;&#1090;&#1072;&#1078;&#1080;</p>
    </a>
    <a class='rot-path-card' expr:href='data:blog.homepageUrl + &quot;search/label/%D0%9C%D1%83%D0%B7%D0%B5%D0%B8&quot;'>
      <span class='rot-path-icon'>&#127963;&#65039;</span>
      <div class='rot-path-title'>&#1052;&#1091;&#1079;&#1077;&#1080;</div>
      <p class='rot-path-desc'>&#1050;&#1086;&#1083;&#1083;&#1077;&#1082;&#1094;&#1080;&#1080;</p>
    </a>
    <a class='rot-path-card' expr:href='data:blog.homepageUrl + &quot;search/label/%D0%90%D1%80%D1%82%D0%B5%D1%84%D0%B0%D0%BA%D1%82%D1%8B&quot;'>
      <span class='rot-path-icon'>&#129680;</span>
      <div class='rot-path-title'>&#1040;&#1088;&#1090;&#1077;&#1092;&#1072;&#1082;&#1090;&#1099;</div>
      <p class='rot-path-desc'>&#1058;&#1077;&#1093;&#1085;&#1080;&#1082;&#1072;</p>
    </a>
    <a class='rot-path-card' expr:href='data:blog.homepageUrl + &quot;search/label/%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F&quot;'>
      <span class='rot-path-icon'>&#128220;</span>
      <div class='rot-path-title'>&#1048;&#1089;&#1090;&#1086;&#1088;&#1080;&#1103;</div>
      <p class='rot-path-desc'>&#1057;&#1086;&#1073;&#1099;&#1090;&#1080;&#1103;</p>
    </a>
  </div>
</div>

</div><!-- /.rot-below-grid -->
<!-- ═══ END EXTRA BLOCKS ══════════════════════════════════════════ -->
"""

# Вставляем после content-wrapper, перед footer-widgets-container
src = src.replace(
    "<div style='clear:both;'/>\n<div id='footer-widgets-container'>",
    EXTRA_BLOCKS + "<div style='clear:both;'/>\n<div id='footer-widgets-container'>"
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
    <h3 class='rot-card-title'><a expr:href='data:post.url'><data:post.title/></a></h3>
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
      <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%AD%D0%BA%D1%81%D0%BF%D0%B5%D0%B4%D0%B8%D1%86%D0%B8%D0%B8&quot;'>&#1069;&#1082;&#1089;&#1087;&#1077;&#1076;&#1080;&#1094;&#1080;&#1080;</a></li>
      <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%9C%D1%83%D0%B7%D0%B5%D0%B8&quot;'>&#1052;&#1091;&#1079;&#1077;&#1080;</a></li>
      <li><a expr:href='data:blog.homepageUrl + &quot;search/label/%D0%90%D1%80%D1%82%D0%B5%D1%84%D0%B0%D0%BA%D1%82%D1%8B&quot;'>&#1040;&#1088;&#1090;&#1077;&#1092;&#1072;&#1082;&#1090;&#1099;</a></li>
    </ul>
  </div>
  <div>
    <p class='rot-footer-col-title'>&#1048;&#1085;&#1092;&#1086;&#1088;&#1084;&#1072;&#1094;&#1080;&#1103;</p>
    <ul class='rot-footer-links'>
      <li><a href='/p/about.html'>&#1054; &#1087;&#1088;&#1086;&#1077;&#1082;&#1090;&#1077;</a></li>
      <li><a href='/p/contacts.html'>&#1050;&#1086;&#1085;&#1090;&#1072;&#1082;&#1090;&#1099;</a></li>
      <li><a expr:href='data:blog.homepageUrl + &quot;feeds/posts/default&quot;'>RSS</a></li>
    </ul>
  </div>
  <div>
    <p class='rot-footer-col-title'>&#1057;&#1083;&#1077;&#1076;&#1080;&#1090;&#1077; &#1079;&#1072; &#1085;&#1072;&#1084;&#1080;</p>
    <ul class='rot-footer-links'>
      <li><a href='#'>VK</a></li>
      <li><a href='#'>Telegram</a></li>
      <li><a href='#'>YouTube</a></li>
    </ul>
  </div>
</div>
<div class='rot-footer-bottom-bar'>
  <div class='rot-footer-bottom'>
    <span>&#169; 2026 &#1044;&#1086;&#1088;&#1086;&#1075;&#1080; &#1042;&#1088;&#1077;&#1084;&#1105;&#1085;</span>
    <div><a href='#' style='color:#7a7060;margin-right:10px'>VK</a><a href='#' style='color:#7a7060;margin-right:10px'>TG</a><a href='#' style='color:#7a7060'>YT</a></div>
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
src = src.replace('</body>', SLIDER_JS + '</body>')

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
