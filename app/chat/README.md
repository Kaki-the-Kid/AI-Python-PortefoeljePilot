# Chat med din CV-assistent

## Arkitektur: Lokal AI-assistent med JSON som kontekst

### 1. Promptmotor

- Læser `competence.json`
- Kombinerer det med brugerens spørgsmål
- Sender det til en AI-model (lokal eller API)

### 2. Flask-route: `/chat`

- POST-endpoint der modtager spørgsmål
- Returnerer AI-genereret svar
- Kan udvides med Material UI eller WebSocket

### 3. **Eksempel på promptmotor**

```python
def generate_cv_response(user_input, competence_data):
    prompt = f"""
Du er en professionel CV-assistent. Brug følgende JSON-data som baggrund:

{json.dumps(competence_data, indent=2, ensure_ascii=False)}

Brugerens spørgsmål: {user_input}

Svar med en professionel, dansk tekst.
"""
    response = call_ai_model(prompt)  # fx OpenAI, LM Studio, LMDeploy
    return response
```

---

## Flask-chatroute

```python
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        competence_data = json.load(f)
    reply = generate_cv_response(user_input, competence_data)
    return jsonify({"reply": reply})
```

---

## 💬 Frontend: Material 3 chat UI (valgfrit)

Du kan bruge:

- `md-outlined-text-field` til input
- `md-elevated-card` til svar
- `fetch("/chat", { method: "POST", body: JSON.stringify({ message }) })` i JS

---

## Hvis du vil bruge det fra ekstern webside

- Eksponér `/chat` via reverse proxy (fx `https://pilot.karsten.dk/chat`)
- Din eksterne webside kan sende POST-requests og vise svaret

---

## Næste trin

1. Vil du bruge en lokal AI-model (fx LM Studio) eller en API som OpenAI?
2. Skal vi bygge en Material UI-chat i browseren?
3. Skal den kunne foreslå tekst, rette formuleringer eller generere hele ansøgninger?

## Min AI-co-pilot

Klar til at skrive min første promptmotor
