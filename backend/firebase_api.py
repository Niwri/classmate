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






