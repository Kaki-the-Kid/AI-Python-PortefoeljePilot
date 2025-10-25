from flask import Blueprint, render_template, request, jsonify, Response, send_file
import markdown, subprocess, json, socket, requests, os

import subprocess
import json
import socket
import requests
import os

main_bp = Blueprint("main", __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "competence.json")


@main_bp.route("/")
def index():
    return render_template("index.html", status=get_status())


def get_status():
    status = {
        "flask": "OK",
        "localai": "NOT OK",
        "watchdog": "NOT OK"
    }

    # Tjek LocalAI via HTTP
    try:
        r = requests.get("http://localhost:8080/health", timeout=1)
        if r.status_code == 200:
            status["localai"] = "OK"
    except:
        status["localai"] = "NOT OK"

    # Tjek om watchdog-porten er åben (fx 5051)
    try:
        sock = socket.create_connection(("localhost", 5051), timeout=1)
        sock.close()
        status["watchdog"] = "OK"
    except:
        status["watchdog"] = "NOT OK"

    return status


@main_bp.route("/kompetencer")
def show_competences():
    if not os.path.exists(DATA_PATH):
        return "Ingen kompetencefil fundet."

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        cv = json.load(f)

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

    return render_template("competences.html", html=html)


def generate_cv_response(user_input, competence_data):
    prompt = f"""
Du er en dansk CV-assistent. Brug følgende JSON-data som baggrund:

{json.dumps(competence_data, indent=2, ensure_ascii=False)}

Brugerens spørgsmål: {user_input}
Svar med en professionel, dansk tekst.
"""

    response = requests.post("http://localai:8080/v1/chat/completions", json={
        "model": "mistral",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    })

    return response.json()["choices"][0]["message"]["content"]


@main_bp.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "Ingen besked modtaget"}), 400

    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            competence_data = json.load(f)
    else:
        competence_data = {}

    reply = generate_cv_response(user_input, competence_data)
    return jsonify({"reply": reply})


@main_bp.route("/status")
def status():
    return jsonify(get_status())


@main_bp.route("/test")
def run_tests():
    result = subprocess.run(
        ["pytest", "--tb=short", "--disable-warnings"],
        capture_output=True,
        text=True
    )
    return Response(result.stdout, mimetype="text/plain")


@main_bp.route("/test-report")
def show_report():
    return send_file("tests/report.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
