from flask import Blueprint, jsonify

firebase_api = Blueprint('firebase', __name__)

@firebase_api.route('/firebase', methods=['GET'])
def test_firebase():
    return jsonify({"message": "Firebase route is working!"})