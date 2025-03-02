from flask import Flask, request, jsonify
import uuid
import math
from datetime import datetime

app  = Flask(__name__)
receipts = {}

"""
Calculate points of the receipt
:param receipt: the receipt
:type receipt: json
:return: The total calculated points for the receipt
:rtype: int
"""
def calculate_points(receipt):
    point = 0
    retailer = receipt["retailer"]
    total = float(receipt["total"])
    items = receipt["items"]
    purchaseDate = datetime.strptime(receipt["purchaseDate"], "%Y-%m-%d")
    purchaseTime = datetime.strptime(receipt["purchaseTime"], "%H:%M")

    point += sum(c.isalnum() for c in retailer)

    if total.is_integer():
        point+=50

    if total %0.25 == 0:
        point+=25

    point+= (len(items)//2)*5

    for item in receipt["items"]:
        description = item["shortDescription"].strip()
        price = float(item["price"])
        if len(description) % 3 == 0:
            point += math.ceil(price * 0.2)
    
    if purchaseDate.day % 2 == 1:
        point += 6

    if 14 <= purchaseTime.hour < 16:
        point += 10

    return point

# Health check endpoint
@app.route("/", methods=["GET"])
def health():
    return "Healthy" ,200

# Endpoint to process receipts and calculate points
@app.route("/receipts/process",methods =["POST"])
def process_receipts():
    try:
        requiredFields = {"retailer", "purchaseDate", "purchaseTime", "total", "items"}
        receipt = request.get_json()

        if not all(field in receipt for field in requiredFields):
            return jsonify({"error": "The receipt is invalid."}), 400

        id = str(uuid.uuid4())
        points = calculate_points(receipt)

        receipts[id] = points
        print(receipts)
        return jsonify({"id": id})

    except Exception as e:
        return jsonify({"error": "The receipt is invalid."}) ,400

# Endpoint to retrieve points for a given receipt ID
@app.route("/receipts/<id>/points", methods=["GET"])
def get_points(id):
    if id in receipts:
        return jsonify({"points": receipts[id]})
    return jsonify({"error": "No receipt found for that ID."}), 404


if __name__ == "__main__":
    app.run(debug=True ,host="0.0.0.0",port=8080)