# WellVia

**WellVia** is a support-matching platform that helps people find the right healthcare,
elder care, disability support, mental wellness, food support, and community services
based on their individual needs.

> Built as a hackathon demo project using Python + Flask.

---

## 📁 Project Structure

```
WellVia/
├── app.py                  ← Main Flask application (routes + matching algorithm)
├── requirements.txt        ← Python packages needed
├── Dockerfile              ← For deploying on Google Cloud Run
├── README.md               ← This file
├── templates/
│   ├── index.html          ← Home page
│   ├── help.html           ← "I Need Help" form
│   ├── results.html        ← Matching results page
│   ├── want_help.html      ← "I Want to Help" form
│   └── providers.html      ← Full provider directory
└── static/
    ├── style.css           ← All CSS styles
    └── script.js           ← JavaScript (nav toggle, form validation)
```

---

## 🚀 How to Run Locally

### Step 1 — Make sure Python is installed
Open a terminal and run:
```bash
python --version
```
You should see something like `Python 3.11.x`. If not, download it from https://python.org

### Step 2 — Install dependencies
In your terminal, navigate to the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 3 — Start the app
```bash
python app.py
```

### Step 4 — Open in your browser
Visit: **http://localhost:5000**

---

## 🧪 How to Test the Matching Feature

1. Go to **http://localhost:5000/help**
2. Select a category (e.g. **Healthcare**)
3. Enter a city (e.g. **Delhi**)
4. Choose budget and language
5. Click **Find Matching Providers**
6. You'll see results sorted by match percentage (highest first)

### Example test — 100% match:
- Category: `Healthcare`
- Location: `Delhi`
- Budget: `Free`
- Language: `Hindi`

Expected top result: **City Health Clinic** — 100% match ✅

### Example test — Partial match:
- Category: `Healthcare`
- Location: `Kolkata`  ← no provider in Kolkata for Healthcare
- Budget: `Any`
- Language: `Any`

This will return providers that match on category but not location.

---

## 📋 How the Matching Algorithm Works

The algorithm in `app.py` gives each provider a score out of 4:

| Criterion | Match | Points |
|-----------|-------|--------|
| Category  | Same as user's choice | +1 |
| Location  | Same city (case-insensitive) | +1 |
| Budget    | Same budget OR user chose "Any" | +1 |
| Language  | Same language OR provider offers "Both" OR user chose "Any" | +1 |

Match % = `(score / 4) × 100`

Results are sorted from highest to lowest match %.

---

## 🌐 Pages

| URL | Page |
|-----|------|
| `/` | Home page |
| `/help` | I Need Help form |
| `/results` | Matching results (POST from /help) |
| `/want-help` | I Want to Help form |
| `/submit-provider` | Handles provider form submission (POST) |
| `/providers` | Full provider directory |

---

## ☁️ Deploying on Google Cloud Run

### Prerequisites
- Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- Create a Google Cloud project
- Enable Cloud Run and Container Registry APIs

### Deploy Steps
```bash
# 1. Build the Docker image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/wellvia

# 2. Deploy to Cloud Run
gcloud run deploy wellvia \
  --image gcr.io/YOUR_PROJECT_ID/wellvia \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Replace `YOUR_PROJECT_ID` with your actual Google Cloud project ID.

---

## ⚠️ Disclaimer

All provider data in this application is **sample/demo data** created for demonstration
purposes only. It does not represent real organisations or services. Always verify
provider details independently before making any healthcare or support decisions.

---

## 🛠️ Technologies Used

- **Python 3.11**
- **Flask 3.0** — web framework
- **Gunicorn** — production web server (for deployment)
- **HTML5 + CSS3** — frontend templates
- **Vanilla JavaScript** — navigation and form validation
- **No external APIs, no database** — keeps it simple!

---

*Built with ❤️ for the WellVia hackathon.*
