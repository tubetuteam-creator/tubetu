(function(){
var L=[['ru','Русский'],['kz','Қазақша'],['en','English'],['tr','Türkçe'],['zh','中文'],['es','Español'],['hi','हिन्दी'],['sw','Kiswahili'],['pt','Português'],['ar','العربية']];
var ON=['ru','kz','en'];L=L.filter(function(x){return ON.indexOf(x[0])>=0;});
var ALL=['ru','kz','en','tr','zh','es','hi','sw','pt','ar'];
var codes=ALL;var _c=L.map(function(x){return x[0];});
var m=location.pathname.match(/^\/([a-z]{2})(\/.*)$/),cur='ru',base=location.pathname;
if(m&&codes.indexOf(m[1])>0){cur=m[1];base=m[2];}
function url(c){return (c==='ru'?'':'/'+c)+base+location.search+location.hash;}
var css='.tg-lang{position:fixed;left:12px;bottom:12px;z-index:9999;font-family:Nunito,system-ui,sans-serif}'+
'.tg-lang>button{border:0;cursor:pointer;background:rgba(11,18,64,.85);color:#fff;font:900 14px Nunito,system-ui,sans-serif;padding:9px 13px;border-radius:999px;box-shadow:0 6px 18px rgba(0,0,0,.25);backdrop-filter:blur(8px)}'+
'.tg-lang ul{position:absolute;left:0;bottom:46px;margin:0;padding:6px;list-style:none;background:#fff;border-radius:16px;box-shadow:0 12px 32px rgba(0,0,0,.3);display:none;min-width:160px;max-height:70vh;overflow:auto}'+
'.tg-lang.open ul{display:block}.tg-lang a{display:block;padding:8px 12px;border-radius:10px;color:#0B1240;text-decoration:none;font-weight:800;font-size:15px}'+
'.tg-lang a:hover,.tg-lang a.on{background:#EEF2FF}.tg-tip{position:fixed;left:12px;bottom:58px;z-index:9999;background:#fff;color:#0B1240;border-radius:16px;padding:10px 14px;font:800 14px Nunito,system-ui,sans-serif;box-shadow:0 12px 32px rgba(0,0,0,.3)}.tg-tip a{color:#FF7A00}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
var box=document.createElement('div');box.className='tg-lang';
box.innerHTML='<button type="button" aria-label="Language">🌐 '+cur.toUpperCase()+'</button><ul>'+L.map(function(x){return '<li><a href="'+url(x[0])+'" class="'+(x[0]===cur?'on':'')+'" data-l="'+x[0]+'">'+x[1]+'</a></li>';}).join('')+'</ul>';
document.body.appendChild(box);
box.querySelector('button').onclick=function(e){e.stopPropagation();box.classList.toggle('open');};
document.addEventListener('click',function(){box.classList.remove('open');});
box.querySelectorAll('a').forEach(function(a){a.onclick=function(){try{localStorage.setItem('tubetu_lang',a.dataset.l);}catch(e){}};});
try{var saved=localStorage.getItem('tubetu_lang');
 if(!saved&&cur==='ru'){var nav=(navigator.language||'').slice(0,2).toLowerCase();if(nav==='kk')nav='kz';
  if(nav&&nav!=='ru'&&_c.indexOf(nav)>0){var name=L[_c.indexOf(nav)][1];var tip=document.createElement('div');tip.className='tg-tip';tip.innerHTML='🌐 <a href="'+url(nav)+'">'+name+'</a> ✕';tip.onclick=function(e){if(e.target.tagName!=='A'){tip.remove();try{localStorage.setItem('tubetu_lang','ru');}catch(x){}}};document.body.appendChild(tip);}}}catch(e){}
})();
