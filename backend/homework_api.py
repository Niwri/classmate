from flask import Blueprint, jsonify, request, render_template
import os 
from openai import OpenAI
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
import pytesseract
import cv2 
import numpy as np
from firebase_api import getAssignmentQA
import re

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

@homework_api.route('/evaluate-assignment', methods=['POST'])
def evaluate_assignment():
    if 'file' not in request.files:
        print("No files.")
        return jsonify({
            "status": 0,
            "message": "No files."
        }), 400



    file = request.files['file']
    if file is None or file.filename == '':
        print("No selected file.")
        return jsonify({
            "status": 0,
            "message": "No selected file."
        }), 400
    
    if allowed_file(file.filename) is False:
        print("Invalid file type. Only PDF files are allowed.")
        return jsonify({
            "status": 0,
            "message": "Invalid file type. Only PDF files are allowed."
        }), 400
    
    classroomId = request.form.get('classroomId')
    if(classroomId is None):
        print("classroomId is required")
        return jsonify({
            "status": 0,
            "message": "classroomId is required"
        }), 400
    
    assignmentId = request.form.get('assignmentId')
    if(assignmentId is None):
        print("assignmentId is required")
        return jsonify({
            "status": 0,
            "message": "assignmentId is required"
        }), 400

    studentId = request.form.get('studentId')
    if(studentId is None):
        print("studentId is required")
        return jsonify({
            "status": 0,
            "message": "studentId is required"
        }), 400
    
    questionAnswerList = getAssignmentQA(classroomId, assignmentId)
    if(questionAnswerList is None):
        print("Either classroomID or assignmentID is invalid.")
        return jsonify({
            "status": 0,
            "message": "Either classroomID or assignmentID is invalid."
        })

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    print(filepath)
    file.save(filepath)
    # Use --psm 3 to generate questions
    # Use --psm 11 to match questions
    custom_config = r"--psm 11 -c preserve_interword_spaces=1 tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,^+-*/=()"
    images = convert_from_path(filepath, dpi=200)
    pdfText = ""
    print("Works", len(images))
    for image in images:
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        image = cv2.convertScaleAbs(image, alpha=1.5, beta=0)
        image = cv2.fastNlMeansDenoising(image)
        _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

        pdfText += pytesseract.image_to_string(image, output_type=pytesseract.Output.STRING, config=custom_config) + "\n"
    
    print("PDF:", pdfText)

    print(questionAnswerList)
    startAnswer = False
    currentQuestionIndex = 0
    currentString = ""
    answerList = []
    for i in range(len(pdfText)):
        startAnswer = currentQuestionIndex > 0
        currentString += pdfText[i]
            
        if(
            currentQuestionIndex < len(questionAnswerList['questions']) and 
            (re.sub(r'[\s\n\.]', '', questionAnswerList['questions'][currentQuestionIndex]).replace('\\n', '')
              in 
            re.sub(r'[\s\n\.]', '', currentString))):
            if(startAnswer):
                answerList.append(re.sub(r'[\s\n\.]', '', currentString).replace(re.sub(r'[\s\n\.]', '', questionAnswerList['questions'][currentQuestionIndex]).replace('\\n', ''), ''))
            currentString = ""
            currentQuestionIndex += 1
    
    if(currentQuestionIndex == len(questionAnswerList['questions'])):
        answerList.append(currentString)

    for i in range(len(answerList)):
        answerList[i] = answerList[i].replace('\n', '')

    print(answerList)
    feedbackList = []
    for i in range(len(answerList)):
       feedbackList.append(examineSolution(answerList[i], questionAnswerList['answers'][i]))


    return jsonify({
        "status": 1,
        "feedbackList": feedbackList,
        "questionList": questionAnswerList['questions'],
        "solutionList": questionAnswerList['answers'],
        "answerList": answerList
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
