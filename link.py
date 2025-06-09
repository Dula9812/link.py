from flask import Flask, request, render_template_string
import uuid
import json
import os

app = Flask(__name__)
DB_FILE = 'data.json'

# Replace with your real Adsterra direct link
ADSTERRA_DIRECT_LINK = "https://databoilrecommendation.com/a52kwdsp?key=48733586a54d108787728e166e87a4b6"

# Load existing data or create new
if os.path.exists(DB_FILE):
    with open(DB_FILE, 'r') as f:
        url_db = json.load(f)
else:
    url_db = {}

def save_db():
    with open(DB_FILE, 'w') as f:
        json.dump(url_db, f)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="7searchppc" content="0441801e11cd79128f45417f4a693374"/>
        <title>QuickLink Shortener</title>
        <style>
            body {
                background: #f0f4f8;
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 500px;
                width: 90%;
            }
            input[type="text"] {
                width: 80%;
                padding: 10px;
                margin-top: 20px;
                font-size: 16px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            input[type="submit"] {
                margin-top: 20px;
                padding: 10px 20px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🔗 QuickLink Shortener</h2>
            <form action="/shorten" method="post">
                <input type="text" name="long_url" placeholder="Paste your long URL here" required />
                <br>
                <input type="submit" value="Shorten URL" />
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    key = str(uuid.uuid4())[:8]
    url_db[key] = {"url": long_url}
    save_db()
    
    short_link = f"/go/{key}"

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shortened URL</title>
        <style>
            body {{
                background: #f7f8fc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .card {{
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                text-align: center;
                width: 90%;
                max-width: 500px;
            }}
            .link-box {{
                margin: 20px 0;
                font-size: 18px;
                word-wrap: break-word;
                background: #f0f0f0;
                padding: 10px;
                border-radius: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .btn {{
                padding: 10px 20px;
                border: none;
                background: #4CAF50;
                color: white;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                margin: 10px;
            }}
            .btn:hover {{
                background: #45a049;
            }}
            .copy-btn {{
                background: #008CBA;
            }}
            .copy-btn:hover {{
                background: #0078a0;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>✅ Your Shortened Link</h2>
            <div class="link-box">
                <span id="shortLink">urlsh.com{short_link}</span>
                <button class="btn copy-btn" onclick="copyLink()">Copy</button>
            </div>
            <a href="/" class="btn">🔁 Short Another URL</a>
        </div>

        <script>
            function copyLink() {{
                const text = document.getElementById('shortLink').innerText;
                navigator.clipboard.writeText(window.location.origin + '{short_link}');
                alert("Link copied to clipboard!");
            }}
        </script>
    </body>
    </html>
    '''

@app.route('/go/<key>')
def go(key):
    if key not in url_db:
        return "Invalid or expired link", 404

    long_url = url_db[key]['url']

    return render_template_string(f"""
    <html>
    <head>
        <title>Redirecting...</title>
        <script>
            window.onload = function() {{
                window.open("{ADSTERRA_DIRECT_LINK}", "_blank");
                window.open("{long_url}", "_blank");
            }};
        </script>
    </head>
    <body>
        <h3>✅ Both links are opening in new tabs...</h3>
        <p>If nothing happens, please allow pop-ups.</p>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)
