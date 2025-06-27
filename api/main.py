from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from typing import Optional
from datetime import datetime
import sqlite3
import os
import hashlib
import secrets
# BaseTPMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# Database path and token store
DB_PATH = os.path.join(os.path.dirname(__file__), "helpdesk.db")
tokens = {}  # Store tokens in memory (use Redis in production)

# Initialize database tables
def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        
        db.execute("""CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            priority TEXT DEFAULT 'low',
            type TEXT DEFAULT 'general',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            assigned_admin_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (assigned_admin_id) REFERENCES users (id)
        )""")
        
        db.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            sender TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ticket_id INTEGER,
            FOREIGN KEY (ticket_id) REFERENCES tickets (id)
        )""")
        db.commit()

async def register(request: Request):
    data = await request.json()
    email = data.get('email')
    password = data.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    with sqlite3.connect(DB_PATH) as db:
        try:
            db.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, hashed_password)
            )
            db.commit()
            return JSONResponse({"message": "User registered successfully"})
        except sqlite3.IntegrityError:
            return JSONResponse({"detail": "Email already registered"}, status_code=400)

async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.execute(
            "SELECT id, email, is_admin, issue_type FROM users WHERE email = ? AND password = ?",
            (email, hashed_password)
        )
        user = cursor.fetchone()
        if user is None:
            return JSONResponse({"detail": "Invalid credentials"}, status_code=401)
        
        token = secrets.token_urlsafe(32)
        tokens[token] = {
            "id": user[0], 
            "email": user[1], 
            "is_admin": bool(user[2]),
            "issue_type": user[3]
        }
        
        return JSONResponse({
            "access_token": token, 
            "token_type": "bearer",
            "user": {
                "id": user[0],
                "email": user[1],
                "is_admin": bool(user[2]),
                "issue_type": user[3]
            }
        })

def get_current_user(token: str):
    if token not in tokens:  # Check tokens dictionary instead of token string
        return JSONResponse({"detail": "Invalid token"}, status_code=401)
    return tokens[token]  # Return user data from tokens dictionary

async def get_tickets(request: Request):
    current_user = request.state.user
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        if current_user["is_admin"]:
            # Admin sees only tickets matching their issue type
            cursor = db.execute(
                """SELECT t.*, u.email as user_email 
                   FROM tickets t 
                   JOIN users u ON t.user_id = u.id 
                   JOIN users admin ON admin.id = ?
                   WHERE t.type = admin.issue_type
                   ORDER BY t.created_at DESC""",
                (current_user["id"],)
            )
        else:
            # Regular users see their own tickets
            cursor = db.execute(
                """SELECT t.*, u.email as assigned_admin_email 
                   FROM tickets t 
                   LEFT JOIN users u ON t.assigned_admin_id = u.id 
                   WHERE t.user_id = ? 
                   ORDER BY t.created_at DESC""",
                (current_user["id"],)
            )
        tickets = cursor.fetchall()
        return JSONResponse([dict(ticket) for ticket in tickets])

async def create_ticket(request: Request):
    try:
        data = await request.json()
        current_user = request.state.user
        ticket_type = data.get('type', 'general')
        
        with sqlite3.connect(DB_PATH) as db:
            # Find the admin responsible for this type of issue
            cursor = db.execute(
                "SELECT id FROM users WHERE is_admin = 1 AND issue_type = ?",
                (ticket_type,)
            )
            admin = cursor.fetchone()
            if not admin:
                return JSONResponse(
                    {"detail": f"No admin available for issue type: {ticket_type}"}, 
                    status_code=400
                )
            
            # Create ticket with assigned admin
            cursor = db.execute(
                """INSERT INTO tickets 
                   (subject, description, priority, type, user_id, assigned_admin_id) 
                   VALUES (?, ?, ?, ?, ?, ?) RETURNING id""",
                (
                    data['subject'], 
                    data['description'], 
                    data.get('priority', 'low'),
                    ticket_type,
                    current_user['id'],
                    admin[0]
                )
            )
            ticket_id = cursor.fetchone()[0]
            db.commit()
            
            return JSONResponse({
                "id": ticket_id,
                "message": "Ticket created and assigned successfully"
            })
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=400)

async def get_messages(request: Request):
    ticket_id = request.path_params['ticket_id']
    current_user = request.state.user
    
    with sqlite3.connect(DB_PATH) as db:
        # First verify ticket access
        cursor = db.execute(
            "SELECT user_id FROM tickets WHERE id = ?",
            (ticket_id,)
        )
        ticket = cursor.fetchone()
        if not ticket or (ticket[0] != current_user["id"] and not current_user["is_admin"]):
            return JSONResponse({"detail": "Not authorized"}, status_code=403)
        
        # Then fetch messages
        db.row_factory = sqlite3.Row
        cursor = db.execute(
            """SELECT content, sender, created_at 
               FROM messages 
               WHERE ticket_id = ? 
               ORDER BY created_at ASC""",
            (ticket_id,)
        )
        messages = cursor.fetchall()
        return JSONResponse([{
            'text': message['content'],
            'sender': message['sender'],
            'created_at': message['created_at']
        } for message in messages])

async def create_message(request: Request):
    ticket_id = request.path_params['ticket_id']
    data = await request.json()
    content = data.get('content')
    current_user = request.state.user
    
    if not content:
        return JSONResponse({"detail": "Message content is required"}, status_code=400)
    
    with sqlite3.connect(DB_PATH) as db:
        # Verify ticket access
        cursor = db.execute(
            "SELECT user_id FROM tickets WHERE id = ?",
            (ticket_id,)
        )
        ticket = cursor.fetchone()
        if not ticket or (ticket[0] != current_user["id"] and not current_user["is_admin"]):
            return JSONResponse({"detail": "Not authorized"}, status_code=403)
        
        # Insert message
        cursor = db.execute(
            """INSERT INTO messages (content, sender, ticket_id) 
               VALUES (?, ?, ?) RETURNING id""",
            (content, current_user["email"], ticket_id)
        )
        message_id = cursor.fetchone()[0]
        db.commit()
        
        return JSONResponse({
            "id": message_id,
            "message": "Message sent successfully",
            "created_at": datetime.utcnow().isoformat()
        })

async def update_ticket(request: Request):
    ticket_id = request.path_params['ticket_id']
    data = await request.json()
    status = data.get('status')
    priority = data.get('priority')
    current_user = request.state.user
    
    if not current_user["is_admin"]:
        return JSONResponse({"detail": "Admin access required"}, status_code=403)
    
    with sqlite3.connect(DB_PATH) as db:
        if status:
            db.execute(
                "UPDATE tickets SET status = ? WHERE id = ?",
                (status, ticket_id)
            )
        if priority:
            db.execute(
                "UPDATE tickets SET priority = ? WHERE id = ?",
                (priority, ticket_id)
            )
        db.commit()
        return JSONResponse({"message": "Ticket updated successfully"})

# Add a middleware to handle authentication
async def auth_middleware(request: Request, call_next):
    # Skip auth for login and register
    if request.url.path in ['/api/login', '/api/register']:
        return await call_next(request)

    # Debug logging
    print("Auth headers:", request.headers.get('Authorization'))
    
    # Check for Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        print("No auth header found")
        return JSONResponse(
            {"detail": "No authorization header"}, 
            status_code=401
        )

    # Extract token
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != 'bearer':
            print(f"Invalid scheme: {scheme}")
            return JSONResponse(
                {"detail": "Invalid authentication scheme"}, 
                status_code=401
            )
    except ValueError:
        print("Invalid header format")
        return JSONResponse(
            {"detail": "Invalid authorization header"}, 
            status_code=401
        )

    # Validate token
    user = tokens.get(token)
    if not user:
        print(f"Token not found: {token}")
        return JSONResponse(
            {"detail": "Invalid or expired token"}, 
            status_code=401
        )

    # Set user in request state
    request.state.user = user
    return await call_next(request)

# Update the routes and middleware configuration
routes = [
    Route('/api/register', register, methods=['POST']),
    Route('/api/login', login, methods=['POST']),
    Route('/api/tickets', get_tickets, methods=['GET']),
    Route('/api/tickets', create_ticket, methods=['POST']),
    Route('/api/tickets/{ticket_id}/messages', get_messages, methods=['GET']),
    Route('/api/tickets/{ticket_id}/messages', create_message, methods=['POST']),
    Route('/api/admin/tickets/{ticket_id}', update_ticket, methods=['PUT']),
]

middleware = [
    Middleware(CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(BaseHTTPMiddleware, dispatch=auth_middleware)
]

app = Starlette(
    debug=True,
    routes=routes,
    middleware=middleware,
    on_startup=[init_db]
)