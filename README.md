# scikit-learn docs RAG assistant

AI-ассистент по официальной документации scikit-learn. Задаёте вопрос
на естественном языке — получаете ответ с цитатами из документации.


## Архитектура

\`\`\`mermaid
flowchart LR
    USER[Пользователь] --> NGINX[Nginx HTTPS]
    NGINX --> APP[FastAPI + Gradio streaming]
    APP --> EMB[multilingual-e5-small embedder]
    APP --> Q[(Qdrant)]
    APP --> LLM[OpenRouter -> llama-3.3-70b-instruct]
\`\`\`

## Живой сервис

http://5-63-158-113.nip.io/docs

## Индексация на VPS (сначала только Qdrant)

App и индексер оба грузят e5 в RAM. На 1.9 GiB сначала остановите `rag-servise`, оставьте Qdrant, прогоните job с `--rm`, потом поднимите app.

```bash
ssh root@5.63.158.113
free -h   # Swap ~2.0Gi

# если app уже запущен из GHCR — выключить, qdrant не трогать
docker stop rag-servise 2>/dev/null; docker rm rag-servise 2>/dev/null

cd /opt/mentoring
# git clone <repo> rag-service   # если репозитория ещё нет
cd rag-service
cp -n .env.example .env   # дописать LLM_API_KEY

docker compose up -d qdrant

# образ с CI, без сборки torch на VPS
export RAG_IMAGE=ghcr.io/alexovchgen/rag-servise:latest
docker compose pull app

docker compose run --rm app sh -c \
  "python -m app.scripts.load_corpus && python -m app.scripts.index_corpus"

docker compose up -d app
```

Если контейнер `qdrant` уже жив не из этого compose и `up -d qdrant` ругается на имя — не поднимайте второй, а индексируйте так:

```bash
docker compose run --rm --no-deps app sh -c \
  "python -m app.scripts.load_corpus && python -m app.scripts.index_corpus"
```

## Результаты оценки (свой прогон, 2026-10-04)

Замеры на реальной системе (10 вопросов golden dataset,
3 sklearn-модуля + about.md → 267 чанков, llama-3.3-70b-instruct,
`notebooks/rag_eval.ipynb`):

Снимок настроек и цифр: `notebooks/rag_metrics.json`.

- 10 golden-вопросов (linear_model, tree, model_evaluation, about.md)
- LLM: `qwen/qwen3.7-flash`, temperature 0
- Embeddings: `intfloat/multilingual-e5-small` (384-d, normalize)
- `top_k = 4`

| Метрика | Результат |
|---|---|
| Recall@4 | 1.00 (10/10) |
| Faithfulness | 0.88 |
| Response Relevancy | 0.94 |

Ориентир курса: Recall@4 ≥ 0.80, Faithfulness ≥ 0.75, Response Relevancy ≥ 0.75. Авторский прогон (llama-3.3-70b): 1.00 / 0.92 / 0.83. Дальше сравнивать изменения с этой таблицей.

## Локальный запуск

\`\`\`bash
docker compose up
python -m app.scripts.load_corpus
python -m app.scripts.index_corpus
\`\`\`

Откройте http://localhost:8000

## Для резюме

> RAG-сервис над документацией scikit-learn на FastAPI + LangChain
> LCEL + Qdrant + multilingual-e5-small. Streaming-чат в Gradio
> (TTFT < 1s через chain.stream), оценка качества через RAGAS на
> golden dataset (Recall@4 1.00, Faithfulness 0.92). LLM-провайдер
> абстрагирован через OpenAI-совместимый endpoint — меняется одной
> правкой `app/config.py`.