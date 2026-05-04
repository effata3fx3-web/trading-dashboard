from flask import Flask, render_template, jsonify
import requests, time

app = Flask(__name__)

ACCESS_TOKEN = "kkiGFyckd7CaG3zBwHQdeo68HGbM330qgGobEce9Mj8"
ACCOUNT_ID   = 3729695
# cTrader Open API v2
BASE_URL     = "https://api.spotware.com"

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
        # Try v2 endpoint first
        data = ct_get(f"/v2/webserv/traders/{ACCOUNT_ID}")
        return jsonify({"ok": True, "data": data})
    except Exception as e1:
        try:
            data = ct_get(f"/connect/tradingaccounts/{ACCOUNT_ID}")
            return jsonify({"ok": True, "data": data})
        except Exception as e2:
            return jsonify({"ok": False, "error": str(e1) + " | " + str(e2)}), 500

@app.route("/api/positions")
def api_positions():
    try:
        data = ct_get(f"/v2/webserv/traders/{ACCOUNT_ID}/positions")
        return jsonify({"ok": True, "data": data})
    except Exception as e1:
        try:
            data = ct_get(f"/connect/tradingaccounts/{ACCOUNT_ID}/positions")
            return jsonify({"ok": True, "data": data})
        except Exception as e2:
            return jsonify({"ok": False, "error": str(e1) + " | " + str(e2)}), 500

@app.route("/api/orders")
def api_orders():
    try:
        data = ct_get(f"/v2/webserv/traders/{ACCOUNT_ID}/orders")
        return jsonify({"ok": True, "data": data})
    except Exception as e1:
        try:
            data = ct_get(f"/connect/tradingaccounts/{ACCOUNT_ID}/orders")
            return jsonify({"ok": True, "data": data})
        except Exception as e2:
            return jsonify({"ok": False, "error": str(e1) + " | " + str(e2)}), 500

@app.route("/api/deals")
def api_deals():
    try:
        now_ms  = int(time.time() * 1000)
        from_ms = now_ms - (30 * 24 * 3600 * 1000)
        data = ct_get(f"/v2/webserv/traders/{ACCOUNT_ID}/deals", {"from": from_ms, "to": now_ms, "limit": 100})
        return jsonify({"ok": True, "data": data})
    except Exception as e1:
        try:
            now_ms  = int(time.time() * 1000)
            from_ms = now_ms - (30 * 24 * 3600 * 1000)
            data = ct_get(f"/connect/tradingaccounts/{ACCOUNT_ID}/deals", {"from": from_ms, "to": now_ms, "limit": 100})
            return jsonify({"ok": True, "data": data})
        except Exception as e2:
            return jsonify({"ok": False, "error": str(e1) + " | " + str(e2)}), 500

@app.route("/api/debug")
def api_debug():
    """Test endpoint to see raw API response"""
    results = {}
    endpoints = [
        f"/v2/webserv/traders/{ACCOUNT_ID}",
        f"/connect/tradingaccounts/{ACCOUNT_ID}",
        f"/v2/webserv/traders/{ACCOUNT_ID}/positions",
        f"/connect/tradingaccounts/{ACCOUNT_ID}/positions",
    ]
    for ep in endpoints:
        try:
            data = ct_get(ep)
            results[ep] = {"ok": True, "data": data}
        except Exception as e:
            results[ep] = {"ok": False, "error": str(e)}
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
