from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "resume-secret-key-2026"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "messages.db")

# ---------- دیتای سایت (اینجا اسم و مشخصات خودت رو عوض کن) ----------
PROFILE = {
    "name": "نیکان عظیمی",
    "title": "توسعه‌دهنده پایتون و وب",
    "bio": "من عاشق ساختن چیزهای کاربردی با پایتونم؛ از سایت و ربات تا ابزارهای کوچک. دنبال پروژه‌های واقعی و یادگیری عمیق.",
    "email": "nikanazimi1393@gmail.com",
    "phone": "0912-000-0000",
    "location": "تهران، ایران",
    "github": "https://github.com/nikanazimi1393-design",
    "linkedin": "https://linkedin.com/",
    "avatar": "ن",
}

SKILLS = [
    {"name": "Python", "level": 85},
    {"name": "Flask", "level": 80},
    {"name": "HTML / CSS", "level": 75},
    {"name": "JavaScript", "level": 60},
    {"name": "Git", "level": 70},
    {"name": "SQL", "level": 65},
]

PROJECTS = [
    {"id": 1, "title": "بازی رانندگی ایران (Iran Driving)", "cat": "بازی",
     "desc": "بازی رانندگی اول‌شخص با Godot 4؛ فرمون لمسی، بیلد خودکار APK با GitHub Actions و نقشه واقعی خیابون‌های تهران از OpenStreetMap.",
     "tech": ["Godot 4", "GDScript", "Python"], "emoji": "🚗",
     "link": "https://github.com/nikanazimi1393-design/iran-driving"},
    {"id": 2, "title": "مینی GTA (OutlawCity)", "cat": "بازی",
     "desc": "بازی جهان‌باز شبه-GTA با Godot؛ صحنه‌های شهری، اسکریپت‌های گیم‌پلی و خروجی APK اندروید.",
     "tech": ["Godot", "C#"], "emoji": "🏙️",
     "link": "https://github.com/nikanazimi1393-design/mini-gta-game"},
    {"id": 3, "title": "ربات تلگرام هوش مصنوعی", "cat": "پایتون",
     "desc": "ربات تلگرامی متصل به OpenRouter؛ جواب‌گویی هوشمند، تاریخچه چت در RAM، دستور start و استقرار روی Termux.",
     "tech": ["Python", "Telegram Bot", "OpenRouter"], "emoji": "🤖",
     "link": "https://github.com/nikanazimi1393-design/telegram-ai-bot"},
    {"id": 4, "title": "اپ چت هوش مصنوعی (AI Chat)", "cat": "وب",
     "desc": "وب‌اپ چت با هوش مصنوعی؛ رابط مدرن و اتصال به API مدل‌های زبانی.",
     "tech": ["HTML", "JavaScript", "API"], "emoji": "💬",
     "link": "https://github.com/nikanazimi1393-design/ai-chat-app"},
    {"id": 5, "title": "بازی Warzone سه‌بعدی", "cat": "بازی",
     "desc": "بتل‌رویال اول‌شخص تحت وب با Three.js؛ ۲۴ بات هوشمند، زون گازی، کیل‌استریک UAV و حمله هوایی.",
     "tech": ["JavaScript", "Three.js"], "emoji": "🎮",
     "link": ""},
    {"id": 6, "title": "سایت رزومه شخصی (همین سایت)", "cat": "وب",
     "desc": "سایت رزومه فارسی با Flask؛ چند صفحه، فرم تماس با دیتابیس، حالت شب/روز و API پروژه‌ها.",
     "tech": ["Python", "Flask", "SQLite"], "emoji": "📄",
     "link": "https://github.com/nikanazimi1393-design/rozume"},
]

TIMELINE = [
    {"year": "۱۴۰۵", "title": "بازی‌سازی با Godot", "text": "ساخت Iran Driving و Mini-GTA؛ بیلد APK و GitHub Actions."},
    {"year": "۱۴۰۴", "title": "هوش مصنوعی و ربات", "text": "ساخت ربات تلگرام AI با OpenRouter و وب‌اپ چت."},
    {"year": "۱۴۰۳", "title": "شروع برنامه‌نویسی", "text": "آشنایی با پایتون، HTML و اولین پروژه‌های وب."},
]

# ---------- دیتابیس پیام‌ها ----------
def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT, msg TEXT, created TEXT)""")
    con.commit()
    con.close()

init_db()

# ---------- روت‌ها ----------
@app.route("/")
def index():
    return render_template("index.html", profile=PROFILE,
                           skills=SKILLS, projects=PROJECTS[:3])

@app.route("/about")
def about():
    return render_template("about.html", profile=PROFILE,
                           skills=SKILLS, timeline=TIMELINE)

@app.route("/portfolio")
def portfolio():
    cat = request.args.get("cat", "همه")
    cats = ["همه"] + sorted(set(p["cat"] for p in PROJECTS))
    if cat == "همه":
        items = PROJECTS
    else:
        items = [p for p in PROJECTS if p["cat"] == cat]
    return render_template("portfolio.html", projects=items,
                           cats=cats, active=cat, profile=PROFILE)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        msg = request.form.get("msg", "").strip()
        if not name or not msg:
            flash("نام و متن پیام الزامی است.", "error")
        else:
            con = sqlite3.connect(DB)
            cur = con.cursor()
            cur.execute("INSERT INTO messages(name,email,msg,created) VALUES(?,?,?,?)",
                        (name, email, msg, datetime.now().strftime("%Y-%m-%d %H:%M")))
            con.commit()
            con.close()
            flash("پیامت رسید! به‌زودی جواب میدم. ✅", "ok")
            return redirect(url_for("contact"))
    return render_template("contact.html", profile=PROFILE)

@app.route("/api/projects")
def api_projects():
    return jsonify(PROJECTS)

@app.route("/messages")
def messages():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT name,email,msg,created FROM messages ORDER BY id DESC LIMIT 20")
    rows = cur.fetchall()
    con.close()
    html = "<h2>پیام‌ها (فقط خودت ببین)</h2>" + "".join(
        f"<div style='border:1px solid #333;padding:10px;margin:8px;border-radius:8px'><b>{r[0]}</b> ({r[1]})<br>{r[2]}<br><small>{r[3]}</small></div>"
        for r in rows) or "<p>پیامی نیست.</p>"
    return html

if __name__ == "__main__":
    app.run(debug=True, port=5000)
