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
import json
from dotenv import load_dotenv
load_dotenv()

UPLOAD_FOLDER = 'uploads'
homework_api = Blueprint('homework', __name__)
ALLOWED_EXTENSIONS = {'pdf'}

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

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
    #print("Works", len(images))
    for image in images:
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        image = cv2.convertScaleAbs(image, alpha=1.5, beta=0)
        image = cv2.fastNlMeansDenoising(image)
        _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

        pdfText += pytesseract.image_to_string(image, output_type=pytesseract.Output.STRING, config=custom_config) + "\n"
    
    #print("PDF:", pdfText)

    #print(questionAnswerList)
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

    #print(answerList)
    feedbackList = []
    for i in range(len(answerList)):
       feedbackList.append(examineSolution(question=questionAnswerList['questions'][i], studentAnswer=answerList[i], realAnswer=questionAnswerList['answers'][i]))

    #print(feedbackList)
    mistakes = 0
    total = len(feedbackList)
    for i in range(len(feedbackList)):
        mistakes += 1 if feedbackList[i][0] == 0 else 0

    print({
        "status": 1,
        "feedbackList": feedbackList,
        "questionList": questionAnswerList['questions'],
        "solutionList": questionAnswerList['answers'],
        "answerList": answerList,
        "mistakes": mistakes,
        "total": total,
        "assignmentName": questionAnswerList['name']
    })
    return jsonify({
        "status": 1,
        "feedbackList": feedbackList,
        "questionList": questionAnswerList['questions'],
        "solutionList": questionAnswerList['answers'],
        "answerList": answerList,
        "mistakes": mistakes,
        "total": total,
        "assignmentName": questionAnswerList['name']
    })

@homework_api.route('/generate-question', methods=['POST'])
def generate_question():
    
    question = request.form.get('question')
    print("Generating...")
    completion = client.chat.completions.create(
        model= "gpt-4o-mini-2024-07-18",
        messages = [
            {
                "role": "user",
                "content": """
                    Given this question: (%s), 
                    Generate another question that is similar in difficulty and is based on the same topic. 
                    Ensure that you show the equations explicitly with newlines.
                    The question is targeted to a grade 7 math student.
                    Provide an answer for this question and two hints.
                    Explain the answer to the question, then fill in this JSON form at the end of your response:

                    ```json
                        {
                            "question": (string),
                            "answer": (string),
                            "hintOne": (string),
                            "hintTwo": (string)
                        } 
                    ```
                """ % (question)
            }
        ]
    )
    
    promptResponse = completion.choices[0].message.content
    print(promptResponse)

    regex_pattern = r'```json\s*(.*?)\s*```'
    content = re.search(regex_pattern, promptResponse, re.DOTALL).group(1)
    parsed_json = json.loads(content)
    print(parsed_json)
    return jsonify({
        "question": parsed_json["question"],
        "answer": parsed_json["answer"],
        "hintOne": parsed_json["hintOne"],
        "hintTwo": parsed_json["hintTwo"],
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
    promptResponse = client.chat.completions.create(
        model= "gpt-4o-mini-2024-07-18",
        messages = [
            {
                "role": "user",
                "content": "given this question grade 7 math question %s, return an answer (labeled \"answer\") as a numerical answer and a solution (labeled \"solution\") REPLY IN JSON" % (question)
            }
        ]
    )["choice"][0]["message"]["content"]

    parsed_json = json.loads(promptResponse)

    return (parsed_json["answer"], parsed_json["solution"])

def examineSolution(question: str, realAnswer: str, studentAnswer: str):
    completion = client.chat.completions.create(
        model= "gpt-4o-mini-2024-07-18",
        messages = [
            {
                "role": "user",
                "content": """
                        This is the math question: %s.
                        
                        This is the student's answer: %s. 

                        This is the real answer: %s. 
                        Say if its correct or not, and provide feedback to the student. 
                        Explain the feedback as though the student is in 7th grade. 
                        The answers are written with removed white spaces, so try your best to interpret them.
                        At the end, fill in the following JSON:

                        ```json
                        {
                            "mark": (0 for incorrect, 1 for correct),
                            "feedback": (Insert feedback here)
                        }
                        ```
            
                """ % (question, realAnswer, studentAnswer)
            }
        ]
    )
    
    promptResponse = completion.choices[0].message.content

    regex_pattern = r'```json\s*(.*?)\s*```'
    content = re.search(regex_pattern, promptResponse, re.DOTALL).group(1)
    if(len(content) == 0):
        parsed_json = json.loads(promptResponse)
    else:
        parsed_json = json.loads(content)
    print(parsed_json)
    
    return (parsed_json["mark"], parsed_json["feedback"])

def generateSummaryFeedback(totalQuestions: list[str], totalFeedback: list[str]):
    promptResponse = client.chat.completions.create(
        model= "gpt-4o-mini-2024-07-18",
        messages = [
            {
                "role": "user",
                "content": f"Given this list of questions {totalQuestions} and this set of student solutions for the questions {totalFeedback}, provide feedback. Label your feedback as \"feedback\" The student is a grade 7 Math Student REPLY IN JSON"
            }
        ]
    )["choice"][0]["message"]["content"]

    parsed_json = json.loads(promptResponse)

    return parsed_json["feedback"]

### ANALYSIS CALLS 
def getGrading(question: list[str], mistakes: list[int]):
    pass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

