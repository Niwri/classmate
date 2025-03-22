from flask import Blueprint, jsonify, request, render_template
import os 
from openai import OpenAI
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
import pytesseract
import cv2 
import numpy as np
UPLOAD_FOLDER = 'uploads'
homework_api = Blueprint('homework', __name__)
ALLOWED_EXTENSIONS = {'pdf'}

# client = OpenAI(
#     # This is the default and can be omitted
#     api_key=os.environ.get("OPENAI_API_KEY"),
# )

### API ROUTES ###
@homework_api.route('/test', methods=['GET'])
def test_firebase():
    return jsonify({
        "message": "OpenAI route is working!"
    })

@homework_api.route('/evaluate-assignment', methods=['GET'])
def evaluate_assignment():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file is None or file.filename == '':
        return jsonify({
            "status": 0,
            "message": "No selected file."
        }), 400
    
    if allowed_file(file.filename) is False:
        return jsonify({
            "status": 0,
            "message": "Invalid file type. Only PDF files are allowed."
        }), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    print(filepath)
    file.save(filepath)
    custom_config = r"--psm 6 --oem 1 -c tessedit_char_whitelist=\"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.\^\+-*/=() \""
    images = convert_from_path(filepath, dpi=200)
    answerList = []
    for image in images:
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Apply thresholding
        _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

        data = pytesseract.image_to_string(image, output_type=pytesseract.Output.STRING, config=custom_config)
        print(data)

    return jsonify({
        "message": "!"
    })

@homework_api.route('/generate-question', methods=['GET'])
def generate_question():

    generatedQuestion = ""
    generatedAnswer = ""
    hintOne = ""
    hintTwo = ""
    
    question = request.form.get('question')
    # TODO: Ask LLM for a similar question with answer and two hints

    return jsonify({
        "question": generatedQuestion,
        "answer": generatedAnswer,
        "hintOne": hintOne,
        "hintTwo": hintTwo,
        "status": 1
    })

@homework_api.route('/create-assignment', methods=['POST'])
def create_assignment():

    return jsonify({
        "status": 1
    })


### LLM FUNCTION CALLS
def generateKeys(question: str, answer: str = None):
    pass

def generateSolution(question: str):
    pass

def examineSolution(realAnswer: str, studentAnswer: str):
    pass

def generateSummaryFeedback(totalFeedback: list[str]):
    pass

### ANALYSIS CALLS 
def getGrading(question: list[str], mistakes: list[int]):
    pass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
