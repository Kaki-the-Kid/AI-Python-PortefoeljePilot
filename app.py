from flask import Flask, render_template_string
import markdown
import os

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
