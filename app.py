from flask import Flask, render_template, request, redirect, session, jsonify
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = "kutta_hunt_secret"

# ---- JSON DB HANDLERS ----
def load_db():
    if not os.path.exists("db.json"):
        default_db = {
            "teams": [],
            "scores": {},
            "hunt_start_time": "",
            "official_qr_code": "SIET-RUSH-HUNT-2026"
        }
        save_db(default_db)
        return default_db

    with open("db.json", "r") as f:
        return json.load(f)

def save_db(db):
    with open("db.json", "w") as f:
        json.dump(db, f, indent=2)

# ---- LOGIN ----
@app.route("/login", methods=["GET", "POST"])
def login():
    db = load_db()

    if request.method == "POST":
        team_input = request.form["team_name"].strip()
        team_lower = team_input.lower()
        teams_lower = {t.lower(): t for t in db["teams"]}

        if team_lower in teams_lower:
            actual_team = teams_lower[team_lower]
            session["team"] = actual_team

            # If first login in the hunt, start timer
            if not db["hunt_start_time"]:
                start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db["hunt_start_time"] = start
                save_db(db)

            # Add team to scores if not already present
            if actual_team not in db["scores"]:
                db["scores"][actual_team] = {
                    "score": 0,
                    "updated_at": datetime.now().strftime("%H:%M:%S"),
                    "login_time": datetime.now().strftime("%H:%M:%S")
                }
                save_db(db)

            return redirect("/index")

        else:
            return render_template("login.html", error="Team not registered ❌")

    return render_template("login.html")

# ---- HOME ----
@app.route("/")
def home():
    return redirect("/login")

@app.route("/index")
def index_page():
    if "team" not in session:
        return redirect("/login")
    return render_template("index.html", team=session["team"])

# ---- LEVEL ROUTES ----
@app.route("/level1")
def level1():
    if "team" not in session: return redirect("/login")
    return render_template("level1.html", team=session["team"])

@app.route("/level2")
def level2():
    if "team" not in session: return redirect("/login")
    return render_template("level2.html", team=session["team"])

@app.route("/level3")
def level3():
    if "team" not in session: return redirect("/login")
    return render_template("level3.html", team=session["team"])

@app.route("/level4")
def level4():
    if "team" not in session: return redirect("/login")
    return render_template("level4.html", team=session["team"])

@app.route("/level5")
def level5():
    if "team" not in session: return redirect("/login")
    return render_template("level5.html", team=session["team"])

@app.route("/level6")
def level6():
    if "team" not in session: return redirect("/login")
    return render_template("level6.html", team=session["team"])

@app.route("/final")
def final_page():
    if "team" not in session: return redirect("/login")
    return render_template("final.html", team=session["team"])

@app.route("/leaderboard")
def leaderboard():
    if "team" not in session:
        return redirect("/login")

    db = load_db()
    return render_template("leaderboard.html", team=session["team"], scores=db["scores"])


# ---- QR VERIFY ----
@app.route("/verify_qr", methods=["POST"])
def verify_qr():
    db = load_db()
    scanned = request.json.get("qr", "").strip().lower()
    official = db["official_qr_code"].strip().lower()
    return jsonify({"valid": scanned == official})

# ---- SCORE UPDATE (LEVEL SUCCESS) ----
@app.route("/update_score", methods=["POST"])
def update_score():
    if "team" not in session:
        return jsonify({"error": "Not logged in"}), 401

    db = load_db()
    team = session["team"]
    add = request.json.get("score", 0)

    # Check 2-hour hunt limit
    start_time = datetime.strptime(db["hunt_start_time"], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > start_time + timedelta(hours=2):
        return jsonify({"hunt_active": False, "message": "⏳ Hunt time is over!"})

    # Update score without overwriting
    db["scores"][team]["score"] += add
    db["scores"][team]["updated_at"] = datetime.now().strftime("%H:%M:%S")
    save_db(db)

    return jsonify({"updated": True, "hunt_active": True})

# ---- GET SCORES FOR FRONTEND ----
@app.route("/get_scores")
def get_scores():
    db = load_db()
    return jsonify({"scores": db["scores"], "hunt_start_time": db["hunt_start_time"]})

# ---- LOGOUT ----
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
