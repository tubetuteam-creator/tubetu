import sys,os,json;sys.path.insert(0,os.path.dirname(__file__))
from common import *
seen={};order=[]
def add(s,page):
    if s not in seen:seen[s]=page;order.append(s)
for p in PAGES:
    html=open(os.path.join(ROOT,p)).read();soup=BeautifulSoup(html,'html.parser')
    for t in soup.find_all(string=True):
        if isinstance(t,Comment):continue
        par=t.parent.name
        if par=='script':
            if t.parent.get('type')=='application/ld+json':
                for s in re.findall(r'"([^"]*[А-Яа-яЁё][^"]*)"',t):add(s,p)
            else:
                for s in js_strings(str(t)):add(s,p)
            continue
        if par=='style':continue
        n=norm(str(t))
        if CYR.search(n):add(n,p)
    for el in soup.find_all(True):
        for a in ATTRS:
            v=el.get(a)
            if isinstance(v,str) and CYR.search(v):add(norm(v),p)
json.dump([{'ru':s,'page':seen[s]} for s in order],open(os.path.join(ROOT,'i18n','strings.json'),'w'),ensure_ascii=False,indent=0)
print(len(order),'strings',sum(len(s) for s in order),'chars')
