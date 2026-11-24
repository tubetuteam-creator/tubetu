import re,os,json
from bs4 import BeautifulSoup,NavigableString,Comment
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CYR=re.compile('[А-Яа-яЁё]')
PAGES=['index.html','seriya-1/index.html','geroi/index.html']+[f'geroi/{d}/index.html' for d in sorted(os.listdir(os.path.join(ROOT,'geroi'))) if os.path.isdir(os.path.join(ROOT,'geroi',d))]+\
 ['dver/index.html','games/index.html','games/pazl/index.html','games/otlichiya/index.html','raskraska/index.html','pozdravlenie/index.html','risunki/index.html','platform.html','404.html']
ATTRS=['alt','placeholder','title','aria-label','content']
JSSTR=re.compile(r"""'((?:[^'\\\n]|\\.)*)'|"((?:[^"\\\n]|\\.)*)\"""")
def norm(s):return re.sub(r'\s+',' ',s).strip()
def js_strings(code):
    out=[]
    for m in JSSTR.finditer(code):
        s=m.group(1) if m.group(1) is not None else m.group(2)
        if s and CYR.search(s):out.append(s)
    return out
