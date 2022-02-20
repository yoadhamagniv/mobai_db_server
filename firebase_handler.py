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
    doc_ref = db.collection(camera_id).document(f"{start_time}")
    doc_ref.set({
        'state': state,
        'start_time': start_time,
        'end_time': end_time,
    })

def add_curr_state(camera_id, state, start_time, db):
    doc_ref = db.collection(camera_id).document("CurrentState")
    doc_ref.set({
        'state': state,
        'start_time': start_time,
    })

def get_curr_state(camera_id, db):
    schedule_ref = db.collection(camera_id)
    schedule = schedule_ref.stream()
    for doc in schedule:
        if doc.id == "CurrentState":
            return (doc.to_dict())
    return "none"

def add_user(camera_id, password, email, baby_birthdate, db):#supposed to check if user already exists (return "ok" if not and "exists" if exists)
    doc_ref = db.collection(camera_id).document("user info")
    doc_ref.set({
        'username/camera id': camera_id,
        'password': password,
        'email': email,
        'baby birthdate': baby_birthdate
    })
    return "ok"

def get_schedule_for_time_span(camera_id, time1, time2, db):
    states = {}
    schedule_ref = db.collection(camera_id)
    schedule = schedule_ref.where('start_time', '>=', time1).where('start_time', '<=', time2).stream()
    for doc in schedule:
        if f'{doc.id}' != 'CurrentState':
            dodict = doc.to_dict()
            if (dodict.get("state") not in list(states.keys())):
                states[dodict.get("state")] = [(doc.id, dodict.get('end_time'))]
            else:
                states[dodict.get("state")].append((doc.id, dodict.get('end_time')))

    return states
