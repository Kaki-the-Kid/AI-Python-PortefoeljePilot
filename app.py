from flask import Flask, render_template_string, Response, send_file
import markdown
import subprocess
import json
import os

app = Flask(__name__)
DATA_PATH = "./data/competence.json"


@app.route("/")
def index():
    md_path = "./docker/portefoljepilot/data/intro.md"
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        html = markdown.markdown(content)
        return render_template_string("<html><body>{{ html|safe }}</body></html>", html=html)
    else:
        return "Ingen data fundet."

    
@app.route("/kompetencer")
def vis_kompetencer():
    if not os.path.exists(DATA_PATH):
        return "Ingen kompetencefil fundet."
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    html = "<h1>Kompetencer</h1>"
    for kategori in data:
        html += f"<h2>{kategori['category']}</h2><ul>"
        for skill in kategori["skills"]:
            html += f"<li>{skill}</li>"
        html += "</ul>"
    return render_template_string(html)


@app.route("/rediger", methods=["GET", "POST"])
def rediger_kompetencer():
    if request.method == "POST":
        ny_data = request.form.get("jsondata")
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
