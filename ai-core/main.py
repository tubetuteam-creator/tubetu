"""TUBETU AI local rules engine API. No external LLM/API calls."""
import os, re, time, unicodedata
from collections import defaultdict, deque
from typing import Any
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
MAX_PER_MINUTE = max(1, int(os.getenv("AI_MAX_REQUESTS_PER_MINUTE", "30")))
origins = [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "https://tubetuteam-creator.github.io").split(",") if x.strip()]
app = FastAPI(title="TUBETU AI Core", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])
db: Client | None = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY) if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY else None
rate: dict[str, deque[float]] = defaultdict(deque)
CATEGORIES = {
 "Недвижимость": ["квартира","дом","участок","комната","гараж","недвижимость","пәтер","үй","жер"],
 "Транспорт": ["авто","автомобиль","машина","колёса","колеса","седан","кроссовер","көлік"],
 "Техника и оборудование": ["инструмент","оборудование","перфоратор","генератор","станок","құрал"],
 "Услуги": ["услуга","ремонт","монтаж","мастер","услуги","қызмет"],
 "Логистика и перевозки": ["перевозка","доставка","груз","склад","тасымал"],
 "Проекты и идеи": ["проект","стартап","партнёр","партнер","идея","жоба"],
 "Контент": ["видео","контент","фото","текст"],
 "Игры": ["игра","гейминг","киберспорт"],
 "Товары и ресурсы": ["диван","стол","шкаф","телефон","ноутбук","смартфон","товар","ресурс"],
}
CITIES = ["Алматы","Астана","Шымкент","Караганда","Актобе","Тараз","Павлодар","Усть-Каменогорск","Семей","Костанай","Кызылорда","Атырау","Актау","Талдыкорган","Қазақстан","Казахстан"]
KB = [
 {"title":"Главная","keys":["главная","домой","басты бет"],"answer":"Откройте «Главная» в нижнем меню.","view":"home"},
 {"title":"Поиск и публикации","keys":["поиск","найти объявление","каталог","категории","іздеу"],"answer":"Используйте поиск на главной странице или раздел «Исследовать».","view":"explore"},
 {"title":"Создание объявления","keys":["создать объявление","разместить объявление","подать объявление","жарнама жариялау"],"answer":"Откройте «Подать» в нижнем меню, проверьте поля и опубликуйте через форму.","view":"submit"},
 {"title":"Личный кабинет","keys":["кабинет","профиль","аккаунт","жеке кабинет"],"answer":"Откройте «Кабинет» в нижнем меню. Некоторые функции требуют входа.","view":"cabinet"},
 {"title":"Мои объявления","keys":["мои объявления","мои публикации","мои карточки","менің хабарландыруларым"],"answer":"Откройте «Кабинет» и найдите свои публикации; доступность управления зависит от входа и текущих функций сайта.","view":"cabinet"},
 {"title":"Настройки","keys":["настройки профиля","настройки","язык","регион","параметры","баптаулар"],"answer":"Откройте «Настройки» в меню сайта, если этот пункт доступен в вашей версии.","view":"settings"},
 {"title":"Сообщества","keys":["сообщества","группы","қауымдастық"],"answer":"Откройте «Сообщества» в нижнем меню.","view":"communities"},
 {"title":"Чат","keys":["чат","сообщения","переписка","хабарламалар"],"answer":"Откройте «Чат» в нижнем меню.","view":"chat"},
]
BLOCKED = re.compile(r"\b(куплю\s+наркотики|продам\s+наркотики|оружие\s+без\s+лицензии|финансовая\s+пирамида)\b", re.I)
CREATE = re.compile(r"\b(создай|создать|размести|разместить|подай|подать|опубликуй|продам|продаю|сдам|сдаю|предлагаю|жарнама\s+жариялау)\b", re.I)
SEARCH = re.compile(r"\b(найди|найти|покажи|ищу|куплю|нужен|нужна|требуется|іздеймін|тауып\s+бер)\b", re.I)
PRICE = re.compile(r"(?:(?:цена|стоимость|за|по цене)\s*)?(\d[\d\s.,]*)\s*(тысяч(?:а|и)?|тыс\.?|млн|миллион(?:а|ов)?|тенге|тг|₸|kzt|usd|\$)", re.I)
PHONE = re.compile(r"(?<!\d)(?:\+?7|8)[\s(-]*\d{3}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?!\d)")
INJECTION = re.compile(r"(?i)\b(drop\s+table|union\s+select|insert\s+into|delete\s+from|update\s+\w+\s+set|or\s+1\s*=\s*1)\b")

class Query(BaseModel):
 text: str = Field(min_length=1, max_length=2000)
 confirm_publish: bool = False
 draft: dict[str, Any] | None = None

def normalize(value: str) -> str:
 value = unicodedata.normalize("NFKC", value).replace("ё", "е").replace("Ё", "Е")
 value = "".join(ch if ch in "\n\t" or unicodedata.category(ch)[0] != "C" else " " for ch in value)
 return re.sub(r"\s+", " ", value).strip()

def rate_limit(request: Request) -> None:
 key = request.client.host if request.client else "unknown"
 now = time.monotonic(); q = rate[key]
 while q and now-q[0] > 60: q.popleft()
 if len(q) >= MAX_PER_MINUTE: raise HTTPException(429, "Слишком много запросов. Попробуйте позже.")
 q.append(now)

def classify(text: str) -> dict[str, Any]:
 t = normalize(text); low = t.casefold()
 city = next((c for c in CITIES if c.casefold() in low), "")
 price = PRICE.search(t); phone = PHONE.search(t)
 category = next((name for name, words in CATEGORIES.items() if any(w in low for w in words)), "Товары и ресурсы")
 intent = "Аренда" if re.search(r"\b(сдам|сдаю|аренда|в аренду|напрокат|жалға)\b", low) else ("Запрос" if SEARCH.search(low) else "Предложение")
 title = re.sub(r"^(хочу\s+)?(создай|создать|размести|разместить|подай|подать|опубликуй|продам|продаю|сдам|сдаю|предлагаю|ищу|куплю)\s*", "", t, flags=re.I).strip(" .,!?:;")[:120]
 return {"title": title, "description": t, "category": category, "location": city, "price": (price.group(1).strip()+" "+price.group(2)).strip() if price else "", "contacts": phone.group(0) if phone else "", "intent": intent, "language": "kk" if re.search(r"[әіңғүұқөһ]", low) else "ru"}

def knowledge(text: str):
 low = normalize(text).casefold()
 if re.search(r"правил|запрещен|что нельзя|ереже|тыйым", low):
  return {"title":"Правила TUBETU","answer":"Я могу сообщать только правила, подтверждённые в текущей версии сайта. Не буду придумывать отсутствующие правила."}
 for item in KB:
  if any(k in low for k in item["keys"]): return item
 return None

def get_user(token: str):
 if not db: raise HTTPException(503, "Backend не настроен: отсутствуют серверные параметры Supabase.")
 try:
  result = db.auth.get_user(token)
  if not result or not result.user: raise ValueError("No user")
  return result.user
 except Exception: raise HTTPException(401, "Войдите в аккаунт TUBETU.")

@app.get("/health")
def health():
 return {"ok": True, "service":"TUBETU AI Core", "database_configured": db is not None, "external_llm": False}

@app.post("/ai/query")
def query(payload: Query, request: Request, authorization: str | None = Header(default=None)):
 rate_limit(request)
 text = normalize(payload.text)
 if not text: raise HTTPException(400, "Введите запрос.")
 if INJECTION.search(text): return {"kind":"refusal","message":"Запрос содержит недопустимую техническую конструкцию. Я могу помогать только с функциями TUBETU."}
 if BLOCKED.search(text): return {"kind":"moderation","message":"Запрос требует проверки на соответствие правилам TUBETU."}
 if CREATE.search(text):
  draft = classify(text)
  missing = [k for k in ("title","description","category","location","price") if not draft.get(k)]
  return {"kind":"draft","draft":draft,"missing":missing,"message":"Черновик подготовлен. Проверьте поля; публикация возможна только после входа и явного подтверждения."}
 item = knowledge(text)
 if item: return {"kind":"knowledge","answer":item["answer"],"title":item["title"],"view":item.get("view")}
 if SEARCH.search(text): return {"kind":"search","query":text,"message":"Передайте запрос во встроенный поиск объявлений TUBETU."}
 return {"kind":"refusal","message":"Я — специализированный помощник TUBETU. Могу помочь с объявлениями, поиском и функциями платформы."}

@app.post("/ai/publish")
def publish(payload: Query, request: Request, authorization: str | None = Header(default=None)):
 rate_limit(request)
 if not payload.confirm_publish: raise HTTPException(400, "Для публикации требуется явное подтверждение.")
 if not authorization or not authorization.lower().startswith("bearer "): raise HTTPException(401, "Войдите в аккаунт TUBETU.")
 user = get_user(authorization.split(" ",1)[1].strip())
 draft = payload.draft or {}
 if any(not str(draft.get(k,"")).strip() for k in ("title","description","category")): raise HTTPException(422, "Заполните название, описание и категорию.")
 if BLOCKED.search(str(draft.get("title",""))+" "+str(draft.get("description",""))): raise HTTPException(422, "Объявление отправлено на проверку модерации.")
 if not db: raise HTTPException(503, "База данных не настроена.")
 full_text = "Намерение: "+str(draft.get("intent","Предложение"))+"\nГеография: "+str(draft.get("location",""))+"\nЦена/условия: "+str(draft.get("price",""))+"\n\n"+str(draft["description"])
 try:
  result = db.table("posts").insert({"title":str(draft["title"])[:120],"text":full_text[:10000],"category":str(draft["category"])[:100],"author_id":user.id}).execute()
  row = result.data[0] if result.data else {}
  return {"ok":True,"id":row.get("id"),"message":"Карточка опубликована."}
 except Exception: raise HTTPException(500, "Не удалось записать карточку. Проверьте схему posts и политики Supabase.")

@app.get("/ai/store-stats")
def store_stats(request: Request, authorization: str | None = Header(default=None)):
 rate_limit(request)
 if not authorization or not authorization.lower().startswith("bearer "): raise HTTPException(401, "Войдите в аккаунт TUBETU.")
 get_user(authorization.split(" ",1)[1].strip())
 raise HTTPException(501, "Аналитика магазина не подключена: в текущем репозитории не подтверждены таблица витрин, события просмотров и биллинг.")
