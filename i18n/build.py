import sys,os,json,re;sys.path.insert(0,os.path.dirname(__file__))
from common import *
LANGS={'kz':('kk','kk-KZ'),'en':('en','en-US'),'tr':('tr','tr-TR'),'zh':('zh','zh-CN'),'es':('es','es-ES'),'hi':('hi','hi-IN'),'sw':('sw','sw-KE'),'pt':('pt','pt-BR'),'ar':('ar','ar-SA')}
STR=json.load(open(os.path.join(ROOT,'i18n','strings.json')))
BYRU={x['ru']:x['id'] for x in STR}
LOCAL=r'(?:geroi/|seriya-1/|dver/|games/(?!img/|_common)|raskraska/(?!img/)|pozdravlenie/|risunki/|platform\.html|#)'
def jsesc(t,q):return t.replace('\\','\\\\').replace(q,'\\'+q).replace('\n','\\n')
def build(L):
    hl,speech=LANGS[L]
    tr=json.load(open(os.path.join(ROOT,'i18n',L+'.json')))
    T=lambda ru:tr.get(BYRU.get(ru,''),None)
    miss=set()
    for p in PAGES:
        src=open(os.path.join(ROOT,p)).read();soup=BeautifulSoup(src,'html.parser')
        for t in list(soup.find_all(string=True)):
            if isinstance(t,Comment):continue
            par=t.parent.name
            if par=='style':continue
            if par=='script':
                code=str(t)
                if t.parent.get('type')=='application/ld+json':
                    code=re.sub(r'"([^"]*[А-Яа-яЁё][^"]*)"',lambda m:'"'+(T(m.group(1)) or m.group(1)).replace('"','\\"')+'"',code)
                else:
                    def rep(m):
                        q="'" if m.group(1) is not None else '"';s=m.group(1) if m.group(1) is not None else m.group(2)
                        if not CYR.search(s):return m.group(0)
                        v=T(s)
                        if v is None:
                            miss.add(s);return m.group(0)
                        return q+jsesc(v,q)+q
                    code=JSSTR.sub(rep,code)
                t.replace_with(code);continue
            raw=str(t);n=norm(raw)
            if not CYR.search(n):continue
            v=T(n)
            if v is None:miss.add(n);continue
            lead=raw[:len(raw)-len(raw.lstrip())];trail=raw[len(raw.rstrip()):]
            t.replace_with(lead+v+trail)
        for el in soup.find_all(True):
            for a in ATTRS:
                val=el.get(a)
                if isinstance(val,str) and CYR.search(val):
                    v=T(norm(val))
                    if v is None:miss.add(norm(val))
                    else:el[a]=v
        if soup.html:
            soup.html['lang']=hl
            if L=='ar':soup.html['dir']='rtl'
        out=str(soup)
        # scripts: bs4 keeps script text raw, ok
        out=re.sub(r'(["\'(=])/'+LOCAL,lambda m:m.group(1)+'/'+L+'/'+m.group(0)[len(m.group(1))+1:],out)
        out=re.sub(r'href=(["\'])/\1',lambda m:'href='+m.group(1)+'/'+L+'/'+m.group(1),out)
        out=out.replace('https://tubetu.com/platform.html','https://tubetu.com/'+L+'/platform.html')
        out=re.sub(r'(<link rel="canonical" href="https://tubetu\.com/)',r'\g<1>'+L+'/',out)
        out=re.sub(r'(<meta content="https://tubetu\.com/)(?!assets)([^"]*)(" property="og:url")',r'\g<1>'+L+r'/\2\3',out)
        out=out.replace("rec.lang='ru-RU'","rec.lang='"+speech+"'")
        if p=='games/index.html':out=out.replace("'img/","'/games/img/").replace('"img/','"/games/img/')
        if p.startswith('games/pazl') or p.startswith('games/otlichiya') or p.startswith('games/stroim'):out=out.replace('../_common','/games/_common')
        if p=='raskraska/index.html':out=out.replace("'img/","'/raskraska/img/").replace('"img/','"/raskraska/img/')
        dst=os.path.join(ROOT,L,p);os.makedirs(os.path.dirname(dst),exist_ok=True)
        open(dst,'w').write(out)
    return miss
if __name__=='__main__':
    for L in sys.argv[1:]:
        m=build(L);print(L,'missing',len(m));[print('  ',x[:90]) for x in sorted(m)[:400]]
