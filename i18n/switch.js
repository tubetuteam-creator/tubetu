/* Яндекс Метрика: только подсчёт посещений (без Вебвизора). Счётчик 114653877 */
(function(m,e,t,r,i,k,a){
if(!/(^|\.)tubetu\.com$/.test(location.hostname))return;
m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();
for(var j=0;j<e.scripts.length;j++){if(e.scripts[j].src===r)return;}
k=e.createElement(t);a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);
m[i](114653877,'init',{ssr:true,webvisor:false,clickmap:true,referrer:e.referrer,url:location.href,accurateTrackBounce:true,trackLinks:true});
})(window,document,'script','https://mc.yandex.ru/metrika/tag.js?id=114653877','ym');
/* TUBETU: кнопки «Поделиться», «Установить на телефон» и выбор языка — на всех страницах */
(function(){
var L=[['ru','Русский'],['kz','Қазақша'],['en','English'],['tr','Türkçe'],['zh','中文'],['es','Español'],['hi','हिन्दी'],['sw','Kiswahili'],['pt','Português'],['ar','العربية']];
var codes=L.map(function(x){return x[0];});
var m=location.pathname.match(/^\/([a-z]{2})(\/.*)$/),cur='ru',base=location.pathname;
if(m&&codes.indexOf(m[1])>0){cur=m[1];base=m[2];}
function url(c){return (c==='ru'?'':'/'+c)+base+location.search+location.hash;}
var T={
ru:{share:'Поделиться',copied:'Ссылка скопирована!',inst:'Установить',instT:'TUBETU на экран телефона',ios:'Нажмите внизу кнопку <b>«Поделиться»</b> <span class="ic">⬆️</span>, потом <b>«На экран Домой»</b> ➕',and:'Откройте меню браузера <b>⋮</b> и выберите <b>«Добавить на главный экран»</b> или <b>«Установить приложение»</b>',ok:'Понятно',txt:'TUBETU — мультик, где добро возвращается! Игры, раскраски и герои:'},
kz:{share:'Бөлісу',copied:'Сілтеме көшірілді!',inst:'Орнату',instT:'TUBETU телефон экранына',ios:'Төмендегі <b>«Бөлісу»</b> <span class="ic">⬆️</span> батырмасын басып, <b>«Басты экранға»</b> ➕ таңдаңыз',and:'Браузер мәзірін <b>⋮</b> ашып, <b>«Басты экранға қосу»</b> немесе <b>«Қолданбаны орнату»</b> таңдаңыз',ok:'Түсінікті',txt:'TUBETU — мейірім қайтып оралатын мультфильм! Ойындар, бояулар, кейіпкерлер:'},
en:{share:'Share',copied:'Link copied!',inst:'Install',instT:'TUBETU on your home screen',ios:'Tap <b>Share</b> <span class="ic">⬆️</span> at the bottom, then <b>Add to Home Screen</b> ➕',and:'Open the browser menu <b>⋮</b> and choose <b>Add to Home screen</b> or <b>Install app</b>',ok:'Got it',txt:'TUBETU — a cartoon where kindness comes back! Games, coloring and heroes:'},
tr:{share:'Paylaş',copied:'Bağlantı kopyalandı!',inst:'Yükle',instT:'TUBETU ana ekranda',ios:'Alttaki <b>Paylaş</b> <span class="ic">⬆️</span> düğmesine, sonra <b>Ana Ekrana Ekle</b> ➕ seçeneğine dokunun',and:'Tarayıcı menüsünü <b>⋮</b> açın ve <b>Ana ekrana ekle</b> veya <b>Uygulamayı yükle</b> seçin',ok:'Tamam',txt:'TUBETU — iyiliğin geri döndüğü çizgi film! Oyunlar, boyama ve kahramanlar:'},
zh:{share:'分享',copied:'链接已复制！',inst:'安装',instT:'把TUBETU放到手机桌面',ios:'点底部的<b>分享</b> <span class="ic">⬆️</span>，再点<b>添加到主屏幕</b> ➕',and:'打开浏览器菜单 <b>⋮</b>，选择<b>添加到主屏幕</b>或<b>安装应用</b>',ok:'知道了',txt:'TUBETU——善良总会回来的动画片！游戏、涂色和角色：'},
es:{share:'Compartir',copied:'¡Enlace copiado!',inst:'Instalar',instT:'TUBETU en tu pantalla de inicio',ios:'Toca <b>Compartir</b> <span class="ic">⬆️</span> abajo y luego <b>Añadir a pantalla de inicio</b> ➕',and:'Abre el menú del navegador <b>⋮</b> y elige <b>Añadir a pantalla de inicio</b> o <b>Instalar aplicación</b>',ok:'Entendido',txt:'TUBETU — ¡una serie donde la bondad regresa! Juegos, dibujos y héroes:'},
hi:{share:'शेयर',copied:'लिंक कॉपी हो गया!',inst:'इंस्टॉल',instT:'TUBETU को होम स्क्रीन पर लाएँ',ios:'नीचे <b>शेयर</b> <span class="ic">⬆️</span> दबाएँ, फिर <b>होम स्क्रीन पर जोड़ें</b> ➕',and:'ब्राउज़र मेनू <b>⋮</b> खोलें और <b>होम स्क्रीन पर जोड़ें</b> या <b>ऐप इंस्टॉल करें</b> चुनें',ok:'ठीक है',txt:'TUBETU — एक कार्टून जहाँ अच्छाई लौटकर आती है! गेम, रंग भरना और हीरो:'},
sw:{share:'Shiriki',copied:'Kiungo kimenakiliwa!',inst:'Sakinisha',instT:'TUBETU kwenye skrini ya simu',ios:'Gusa <b>Shiriki</b> <span class="ic">⬆️</span> chini, kisha <b>Ongeza kwenye Skrini ya Mwanzo</b> ➕',and:'Fungua menyu ya kivinjari <b>⋮</b> na uchague <b>Ongeza kwenye skrini ya mwanzo</b> au <b>Sakinisha programu</b>',ok:'Sawa',txt:'TUBETU — katuni ambapo wema hurudi! Michezo, kupaka rangi na mashujaa:'},
pt:{share:'Compartilhar',copied:'Link copiado!',inst:'Instalar',instT:'TUBETU na tela inicial',ios:'Toque em <b>Compartilhar</b> <span class="ic">⬆️</span> embaixo e depois em <b>Adicionar à Tela de Início</b> ➕',and:'Abra o menu do navegador <b>⋮</b> e escolha <b>Adicionar à tela inicial</b> ou <b>Instalar app</b>',ok:'Entendi',txt:'TUBETU — um desenho em que a bondade volta! Jogos, colorir e heróis:'},
ar:{share:'مشاركة',copied:'تم نسخ الرابط!',inst:'تثبيت',instT:'TUBETU على شاشة الهاتف',ios:'اضغط <b>مشاركة</b> <span class="ic">⬆️</span> في الأسفل ثم <b>إضافة إلى الشاشة الرئيسية</b> ➕',and:'افتح قائمة المتصفح <b>⋮</b> واختر <b>إضافة إلى الشاشة الرئيسية</b> أو <b>تثبيت التطبيق</b>',ok:'حسنًا',txt:'TUBETU — كرتون يعود فيه الخير! ألعاب وتلوين وأبطال:'}
}[cur];
var css='.tb-acts{display:flex;gap:6px;align-items:center;font-family:Nunito,system-ui,sans-serif;flex:none;position:relative;z-index:30}'+
'.tb-acts.float{position:fixed;top:10px;right:10px;z-index:9999}html[dir=rtl] .tb-acts.float{right:auto;left:10px}'+
'.tb-acts>button,.tb-lang>button{border:0;cursor:pointer;background:rgba(255,255,255,.16);color:#fff;font:900 13px Nunito,system-ui,sans-serif;height:36px;min-width:36px;padding:0 10px;border-radius:999px;display:flex;align-items:center;gap:5px;white-space:nowrap}'+
'.tb-acts.float>button,.tb-acts.float .tb-lang>button,.tb-acts.light>button,.tb-acts.light .tb-lang>button{background:rgba(11,18,64,.82);box-shadow:0 4px 14px rgba(0,0,0,.25);backdrop-filter:blur(8px)}'+
'@media(max-width:440px){.tb-lang .lc{display:none}.tb-acts{gap:4px}.tb-acts>button,.tb-lang>button{padding:0 8px!important;min-width:34px;height:34px}nav.nav .logo img{height:30px!important;width:auto}nav.nav .wrap{gap:6px}.tb-acts .tb-share .lbl{font-size:12px}}'+
'@media(max-width:350px){.tb-acts .tb-share .lbl{display:none}header.top a:not(:first-child){max-width:22vw!important}}'+
'.tb-acts .tb-share{background:linear-gradient(180deg,#FFD23F,#FF9F1C)!important;color:#3a2300!important;box-shadow:0 3px 0 #B86E00!important}.tb-acts .lbl{display:inline}header.top a{white-space:nowrap}@media(max-width:520px){header.top,header.top .w{gap:6px!important;min-width:0}header.top h1{display:none}header.top .sp{flex:1 1 0;min-width:0}header.top a:not(:first-child),header.top .w>a:not(:first-child){font-size:13px!important;padding:6px 9px!important;max-width:28vw;overflow:hidden;text-overflow:ellipsis;flex:0 1 auto}header.top img{max-width:84px;object-fit:contain}}'+
'@media(max-width:520px){.tb-acts .tb-inst .lbl{display:none}.tb-lang>button{font-size:12px}.tb-acts>button,.tb-lang>button{padding:0 9px}}'+
'.tb-lang{position:relative}.tb-lang ul{position:absolute;right:0;top:42px;margin:0;padding:6px;list-style:none;background:#fff;border-radius:16px;box-shadow:0 12px 32px rgba(0,0,0,.3);display:none;min-width:160px;max-height:70vh;overflow:auto;z-index:10000}'+
'html[dir=rtl] .tb-lang ul{right:auto;left:0}.tb-lang.open ul{display:block}.tb-lang a{display:block;padding:9px 12px;border-radius:10px;color:#0B1240;text-decoration:none;font-weight:800;font-size:15px}.tb-lang a:hover,.tb-lang a.on{background:#EEF2FF}'+
'.tb-toast{position:fixed;left:50%;top:70px;transform:translateX(-50%);background:#0B1240;color:#fff;font:900 15px Nunito,system-ui,sans-serif;padding:10px 18px;border-radius:999px;z-index:10001;box-shadow:0 10px 30px rgba(0,0,0,.3)}'+
'.tb-sheet{position:fixed;inset:0;background:rgba(11,18,64,.55);z-index:10002;display:flex;align-items:flex-end;justify-content:center;font-family:Nunito,system-ui,sans-serif}'+
'.tb-sheet .c{background:#fff;color:#0B1240;border-radius:24px 24px 0 0;padding:22px 20px calc(22px + env(safe-area-inset-bottom));max-width:480px;width:100%;text-align:center}'+
'.tb-sheet img{display:block;margin:0 auto;width:72px;height:72px;border-radius:18px;box-shadow:0 6px 18px rgba(0,0,0,.2)}.tb-sheet h3{margin:12px 0 8px;font-size:20px;font-weight:900}.tb-sheet p{font-size:16px;font-weight:700;line-height:1.45;margin:0 0 16px}'+
'.tb-sheet .ic{display:inline-block;background:#EEF2FF;border-radius:8px;padding:0 4px}.tb-sheet button{border:0;background:linear-gradient(180deg,#FFB347,#FF7A00);color:#fff;font:900 17px Nunito,sans-serif;padding:13px 30px;border-radius:999px;box-shadow:0 5px 0 #B85500;cursor:pointer}'+
'.tb-tip{position:fixed;right:10px;top:56px;z-index:9999;background:#fff;color:#0B1240;border-radius:16px;padding:10px 14px;font:800 14px Nunito,system-ui,sans-serif;box-shadow:0 12px 32px rgba(0,0,0,.3)}.tb-tip a{color:#FF7A00}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

var standalone=matchMedia('(display-mode: standalone)').matches||navigator.standalone;
var ua=navigator.userAgent,isIOS=/iPhone|iPad|iPod/.test(ua)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
var deferred=null;addEventListener('beforeinstallprompt',function(e){e.preventDefault();deferred=e;});

var box=document.createElement('div');box.className='tb-acts';
var mobile=/Android|iPhone|iPad|iPod/.test(ua)||(navigator.maxTouchPoints>1&&innerWidth<1100);
box.innerHTML='<button type="button" class="tb-share" aria-label="'+T.share+'">📤<span class="lbl">'+T.share+'</span></button>'+
 (!standalone&&mobile?'<button type="button" class="tb-inst" aria-label="'+T.inst+'">📲<span class="lbl">'+T.inst+'</span></button>':'')+
 '<div class="tb-lang"><button type="button" aria-label="Language">🌐<span class="lc"> '+cur.toUpperCase()+'</span></button><ul>'+L.map(function(x){return '<li><a href="'+url(x[0])+'" class="'+(x[0]===cur?'on':'')+'" data-l="'+x[0]+'">'+x[1]+'</a></li>';}).join('')+'</ul></div>';

function toast(t){var d=document.createElement('div');d.className='tb-toast';d.textContent=t;document.body.appendChild(d);setTimeout(function(){d.remove();},2200);}
box.querySelector('.tb-share').onclick=function(){var u=location.href.split('#')[0],ttl=document.title;
 if(navigator.share){navigator.share({title:ttl,text:T.txt,url:u}).catch(function(){});}
 else{try{navigator.clipboard.writeText(T.txt+' '+u).then(function(){toast(T.copied);});}catch(e){prompt(T.share,u);}}};
var ib=box.querySelector('.tb-inst');
if(ib)ib.onclick=function(){if(deferred){deferred.prompt();deferred.userChoice.finally(function(){deferred=null;});return;}
 var sh=document.createElement('div');sh.className='tb-sheet';sh.innerHTML='<div class="c"><img src="/assets/app-icon-192.png" alt=""><h3>'+T.instT+'</h3><p>'+(isIOS?T.ios:T.and)+'</p><button type="button">'+T.ok+'</button></div>';
 sh.onclick=function(e){if(e.target===sh||e.target.tagName==='BUTTON')sh.remove();};document.body.appendChild(sh);};
var lang=box.querySelector('.tb-lang');
lang.querySelector('button').onclick=function(e){e.stopPropagation();lang.classList.toggle('open');};
document.addEventListener('click',function(){lang.classList.remove('open');});
lang.querySelectorAll('a').forEach(function(a){a.onclick=function(){try{localStorage.setItem('tubetu_lang',a.dataset.l);}catch(e){}};});

/* куда поставить: в шапку страницы, иначе — плавающие в углу */
var nav=document.querySelector('nav.nav .wrap'),hdr=document.querySelector('header.top'),placed=false;
if(nav){var burger=nav.querySelector('.burger');box.style.marginLeft='auto';
  if(burger&&getComputedStyle(burger).display!=='none'){nav.insertBefore(box,burger);burger.style.marginLeft='6px';}else{nav.appendChild(box);box.style.marginLeft='12px';}placed=true;}
else if(hdr){var w=hdr.querySelector('.w')||hdr;w.appendChild(box);placed=true;}
if(!placed){box.classList.add('float');document.body.appendChild(box);
  var menu=document.getElementById('menu'),hud=document.getElementById('hud');
  if(menu&&hud){setInterval(function(){var vis=getComputedStyle(menu).display!=='none'&&getComputedStyle(menu).visibility!=='hidden'&&+getComputedStyle(menu).opacity>0.05;box.style.display=vis?'flex':'none';},400);}}

try{var saved=localStorage.getItem('tubetu_lang');
 if(!saved&&cur==='ru'){var nl=(navigator.language||'').slice(0,2).toLowerCase();if(nl==='kk')nl='kz';
  if(nl&&nl!=='ru'&&codes.indexOf(nl)>0){var name=L[codes.indexOf(nl)][1];var tip=document.createElement('div');tip.className='tb-tip';tip.innerHTML='🌐 <a href="'+url(nl)+'">'+name+'</a> ✕';tip.onclick=function(e){if(e.target.tagName!=='A'){tip.remove();try{localStorage.setItem('tubetu_lang','ru');}catch(x){}}};document.body.appendChild(tip);setTimeout(function(){tip.remove();},9000);}}}catch(e){}
})();
