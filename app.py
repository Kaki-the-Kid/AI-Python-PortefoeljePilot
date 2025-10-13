from flask import Flask, redirect, render_template_string, Response, request, send_file
import markdown
import subprocess
import json
import os


app = Flask(__name__)
app.config["DEBUG"] = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "competence.json")


@app.route("/")
def index():
    return "PorteføljePilot kører! Bummer!"

    
@app.route("/kompetencer")
def vis_kompetencer():
    if not os.path.exists(DATA_PATH):
        return "Ingen kompetencefil fundet."

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        cv = json.load(f)
        print("CV-indhold:", cv)

    # Byg Markdown-indhold
    md = f"# {cv.get('name', '')}\n\n"
    md += f"**{cv.get('title', '')}**\n\n"

    # Kontaktinfo
    contact = cv.get("contact", {})
    if contact:
        md += "### Kontakt\n"
        for key, value in contact.items():
            md += f"- **{key.capitalize()}**: {value}\n"
        md += "\n"

    # Kompetencer
    skills = cv.get("skills", [])
    if skills:
        md += "### Kompetencer\n"
        for skill in skills:
            md += f"- {skill}\n"
        md += "\n"


    # Erfaring
    experience = cv.get("experience", [])
    if experience:
        md += "### Erfaring\n"
        for job in experience:
            md += f"**{job['role']}**, {job['company']} ({job['period']})\n"
            for point in job.get("highlights", []):
                md += f"- {point}\n"
            md += "\n"

    # Uddannelse (hvis du har den med)
    education = cv.get("education", [])
    if education:
        md += "### Uddannelse\n"
        for edu in education:
            md += f"**{edu.get('degree', '')}**, {edu.get('institution', '')} ({edu.get('period', '')})\n\n"

    # Kurser
    courses = cv.get("courses", [])
    if courses:
        md += "### Kurser\n"
        for course in courses:
            title = course.get("title", "")
            provider = course.get("provider", "")
            year = course.get("year", "")
            md += f"- {title} ({provider}, {year})\n"
        md += "\n"

    # Sprog
    languages = cv.get("languages", {})
    if languages:
        md += "### Sprog\n"
        for lang, level in languages.items():
            md += f"- {lang.capitalize()}: {level}\n"
        md += "\n"

    # Frivilligt arbejde
    volunteer = cv.get("volunteer", [])
    if volunteer:
        md += "### Frivilligt arbejde\n"
        for v in volunteer:
            md += f"- **{v['role']}**, {v['organization']} ({v['period']})\n"
        md += "\n"

    # Konverter Markdown til HTML
    html = markdown.markdown(md)

    return render_template_string("""
        <html>
        <head>
            <title>Kompetencer</title>
            <style>
                body { font-family: sans-serif; max-width: 800px; margin: auto; padding: 2em; }
                h1, h2, h3 { color: #2c3e50; }
                ul { padding-left: 1.2em; }
            </style>
        </head>
        <body>
            {{ html | safe }}
        </body>
        </html>
    """, html=html)


@app.route("/rediger", methods=["GET", "POST"])
def rediger_kompetencer():
    if request.method == "POST":
        ny_data = request.form.get("jsondata")
        if not ny_data:
            return "Ingen data modtaget."
        try:
            parsed = json.loads(ny_data)
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2, ensure_ascii=False)
            return redirect("/kompetencer")
        except Exception as e:
            return f"Fejl i JSON: {e}"
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            eksisterende = f.read()
    else:
        eksisterende = "[]"
    return render_template_string("""
        <h1>Rediger kompetencer</h1>
        <form method="post">
            <textarea name="jsondata" rows="20" cols="80">{{ eksisterende }}</textarea><br>
            <button type="submit">Gem</button>
        </form>
    """, eksisterende=eksisterende)


@app.route("/test")
def run_tests():
    result = subprocess.run(
        ["pytest", "--tb=short", "--disable-warnings"],
        capture_output=True,
        text=True
    )
    return Response(result.stdout, mimetype="text/plain")


@app.route("/test-report")
def show_report():
    return send_file("tests/report.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
