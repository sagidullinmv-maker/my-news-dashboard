# -*- coding: utf-8 -*-
from flask import Flask, render_template
from datetime import datetime, timedelta
import feedparser
import random
import json
import os
import requests
import re

app = Flask(__name__)

# ===== КОНФИГУРАЦИЯ =====
# Используем постоянное хранилище /data (на Amvera)
CACHE_FILE = '/data/news_cache.json'
CACHE_DURATION = timedelta(hours=24)

# ===== ИСТОЧНИКИ НОВОСТЕЙ =====
RSS_SOURCES = {
    "Дроны": [
        "https://dronedj.com/feed/",
        "https://www.dronezon.com/feed/",
    ],
    "3D-печать": [
        "https://3dprint.com/feed/",
        "https://all3dp.com/feed/",
    ],
    "Metal-Base (The Metal 1.0)": [
        "https://3dprint.com/feed/",
        "https://3dprintingindustry.com/feed/",
        "https://www.voxelmatters.com/feed/",
    ],
    "MetalPrinting (Gauss MT90)": [
        "https://3dprint.com/feed/",
        "https://3dprintingindustry.com/feed/",
        "https://www.voxelmatters.com/feed/",
    ],
    "Недвижимость Москвы": [
        "https://www.cian.ru/rss/cian.xml",
        "https://www.rbc.ru/rss/news/5e7ff4e19a79475db4281e4b",
    ],
    "Акции/облигации РФ": [
        "https://1prime.ru/rss/main.xml",
        "https://www.1prime.ru/rss/finance/",
    ],
    "ИИ в строительстве": [
        "https://www.constructiondive.com/rss/",
        "https://www.autodesk.com/blogs/autodesk-revit-architecture/feed",
    ],
    "Китайские источники": [
        "https://www.caixinglobal.com/rss/latest.rss",
        "https://36kr.com/feed",
    ]
}

# ===== ФУНКЦИИ КЭШИРОВАНИЯ =====
def ensure_data_dir():
    """Создаёт папку /data, если её нет (на случай, если запуск не на Amvera)"""
    data_dir = os.path.dirname(CACHE_FILE)
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
            print(f"✅ Создана папка {data_dir}")
        except Exception as e:
            print(f"⚠️ Не удалось создать папку {data_dir}: {e}")

def is_cache_valid():
    if not os.path.exists(CACHE_FILE):
        return False
    file_time = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
    return datetime.now() - file_time < CACHE_DURATION

def load_cached_news():
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_news_to_cache(news):
    ensure_data_dir()  # гарантируем, что папка существует
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(news, f, ensure_ascii=False, indent=2)
        print(f"✅ Кэш сохранён: {len(news)} новостей в {CACHE_FILE}")
    except Exception as e:
        print(f"❌ Ошибка сохранения кэша: {e}")

# ===== ФУНКЦИИ ПЕРЕВОДА =====
def translate_with_mymemory(text, source_lang='zh', target_lang='ru'):
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text[:500],
            "langpair": f"{source_lang}|{target_lang}"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("responseData") and data["responseData"].get("translatedText"):
                return data["responseData"]["translatedText"]
    except Exception as e:
        print(f"MyMemory error: {e}")
    return None

def translate_with_lingva(text, source_lang='zh', target_lang='ru'):
    try:
        url = f"https://lingva.ml/api/v1/{source_lang}/{target_lang}/{requests.utils.quote(text[:200])}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("translation"):
                return data["translation"]
    except Exception as e:
        print(f"Lingva error: {e}")
    return None

def contains_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def contains_english(text):
    cleaned = re.sub(r'[^a-zA-Zа-яА-ЯёЁ]', '', text)
    if len(cleaned) < 10:
        return False
    english_chars = len(re.findall(r'[a-zA-Z]', cleaned))
    russian_chars = len(re.findall(r'[а-яА-ЯёЁ]', cleaned))
    total = english_chars + russian_chars
    if total == 0:
        return False
    english_percent = english_chars / total
    return english_percent > 0.4 and english_chars > russian_chars

def detect_and_translate(text):
    if not text or len(text.strip()) < 10:
        return text, 'unknown'
    if contains_chinese(text):
        source_lang = 'zh'
        print(f"🇨🇳 Найден китайский текст: {text[:50]}...")
    elif contains_english(text):
        source_lang = 'en'
        print(f"🇬🇧 Найден английский текст: {text[:50]}...")
    else:
        return text, 'ru'
    translated = translate_with_mymemory(text, source_lang)
    if not translated or translated == text:
        print(f"↪️ Пробуем Lingva для {source_lang}...")
        translated = translate_with_lingva(text, source_lang)
    if translated and translated != text:
        print(f"✅ Переведено: {translated[:50]}...")
        return translated, source_lang
    else:
        print(f"⚠️ Не удалось перевести, оставляем оригинал")
        return f"[{source_lang.upper()}] {text}", source_lang

def clean_html(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_text_for_display(text, lang):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    if len(text) > 250:
        text = text[:247] + "..."
    return text

# ===== СБОР НОВОСТЕЙ =====
def fetch_news():
    if is_cache_valid():
        print("📦 Используем кэшированные новости")
        return load_cached_news()
    
    print("🔄 Собираем свежие новости...")
    all_news = []
    
    for theme, feeds in RSS_SOURCES.items():
        for feed_url in feeds:
            try:
                print(f"  → Читаю: {feed_url}")
                feed = feedparser.parse(feed_url)
                if not feed.entries:
                    print(f"  ⚠️ Нет записей в {feed_url}")
                    continue
                for entry in feed.entries[:3]:
                    title = clean_html(entry.get('title', ''))
                    summary = clean_html(entry.get('summary', ''))
                    full_text = f"{title}. {summary}" if summary else title
                    translated_text, source_lang = detect_and_translate(full_text)
                    display_text = clean_text_for_display(translated_text, source_lang)
                    importance = 'high' if random.random() > 0.7 else 'medium'
                    news_item = {
                        "theme": theme,
                        "source": feed.feed.get('title', 'Неизвестно'),
                        "summary": display_text,
                        "url": entry.link,
                        "importance": importance,
                        "date": datetime.now().strftime('%Y-%m-%d %H:%M'),
                        "lang": source_lang
                    }
                    all_news.append(news_item)
            except Exception as e:
                print(f"  ❌ Ошибка с {feed_url}: {e}")
                continue
    
    all_news = all_news[:30]
    save_news_to_cache(all_news)
    print(f"✅ Собрано {len(all_news)} новостей")
    return all_news

# ===== МАРШРУТЫ =====
@app.route('/')
def dashboard():
    today = datetime.now().strftime('%d %B %Y')
    news = fetch_news()
    return render_template('index.html', news=news, today=today)

@app.route('/api/refresh')
def refresh_news():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    news = fetch_news()
    return {"status": "ok", "count": len(news)}

# ===== ЗАПУСК =====
if __name__ == '__main__':
    print("🚀 Запуск дашборда на порту 80")
    app.run(host='0.0.0.0', port=80, debug=False)
