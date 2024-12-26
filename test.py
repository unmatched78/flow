from flask import Flask, request, jsonify  
from flask_limiter import Limiter  
from flask_cors import CORS  
from openai import OpenAI  # Update this import to use eopenai  
# from flask_limiter.util import restrict_by_remote_address  # Optional: Use if you want to limit by IP  

app = Flask(__name__)  
CORS(app)
# Initialize OpenAI client with your API key  
client = OpenAI(  
    api_key="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"  
)  

# Initialize the limiter  
limiter = Limiter(app)  # You can optionally define a key function for IP rate limiting  
@app.route('/ping', methods=['GET'])  
def ping():  
    return jsonify({"message": "pong"})
# Rate limit: 5 requests per minute  
@app.route('/chat', methods=['POST'])  
@limiter.limit("5 per minute")  # Adjust the rate limit as needed  
def chat():  
    user_message = request.json.get("message")  

    # Make a request to the OpenAI API  
    try:  
        completion = client.chat.completions.create(  
            model="gpt-4o-mini",  # Specify the model you wish to use  
            messages=[  
                {"role": "user", "content": user_message}  
            ]  
        )  
        print(completion.choices[0].message["content"])
        # Return the AI's response as JSON  
        return jsonify({  
            "response": completion.choices[0].message["content"]  # Access the content of the response  
        })  
        
    except Exception as e:  
        return jsonify({"error": str(e)}), 500  # Return error if there's an issue  

if __name__ == '__main__':  
    app.run(debug=True)
