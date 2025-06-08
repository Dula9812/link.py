from flask import Flask, request, redirect
import uuid

app = Flask(__name__)
url_db = {}

# ✅ Your Adsterra Direct Link (replace if needed)
ADSTERRA_DIRECT_LINK = "https://databoilrecommendation.com/a52kwdsp?key=48733586a54d108787728e166e87a4b6"

@app.route('/', methods=['GET'])
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>QuickLink Converter</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(to right, #ece9e6, #ffffff);
                margin: 0;
                padding: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }
            .container {
                background: #fff;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                text-align: center;
                width: 90%;
                max-width: 500px;
            }
            h2 {
                color: #333;
                margin-bottom: 20px;
            }
            input[type="text"] {
                width: 90%;
                padding: 12px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 16px;
            }
            input[type="submit"] {
                background-color: #3b82f6;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s ease;
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
                <br>
                <input type="submit" value="Shorten">
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
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Link Shortened</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .result {{
                background: #fff;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                text-align: center;
            }}
            a {{
                color: #3b82f6;
                text-decoration: none;
                font-weight: bold;
                font-size: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="result">
            <h2>✅ Shortened Link:</h2>
            <p><a href="/go/{key}" target="_blank">urlsh.com/go/{key}</a></p>
        </div>
    </body>
    </html>
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
