from flask import Flask, render_template, jsonify
import requests, time

app = Flask(__name__)

ACCESS_TOKEN = "kkiGFyckd7CaG3zBwHQdeo68HGbM330qgGobEce9Mj8"
ACCOUNT_ID   = 3729695
BASE_URL     = "https://api.spotware.com/connect"

def ct_get(path, params=None):
    url = f"{BASE_URL}{path}"
    p = {"access_token": ACCESS_TOKEN}
    if params:
        p.update(params)
    r = requests.get(url, params=p, timeout=15)
    r.raise_for_status()
    return r.json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/account")
def api_account():
    try:
        return jsonify({"ok": True, "data": ct_get(f"/tradingaccounts/{ACCOUNT_ID}")})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/positions")
def api_positions():
    try:
        return jsonify({"ok": True, "data": ct_get(f"/tradingaccounts/{ACCOUNT_ID}/positions")})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/orders")
def api_orders():
    try:
        return jsonify({"ok": True, "data": ct_get(f"/tradingaccounts/{ACCOUNT_ID}/orders")})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/deals")
def api_deals():
    try:
        now_ms  = int(time.time() * 1000)
        from_ms = now_ms - (30 * 24 * 3600 * 1000)
        return jsonify({"ok": True, "data": ct_get(f"/tradingaccounts/{ACCOUNT_ID}/deals", {"from": from_ms, "to": now_ms, "limit": 100})})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
