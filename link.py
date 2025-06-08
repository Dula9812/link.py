from flask import Flask, request, redirect
import uuid

app = Flask(__name__)
url_db = {}

# Replace this with your actual Adsterra Direct Link
ADSTERRA_DIRECT_LINK = "https://databoilrecommendation.com/a52kwdsp?key=48733586a54d108787728e166e87a4b6"

@app.route('/', methods=['GET'])
def home():
    return '''
        <h2>QuickLink Converter</h2>
        <form action="/shorten" method="post">
            <input name="long_url" type="text" placeholder="Paste your long URL here" size="50"/>
            <input type="submit" value="Shorten"/>
        </form>
    '''

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    key = str(uuid.uuid4())[:8]
    url_db[key] = long_url
    return f'Shortened Link: <a href="/go/{key}">urlsh.com/go/{key}</a>'

@app.route('/go/<key>')
def go(key):
    if key in url_db:
        final_url = url_db[key]
        return redirect(f"{ADSTERRA_DIRECT_LINK}?ref={final_url}")
    else:
        return "Invalid link.", 404

if __name__ == '__main__':
    app.run(debug=True)
