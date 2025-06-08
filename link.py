from flask import Flask, request, redirect, render_template_string
import uuid
import json
import os

app = Flask(__name__)
DB_FILE = 'data.json'

# Replace with your Adsterra Direct Link
ADSTERRA_DIRECT_LINK = "https://databoilrecommendation.com/a52kwdsp?key=48733586a54d108787728e166e87a4b6"

# Load or initialize database
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
    <head><title>QuickLink</title></head>
    <body style="text-align:center;padding-top:100px;">
        <h2>🔗 QuickLink Shortener</h2>
        <form action="/shorten" method="post">
            <input type="text" name="long_url" placeholder="Enter long URL" size="50" required />
            <br><br>
            <input type="submit" value="Shorten" />
        </form>
    </body>
    </html>
    '''

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    key = str(uuid.uuid4())[:8]
    url_db[key] = {"url": long_url, "visits": 0}
    save_db()
    return f'''
    <html><body style="text-align:center;padding-top:100px;">
    <h2>✅ Shortened Link:</h2>
    <p><a href="/go/{key}" target="_blank">urlsh.com/go/{key}</a></p>
    </body></html>
    '''

@app.route('/go/<key>')
def go(key):
    if key not in url_db:
        return "Invalid or expired link", 404

    info = url_db[key]
    info['visits'] += 1
    save_db()

    if info['visits'] == 1:
        # On first visit, show HTML that opens Adsterra in new tab and redirects to long URL
        return render_template_string(f"""
        <html>
        <head>
            <title>Redirecting...</title>
            <script>
                window.onload = function() {{
                    window.open("{ADSTERRA_DIRECT_LINK}", "_blank");
                    window.location.href = "{info['url']}";
                }};
            </script>
        </head>
        <body>
            <p>Redirecting to your link...</p>
        </body>
        </html>
        """)
    else:
        # From second visit onwards, go directly to long URL
        return redirect(info['url'])

if __name__ == '__main__':
    app.run(debug=True)
