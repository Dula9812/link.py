from flask import Flask, redirect

app = Flask(__name__)

# Your Adsterra Direct Link
ADSTERRA_LINK = "https://www.adsterra.com/example-direct-link"  # replace this with your real link

@app.route('/')
def landing():
    return '''
    <html>
    <head>
        <title>Adsterra Redirect</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                font-size: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(145deg, #d8e6ff, #ffffff);
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                background-color: #3b82f6;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            a:hover {
                background-color: #2563eb;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <p>✅ Your Adsterra redirect link is working!</p>
            <p>Click below to continue to the site:</p>
            <a href="/go">Go to Website</a>
        </div>
    </body>
    </html>
    '''

@app.route('/go')
def go():
    return redirect(ADSTERRA_LINK)

if __name__ == '__main__':
    app.run(debug=True)
