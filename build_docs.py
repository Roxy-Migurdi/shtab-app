import os
import json

BASE = r"E:\ROXY_SYSTEM"
JEV_DIR = os.path.join(BASE, "Roxy_Freelance", "collab", "research", "JEV_2026-09-23")
COLLAB_DIR = os.path.join(BASE, "Roxy_Freelance", "collab")
OUT_JS = os.path.join(BASE, "Shtab_Miniapp", "docs_data.js")

docs = []

def add_doc(doc_id, task_id, group, title, author, date, filepath, summary):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            docs.append({
                "id": doc_id,
                "task_id": task_id,
                "group": group,
                "title": title,
                "author": author,
                "date": date,
                "summary": summary,
                "content": content
            })
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

# 1. JEV Research (23.09.2026)
add_doc(
    "doc-jev-r3", "sh-das", "🔥 Исследование JEV & System 1",
    "R3: Стратегия интеграции System 1 (Jev/Kev)", "ROXY & Claude", "2026-09-23",
    os.path.join(JEV_DIR, "R3_strategy.md"),
    "Применение: Freelance Hunter скоринг ($0.000004 за заказ, 50мс), диспетчер. Матрица OpenRouter vs локалка."
)
add_doc(
    "doc-jev-r2", "sh-das", "🔥 Исследование JEV & System 1",
    "R2: Добор фактов по JEV (цены, OpenRouter, локалка)", "ROXY", "2026-09-23",
    os.path.join(JEV_DIR, "R2_gaps.md"),
    "Разбор ценников OpenRouter, веса моделей, запуск через Ollama/vLLM на Ryzen/32GB."
)
add_doc(
    "doc-jev-plan", "sh-das", "🔥 Исследование JEV & System 1",
    "README: План исследования JEV и 6 ссылок", "ROXY & Claude", "2026-09-23",
    os.path.join(JEV_DIR, "README.md"),
    "Структура исследования, деление на группы A (jev) и B (разбор тем), требования Виктории."
)
add_doc(
    "doc-jev-a1", "sh-das", "🔥 Исследование JEV & System 1",
    "A1: Разбор поста @bibryam (Jev модель)", "ROXY (саб-агент A1)", "2026-09-23",
    os.path.join(JEV_DIR, "A1.md"),
    "Анализ первой ссылки Виктории о модели Jev и оптимизации."
)
add_doc(
    "doc-jev-b1", "sh-das", "🔥 Исследование JEV & System 1",
    "B1: Разбор поста @engmoelgaraihy (AI & UE5)", "ROXY (саб-агент B1)", "2026-09-23",
    os.path.join(JEV_DIR, "B1.md"),
    "Анализ поста по игровым AI пайплайнам и Unreal Engine."
)

# 2. Инфраструктура и API
add_doc(
    "doc-miniapp-api", "sh-492", "🏗 Инфраструктура Штаба 2.0",
    "Спецификация контракта Local API для Mini App", "ROXY & Claude", "2026-09-19",
    os.path.join(COLLAB_DIR, "SPEC_MINIAPP_API.md"),
    "REST-контракт на порту 54125: эндпоинты /api/status, /api/board/issues, /api/command."
)
add_doc(
    "doc-knowledge-manifest", "sh-8id", "🧠 Архитектура Знаний и Партнерство",
    "Архитектура знаний Роя (2026) и Манифест фронтира", "ROXY & Victoria", "2026-09-19",
    os.path.join(COLLAB_DIR, "knowledge_graph_architecture_and_frontier_pact.md"),
    "Отказ от зоопарка из 3 внешних БД. Единый позвоночник: GitNexus + Engram + Obsidian."
)
add_doc(
    "doc-consensus", "sh-vgc", "📜 Регламенты и Протоколы",
    "Протокол консенсуса 2 из 3 и Fast-Track", "Claude & ROXY", "2026-09-19",
    os.path.join(COLLAB_DIR, "CONSENSUS_2_OF_3_PROTOCOL.md"),
    "Кворум 2 из 3 (Виктория + ROXY + Клод) для архитектурных решений. Fast-track для багов."
)
add_doc(
    "doc-dual-audit", "sh-d3q", "📜 Регламенты и Протоколы",
    "Протокол двойного аудита (Zero Self-Approval)", "Claude & ROXY", "2026-09-19",
    os.path.join(COLLAB_DIR, "DUAL_AUDIT_PROTOCOL.md"),
    "Правило двух галочек: закрытую одним карточку обязательно независимо проверяет второй агент."
)

with open(OUT_JS, "w", encoding="utf-8") as f:
    f.write("window.SHTAB_DOCS = " + json.dumps(docs, ensure_ascii=False, indent=2) + ";\n")

print(f"SUCCESS: {len(docs)} documents written to {OUT_JS}")
