from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# ===== ДАННЫЕ (временно в коде) =====
NEWS = [
    {
        "theme": "Дроны",
        "source": "Drone Industry Insights",
        "summary": "DJI представила новую линейку дронов для мониторинга стройплощадок с ИИ-аналитикой",
        "url": "#",
        "importance": "high"
    },
    {
        "theme": "3D-печать",
        "source": "3DPrint.com",
        "summary": "Китайская компания напечатала первый жилой дом за 24 часа",
        "url": "#",
        "importance": "medium"
    },
    {
        "theme": "Недвижимость Москвы",
        "source": "ЦИАН",
        "summary": "Цены на новостройки в Новой Москве выросли на 12% за квартал",
        "url": "#",
        "importance": "high"
    },
    {
        "theme": "Акции/облигации РФ",
        "source": "Мосбиржа",
        "summary": "Облигации Минфина: ставки снижаются на фоне стабильной инфляции",
        "url": "#",
        "importance": "medium"
    },
    {
        "theme": "ИИ в строительстве",
        "source": "Autodesk Blog",
        "summary": "Новая система предсказания дефектов бетона на основе компьютерного зрения",
        "url": "#",
        "importance": "medium"
    }
]

@app.route('/')
def dashboard():
    today = datetime.now().strftime('%d %B %Y')
    return render_template('index.html', news=NEWS, today=today)

if __name__ == '__main__':
    app.run(debug=True)
