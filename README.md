# Oracle Session Auth

A standalone session management system using native Oracle authentication.

Users connect with real Oracle DB credentials — no separate user tables, no JWT tokens.  
Each session is stored in memory, tracked by IP address, and verified via lightweight queries to Oracle.

---

## 🔧 How It Works

- `create_session(ip, username, password)`  
  Connects directly to Oracle using provided credentials.  
  Stores session with a UUID, linked to the user's IP and Oracle connection.

- `check_session(session_id, ip)`  
  Checks if a session exists and is valid by executing `SELECT 1 FROM DUAL`.  
  Ensures the request comes from the original IP.

- `close_session(session_id)`  
  Closes the Oracle connection and cursor, and removes the session from memory.

- `get_sessions()`  
  Returns a list of active sessions with masked user info.

---

## 📦 Stack

- Python 3
- [oracledb](https://pypi.org/project/oracledb/) (Oracle DB driver)
- Any backend (FastAPI, Flask, etc.) — integration ready

---

## 💡 Why This Is Different

Typical web authentication uses a local database of users, hashed passwords, and token-based sessions.

This system:
- **delegates all auth to Oracle itself**
- respects Oracle roles, privileges, and profiles
- allows clean session lifecycle without storing passwords or handling hashing
- is **stateless at the database layer** — all session data lives in memory

---

## 🔒 Security Notes

- IP-based session locking is used to mitigate session hijacking.
- This design assumes Oracle access is properly restricted and audited.
- Should be combined with HTTPS and additional middleware if exposed over the internet.

---

## 📁 Example

python
session_id, error = create_session(ip="192.168.1.10", username="appuser", password="secret123")
if session_id:
    print("Session started:", session_id)
else:
    print("Login failed:", error)
