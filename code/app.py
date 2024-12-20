from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "Ysk-proj-V4kEH8QHKDLJ1GU1LOoQiGQtsg-_j2Bg6739atNlY-1z0Gu_1KCzFJtSt7btyLgJhVhjw_PAf_T3BlbkFJMGiI20cVgtDco9tPZLCfgRS0qmvpQrQvGbbdo3V_-SEhmWCJXderglwPT5JWuf2vvg9Hsch7cA"

def fetch_hotel_suggestions(destination):
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        params = {"destination": destination}
        response = requests.get(API_URL, headers=headers, params=params)
        if response.status_code == 200:
            hotels = response.json().get("hotels", [])
            if hotels:
                return [f"{hotel['name']} - {hotel['price']} {hotel['currency']}" for hotel in hotels]
            else:
                return ["No hotels found for the specified destination."]
        else:
            return ["Failed to fetch hotel data from the API."]
    except Exception as e:
        return [f"Error occurred: {str(e)}"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()
    if "hello" in user_message or "hi" in user_message:
        bot_message = "Hello! How can I assist you with your travel plans today?"
    elif "hotel" in user_message:
        bot_message = "Please provide a destination for hotel suggestions."
    elif "destination:" in user_message:
        destination = user_message.split("destination:")[1].strip()
        hotel_suggestions = fetch_hotel_suggestions(destination)
        bot_message = "\n".join(hotel_suggestions)
    elif "thank" in user_message:
        bot_message = "You're welcome! Have a great day!"
    else:
        bot_message = "I'm sorry, I didn't understand that. Can you please rephrase your question?"
    return jsonify({"bot_message": bot_message})

if __name__ == "__main__":
    app.run(debug=True)
