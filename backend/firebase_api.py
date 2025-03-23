from flask import Blueprint, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

firebase_api = Blueprint('firebase', __name__)

cred = credentials.Certificate('classmate-43cb9-firebase-adminsdk-fbsvc-c34d7233a7.json')  
app = firebase_admin.initialize_app(cred)
db = firestore.client()

### API ROUTES ###
@firebase_api.route('/test', methods=['GET'])
def test_firebase():
    return jsonify({"message": "Firebase route is working!"})


### FIREBASE FUNCTION CALLS
def createClassroom():
    pass

def createAssignment(classroom: str):
    pass

def getTags(classroom: str, assigment: str) -> list[str]:
    """
    Retrieves the list of tags associated with an assignment in a classroom
    Args:
        Input
            classroom: UUIDv4 ID
            assignment: UUIDv4 ID
        Output
            list[str]: List of Tags
    """
    pass

def getStudentInfo(classroom: str, student: str):
    """
    Retrieves the student information associated with the student ID in the classroom ID
    Args:
        Input
            classroom: UUIDv4 ID
            student: UUIDv4 ID
        Output 
            {
                "name": (),
                "year": ()
            }
    """
    pass

def getAssignmentQA(classroom: str, assignment: str):

    if(collection_exists(collection_name=classroom) == False):
        return {
            "status": -1,
            "message": f"{classroom} does not exist!"
        }
    
    classroomCollection = db.collection(classroom)
    assignmentDocument = classroomCollection.document("assignment-list")
    
    if(collection_exists(collection_name=assignment, document=assignmentDocument) == False):
        return {
            "status": -1,
            "message": f"{classroom} does not exist!"
        }

    questionAnswerList = assignmentDocument.collection(assignment).document("question-answer").get()
    infoRef = assignmentDocument.collection(assignment).document("info").get()
    
    questionAnswerData = questionAnswerList.to_dict()
    infoData = infoRef.to_dict()
    return {
        "status": 1,
        "message": "",
        "questions": questionAnswerData.get("questions", []),
        "answers": questionAnswerData.get("answers", []),
        "name": infoData.get('name', "")
        
    }




def collection_exists(collection_name, document=None):
    docs = db.collection(collection_name).limit(1).stream()
    if(document is not None):
        docs = document.collection(collection_name).limit(1).stream()
    
    

    return any(docs) 