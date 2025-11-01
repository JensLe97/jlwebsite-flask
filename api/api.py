from flask import Flask
from flask import request, jsonify
from flask_mail import Mail
from flask_mail import Message
from flask_cors import CORS

from dotenv import load_dotenv
import os

# 0. Activate virtual environment from root directory (api\.venv\Scripts\activate)
# 1. First, start the backend flask application (npm run start-api)
# 2. Second, start the react application (npm start)

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['MAIL_SERVER']='smtp.1blu.de'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('USER')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSW')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL')
# app.config['MAIL_DEBUG'] = False
app.config['MAIL_MAX_EMAILS'] = 50
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://jenslemke.com",
            "https://www.jenslemke.com",
            "https://lemkjens.de",
            "https://www.lemkjens.de",
        ]
    }
})

@app.route('/api/footer', methods=['GET', 'POST'])
def footer():
    if request.method == 'POST':
        req = jsonify(request.get_json()).get_data(as_text=True)
        msg = Message("Neuer Abonnent",
                recipients=[os.environ.get('EMAIL')])
        msg.body = "Neuer Abonennt mit E-Mail: " + req
        mail.send(msg)
        return { 'submission' : 'Success'}
    return { 'submission' : 'No Request'}

@app.route('/api/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        req = jsonify(request.get_json()).get_data(as_text=True)
        msg = Message("Neue Kontaktanfrage",
                recipients=[os.environ.get('EMAIL')])
        msg.body = "Hi, du hast eine neue Kontaktanfrage mit den folgenden Daten:\n" + req
        mail.send(msg)
        return { 'submission' : 'Success'}
    return { 'submission' : 'No Request'} # redirect(url_for("contact"))

if __name__ == '__main__':
    app.run(debug=False)