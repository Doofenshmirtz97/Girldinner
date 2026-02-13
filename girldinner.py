from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

responses = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rsvp", methods=["POST"])
def rsvp():
    data = request.get_json()
    name = data.get("name")
    response = data.get("response")

    responses.append({"name": name, "response": response})
    
    print(f"RSVP received: {name} - {response}")  # For debugging

    return jsonify({"message": f"Thanks {name}!"})

@app.route("/responses", methods=["GET"])
def get_responses():
    """Optional endpoint to view all responses"""
    return jsonify(responses)

if __name__ == "__main__":
    app.run(debug=True)