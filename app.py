from flask import Flask, render_template, jsonify
import requests, time

app = Flask(__name__)

ACCESS_TOKEN = "vgKsPgVO0xmk8_omH6SqlB-EexlSCaP_d0G9SDM6ap0"
ACCOUNT_ID   = 3729695

def ct_get(base, path, params=None):
    url = f"{base}{path}"
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
        data = ct_get("https://api.spotware.com", f"/connect/tradingaccounts/{ACCOUNT_ID}")
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/positions")
def api_positions():
    try:
        data = ct_get("https://api.spotware.com", f"/connect/tradingaccounts/{ACCOUNT_ID}/positions")
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/orders")
def api_orders():
    try:
        data = ct_get("https://api.spotware.com", f"/connect/tradingaccounts/{ACCOUNT_ID}/orders")
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/deals")
def api_deals():
    try:
        now_ms  = int(time.time() * 1000)
        from_ms = now_ms - (30 * 24 * 3600 * 1000)
        data = ct_get("https://api.spotware.com", f"/connect/tradingaccounts/{ACCOUNT_ID}/deals",
                      {"from": from_ms, "to": now_ms, "limit": 100})
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/debug")
def api_debug():
    results = {}
    tests = [
        ("https://api.spotware.com", f"/connect/tradingaccounts/{ACCOUNT_ID}"),
        ("https://api.spotware.com", f"/connect/tradingaccounts/{ACCOUNT_ID}/positions"),
        ("https://openapi.ctrader.com", f"/connect/tradingaccounts/{ACCOUNT_ID}"),
        ("https://openapi.ctrader.com", f"/connect/tradingaccounts/{ACCOUNT_ID}/positions"),
    ]
    for base, path in tests:
        try:
            data = ct_get(base, path)
            results[base+path] = {"ok": True, "data": data}
        except Exception as e:
            results[base+path] = {"ok": False, "error": str(e)}
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
