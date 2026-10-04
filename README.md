# task-api

RAG сервис. Docker + автодеплоцй.

## Локальный запуск

    conda create -y -n task-api python=3.11
    conda activate task-api
    pip install -r requirements.txt
    uvicorn app.main:app --reload


## Живой сервис

http://5-63-158-113.nip.io/docs

## Результаты оценки (свой прогон, 2026-10-04)

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