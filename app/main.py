from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',
                         app_name=os.getenv("AZURE_APP_NAME", "Meu App Python"),
                         status="online")

@app.route('/health')
def health():
    return {"status": "OK"}, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)