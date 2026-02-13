from flask import Flask, render_template, request, jsonify
import resend  # <--- Changed
from datetime import datetime
import os

app = Flask(__name__)

responses = []

# 1. Initialize Resend with your API Key from Railway Environment Variables
resend.api_key = os.environ.get('RESEND_API_KEY')
NOTIFY_EMAIL = os.environ.get('NOTIFY_EMAIL', 'fazeelath.faruqhi@gmail.com')

def send_email_notification(name, response):
    """Send email notification using Resend API (Railway Friendly)"""
    try:
        # 2. Construct the email parameters
        params = {
            "from": "Galentine RSVP <onboarding@resend.dev>",
            "to": [NOTIFY_EMAIL],
            "subject": f"🎉 Galentine's RSVP: {name} said {response}!",
            "html": f"""
                <h3>New RSVP Alert! 💖</h3>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Response:</strong> {response}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <hr>
                <p>Total RSVPs so far: {len(responses)}</p>
            """
        }
        
        # 3. Send via Resend (uses HTTPS Port 443, which isn't blocked)
        email = resend.Emails.send(params)
        
        print(f"Email sent via Resend for {name}!")
        return True
    except Exception as e:
        print(f"Resend API Failed: {e}")
        return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rsvp", methods=["POST"])
def rsvp():
    data = request.get_json()
    name = data.get("name")
    response = data.get("response")

    responses.append({
        "name": name, 
        "response": response,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Send the email
    send_email_notification(name, response)

    return jsonify({"message": f"Thanks {name}!"})

@app.route("/responses", methods=["GET"])
def get_responses():
    return jsonify(responses)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)