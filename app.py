from flask import Flask, request, jsonify
import threading
import requests
import time
import random

app = Flask(__name__)

# In-memory data storage
vehicle_data = []
vehicle_recall_data = []

# Vehicle Data API
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    return jsonify(vehicle_data)

@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    new_vehicle = request.json
    vehicle_data.append(new_vehicle)
    return jsonify(new_vehicle), 201

# Vehicle Recall Data API
@app.route('/recalls', methods=['GET'])
def get_recalls():
    return jsonify(vehicle_recall_data)

@app.route('/recalls', methods=['POST'])
def add_recall():
    new_recall = request.json
    vehicle_recall_data.append(new_recall)
    return jsonify(new_recall), 201

# Helper Functions to Generate Random Data
def generate_vehicle_data(num_records=5):
    manufacturers = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan"]
    models = ["Corolla", "Civic", "Mustang", "Impala", "Altima"]
    fuel_types = ["Petrol", "Diesel", "Electric", "Hybrid"]
    vehicles = []

    for i in range(num_records):
        vehicle = {
            "vehicle_id": i + 1,
            "manufacturer": random.choice(manufacturers),
            "model": random.choice(models),
            "year": random.randint(2000, 2023),
            "price": random.randint(15000, 50000),
            "fuel_type": random.choice(fuel_types),
            "mileage_kmpl": random.uniform(10, 25),
            "is_available": random.choice([True, False])
        }
        vehicles.append(vehicle)
    return vehicles

def generate_recall_data(num_records=5):
    manufacturers = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan"]
    models = ["Corolla", "Civic", "Mustang", "Impala", "Altima"]
    issues = ["Airbag issue", "Brake failure", "Engine overheating", "Transmission fault", "Suspension defect"]
    risks = ["Low", "Medium", "High"]
    recalls = []

    for i in range(num_records):
        recall = {
            "recall_id": i + 1,
            "manufacturer": random.choice(manufacturers),
            "model": random.choice(models),
            "year": random.randint(2000, 2023),
            "issue_description": random.choice(issues),
            "recall_date": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "safety_risk": random.choice(risks)
        }
        recalls.append(recall)
    return recalls

# Function to send data to the API
def send_data():
    time.sleep(1)  # Ensure server starts before sending data
    vehicle_api_url = "http://127.0.0.1:5000/vehicles"
    recall_api_url = "http://127.0.0.1:5000/recalls"

    # Generate Random Data
    vehicles = generate_vehicle_data(5)
    recalls = generate_recall_data(5)

    # Send Vehicle Data to API
    for vehicle in vehicles:
        response = requests.post(vehicle_api_url, json=vehicle)
        print(f"Vehicle Response: {response.json()}")

    # Send Recall Data to API
    for recall in recalls:
        response = requests.post(recall_api_url, json=recall)
        print(f"Recall Response: {response.json()}")

if __name__ == '__main__':
    # Start Flask server in a separate thread
    server_thread = threading.Thread(target=lambda: app.run(debug=True, use_reloader=False))
    server_thread.start()

    # Send data to the API
    send_data()
