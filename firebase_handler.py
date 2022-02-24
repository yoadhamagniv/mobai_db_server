import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def try_open_db(db):
    doc_ref = db.collection("TestCamera").document("CurrentState")
    doc = doc_ref.get()
    if doc.exists:
        print("db exists")
        return True
    else:
        print("db doesn't exist")
        return False


def add_state(camera_id, state, start_time, end_time, db):
    try:
        doc_ref = db.collection(camera_id).document(f"{start_time}")
        doc_ref.set({
            'state': state,
            'start_time': start_time,
            'end_time': end_time,
        })
        return "OK"
    except:
        return "failed"

def add_curr_state(camera_id, state, start_time, db):
    try:
        doc_ref = db.collection(camera_id).document("CurrentState")
        doc_ref.set({
            'state': state,
            'start_time': start_time,
        })
        return "OK"
    except:
        return "FAILED"


def get_curr_state(camera_id, db):
    schedule_ref = db.collection(camera_id)
    schedule = schedule_ref.stream()
    for doc in schedule:
        if doc.id == "CurrentState":
            return (doc.to_dict())
    return "NONE"


def is_username_valid(username, db):
    ref = db.collection(username).stream()
    for doc in ref:
        if doc.id == "user_info":
            return "YES"
    return "NO"


def does_password_match(username, password, db):
    schedule_ref = db.collection(username)
    schedule = schedule_ref.stream()
    for doc in schedule:
        if doc.id == "user_info":
            if doc.to_dict()['password'] == password:
                sorted_items = sorted(list(doc.to_dict().items()),key=lambda x: x[0])
                return "YES#" + '#'.join([item[1] for item in sorted_items])
    return "NO"


def add_user(camera_id, password, email, baby_birthdate, babyName, db): #sign up
    try:
        ref = db.collection(camera_id).stream()
        for doc in ref:
            if doc.id == "is_set" and doc.to_dict()["is_set"]=="true":
                raise Exception("camera is already set")
        doc_ref = db.collection(camera_id).document("user_info")
        doc_ref.set({
        'username/camera_id': camera_id,
        'password': password,
        'email': email,
        'baby_birthdate': baby_birthdate,
        'baby_name': babyName
        })
        doc_ref = db.collection(camera_id).document("is_set")
        doc_ref.set({'is_set': "true"})
        return "OK"
    except:
        return "FAILED"


def get_schedule_for_time_span(camera_id, time1, time2, db):
    last_state = ""
    states = {}
    schedule_ref = db.collection(camera_id)
    schedule = schedule_ref.where('start_time', '>=', time1).where('start_time', '<=', time2).stream()
    for doc in schedule:
        if f'{doc.id}' not in ['CurrentState',"user_info"]:
            dodict = doc.to_dict()
            curr_state = dodict.get("state")
            if (curr_state not in list(states.keys())):
                states[curr_state] = [(doc.id, dodict.get('end_time'))]
            else:
                states[curr_state].append((doc.id, dodict.get('end_time')))
    return states
