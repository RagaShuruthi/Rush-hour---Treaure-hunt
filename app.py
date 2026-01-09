from flask import Flask, render_template, jsonify

app = Flask(__name__)

# ---- HOME ----
@app.route("/")
def home():
    return render_template("index.html")

# ---- LEVEL ROUTES (No login/session) ----
@app.route("/level1")
def level1():
    return render_template("level1.html")

@app.route("/level2")
def level2():
    return render_template("level2.html")

@app.route("/level3")
def level3():
    return render_template("level3.html")

@app.route("/level4")
def level4():
    return render_template("level4.html")

@app.route("/level5")
def level5():
    return render_template("level5.html")

@app.route("/level6")
def level6():
    return render_template("level6.html")

@app.route("/final")
def final_page():
    return render_template("final.html")

# ---- Local QR Verify API (optional if needed later) ----
@app.route("/api/official-qr")
def official_qr():
    return jsonify({"qr": "SIET-RUSH-HUNT-2026"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
