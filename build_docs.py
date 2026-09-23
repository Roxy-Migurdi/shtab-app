import sys
import os
import json
import re
import datetime

BASE = r"E:\ROXY_SYSTEM"
OUT_ENC = os.path.join(BASE, "Shtab_Miniapp", "docs.enc.json")
OUT_LEGACY_JS = os.path.join(BASE, "Shtab_Miniapp", "docs_data.js")

SCAN_PATHS = [
    os.path.join(BASE, "Roxy_Freelance", "collab"),
    os.path.join(BASE, "Shtab_Board", "handoffs"),
    os.path.join(BASE, "docs")
]

# Явные сопоставления файлов и задач
TASK_MAPPING = {
    "a1.md": ("sh-das", "🔥 Исследования и Фронтир", "ROXY (саб-агент A1)"),
    "a2.md": ("sh-das", "🔥 Исследования и Фронтир", "ROXY (саб-агент A2)"),
    "a3.md": ("sh-das", "🔥 Исследования и Фронтир", "ROXY (саб-агент A3)"),
    "b1.md": ("sh-das", "🔥 Исследования и Фронтир", "ROXY (саб-агент B1)"),
    "b2.md": ("sh-das", "🔥 Исследования и Фронтир", "ROXY (саб-агент B2)"),
    "b3.md": ("sh-das", "🔥 Исследования и Фронтир", "ROXY (саб-агент B3)"),
    "r2_gaps.md": ("sh-das", "🔥 Исследования и Фронтир", "ROXY"),
    "r3_strategy.md": ("sh-das", "🔥 Исследования и Фронтир", "ROXY & Claude"),
    "readme.md": ("sh-das", "🔥 Исследования и Фронтир", "Claude & ROXY"),
    "spec_miniapp_api.md": ("sh-492", "🏗 Спецификации и API", "ROXY & Claude"),
    "spec_dispatcher.md": ("sh-wnd", "🏗 Спецификации и API", "Claude & ROXY"),
    "spec_board_v2.md": ("sh-27x", "🏗 Спецификации и API", "Claude"),
    "consensus_2_of_3_protocol.md": ("sh-vgc", "📜 Регламенты и Протоколы", "Claude & ROXY"),
    "dual_audit_protocol.md": ("sh-d3q", "📜 Регламенты и Протоколы", "Claude & ROXY"),
    "collab_protocol.md": ("sh-vgc", "📜 Регламенты и Протоколы", "ROXY & Claude"),
    "knowledge_graph_architecture_and_frontier_pact.md": ("sh-8id", "🧠 Архитектура Системы", "ROXY & Victoria"),
    "system_map.md": ("sh-map", "🧠 Архитектура Системы", "ROXY & Claude"),
    "services.md": ("sh-srv", "🏗 Спецификации и API", "ROXY"),
    "shtab_2_plan.md": ("sh-pln", "🧠 Архитектура Системы", "Claude & ROXY"),
    "research_2026_agent_stack.md": ("sh-stk", "🔥 Исследования и Фронтир", "ROXY"),
    "benchmark_engram_vs_mem0.md": ("sh-eng", "🔥 Исследования и Фронтир", "ROXY"),
}

def extract_meta_from_content(filename, content, filepath):
    basename = filename.lower()
    
    # Дефолтные значения
    task_id = "sh-doc"
    group = "📚 Документация"
    author = "ROXY & Claude"
    
    if basename in TASK_MAPPING:
        task_id, group, author = TASK_MAPPING[basename]
    elif "handoff" in filepath.lower():
        task_id = "sh-l89"
        group = "🤝 Передача эстафеты (Handoffs)"
        author = "Claude" if "claude" in basename else "ROXY"
    elif "spec" in basename:
        group = "🏗 Спецификации и API"
    elif "protocol" in basename or "recreg" in basename:
        group = "📜 Регламенты и Протоколы"
    elif "research" in basename or "benchmark" in basename:
        group = "🔥 Исследования и Фронтир"
        
    # Ищем упоминания sh-... в тексте, если нет в маппинге
    if task_id == "sh-doc":
        m_task = re.search(r'\b(sh-[a-z0-9]{3})\b', content)
        if m_task:
            task_id = m_task.group(1)

    # Ищем H1 заголовок
    m_h1 = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = m_h1.group(1).strip() if m_h1 else os.path.splitext(filename)[0].replace('_', ' ').capitalize()

    # Дата модификации файла или из текста
    try:
        mtime = os.path.getmtime(filepath)
        date_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
    except Exception:
        date_str = "2026-09-23"

    m_date = re.search(r'\b(2026-\d{2}-\d{2})\b', content)
    if m_date:
        date_str = m_date.group(1)

    # Извлекаем краткое содержание (первые 200 символов чистого текста без решеток)
    clean_lines = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('---') or line.startswith('```') or line.startswith('!['):
            continue
        clean_lines.append(line)
        if len(" ".join(clean_lines)) > 220:
            break
            
    summary = " ".join(clean_lines)[:220].strip()
    if not summary:
        summary = f"Документ {title} системы Штаб 2.0."
    elif len(summary) >= 220:
        summary += "..."

    return task_id, group, title, author, date_str, summary

def scan_all_documents():
    docs = []
    seen_ids = set()

    for scan_dir in SCAN_PATHS:
        if not os.path.exists(scan_dir):
            continue
            
        for root, _, files in os.walk(scan_dir):
            for file in files:
                if not file.endswith('.md'):
                    continue
                if file.startswith('.') or file.lower() == 'license.md':
                    continue
                    
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                        
                    if len(content.strip()) < 40:
                        continue
                        
                    rel_path = os.path.relpath(filepath, BASE).replace('\\', '/')
                    doc_id = "doc_" + re.sub(r'[^a-zA-Z0-9]', '_', rel_path).strip('_')
                    
                    if doc_id in seen_ids:
                        continue
                    seen_ids.add(doc_id)
                    
                    task_id, group, title, author, date_str, summary = extract_meta_from_content(file, content, filepath)
                    
                    docs.append({
                        "id": doc_id,
                        "task_id": task_id,
                        "group": group,
                        "title": title,
                        "author": author,
                        "date": date_str,
                        "path": rel_path,
                        "summary": summary,
                        "content": content
                    })
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    # Сортировка: сначала самые свежие даты и исследования
    docs.sort(key=lambda x: (x["group"] != "🔥 Исследования и Фронтир", x["date"]), reverse=True)
    return docs

def build():
    docs = scan_all_documents()
    os.makedirs(os.path.dirname(OUT_ENC), exist_ok=True)

    # Шифрование тем же способом и паролем, что и доска (sh-15m / sh-kv7)
    board_dir = os.path.join(BASE, "Shtab_Board")
    if board_dir not in sys.path:
        sys.path.append(board_dir)
    import publish_board
    password, _ = publish_board.get_or_create_password()

    docs_json = json.dumps(docs, ensure_ascii=False)
    payload = publish_board.encrypt(docs_json, password)

    with open(OUT_ENC, "w", encoding="utf-8") as f:
        json.dump(payload, f)

    # Удаляем незашифрованный docs_data.js для предотвращения утечек
    if os.path.exists(OUT_LEGACY_JS):
        try:
            os.remove(OUT_LEGACY_JS)
        except Exception as e:
            print(f"Warning: could not remove {OUT_LEGACY_JS}: {e}")

    print(f"[BUILD-DOCS-SUCCESS] Автоматически зашифровано и сохранено {len(docs)} документов в {OUT_ENC}!")
    return len(docs)

if __name__ == "__main__":
    build()
