from flask import Flask, request, redirect
import uuid
import json
import os

app = Flask(__name__)
DB_FILE = 'data.json'

# Adsterra direct link
ADSTERRA_DIRECT_LINK = "https://databoilrecommendation.com/a52kwdsp?key=48733586a54d108787728e166e87a4b6"

# Load existing data
if os.path.exists(DB_FILE):
    with open(DB_FILE, 'r') as f:
        url_db = json.load(f)
else:
    url_db = {}

@app.route('/', methods=['GET'])
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>QuickLink Converter</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(to right, #ece9e6, #ffffff);
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                text-align: center;
                width: 90%;
                max-width: 500px;
            }
            input[type="text"], input[type="submit"] {
                width: 90%;
                padding: 12px;
                margin: 10px 0;
                font-size: 16px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            input[type="submit"] {
                background-color: #3b82f6;
                color: white;
                border: none;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #2563eb;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔗 QuickLink Converter</h2>
            <form action="/shorten" method="post">
                <input name="long_url" type="text" placeholder="Paste your long URL here" required/>
                <input type="submit" value="Shorten"/>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    key = str(uuid.uuid4())[:8]
    url_db[key] = long_url
    with open(DB_FILE, 'w') as f:
        json.dump(url_db, f)
    return f'''
    <html><body style="text-align:center;padding-top:100px;">
    <h2>✅ Shortened Link:</h2>
    <p><a href="/go/{key}" target="_blank">urlsh.com/go/{key}</a></p>
    </body></html>
    '''

@app.route('/go/<key>')
def go(key):
    if key in url_db:
        final_url = url_db[key]
        return redirect(f"{ADSTERRA_DIRECT_LINK}?ref={final_url}")
    else:
        return "Invalid link.", 404

if __name__ == '__main__':
    app.run(debug=True)
