# ============================================================
# WellVia - Flask Backend
# ============================================================
# This is the main application file.
# It defines all the routes (pages) and the matching algorithm.
# ============================================================

from flask import Flask, render_template, request, redirect, url_for
import json
import os

# Create the Flask app
app = Flask(__name__)

# ============================================================
# SAMPLE PROVIDER DATA
# This is our demo data. In a real app, this would come from
# a database. Here we store it in a Python list.
# ============================================================
PROVIDERS = [
    {
        "id": 1,
        "name": "City Health Clinic",
        "category": "Healthcare",
        "location": "Delhi",
        "budget": "Free",
        "language": "Hindi",
        "description": "A community health clinic offering free consultations for low-income families, general check-ups, and referrals.",
        "contact": "cityhealthclinic@example.com | 011-2345-6789"
    },
    {
        "id": 2,
        "name": "Sunrise Elder Care",
        "category": "Elder Care",
        "location": "Mumbai",
        "budget": "Moderate",
        "language": "English",
        "description": "Professional elder care services including day care, assisted living support, and home visits for seniors.",
        "contact": "sunrise@example.com | 022-9876-5432"
    },
    {
        "id": 3,
        "name": "Sahayak Disability Support",
        "category": "Disability Support",
        "location": "Bangalore",
        "budget": "Low Cost",
        "language": "Both",
        "description": "Assistive technology, mobility aids, and counselling services for people with physical and developmental disabilities.",
        "contact": "sahayak@example.com | 080-1122-3344"
    },
    {
        "id": 4,
        "name": "MindEase Wellness Centre",
        "category": "Mental Wellness",
        "location": "Delhi",
        "budget": "Low Cost",
        "language": "Both",
        "description": "Confidential mental health counselling, stress management workshops, and community support groups.",
        "contact": "mindease@example.com | 011-5566-7788"
    },
    {
        "id": 5,
        "name": "Annapurna Food Bank",
        "category": "Food Support",
        "location": "Chennai",
        "budget": "Free",
        "language": "Hindi",
        "description": "Daily meal distribution, grocery aid, and nutrition support for families in need.",
        "contact": "annapurna@example.com | 044-2233-4455"
    },
    {
        "id": 6,
        "name": "Neighbourhood Connect",
        "category": "Community Support",
        "location": "Hyderabad",
        "budget": "Free",
        "language": "English",
        "description": "Volunteers help with errands, companionship, and connecting residents to local services.",
        "contact": "nbconnect@example.com | 040-6677-8899"
    },
    {
        "id": 7,
        "name": "HopeWell Clinic",
        "category": "Healthcare",
        "location": "Mumbai",
        "budget": "Low Cost",
        "language": "Both",
        "description": "Affordable general health services, preventive care, and women's health programmes.",
        "contact": "hopewell@example.com | 022-4455-6677"
    },
    {
        "id": 8,
        "name": "GoldenYears Home Care",
        "category": "Elder Care",
        "location": "Delhi",
        "budget": "Moderate",
        "language": "Hindi",
        "description": "In-home elder care with trained caregivers, physiotherapy, and companionship services.",
        "contact": "goldenyears@example.com | 011-8899-0011"
    },
    {
        "id": 9,
        "name": "Shakti Community Kitchen",
        "category": "Food Support",
        "location": "Bangalore",
        "budget": "Free",
        "language": "Both",
        "description": "Hot meals served daily. Special nutrition plans for children, pregnant women, and the elderly.",
        "contact": "shakti@example.com | 080-3344-5566"
    },
    {
        "id": 10,
        "name": "CalmPath Mental Health",
        "category": "Mental Wellness",
        "location": "Pune",
        "budget": "Moderate",
        "language": "English",
        "description": "Professional therapists, anxiety and depression support, and online session options.",
        "contact": "calmpath@example.com | 020-7788-9900"
    },
    {
        "id": 11,
        "name": "AccessLife Support",
        "category": "Disability Support",
        "location": "Delhi",
        "budget": "Free",
        "language": "Hindi",
        "description": "Legal aid, workplace accessibility consulting, and peer support for persons with disabilities.",
        "contact": "accesslife@example.com | 011-2200-3311"
    },
    {
        "id": 12,
        "name": "Community Roots",
        "category": "Community Support",
        "location": "Kolkata",
        "budget": "Free",
        "language": "Both",
        "description": "Grassroots community network offering skill workshops, local events, and social connection programmes.",
        "contact": "communityroots@example.com | 033-4455-6677"
    },
]

# ============================================================
# PATH TO THE JSON FILE WHERE REGISTERED PROVIDERS ARE SAVED
# The file sits in the same folder as app.py.
# It is created automatically on the first submission.
# ============================================================
REGISTERED_FILE = os.path.join(os.path.dirname(__file__), "providers.json")


def load_registered_providers():
    """
    Read providers.json and return a list of provider dicts.
    Returns an empty list if the file does not exist or is corrupt —
    so the app never crashes due to a missing/bad file.
    """
    if not os.path.exists(REGISTERED_FILE):
        return []
    try:
        with open(REGISTERED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Make sure we always return a list
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        # File is empty or malformed — treat as no submissions yet
        return []


def save_registered_providers(providers_list):
    """
    Write the full list of registered providers to providers.json.
    indent=2 makes the file human-readable (easy to inspect).
    """
    with open(REGISTERED_FILE, "w", encoding="utf-8") as f:
        json.dump(providers_list, f, indent=2, ensure_ascii=False)


# ============================================================
# STATE → CITIES MAPPING
# Allows a user who types a state name to match providers in
# cities within that state.
# Add more states/cities here as needed.
# ============================================================
STATE_CITIES = {
    "chhattisgarh": ["raipur", "bhilai", "bilaspur", "durg"],
    "maharashtra":  ["mumbai", "pune", "nagpur", "nashik", "aurangabad"],
    "delhi":        ["delhi", "new delhi"],
    "karnataka":    ["bangalore", "mysore", "hubli", "mangalore"],
    "tamil nadu":   ["chennai", "coimbatore", "madurai", "salem"],
    "west bengal":  ["kolkata", "howrah", "durgapur", "asansol"],
    "telangana":    ["hyderabad", "warangal", "karimnagar"],
    "uttar pradesh":["lucknow", "kanpur", "agra", "varanasi", "noida"],
    "gujarat":      ["ahmedabad", "surat", "vadodara", "rajkot"],
    "rajasthan":    ["jaipur", "jodhpur", "udaipur", "kota"],
    "punjab":       ["chandigarh", "ludhiana", "amritsar", "jalandhar"],
}

def location_matches(user_input, provider_city):
    """
    Returns True if the user's location input matches the provider's city.

    Three ways it can match:
      1. Exact city match (case-insensitive):  "Delhi" == "Delhi"
      2. User typed a state and provider is in that state:
         "Chhattisgarh" → matches "Raipur", "Bhilai", etc.
      3. Provider's city is a state name that contains the user's city
         (reverse lookup — less common but handles edge cases)
    """
    user_lower     = user_input.strip().lower()
    provider_lower = provider_city.strip().lower()

    # 1. Direct city match
    if user_lower == provider_lower:
        return True

    # 2. User typed a state name → check if provider's city is in that state
    if user_lower in STATE_CITIES:
        if provider_lower in STATE_CITIES[user_lower]:
            return True

    # 3. Provider's city appears to be a state name that contains the user's city
    if provider_lower in STATE_CITIES:
        if user_lower in STATE_CITIES[provider_lower]:
            return True

    return False


# ============================================================
# WEIGHTED MATCHING ALGORITHM
#
# Each criterion contributes a fixed percentage to the final score:
#   Category  = 40 points  (most important — must be the right type)
#   Location  = 30 points  (second — proximity matters)
#   Budget    = 20 points  (third — affordability)
#   Language  = 10 points  (fourth — nice to have)
#   Total max = 100 points
#
# For every criterion we also record a human-readable reason
# (matched or not) so the results page can show ✓ / ✗ rows.
# ============================================================
def match_providers(category, location, budget, language):
    results = []

    # Load registered providers fresh from the JSON file each time.
    # This means newly submitted providers are always included.
    registered = load_registered_providers()

    for provider in PROVIDERS + registered:
        score = 0

        # Each item in breakdown is a dict:
        #   { "label": "...", "points": N, "matched": True/False, "note": "..." }
        breakdown = []

        # --- Category (40 points) ---
        cat_matched = provider["category"] == category
        if cat_matched:
            score += 40
        breakdown.append({
            "label":   "Category",
            "points":  40,
            "matched": cat_matched,
            "note":    f"Offers {provider['category']}" if cat_matched
                       else f"Offers {provider['category']}, you need {category}",
        })

        # --- Location (30 points) ---
        loc_matched = location_matches(location, provider["location"])
        if loc_matched:
            score += 30
        breakdown.append({
            "label":   "Location",
            "points":  30,
            "matched": loc_matched,
            "note":    f"Located in {provider['location']}" if loc_matched
                       else f"Provider is in {provider['location']}",
        })

        # --- Budget (20 points) ---
        # Matches when: user chose "Any", OR budgets are equal, OR provider is "Any"
        bud_matched = (
            budget == "Any"
            or provider["budget"] == budget
            or provider["budget"] == "Any"
        )
        if bud_matched:
            score += 20
        breakdown.append({
            "label":   "Budget",
            "points":  20,
            "matched": bud_matched,
            "note":    f"Provider offers {provider['budget']} services" if bud_matched
                       else f"Provider is {provider['budget']}, you want {budget}",
        })

        # --- Language (10 points) ---
        # Matches when: user chose "Any", OR provider offers "Both",
        # OR user wants "Both", OR exact match
        provider_lang = provider["language"]
        lang_matched = (
            language == "Any"
            or provider_lang == language
            or provider_lang == "Both"
            or language == "Both"
        )
        if lang_matched:
            score += 10
        breakdown.append({
            "label":   "Language",
            "points":  10,
            "matched": lang_matched,
            "note":    f"Available in {provider_lang}" if lang_matched
                       else f"Provider uses {provider_lang}, you prefer {language}",
        })

        results.append({
            **provider,
            "score":         score,         # 0–100
            "match_percent": score,          # already out of 100
            "breakdown":     breakdown,      # list of 4 criterion dicts
        })

    # Sort highest match first
    results.sort(key=lambda x: x["score"], reverse=True)

    # Drop providers with zero score
    results = [r for r in results if r["score"] > 0]

    return results


# ============================================================
# ROUTES (Pages)
# ============================================================

# --- Home Page ---
@app.route("/")
def index():
    return render_template("index.html")


# --- I Need Help Page (shows the form) ---
@app.route("/help")
def help_page():
    return render_template("help.html")


# --- Process the Help form and show results ---
@app.route("/results", methods=["POST"])
def results():
    # Read form data submitted by the user
    category = request.form.get("category", "").strip()
    location = request.form.get("location", "").strip()
    budget = request.form.get("budget", "Any")
    language = request.form.get("language", "Any")

    # Basic validation: category and location are required
    errors = []
    if not category:
        errors.append("Please select a support category.")
    if not location:
        errors.append("Please enter your location.")

    if errors:
        return render_template("help.html", errors=errors)

    # Run the matching algorithm
    matched = match_providers(category, location, budget, language)

    return render_template(
        "results.html",
        providers=matched,
        query={
            "category": category,
            "location": location,
            "budget": budget,
            "language": language,
        },
    )


# --- I Want to Help Page (shows the form) ---
@app.route("/want-help")
def want_help():
    return render_template("want_help.html")


# --- Process the "I Want to Help" form ---
@app.route("/submit-provider", methods=["POST"])
def submit_provider():
    name        = request.form.get("name", "").strip()
    category    = request.form.get("category", "").strip()
    location    = request.form.get("location", "").strip()
    budget      = request.form.get("budget", "").strip()
    language    = request.form.get("language", "").strip()
    description = request.form.get("description", "").strip()
    contact     = request.form.get("contact", "").strip()

    # Validate required fields
    errors = []
    if not name:
        errors.append("Organisation/Volunteer name is required.")
    if not category:
        errors.append("Please select a support category.")
    if not location:
        errors.append("Please enter your location.")
    if not contact:
        errors.append("Contact information is required.")

    if errors:
        return render_template("want_help.html", errors=errors)

    # Load the current list of registered providers from the JSON file
    registered = load_registered_providers()

    # Build the new provider record.
    # "type": "registered" distinguishes it from the built-in demo providers.
    new_provider = {
        "id":          len(PROVIDERS) + len(registered) + 1,
        "type":        "registered",
        "name":        name,
        "category":    category,
        "location":    location,
        "budget":      budget      if budget      else "Any",
        "language":    language    if language    else "Any",
        "description": description if description else "",
        "contact":     contact,
    }

    # Add to the list and save back to providers.json
    registered.append(new_provider)
    save_registered_providers(registered)

    return render_template("want_help.html", success=True, provider_name=name)


# --- Provider Directory ---
@app.route("/providers")
def providers():
    # Combine hardcoded demo providers with JSON-persisted registered providers.
    # Demo providers get "type": "demo" added here so the template can tell them apart.
    demo = [{**p, "type": "demo"} for p in PROVIDERS]
    registered = load_registered_providers()
    all_providers = demo + registered
    return render_template("providers.html", providers=all_providers)


# ============================================================
# Run the app
# PORT is read from environment so Google Cloud Run can set it.
# ============================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
