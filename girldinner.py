from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

app = Flask(__name__)

responses = []

# Email configuration - uses environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS', 'fazeelath.faruqhi@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'pbal swom pqwj jjgi')
NOTIFY_EMAIL = os.environ.get('NOTIFY_EMAIL', 'fazeelath.faruqhi@gmail.com')

def send_email_notification(name, response):
    """Send email notification when someone RSVPs"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = NOTIFY_EMAIL
        msg['Subject'] = f"🎉 Galentine's RSVP: {name} said {response}!"
        
        # Email body
        body = f"""
        New RSVP Alert! 💖
        
        Name: {name}
        Response: {response}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Total RSVPs so far: {len(responses)}
        
        ---
        Galentine's Night 💕
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email via Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent for {name}'s RSVP!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
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
    
    print(f"RSVP received: {name} - {response}")
    
    # Send email notification
    send_email_notification(name, response)

    return jsonify({"message": f"Thanks {name}!"})

@app.route("/responses", methods=["GET"])
def get_responses():
    """View all responses"""
    return jsonify(responses)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)