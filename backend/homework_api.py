from flask import Blueprint, jsonify, request, render_templates
import os 
from openai import OpenAI
from werkzeug.utils import secure_filename
from main import UPLOAD_FOLDER
from pdf2image import convert_from_path
import pytesseract
import json

homework_api = Blueprint('homework', __name__)
ALLOWED_EXTENSIONS = {'pdf'}

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


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
    file.save(filepath)
    
    images = convert_from_path(filepath)
    full_text = ''
    for image in images:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    

    return jsonify({
        "message": "!"
    })

@homework_api.route('/generate-question', methods=['GET'])
def generate_question():
    
    question = request.form.get('question')
    # TODO: Ask LLM for a similar question with answer and two hints 
    promptResponse = client.chat.completions.create(
        model= "gpt-4",
        messages = [
            {
                "role": "user",
                "content": "based on this question %s generate another question (labeled as \"question\"). The question has to be similar in difficulty and be based on the same topic. The question is targeted to a grade 7 math student (labeled as \"answer\"). The answer for the question should be just a number. Provide an answer for this question (labeled \"answer\") and two hints (labeled \"hintOne\" and \"hintTwo\") REPLY IN JSON" % (question)
            }
        ]
    )["choice"][0]["message"]["content"]

    parsed_json = json.loads(promptResponse)
    

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
        model= "gpt-4",
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
    promptResponse = client.chat.completions.create(
        model= "gpt-4",
        messages = [
            {
                "role": "user",
                "content": "This is the math question %s. Compare the student answer %s to the real answer %s. Say if its correct or not (labeled \"mark\"), and provide feedback to the student (labeled \"feedback\"). The student is a grade 7 math student REPLY IN JSON" % (question, realAnswer, studentAnswer)
            }
        ]
    )["choice"][0]["message"]["content"]
    
    parsed_json = json.loads(promptResponse)
    
    return (parsed_json["mark"], parsed_json["feedback"])

def generateSummaryFeedback(totalQuestions: list[str], totalFeedback: list[str]):
    promptResponse = client.chat.completions.create(
        model= "gpt-4",
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
