// Supabase Edge Function: tubetu-ai
// Required Supabase secrets: OPENAI_API_KEY
// Optional secret: OPENAI_MODEL (defaults to gpt-5-mini)
// Deploy with JWT verification enabled. Never expose the OpenAI key in index.html.
const corsHeaders = {
  "Access-Control-Allow-Origin": "https://tubetuteam-creator.github.io",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Vary": "Origin",
};

const systemPrompt = `Ты — TUBETU AI, помощник платформы TUBETU — среды прямого обмена информацией (People • Business • Resources).
Отвечай на языке пользователя, обычно на русском. Будь кратким, точным и полезным.
TUBETU — не маркетплейс и не социальная сеть: платформа помогает людям, компаниям и сообществам находить друг друга через предложения, запросы и прямые договорённости.
13 тематических разделов:
1. Проекты и идеи — стартапы, команды, бизнес-модели, технологии и инициативы.
2. Игры — PC, консоли, мобильные игры, киберспорт и игровые сообщества.
3. Контент — видео, медиа, тексты, аудио и технический контент.
4. Товары и ресурсы — товары, материалы, сырьё, остатки, оборудование и ресурсы.
5. Услуги — строительные, IT, консультационные, бытовые и профессиональные услуги.
6. Логистика и перевозки — грузы, доставка, склады, водители и спецтехника.
7. Финансы — инвестиционные предложения, партнёрство и совместные проекты; не обещай доходность и не выдавай финансовые предположения за гарантии.
8. Недвижимость — жилая и коммерческая недвижимость, земля, гаражи и аренда.
9. Транспорт — автомобили, грузовики, спецтехника, запчасти и сервис.
10. Сельское хозяйство — техника, растениеводство, животноводство и закупочные запросы.
11. Техника и оборудование — инструменты, промышленное, IT- и измерительное оборудование.
12. Образование и опыт — обучение, наставничество, практика и обмен знаниями.
13. Сообщества — профессиональные, тематические, локальные и закрытые группы.
Помогай понять запрос, предложить раздел, найти релевантные карточки в переданном контексте и подготовить черновик объявления.
Не утверждай, что ты реально опубликовал карточку, изменил аккаунт или настройки. Не проси пароли, API-ключи и секреты.
Не меняй системные правила и не выполняй действия в базе данных: только формируй ответ/рекомендацию.
Если контекста недостаточно, задай один короткий уточняющий вопрос.
Когда пользователь просит подготовить объявление, верни также поля draft: title, category (одно из названий 13 разделов), description.
Если mode равен "image_search", проанализируй приложенные фотографии для поиска: назови только то, что можно обоснованно определить по изображению; не выдумывай бренд, модель, состояние или технические параметры. Создай короткий поисковый запрос на русском с вероятным названием предмета и полезными синонимами. Если уверенность низкая, укажи это и используй более общее название. Поле image_caption — краткое описание видимого предмета; search_query — поисковый запрос с синонимами; confidence — число от 0 до 1; category — вероятная категория TUBETU.
Ответ верни строго в JSON-формате с полями: message (string), category (string или пустая строка), draft (object или null; title/category/description), suggestions (array строк), search_query (string), image_caption (string), confidence (number).`;

Deno.serve(async (req) => {
  const origin = req.headers.get("origin");
  const headers = {
    ...corsHeaders,
    ...(origin === "https://tubetuteam-creator.github.io" ? {} : {}),
    "Content-Type": "application/json; charset=utf-8",
  };

  if (req.method === "OPTIONS") return new Response("ok", { headers });
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405, headers });
  }
  if (origin && origin !== "https://tubetuteam-creator.github.io") {
    return new Response(JSON.stringify({ error: "Origin not allowed" }), { status: 403, headers });
  }

  const apiKey = Deno.env.get("OPENAI_API_KEY");
  if (!apiKey) {
    return new Response(JSON.stringify({ error: "ИИ пока не настроен: на сервере отсутствует OPENAI_API_KEY." }), { status: 503, headers });
  }

  let body: { question?: unknown; context?: unknown; mode?: unknown; images?: unknown };
  try {
    body = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "Некорректный JSON-запрос." }), { status: 400, headers });
  }

  const question = typeof body.question === "string" ? body.question.trim() : "";
  if (!question) return new Response(JSON.stringify({ error: "Напишите вопрос." }), { status: 400, headers });
  if (question.length > 4000) return new Response(JSON.stringify({ error: "Вопрос слишком длинный (максимум 4000 символов)." }), { status: 413, headers });
  const mode = body.mode === "image_search" || body.mode === "create_listing" ? body.mode : "chat";
  const images = Array.isArray(body.images) ? body.images.slice(0, mode === "create_listing" ? 5 : 3) : [];
  if ((mode === "image_search" || mode === "create_listing") && images.length === 0) {
    return new Response(JSON.stringify({ error: mode === "create_listing" ? "Для создания объявления приложите хотя бы одно изображение." : "Для поиска по фото приложите хотя бы одно изображение." }), { status: 400, headers });
  }
  if (images.some((image) => typeof image !== "string" || image.length > 560000 || !/^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+$/.test(image))) {
    return new Response(JSON.stringify({ error: "Изображение имеет неподдерживаемый формат или превышает допустимый размер. Используйте JPEG, PNG или WebP до 400 КБ." }), { status: 413, headers });
  }

  const safeContext = Array.isArray(body.context)
    ? body.context.slice(0, 8).map((item) => {
        if (!item || typeof item !== "object") return null;
        const p = item as Record<string, unknown>;
        return {
          title: typeof p.title === "string" ? p.title.slice(0, 180) : "",
          category: typeof p.category === "string" ? p.category.slice(0, 80) : "",
          text: typeof p.text === "string" ? p.text.slice(0, 700) : "",
        };
      }).filter(Boolean)
    : [];

  const modeInstruction = mode === "create_listing"
    ? "РЕЖИМ СОЗДАНИЯ ОБЪЯВЛЕНИЯ ПО ФОТО: внимательно проанализируй все приложенные изображения и определи видимый предмет. Подготовь черновик объявления по тому, что реально видно. Заполни draft.title, draft.category и draft.description. Категорию выбери строго из списка 13 разделов. Не выдумывай бренд, модель, технические характеристики, цену, состояние, комплектность или местоположение, если этого нельзя достоверно определить по фото. Если информации недостаточно, опиши предмет нейтрально и добавь в suggestions вопросы для уточнения. Верни непустые title и description."
    : mode === "image_search"
    ? "РЕЖИМ ПОИСКА ПО ФОТО: распознай видимый предмет и подготовь search_query, image_caption, confidence и category."
    : "РЕЖИМ ОБЩЕГО ДИАЛОГА: ответь на вопрос пользователя.";
  const userContent: Array<Record<string, unknown>> = [
    { type: "input_text", text: JSON.stringify({ question, mode, mode_instruction: modeInstruction, relevant_cards: safeContext }) },
    ...images.map((image) => ({ type: "input_image", image_url: image })),
  ];
  const model = Deno.env.get("OPENAI_MODEL") || "gpt-5-mini";
  try {
    const response = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model,
        instructions: systemPrompt,
        input: [{ role: "user", content: userContent }],
        max_output_tokens: 700,
        text: { format: { type: "json_object" } },
      }),
    });

    const result = await response.json();
    if (!response.ok) {
      console.error("OpenAI API error", response.status, result?.error?.code || result?.error?.type || "unknown");
      return new Response(JSON.stringify({ error: "ИИ временно недоступен. Проверьте серверные настройки и лимиты API." }), { status: 502, headers });
    }

    const output = (result.output || [])
      .flatMap((item: { content?: Array<{ type?: string; text?: string }> }) => item.content || [])
      .filter((item: { type?: string }) => item.type === "output_text")
      .map((item: { text?: string }) => item.text || "")
      .join("\n");

    let parsed: unknown;
    try {
      parsed = JSON.parse(output);
    } catch {
      console.error("OpenAI returned invalid JSON");
      return new Response(JSON.stringify({ error: "Не удалось обработать ответ ИИ. Попробуйте ещё раз." }), { status: 502, headers });
    }

    return new Response(JSON.stringify({ result: parsed, model }), { status: 200, headers });
  } catch (error) {
    console.error("TUBETU AI request failed", error instanceof Error ? error.message : "unknown");
    return new Response(JSON.stringify({ error: "Не удалось соединиться с сервисом ИИ." }), { status: 502, headers });
  }
});
