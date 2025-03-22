from flask import Blueprint, jsonify
import os 
from openai import OpenAI

classroom_api = Blueprint('classroom', __name__)

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

### API ROUTES ###
@classroom_api.route('/test', methods=['GET'])
def test_firebase():
    return jsonify({"message": "OpenAI route is working!"})

@classroom_api.route('/register-classroom', methods=['GET'])
def register_classroom():
    return jsonify({
        "message": "!"
    })

@classroom_api.route('/register-student', methods=['GET'])
def register_student():
    return jsonify({
        "message": "!"
    })

@classroom_api.route('/get-student-info', methods=['GET'])
def get_student_info():
    return jsonify({
        "message": 1
    })

### LLM FUNCTION CALLS
def generateKeys(question: str, answer: str = None):
    pass


### ANALYSIS CALLS 
def getGrading(question: list[str], mistakes: list[int]):
    pass

