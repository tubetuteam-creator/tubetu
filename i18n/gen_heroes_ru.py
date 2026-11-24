import os,html,json
ROOT='/home/claude/tubetu'
H=[
 dict(id='lisko',name='Лиско',lat='Lisko',group='hero',c='#FF8A1F',img='/games/img/full-lisko.webp',full=True,scene='/assets/lisko-lednik.jpg',
  role='Изобретатель, строитель и полиглот',age='12 лет',quote='Придумываю, строю, чиню — для команды!',
  facts=[('Характер','спокойный, умный, находчивый, уверенный'),('Любимая еда','рыба, орехи, энергетические батончики'),('Транспорт','сине-серебряный ховер-мотороллер с оранжевой подсветкой')],
  powers=['Изобретает, строит, чинит и улучшает любые устройства','Голограмма-невидимка: касается сенсора на перчатке — и становится прозрачным, как стекло','Знает все языки — людей, техники и природы'],
  about='Лиско — самый главный в команде TUBETU. Если что-то сломалось, он починит, а если такой штуки ещё нет — придумает. Не расстаётся с удочкой и жёлтыми перчатками.',color=True,game=0),
 dict(id='dobrik',name='Добрик',lat='Dobrik',group='hero',c='#8BD62A',img='/games/img/full-dobrik.webp',full=True,scene='/assets/dobrik.jpg',
  role='Разведчик, навигатор и связной',age='10 лет',quote='Быстрее, дальше, вместе!',
  facts=[('Характер','активный, смелый, любознательный, командный'),('Любимая еда','снеки, фрукты, энергетические батончики'),('Транспорт','деревянный ховерборд «Лесо» со светящимися листьями')],
  powers=['Скорость и манёвры — обгонит кого угодно','Навигация и разведка','Обмен мыслями: взяв друга за руку, слышит команду на расстоянии'],
  about='Добрик первым мчится вперёд и первым находит дорогу. Иногда слишком быстро — но всегда ради друзей.',color=True,game=1),
 dict(id='vionka',name='Вионка',lat='Vionka',group='hero',c='#8E3BF5',img='/games/img/full-vionka.webp',full=True,scene='/assets/vionka.jpg',
  role='Мастер волшебного вязания',age='',quote='Свяжу идею — и она оживёт!',
  facts=[('Характер','добрая, творческая, находчивая, смелая'),('Любимая еда','ягодный пирог и какао'),('Транспорт','фиолетово-золотая капсула-кресло с золотыми кольцами')],
  powers=['Всё, что она свяжет, становится настоящим: мосты, щит-купол, якорь, антенна','Золотые спицы и волшебное светящееся вязание','Серёжки смелости'],
  about='Вионка связала мишку Квасю — и он ожил! Её вязание спасает команду в самых трудных местах.',color=True,game=2),
 dict(id='asila',name='Асила',lat='Asila',group='hero',c='#FF3FA4',img='/games/img/full-asila.webp',full=True,scene='/assets/asila.jpg',
  role='Мастер музыки и хорошего настроения',age='9 лет',quote='Сладкие идеи делают мир добрее!',
  facts=[('Характер','весёлая, добрая, заботливая, энергичная'),('Любимая еда','чупа-чупсы, ягоды, десерты'),('Транспорт','розово-белый ховер-кар в виде кошки')],
  powers=['Волшебные чупа-чупсы: зелёный — говорить правду, розовый — танцевать, синий — хочется помогать, жёлтый — хохотать','Браслет с кнопкой выдаёт нужный леденец','Её песни заставляют танцевать даже дронов'],
  about='Асила всегда подмигивает и показывает «мир». Рядом с ней невозможно грустить.',color=True,game=3),
 dict(id='kvasya',name='Квася',lat='Kvasya',group='friend',c='#8BD62A',img='/assets/kvasya-tanets.jpg',scene='/assets/kvasya-sharf.jpg',
  role='Вязаный мишка, друг Вионки',quote='Ик! Это газировка… просится обратно!',facts=[('Характер','тихий неуклюжий добряк'),('Кто его создал','Вионка связала его своими спицами')],
  powers=['«Счастливое падение»: всё роняет — но всегда кстати'],about='Квася — настоящая вязаная игрушка крупной вязкой: салатовый, с бирюзовыми ушами и заплатками. Добрый и очень милый.'),
 dict(id='nyukh',name='Нюх',lat='Nyukh',group='friend',c='#FF8A1F',img='/assets/nyukh.jpg',scene='/assets/nyukh-kvasya2.jpg',
  role='Пёс с волшебным носом, друг Добрика',quote='Гав! Мой нос знает дорогу!',facts=[('Характер','добряк и обжора, всех любит'),('Любимое','пицца — всегда носит кусочек в кармане')],
  powers=['Волшебное чутьё: от носа идут голубые волны — найдёт что угодно'],about='Нюх ворует пиццу, поливает фикус Скота и облизывает всех подряд. Без него команде было бы скучно.'),
 dict(id='dyusha',name='Дюша',lat='Dyusha',group='friend',c='#2EA8FF',img='/assets/dyusha.jpg',scene='/assets/ukh2.jpg',
  role='Попугай-навигатор и курьер, друг Асилы',quote='Красавчик!',facts=[('Характер','болтун и паникёр'),('Работа','GPS и курьер команды')],
  powers=['Всегда летит впереди','Космический режим навигатора: на крыльях светятся карты'],about='Дюша всё время путает право и лево, а с него летят перья. Живёт в клетке с пятью замками и побаивается Скота.'),
 dict(id='shushik',name='Шушик',lat='Shushik',group='friend',c='#9FB4FF',img='/assets/shushik.jpg',scene='/assets/tunnel.jpg',
  role='Шиншилла-инженер, друг Лиско',quote='Объявляю сборы!',facts=[('Характер','деловой, ворчливый, вечно занят'),('Особенность','чихает от пыли')],
  powers=['Знает все туннели Скалы','Светящийся планшет с картой туннелей'],about='У Шушика огромные розовые уши, лётные очки и пояс с инструментами. Он собирается в поход дольше всех — зато «самый готовый».'),
 dict(id='skot',name='Скот',lat='Skot',group='friend',c='#8E3BF5',img='/assets/skot.jpg',scene='/assets/shtab.jpg',
  role='Кот, директор штаба',quote='Фрр!',facts=[('Характер','умный и стильный'),('Особенность','не разговаривает — только фыркает')],
  powers=['Следит за командой по большому экрану','Раздаёт советы — правда, не все верные'],about='Кот-«смокинг» с золотым моноклем и фиолетовой бабочкой. Больше всего боится испачкаться — и пачкается первым.'),
 dict(id='ukh',name='Ух',lat='Ukh',group='friend',c='#C89B6D',img='/assets/ukh2.jpg',scene='/assets/dver-bg.jpg',
  role='Совёнок, страж двери Скалы',quote='Ух-ух! Назови пароль!',facts=[('Характер','серьёзный страж — но засыпает на посту'),('Где живёт','в гнезде над дверью Скалы, среди старых книг')],
  powers=['Пускает в Скалу только своих','Объявляет каждую серию мультика'],about='Ух говорит очень важно, но постоянно засыпает. А когда Дюша будит его криком — падает из гнезда.',door=True),
 dict(id='snezhok',name='Снежок',lat='Snezhok',group='friend',c='#9FD8FF',img='/games/img/full-snezhok.webp',full=True,scene='/assets/lednik.jpg',
  role='Барсёнок-ирбис из снежных гор',quote='Мрр-р! Фрр!',facts=[('Характер','игривый, любопытный, неуклюжий'),('Особенность','не разговаривает — мурчит, фыркает и чихает')],
  powers=['Знает все горные тропы'],about='Снежок спал в сугробе, пока в него не влетел Добрик. Имя ему дала Асила. Носит красно-белый вязаный шарфик.',color=True),
 dict(id='skupshchik',name='Скупщик',lat='Skupshchik',group='villain',c='#8B5A2B',img='/games/img/full-skupshchik.webp',full=True,scene='/assets/skupshchik.jpg',
  role='Главный злодей — смешной, а не страшный',quote='Моё!',facts=[('Характер','хитрый, жадный, трусоватый'),('Слабость','всё бесплатное'),('Транспорт','тёмная капсула-капля со стеклянным куполом')],
  powers=['Командует дронами-воришками','Монеты в его карманах пищат, как резиновые уточки'],about='Скупщик хочет забрать себе все кристаллы Скалы и считает всё в деньгах: «А сколько это стоит?»'),
 dict(id='bugor',name='Бугор',lat='Bugor',group='villain',c='#E07A5F',img='/games/img/full-bugor.webp',full=True,scene='/assets/bugor.jpg',
  role='Грузчик шайки Скупщика',quote='Хозяин сказал — тащу!',facts=[('Характер','добрый, медлительный, очень сильный'),('Слабость','угощение — за него легко переходит на сторону добра')],
  powers=['Поднимет что угодно','Слушается того, кто громче'],about='Огромный добродушный кабан с мешком на плече. Совсем не злой — просто попал не в ту компанию.',color=True),
 dict(id='zhuzhzhalki',name='Жужжалки',lat='Drones',group='villain',c='#D62828',img='/assets/drony.jpg',scene='/assets/drony.jpg',
  role='Дроны-воришки',quote='Бзз! Хвать!',facts=[('Характер','весёлые, неуклюжие, любопытные'),('Слабость','музыка и смех — сразу пускаются в пляс')],
  powers=['Быстро летают и хватают всё подряд'],about='Круглые, с вмятинами, глазами-шариками и клешнями. Часто сталкиваются друг с другом. Песня Асилы для них — лучший концерт!'),
]
GROUPS={'hero':'Главные герои','friend':'Друзья команды','villain':'Смешные злодеи'}
CSS='''
:root{--navy:#0B1240;--sky:#EAF6FF;--ink:#1B1F3B;--muted:#5A6185;--gold:#FFC72C}
*{box-sizing:border-box}body{margin:0;font-family:Nunito,system-ui,sans-serif;background:var(--sky);color:var(--ink)}
img{max-width:100%;display:block}a{color:inherit}
.top{background:var(--navy);color:#fff;position:sticky;top:0;z-index:5}.top .w{display:flex;align-items:center;gap:10px;height:60px}
.top img{height:32px}.top .sp{flex:1}.top a.l{color:#fff;text-decoration:none;font-weight:800;background:rgba(255,255,255,.12);padding:7px 12px;border-radius:999px;font-size:14px}
.w{max-width:1100px;margin:0 auto;padding:0 16px}
.crumbs{font-weight:800;font-size:14px;color:var(--muted);margin:16px 0}
.crumbs a{color:var(--muted)}
.hero{display:grid;grid-template-columns:.9fr 1.1fr;gap:26px;align-items:center;background:#fff;border-radius:30px;padding:24px;box-shadow:0 10px 30px rgba(11,18,64,.08);border-top:8px solid var(--c)}
.pic{border-radius:24px;overflow:hidden;background:radial-gradient(circle at 50% 40%,#fff,color-mix(in srgb,var(--c) 22%,#fff));display:flex;align-items:center;justify-content:center;min-height:320px}
.pic img.full{max-height:460px;width:auto;padding:14px;filter:drop-shadow(0 12px 18px rgba(0,0,0,.2))}
.pic img.frame{width:100%;height:100%;object-fit:cover;aspect-ratio:4/3}
h1{font-size:clamp(34px,6vw,58px);font-weight:900;margin:0;color:var(--c);line-height:1}
.role{font-size:19px;font-weight:800;margin:8px 0 12px}
.q{font-size:22px;font-weight:900;font-style:italic;background:color-mix(in srgb,var(--c) 14%,#fff);border-radius:18px;padding:12px 16px;margin:0 0 14px}
.facts{display:grid;gap:8px}.facts div{display:flex;gap:8px;font-weight:700}.facts b{min-width:130px;color:var(--muted)}
.about{font-size:17px;font-weight:700;line-height:1.5;margin:14px 0 0}
h2{font-size:26px;font-weight:900;margin:32px 0 12px}
.powers{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.powers div{background:#fff;border-radius:20px;padding:16px;font-weight:800;border-left:6px solid var(--c);box-shadow:0 6px 18px rgba(11,18,64,.06)}
.scene{border-radius:24px;overflow:hidden;margin-top:10px}.scene img{width:100%;aspect-ratio:16/8;object-fit:cover}
.cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.btn{display:inline-block;text-decoration:none;font-weight:900;padding:12px 20px;border-radius:999px;background:var(--gold);color:var(--ink);box-shadow:0 5px 0 #C98F00}
.btn.alt{background:#fff;box-shadow:0 5px 0 #D7DDF2}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.mini{background:#fff;border-radius:20px;overflow:hidden;text-decoration:none;text-align:center;font-weight:900;box-shadow:0 6px 18px rgba(11,18,64,.06);border-bottom:5px solid var(--c);transition:transform .15s}
.mini:hover{transform:translateY(-3px)}
.mini .im{height:150px;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle,#fff,color-mix(in srgb,var(--c) 18%,#fff))}
.mini .im img{max-height:140px;width:auto}.mini .im img.frame{width:100%;height:150px;object-fit:cover;max-height:none}
.mini span{display:block;padding:10px;color:var(--c)}.mini small{display:block;color:var(--muted);font-weight:700;padding:0 8px 10px;margin-top:-6px}
footer{background:var(--navy);color:#C7CDF5;padding:22px 0;margin-top:40px;font-weight:700;font-size:14px}footer a{color:#fff}
@media(max-width:760px){.hero{grid-template-columns:1fr}.facts b{min-width:110px}}
'''
def head(title,desc,img,url):
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="https://tubetu.com{url}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="https://tubetu.com{img}"><meta property="og:type" content="website">
<meta name="theme-color" content="#0B1240"><link rel="icon" href="/icon.svg" type="image/svg+xml"><link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet"><style>{CSS}</style><link rel="apple-touch-icon" href="/assets/app-icon-180.png">
<link rel="manifest" href="/manifest.webmanifest">
</head><body>
<header class="top"><div class="w"><a href="/"><img src="/assets/logo.png" alt="TUBETU"></a><div class="sp"></div><a class="l" href="/geroi/">Все герои</a><a class="l" href="/games/">🎮 Игры</a></div></header>'''
FOOT='<footer><div class="w">© 2026 TUBETU · <a href="/">tubetu.com</a> · Мультсериал, где добро возвращается</div></footer><script src="/i18n/switch.js" defer></script></body></html>'
def mini(h):
    cls='' if h.get('full') else 'frame'
    return f'<a class="mini" style="--c:{h["c"]}" href="/geroi/{h["id"]}/"><div class="im"><img class="{cls}" src="{h["img"]}" alt="{h["name"]}" loading="lazy"></div><span>{h["name"]}</span><small>{h["role"]}</small></a>'
for h in H:
    url=f'/geroi/{h["id"]}/'
    desc=f'{h["name"]} — {h["role"].lower()} из мультсериала TUBETU «Скала сокровищ». {h["about"]}'[:300]
    imgcls='full' if h.get('full') else 'frame'
    facts=''.join(f'<div><b>{k}:</b><span>{v}</span></div>' for k,v in ([('Возраст',h['age'])] if h.get('age') else [])+h['facts'])
    powers=''.join(f'<div>⭐ {p}</div>' for p in h['powers'])
    cta=[]
    if h.get('color'):cta.append(f'<a class="btn" href="/raskraska/#{h["id"]}">🖌 Раскрасить {h["name"]}</a>' if h['group']!='villain' or h['id']=='bugor' else '')
    if 'game' in h:cta.append(f'<a class="btn" href="/games/?hero={h["game"]}">🎮 Играть за {h["name"]}</a>')
    if h.get('door'):cta.append('<a class="btn" href="/dver/">🔑 Назвать пароль Уху</a>')
    cta.append('<a class="btn alt" href="/games/pazl/">🧩 Пазл</a>')
    same=[x for x in H if x['group']==h['group'] and x['id']!=h['id']]
    others=[x for x in H if x['group']!=h['group']][:4]
    ld={"@context":"https://schema.org","@type":"WebPage","name":f'{h["name"]} — TUBETU',"description":desc,"url":"https://tubetu.com"+url,"isPartOf":{"@type":"WebSite","name":"TUBETU","url":"https://tubetu.com/"}}
    page=head(f'{h["name"]} — {h["role"]} | Мультсериал TUBETU',desc,h['img'] if not h['img'].endswith('webp') else h['scene'],url)+f'''
<main class="w"><div class="crumbs"><a href="/">TUBETU</a> › <a href="/geroi/">Герои</a> › {h["name"]}</div>
<section class="hero" style="--c:{h["c"]}"><div class="pic"><img class="{imgcls}" src="{h["img"]}" alt="{h["name"]} из мультсериала TUBETU"></div>
<div><h1>{h["name"]}</h1><div class="role">{h["role"]}</div><p class="q">«{h["quote"]}»</p><div class="facts">{facts}</div><p class="about">{h["about"]}</p><div class="cta">{"".join(cta)}</div></div></section>
<div style="--c:{h["c"]}"><h2>{"Суперсилы" if h["group"]=="hero" else "Умения"}</h2><div class="powers">{powers}</div>
<div class="scene"><img src="{h["scene"]}" alt="Кадр из мультсериала TUBETU" loading="lazy"></div></div>
<h2>{GROUPS[h["group"]]}</h2><div class="grid">{"".join(mini(x) for x in same)}</div>
<h2>Ещё в TUBETU</h2><div class="grid">{"".join(mini(x) for x in others)}</div>
</main><script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>'''+FOOT
    os.makedirs(f'{ROOT}/geroi/{h["id"]}',exist_ok=True)
    open(f'{ROOT}/geroi/{h["id"]}/index.html','w').write(page)
# index
sections=''.join(f'<h2>{GROUPS[g]}</h2><div class="grid">{"".join(mini(x) for x in H if x["group"]==g)}</div>' for g in ['hero','friend','villain'])
idx=head('Герои мультсериала TUBETU — Лиско, Добрик, Вионка, Асила и друзья','Все герои мультсериала TUBETU «Скала сокровищ»: Лиско, Добрик, Вионка, Асила, их друзья Квася, Нюх, Дюша, Шушик, Скот, Ух, Снежок и смешные злодеи.','/assets/komanda-poster.jpg','/geroi/')+f'''
<main class="w"><div class="crumbs"><a href="/">TUBETU</a> › Герои</div><h1 style="color:#0B1240">Герои TUBETU</h1>
<p class="about">Четыре друга, их помощники-звери и шайка Скупщика. Нажми на героя, чтобы узнать о нём всё!</p>{sections}</main>'''+FOOT
open(f'{ROOT}/geroi/index.html','w').write(idx)
print(len(H),'pages')

# ===== episode page =====
cast=[x for x in H if x['id'] in ('lisko','dobrik','vionka','asila','nyukh','kvasya','dyusha','shushik','skot','ukh','snezhok','skupshchik','bugor','zhuzhzhalki')]
ep=head('Серия 1 «Скала сокровищ» — мультсериал TUBETU','Первая серия мультсериала TUBETU «Скала сокровищ»: Мирошка зовёт на помощь, команда летит на ледник, а Скупщик охотится за кристаллами. Премьера 19 декабря 2026 на YouTube.','/assets/skala.jpg','/seriya-1/')+'''
<style>.cd{display:flex;gap:10px;justify-content:center;margin:14px 0}.cd div{background:#0B1240;color:#fff;border-radius:18px;padding:12px 0;width:84px;text-align:center}.cd b{display:block;font-size:34px;font-weight:900;color:#FFC72C}.cd span{font-size:12px;font-weight:800;opacity:.85}
.prem{background:linear-gradient(120deg,#0B1240,#3B2A86);color:#fff;border-radius:30px;padding:26px;text-align:center}.prem h1{color:#fff}.prem p{font-weight:700;opacity:.92}
video{width:100%;border-radius:24px;background:#000;display:block}
.story{background:#fff;border-radius:24px;padding:22px;font-size:17px;font-weight:700;line-height:1.6;box-shadow:0 6px 18px rgba(11,18,64,.06)}
.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.gal img{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:16px}
@media(max-width:700px){.gal{grid-template-columns:1fr 1fr}.cd div{width:70px}}</style>
<main class="w"><div class="crumbs"><a href="/">TUBETU</a> › Серия 1</div>
<section class="prem"><div style="font-weight:900;color:#FFC72C;letter-spacing:1px">СЕРИЯ 1</div><h1>Скала сокровищ</h1>
<p id="pt">Премьера на YouTube — суббота, 19 декабря 2026, в 19:00 (Алматы)</p>
<div class="cd" id="cd"><div><b id="dd">0</b><span>дней</span></div><div><b id="hh">0</b><span>часов</span></div><div><b id="mm">0</b><span>минут</span></div><div><b id="ss">0</b><span>секунд</span></div></div>
<div class="cta" style="justify-content:center"><a class="btn" href="https://www.youtube.com/@tubetuapp?sub_confirmation=1" target="_blank" rel="noopener">🔔 Подписаться и не пропустить</a><a class="btn alt" href="/dver/">🔑 Секретная дверь</a></div></section>
<h2>Заставка</h2><video src="/assets/zastavka.mp4" poster="/assets/zastavka-poster.jpg" controls playsinline preload="none"></video>
<h2>О чём серия</h2><div class="story">
<p>Утро в штабе внутри Скалы сокровищ начинается весело: Дюша будит совёнка Уха, Нюх опять поливает фикус Скота, а на завтрак — мороженое («Там же молоко!»).</p>
<p>Вдруг звенит тревога: на куполе мигает письмо. Мальчик Мирошка пишет, что его козлёнок упал в ледяную трещину, а сам он полез за ним — и застрял. «Пожалуйста, скорее!»</p>
<p>Лиско, Добрик, Вионка и Асила вылетают из Скалы — через водопад, снежный склон и ущелье. По дороге к ним присоединяется барсёнок Снежок. А тем временем Скупщик видит сияние на леднике: «Там кристаллы! Всё моё!» — и посылает своих дронов-жужжалок.</p>
<p>Успеют ли друзья спасти Мирошку? И что будет, когда в беду попадёт сам Скупщик? Смотрите премьеру — и помните: добро всегда возвращается.</p></div>
<h2>Кадры из серии</h2><div class="gal"><img src="/assets/shtab.jpg" alt="Штаб под куполом" loading="lazy"><img src="/assets/tunnel.jpg" alt="Взлётный туннель" loading="lazy"><img src="/assets/skala.jpg" alt="Скала сокровищ" loading="lazy"><img src="/assets/lednik.jpg" alt="Мирошка и козлёнок в ледяной трещине" loading="lazy"><img src="/assets/lisko-lednik.jpg" alt="Лиско на леднике" loading="lazy"><img src="/assets/komanda.jpg" alt="Вся команда" loading="lazy"></div>
<h2>Герои серии</h2><div class="grid">'''+''.join(mini(x) for x in cast)+'''</div>
</main>
<script>(function(){var T=Date.parse('2026-12-19T14:00:00Z');function f(){var d=Math.max(0,T-Date.now()),s=d/1000|0;document.getElementById('dd').textContent=s/86400|0;document.getElementById('hh').textContent=(s%86400)/3600|0;document.getElementById('mm').textContent=(s%3600)/60|0;document.getElementById('ss').textContent=s%60;if(d<=0){document.getElementById('pt').textContent='Премьера уже на YouTube — смотрите!';document.getElementById('cd').style.display='none';}}f();setInterval(f,1000);})();</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"TVEpisode","name":"Скала сокровищ","episodeNumber":1,"partOfSeries":{"@type":"TVSeries","name":"TUBETU"},"inLanguage":"ru","url":"https://tubetu.com/seriya-1/"}</script>'''+FOOT
open(f'{ROOT}/seriya-1/index.html','w').write(ep)
print('episode ok')
