# AI PorteføljePilot i Python

**PorteføljePilot** er en personlig AI-assistent, der guider besøgende gennem mine kompetencer, projekter og erfaringer – med interaktive forklaringer, kodeeksempler og links til GitHub og CV. Projektet er både en dokumentation af mine evner og en demonstration af, hvordan AI og automation kan bruges til at skabe værdi.

## Formål

- Gøre mine kompetencer levende og søgbare
- Samle mine projekter under én interaktiv platform
- Demonstrere praktisk brug af AI, automation og systemintegration
- Give besøgende en engagerende og personlig oplevelse

## Teknisk Arkitektur (foreløbig)

- **Frontend:** HTML/CSS + JavaScript (evt. med chat UI)
- **Backend:** Python med Flask eller FastAPI
- **LLM-motor:** Lokalt hostet via LM Studio, Ollama eller GPT4All
- **Data:** Kompetencer og projekter struktureret i JSON/Markdown
- **Prompt-engine:** Egen struktur baseret på brugerinput og kontekst

## Eksempler på interaktioner

```text
Bruger: Hvad har Karsten lavet med Python?
Bot: Karsten har udviklet scripts til automatisering, overvågning og integration med Synology NAS. Se et eksempel her: [link]

## Deployment

✅ Lokal drift og privatl
Jeg undgår cloud-afhængighed og bevarer fuld kontrol over data og AI-interaktioner – præcis som du foretrækker.
✅ Let deployment
Med Docker kan jeg:
- Pakke hele appen (Flask + frontend + data) i én container
- Køre den som en webservice på din NAS
- Opdatere og vedligeholde med minimale konflikter
✅ Ressourcevenlig
Jeg kan holde det let:
- Ingen tunge databaser nødvendige (JSON/Markdown er nok)
- Ingen ekstern API-afhængighed, hvis du bruger lokal LLM (fx via Ollama)
✅ Integration med dit eksisterende setup
- Jeg kan koble den til overvågningsscripts, GitHub-webhooks eller endda en lokal promptserver
- Du kan styre adgang via Synology Reverse Proxy og evt. HTTPS
