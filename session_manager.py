import oracledb
from uuid import uuid4
from app.services import database

sessions = {}  # (session_id -> {ip_address, oracle_connection, oracle_cursor})

def check_session(session_id, ip):
    if session_id and session_id in sessions:
        session_data = sessions[session_id]
        if ip == session_data["ip_address"]:
            try:
                session_data["oracle_cursor"].execute("SELECT 1 FROM DUAL")
                return True
            except oracledb.DatabaseError:
                pass
        close_session(session_id)
    return False

def close_session(session_id):
    if session_id in sessions:
        try:
            session_data = sessions[session_id]
            database.close_db(session_data["oracle_connection"], session_data["oracle_cursor"])
        except Exception as e:
            print(f"Error closing session {session_id}: {e}")
        del sessions[session_id]

def create_session(ip, username, password):
    connection, cursor, error = database.connect_db(username, password)
    if error:
        return None, error
    
    session_id = str(uuid4())
    sessions[session_id] = {
        "ip_address": ip,
        "oracle_connection": connection,
        "oracle_cursor": cursor,
        "username": username
    }
    return session_id, None

def get_sessions():
    return {
        session_id: {
            "ip_address": data["ip_address"],
            "username": data.get("username", "Unknown User")
        }
        for session_id, data in sessions.items()
    }
