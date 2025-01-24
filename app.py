from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from mira_sdk import MiraClient
import os

# Load environment variables
load_dotenv()

# Initialize Flask app and Mira Client
app = Flask(__name__)
client = MiraClient(config={"API_KEY": os.getenv("MIRA_API_KEY")})

# Route to render the front-end HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle study planner inputs and run Mira Flow
@app.route('/study-planner', methods=['POST'])
def study_planner():
    # Get input data (from the form submission via AJAX)
    data = request.json
    print("Received Data:", data)  # Log the received data for debugging
    
    try:
        # Retrieve the flow ID and version from environment variables
        flow_id = os.getenv("FLOW_ID")  # Get the flow ID
        flow_version = os.getenv("FLOW_VERSION", "1.0.1")  # Default to 1.0.1 if not provided

        # Construct the flow name
        flow_name = f"{flow_id}/{flow_version}"

        # Access the flow attribute and call its method to execute the flow
        flow = client.flow  # Access the flow object

        # Execute the flow (ensure the method name is correct for your API)
        result = client.flow.execute(flow_name, data)  # Adjust based on actual method name
        
        print("Flow Result:", result)  # Log the result from the Mira API
        
        return jsonify(result)  # Return the response to the front-end
    except Exception as e:
        print("Error:", str(e))  # Log any error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
