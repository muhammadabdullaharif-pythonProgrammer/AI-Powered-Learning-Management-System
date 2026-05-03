# ============================================================
# 🎓 SMART LEARNING MANAGEMENT SYSTEM (SLMS)
# Final Year Project | AI-Powered LMS using Streamlit + SQLite
# ============================================================
# Technology Stack:
#   - Frontend + Backend : Streamlit
#   - Database           : SQLite (auto-create)
#   - AI/ML              : Scikit-learn (Logistic Regression)
#   - Data Handling      : Pandas, NumPy
#   - Visualization      : Matplotlib
# ============================================================

# ─────────────────────────────────────────────
# SECTION 1: IMPORTS (Tamam libraries import karo)
# ─────────────────────────────────────────────
import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import hashlib
import re
import random
import warnings
from datetime import datetime, timedelta
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# SECTION 2: PAGE CONFIGURATION
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Smart LMS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# SECTION 3: CUSTOM CSS (UI ko sundar banao)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .main { background-color: #f0f4f8; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] .stRadio label { color: #ffffff !important; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #0f3460;
    }
    [data-testid="stMetricLabel"] { color: #555 !important; font-size: 13px !important; }
    [data-testid="stMetricValue"] { color: #1a1a2e !important; font-size: 28px !important; font-weight: 700 !important; }

    /* Cards */
    .card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border-top: 4px solid #0f3460;
    }
    .card-success { border-top-color: #2ecc71; }
    .card-warning { border-top-color: #f39c12; }
    .card-danger  { border-top-color: #e74c3c; }

    /* Headings */
    h1 { color: #1a1a2e !important; font-weight: 800 !important; }
    h2 { color: #0f3460 !important; font-weight: 700 !important; }
    h3 { color: #16213e !important; font-weight: 600 !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0f3460, #533483);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(15,52,96,0.4);
    }

    /* Success/Error/Info alerts */
    .stSuccess { border-radius: 8px; }
    .stError   { border-radius: 8px; }
    .stInfo    { border-radius: 8px; }

    /* Table */
    .stDataFrame { border-radius: 8px; overflow: hidden; }

    /* Badge */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px;
    }
    .badge-blue   { background:#dbeafe; color:#1d4ed8; }
    .badge-green  { background:#dcfce7; color:#16a34a; }
    .badge-red    { background:#fee2e2; color:#dc2626; }
    .badge-yellow { background:#fef9c3; color:#ca8a04; }

    /* Logo area */
    .logo-area {
        text-align: center;
        padding: 20px 0 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }

    /* Progress bar custom */
    .prog-wrap { background: #e2e8f0; border-radius: 99px; height: 10px; margin: 6px 0; }
    .prog-fill { height: 10px; border-radius: 99px; background: linear-gradient(90deg,#0f3460,#533483); }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { background: #f8fafc; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; font-weight: 500; }
    .stTabs [aria-selected="true"] { background: white !important; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }

    /* Hide default Streamlit footer */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# SECTION 4: DATABASE SETUP (SQLite auto-create)
# Jab bhi app chalay, DB aur tables apne aap ban jayein
# ═══════════════════════════════════════════════════════════

DB_PATH = "slms.db"

def get_connection():
    """SQLite connection return karo (thread-safe)"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """
    Database aur tamam tables banao agar na hon.
    (Create all tables if they don't exist)
    """
    conn = get_connection()
    c = conn.cursor()

    # ── Users table ──────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    UNIQUE NOT NULL,
            password TEXT    NOT NULL,
            role     TEXT    NOT NULL DEFAULT 'student',
            created_at TEXT  DEFAULT (datetime('now'))
        )
    """)

    # ── Courses table ─────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT NOT NULL,
            description TEXT,
            teacher_id INTEGER,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (teacher_id) REFERENCES users(id)
        )
    """)

    # ── Lectures table ────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS lectures (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id  INTEGER NOT NULL,
            title      TEXT NOT NULL,
            content    TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)

    # ── Quizzes table ─────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id      INTEGER NOT NULL,
            question       TEXT NOT NULL,
            type           TEXT NOT NULL DEFAULT 'mcq',
            option_a       TEXT,
            option_b       TEXT,
            option_c       TEXT,
            option_d       TEXT,
            correct_answer TEXT NOT NULL,
            marks          INTEGER DEFAULT 1,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)

    # ── Results table ─────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id   INTEGER NOT NULL,
            quiz_id      INTEGER NOT NULL,
            course_id    INTEGER NOT NULL,
            answer       TEXT,
            marks        REAL    DEFAULT 0,
            submitted_at TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (student_id) REFERENCES users(id),
            FOREIGN KEY (quiz_id)    REFERENCES quizzes(id)
        )
    """)

    # ── Enrollments table ─────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id  INTEGER NOT NULL,
            enrolled_at TEXT DEFAULT (datetime('now')),
            UNIQUE(student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES users(id),
            FOREIGN KEY (course_id)  REFERENCES courses(id)
        )
    """)

    # ── Announcements table ───────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT NOT NULL,
            message    TEXT,
            created_by INTEGER,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════
# SECTION 5: SEED / DUMMY DATA (100 students + sample data)
# Practice ke liye fake data dalo
# ═══════════════════════════════════════════════════════════

SUBJECTS = ["Python Programming", "Mathematics", "Data Science",
            "Web Development", "Machine Learning", "Database Systems"]

SAMPLE_MCQS = {
    "Python Programming": [
        ("What is Python?", "A) Snake  B) Language  C) Tool  D) Framework",
         "A", "B", "C", "D", "B"),
        ("Which keyword defines a function?", "A) fun  B) define  C) def  D) func",
         "A", "B", "C", "D", "C"),
        ("Output of print(2**3)?", "A) 6  B) 8  C) 9  D) 5",
         "A", "B", "C", "D", "B"),
        ("List is mutable?", "A) True  B) False  C) Maybe  D) Never",
         "A", "B", "C", "D", "A"),
        ("Which is not a data type?", "A) int  B) str  C) real  D) float",
         "A", "B", "C", "D", "C"),
    ],
    "Mathematics": [
        ("Value of pi (approx)?", "A) 3.14  B) 2.71  C) 1.61  D) 4.00",
         "A", "B", "C", "D", "A"),
        ("sqrt(144) = ?", "A) 10  B) 11  C) 12  D) 13",
         "A", "B", "C", "D", "C"),
        ("2 + 2 × 2 = ?", "A) 8  B) 6  C) 4  D) 5",
         "A", "B", "C", "D", "B"),
        ("log(1) = ?", "A) 1  B) 0  C) -1  D) undefined",
         "A", "B", "C", "D", "B"),
        ("Derivative of x² = ?", "A) x  B) 2x  C) 2  D) x²",
         "A", "B", "C", "D", "B"),
    ],
    "Data Science": [
        ("Pandas is used for?", "A) Games  B) Data  C) Web  D) Music",
         "A", "B", "C", "D", "B"),
        ("CSV stands for?", "A) Comma  B) Coded  C) Common  D) Content",
         "A", "B", "C", "D", "A"),
        ("DataFrame is from?", "A) NumPy  B) Pandas  C) SciPy  D) Keras",
         "A", "B", "C", "D", "B"),
        ("Mean of [2,4,6]?", "A) 3  B) 4  C) 5  D) 6",
         "A", "B", "C", "D", "B"),
        ("NaN stands for?", "A) Not Assigned  B) Not a Number  C) Null  D) None",
         "A", "B", "C", "D", "B"),
    ],
    "Web Development": [
        ("HTML stands for?", "A) Hyper Text  B) High Text  C) Hot Text  D) Hybrid",
         "A", "B", "C", "D", "A"),
        ("CSS is used for?", "A) Logic  B) Styling  C) Database  D) Backend",
         "A", "B", "C", "D", "B"),
        ("JavaScript runs where?", "A) Server  B) Browser  C) Database  D) OS",
         "A", "B", "C", "D", "B"),
        ("<br> tag does?", "A) Bold  B) Break  C) Border  D) Background",
         "A", "B", "C", "D", "B"),
        ("HTTP status 404?", "A) OK  B) Error  C) Not Found  D) Redirect",
         "A", "B", "C", "D", "C"),
    ],
    "Machine Learning": [
        ("ML stands for?", "A) Machine Language  B) Machine Learning  C) Math Logic  D) Model Layer",
         "A", "B", "C", "D", "B"),
        ("Overfitting means?", "A) Train good test bad  B) Both bad  C) Both good  D) Test good train bad",
         "A", "B", "C", "D", "A"),
        ("SVM stands for?", "A) Support Vector Machine  B) Simple Vector  C) Super VM  D) Soft VM",
         "A", "B", "C", "D", "A"),
        ("Linear Regression predicts?", "A) Category  B) Continuous  C) Image  D) Text",
         "A", "B", "C", "D", "B"),
        ("k in KNN means?", "A) Kernel  B) Neighbors  C) Key  D) Knot",
         "A", "B", "C", "D", "B"),
    ],
    "Database Systems": [
        ("SQL stands for?", "A) Structured Query Language  B) Simple Query  C) System Query  D) Sequential",
         "A", "B", "C", "D", "A"),
        ("Primary Key is?", "A) Unique identifier  B) Foreign key  C) Index  D) Column",
         "A", "B", "C", "D", "A"),
        ("SELECT * FROM means?", "A) All rows  B) One row  C) Count  D) Delete",
         "A", "B", "C", "D", "A"),
        ("JOIN combines?", "A) Rows  B) Tables  C) Databases  D) Columns",
         "A", "B", "C", "D", "B"),
        ("NULL means?", "A) Zero  B) Empty  C) No Value  D) False",
         "A", "B", "C", "D", "C"),
    ],
}

LECTURE_CONTENT = {
    "Python Programming": """
# Python Programming - Lecture 1: Introduction

## What is Python?
Python ek high-level, interpreted programming language hai jo 1991 mein Guido van Rossum ne banai.
Python easy to read aur write hoti hai isliye beginners ke liye best hai.

## Why Python?
- Simple syntax (Asaan grammar)
- Large community support
- Used in AI, Web, Data Science
- Free aur Open Source

## Basic Syntax:
```python
# Hello World program
print("Hello, World!")

# Variables
name = "Ali"
age = 20
gpa = 3.5

# If condition
if age >= 18:
    print("Adult hai")
else:
    print("Minor hai")
```

## Data Types:
- int: 10, 20, -5
- float: 3.14, 2.5
- str: "Hello"
- list: [1, 2, 3]
- dict: {"key": "value"}
- bool: True, False

## Functions:
```python
def greet(name):
    return f"Hello, {name}!"

result = greet("Ahmed")
print(result)  # Hello, Ahmed!
```
""",
    "Mathematics": """
# Mathematics - Lecture 1: Algebra Basics

## Algebra kya hai?
Algebra mathematics ki branch hai jisme variables (x, y, z) use hote hain unknown values ko represent karne ke liye.

## Linear Equations:
ax + b = c
Example: 2x + 5 = 11
=> 2x = 6
=> x = 3

## Quadratic Equations:
ax² + bx + c = 0
Formula: x = (-b ± √(b²-4ac)) / 2a

## Important Formulas:
- (a+b)² = a² + 2ab + b²
- (a-b)² = a² - 2ab + b²
- (a+b)(a-b) = a² - b²

## Practice Problems:
1. Solve: 3x + 7 = 22 → x = 5
2. Solve: x² - 5x + 6 = 0 → x = 2, 3
""",
    "Data Science": """
# Data Science - Lecture 1: Introduction & Pandas

## Data Science kya hai?
Data Science ek field hai jisme data se useful information nikali jati hai using statistics aur programming.

## Pandas Library:
```python
import pandas as pd

# DataFrame banana
data = {
    'Name': ['Ali', 'Ahmed', 'Sara'],
    'Marks': [85, 92, 78],
    'Grade': ['B', 'A', 'B']
}

df = pd.DataFrame(data)
print(df)

# Basic operations
print(df['Marks'].mean())   # Average
print(df['Marks'].max())    # Maximum
print(df.describe())        # Statistics
```

## Data Cleaning:
- Handle missing values: df.dropna() or df.fillna()
- Remove duplicates: df.drop_duplicates()
- Data types: df.dtypes

## NumPy:
```python
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(np.mean(arr))   # 3.0
print(np.std(arr))    # Standard deviation
```
""",
}

def hash_password(password: str) -> str:
    """Password ko hash karo security ke liye"""
    return hashlib.sha256(password.encode()).hexdigest()


def seed_dummy_data():
    """
    100 students, teachers, courses, quizzes, aur results ka sample data dalo.
    Yeh function sirf ek baar chalta hai.
    """
    conn = get_connection()
    c = conn.cursor()

    # Check karo agar data pehle se hai
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] > 0:
        conn.close()
        return

    # ── 1. Admin account ──────────────────────────────────
    c.execute("""INSERT INTO users (name, email, password, role)
                 VALUES (?, ?, ?, ?)""",
              ("Admin", "admin@slms.com", hash_password("admin123"), "admin"))

    # ── 2. Teachers (6 teachers) ──────────────────────────
    teacher_ids = []
    teachers = [
        ("Dr. Ali Hassan",    "ali@slms.com",    "teach123"),
        ("Prof. Sara Khan",   "sara@slms.com",   "teach123"),
        ("Dr. Ahmed Raza",    "ahmed@slms.com",  "teach123"),
        ("Ms. Fatima Malik",  "fatima@slms.com", "teach123"),
        ("Mr. Usman Tariq",   "usman@slms.com",  "teach123"),
        ("Dr. Ayesha Noor",   "ayesha@slms.com", "teach123"),
    ]
    for name, email, pwd in teachers:
        c.execute("""INSERT INTO users (name, email, password, role)
                     VALUES (?, ?, ?, ?)""",
                  (name, email, hash_password(pwd), "teacher"))
        teacher_ids.append(c.lastrowid)

    # ── 3. Courses ────────────────────────────────────────
    course_descs = [
        "Learn Python from scratch to advanced level.",
        "Master algebra, calculus, and statistics.",
        "Explore data analysis with Python and Pandas.",
        "Build websites with HTML, CSS, JavaScript.",
        "Understand ML algorithms and applications.",
        "Learn SQL, normalization, and database design.",
    ]
    course_ids = []
    for i, subject in enumerate(SUBJECTS):
        c.execute("""INSERT INTO courses (title, description, teacher_id)
                     VALUES (?, ?, ?)""",
                  (subject, course_descs[i], teacher_ids[i % len(teacher_ids)]))
        course_ids.append(c.lastrowid)

    # ── 4. Lectures ───────────────────────────────────────
    for i, cid in enumerate(course_ids):
        subj = SUBJECTS[i]
        content = LECTURE_CONTENT.get(subj,
                  f"# {subj}\n\nYeh lecture {subj} ke baare mein hai.\nContent coming soon...")
        c.execute("""INSERT INTO lectures (course_id, title, content)
                     VALUES (?, ?, ?)""",
                  (cid, f"{subj} - Lecture 1", content))
        c.execute("""INSERT INTO lectures (course_id, title, content)
                     VALUES (?, ?, ?)""",
                  (cid, f"{subj} - Lecture 2",
                   f"# {subj} - Advanced Topics\n\nMore advanced content here.\nPractice exercises included."))

    # ── 5. Quizzes (MCQs) ────────────────────────────────
    quiz_ids_per_course = {}
    for i, cid in enumerate(course_ids):
        subj = SUBJECTS[i]
        qs = SAMPLE_MCQS.get(subj, [])
        quiz_ids_per_course[cid] = []
        for q in qs:
            question, _, oa, ob, oc, od, correct = q
            c.execute("""INSERT INTO quizzes
                         (course_id, question, type, option_a, option_b, option_c, option_d, correct_answer, marks)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (cid, question, "mcq", oa, ob, oc, od, correct, 2))
            quiz_ids_per_course[cid].append(c.lastrowid)

    # ── 6. 100 Students ───────────────────────────────────
    first_names = ["Ali","Ahmed","Sara","Fatima","Omar","Zainab","Hassan","Maryam",
                   "Bilal","Aisha","Usman","Hina","Kamran","Nadia","Tariq","Sana",
                   "Asad","Rabia","Faisal","Anum","Imran","Sadia","Waqar","Maria",
                   "Hamza","Ayesha","Shahid","Iqra","Naveed","Saima","Rizwan","Amna",
                   "Junaid","Hira","Kashif","Rukhsana","Adnan","Shazia","Farhan","Zara"]
    last_names  = ["Khan","Ahmed","Ali","Hassan","Malik","Raza","Butt","Sheikh",
                   "Chaudhry","Qureshi","Siddiqui","Ansari","Mirza","Baig","Gill","Raja"]

    student_ids = []
    for i in range(100):
        fn  = random.choice(first_names)
        ln  = random.choice(last_names)
        name  = f"{fn} {ln}"
        email = f"s{1000+i}@student.com"
        c.execute("""INSERT INTO users (name, email, password, role)
                     VALUES (?, ?, ?, ?)""",
                  (name, email, hash_password("student123"), "student"))
        student_ids.append(c.lastrowid)

    # ── 7. Enrollments + Results ──────────────────────────
    for sid in student_ids:
        # Each student enrolled in 2-4 random courses
        enrolled_courses = random.sample(course_ids, k=random.randint(2, 4))
        for cid in enrolled_courses:
            try:
                c.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
                          (sid, cid))
            except sqlite3.IntegrityError:
                pass

            # Attempt quizzes (simulate random performance)
            ability = random.uniform(0.3, 1.0)  # student ability level
            for qid in quiz_ids_per_course.get(cid, []):
                correct = random.random() < ability
                if correct:
                    # Get correct answer
                    c.execute("SELECT correct_answer, marks FROM quizzes WHERE id=?", (qid,))
                    row = c.fetchone()
                    ans   = row[0]
                    marks = row[1]
                else:
                    wrong_opts = ["A","B","C","D"]
                    c.execute("SELECT correct_answer FROM quizzes WHERE id=?", (qid,))
                    correct_ans = c.fetchone()[0]
                    wrong_opts  = [x for x in wrong_opts if x != correct_ans]
                    ans   = random.choice(wrong_opts)
                    marks = 0

                # Backdate submissions (last 90 days)
                days_ago = random.randint(0, 90)
                sub_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
                c.execute("""INSERT INTO results (student_id, quiz_id, course_id, answer, marks, submitted_at)
                             VALUES (?, ?, ?, ?, ?, ?)""",
                          (sid, qid, cid, ans, marks, sub_date))

    # ── 8. Announcements ─────────────────────────────────
    announcements = [
        ("Welcome to SLMS!", "Smart Learning Management System mein khush aamdeed!"),
        ("Mid-Term Schedule",  "Mid-term exams next week se shuru honge."),
        ("Assignment Due",     "Python assignment kal tak jama karayein."),
        ("Result Announced",   "Quiz 1 ke results portal par available hain."),
    ]
    for title, msg in announcements:
        c.execute("INSERT INTO announcements (title, message, created_by) VALUES (?,?,?)",
                  (title, msg, 1))

    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════
# SECTION 6: AUTHENTICATION (Login / Register)
# User ko verify karo aur session handle karo
# ═══════════════════════════════════════════════════════════

def login_user(email: str, password: str):
    """Email aur password se user dhundo"""
    conn = get_connection()
    c    = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (email, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None


def register_user(name: str, email: str, password: str, role: str = "student") -> bool:
    """Naya user register karo"""
    conn = get_connection()
    c    = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)",
                  (name, email, hash_password(password), role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def render_auth_page():
    """Login/Register page render karo"""
    st.markdown("""
    <div style='text-align:center; padding: 20px 0;'>
        <h1 style='font-size:3em; margin-bottom:4px;'>🎓 Smart LMS</h1>
        <p style='color:#666; font-size:1.1em;'>AI-Powered Learning Management System</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])

        # ── Login Tab ──────────────────────────────────
        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            email    = st.text_input("📧 Email", key="login_email",
                                     placeholder="your@email.com")
            password = st.text_input("🔒 Password", type="password",
                                     key="login_pw", placeholder="••••••••")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Login  →", key="btn_login"):
                if not email or not password:
                    st.error("Email aur password required hain!")
                else:
                    user = login_user(email.strip(), password)
                    if user:
                        st.session_state.user = user
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("❌ Invalid email ya password!")

            st.markdown("""
            <div style='margin-top:16px; padding:12px; background:#f0f9ff;
                        border-radius:8px; font-size:12px; color:#0369a1;'>
            <b>Demo Accounts:</b><br>
            👤 Admin: admin@slms.com / admin123<br>
            👨‍🏫 Teacher: ali@slms.com / teach123<br>
            👨‍🎓 Student: s1000@student.com / student123
            </div>
            """, unsafe_allow_html=True)

        # ── Register Tab ────────────────────────────────
        with tab_register:
            st.markdown("<br>", unsafe_allow_html=True)
            r_name  = st.text_input("👤 Full Name",   key="reg_name",  placeholder="Muhammad Ali")
            r_email = st.text_input("📧 Email",        key="reg_email", placeholder="ali@email.com")
            r_pass  = st.text_input("🔒 Password",     type="password", key="reg_pass",
                                    placeholder="Min 6 characters")
            r_role  = st.selectbox("🎭 Role",
                                   ["student", "teacher"],
                                   key="reg_role")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account  →", key="btn_register"):
                if not all([r_name, r_email, r_pass]):
                    st.error("Tamam fields required hain!")
                elif len(r_pass) < 6:
                    st.error("Password min 6 characters ka hona chahiye!")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", r_email):
                    st.error("Valid email address daalen!")
                else:
                    if register_user(r_name.strip(), r_email.strip(), r_pass, r_role):
                        st.success("✅ Account successfully bana! Ab login karain.")
                    else:
                        st.error("❌ Email already registered hai!")


# ═══════════════════════════════════════════════════════════
# SECTION 7: HELPER / UTILITY FUNCTIONS
# Chhote chhote kaam karne wale functions
# ═══════════════════════════════════════════════════════════

def get_df(query: str, params: tuple = ()) -> pd.DataFrame:
    """SQL query se Pandas DataFrame banao"""
    conn = get_connection()
    df   = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def run_query(query: str, params: tuple = ()):
    """Write query (INSERT/UPDATE/DELETE) chalao"""
    conn = get_connection()
    c    = conn.cursor()
    c.execute(query, params)
    lid = c.lastrowid
    conn.commit()
    conn.close()
    return lid


def evaluate_mcq(answer: str, correct: str) -> bool:
    """MCQ ka jawab check karo (exact match)"""
    return str(answer).strip().upper() == str(correct).strip().upper()


def evaluate_short_answer(answer: str, correct: str) -> float:
    """
    Short answer evaluation (keyword matching NLP)
    Jawab mein kitne keywords hain? Score 0-1 return karo.
    """
    if not answer or not correct:
        return 0.0
    answer_words  = set(answer.lower().split())
    correct_words = set(correct.lower().split())
    if not correct_words:
        return 0.0
    overlap = answer_words & correct_words
    score   = len(overlap) / len(correct_words)
    return min(score, 1.0)


def calculate_grade(percentage: float) -> str:
    """Percentage se grade nikalo"""
    if   percentage >= 90: return "A+"
    elif percentage >= 80: return "A"
    elif percentage >= 70: return "B"
    elif percentage >= 60: return "C"
    elif percentage >= 50: return "D"
    else:                  return "F"


def grade_color(grade: str) -> str:
    """Grade ka color return karo"""
    colors = {"A+": "#16a34a", "A": "#22c55e", "B": "#3b82f6",
              "C": "#f59e0b", "D": "#f97316", "F": "#ef4444"}
    return colors.get(grade, "#6b7280")


# ═══════════════════════════════════════════════════════════
# SECTION 8: AI / ML MODULE
# Performance prediction using Scikit-learn
# ═══════════════════════════════════════════════════════════

def train_performance_model():
    """
    Logistic Regression model train karo:
    Input: average_marks, total_quizzes, completion_rate
    Output: pass (1) ya fail (0)
    """
    np.random.seed(42)
    n = 300

    avg_marks       = np.random.uniform(0, 100, n)
    total_quizzes   = np.random.randint(1, 20,  n)
    completion_rate = np.random.uniform(0, 1,   n)

    # Pass agar average > 50 aur completion > 40%
    labels = ((avg_marks > 50) & (completion_rate > 0.4)).astype(int)
    # Thodi noise dalo
    noise_idx = np.random.choice(n, size=20, replace=False)
    labels[noise_idx] = 1 - labels[noise_idx]

    X = np.column_stack([avg_marks, total_quizzes, completion_rate])
    y = labels

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    model = LogisticRegression(random_state=42, max_iter=200)
    model.fit(X_train_scaled, y_train)

    return model, scaler


def predict_performance(model, scaler, avg_marks: float,
                         total_quizzes: int, completion_rate: float) -> dict:
    """Student ki performance predict karo"""
    X = np.array([[avg_marks, total_quizzes, completion_rate]])
    X_scaled = scaler.transform(X)
    pred   = model.predict(X_scaled)[0]
    proba  = model.predict_proba(X_scaled)[0]
    return {
        "prediction": "Pass ✅" if pred == 1 else "Fail ❌",
        "pass_prob":  round(proba[1] * 100, 1),
        "fail_prob":  round(proba[0] * 100, 1),
        "status":     int(pred)
    }


def detect_weak_subjects(student_id: int) -> pd.DataFrame:
    """
    Student ke weak subjects dhundo:
    Percentage < 60% wale courses weak hain
    """
    df = get_df("""
        SELECT c.title as Subject,
               COUNT(r.id)      as Total_Attempts,
               SUM(r.marks)     as Marks_Earned,
               SUM(q.marks)     as Total_Marks
        FROM   results r
        JOIN   quizzes q ON r.quiz_id  = q.id
        JOIN   courses c ON r.course_id = c.id
        WHERE  r.student_id = ?
        GROUP  BY c.id
    """, (student_id,))

    if df.empty:
        return df

    df["Percentage"]    = np.where(
        df["Total_Marks"] > 0,
        (df["Marks_Earned"] / df["Total_Marks"] * 100).round(1),
        0
    )
    df["Status"] = df["Percentage"].apply(
        lambda p: "⚠️ Weak" if p < 60 else ("✅ Good" if p >= 75 else "📈 Average")
    )
    df["Grade"] = df["Percentage"].apply(calculate_grade)
    return df.sort_values("Percentage")


def get_suggestions(weak_df: pd.DataFrame) -> list:
    """Weak subjects ki base par improvement suggestions do"""
    suggestions = []
    if weak_df.empty:
        return ["Excellent! Keep up the good work! 🌟"]

    for _, row in weak_df.iterrows():
        if row["Percentage"] < 60:
            suggestions.append(
                f"📚 **{row['Subject']}**: Score {row['Percentage']:.1f}% — "
                f"Zyada practice karein. Lectures dobara parhen aur quizzes repeat karein."
            )
        elif row["Percentage"] < 75:
            suggestions.append(
                f"📈 **{row['Subject']}**: Score {row['Percentage']:.1f}% — "
                f"Thodi aur mehnat ki zaroorat hai. Practice sets try karein."
            )
    if not suggestions:
        suggestions.append("🎉 Sab subjects mein acha perform kar rahe ho! Keep it up!")
    return suggestions


# ═══════════════════════════════════════════════════════════
# SECTION 9: VISUALIZATION FUNCTIONS (Charts / Graphs)
# Matplotlib se beautiful charts banao
# ═══════════════════════════════════════════════════════════

def set_chart_style():
    """Chart ka global style set karo"""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size":   10,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "figure.facecolor": "white",
        "axes.facecolor":   "white",
    })


def chart_subject_performance(student_id: int):
    """Bar chart: Subject-wise marks"""
    df = detect_weak_subjects(student_id)
    if df.empty:
        st.info("Koi quiz attempt nahi kiya abhi tak.")
        return

    set_chart_style()
    fig, ax = plt.subplots(figsize=(9, 4))
    colors  = ["#ef4444" if p < 60 else "#f59e0b" if p < 75 else "#22c55e"
               for p in df["Percentage"]]
    bars    = ax.barh(df["Subject"], df["Percentage"], color=colors,
                      edgecolor="white", linewidth=1.5, height=0.6)

    ax.axvline(60, color="#ef4444", linestyle="--", linewidth=1.2,
               label="Pass Line (60%)", alpha=0.7)
    ax.axvline(75, color="#f59e0b", linestyle="--", linewidth=1.2,
               label="Good Line (75%)",  alpha=0.7)

    for bar, val in zip(bars, df["Percentage"]):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{val:.1f}%", va="center", fontsize=9, fontweight="bold")

    ax.set_xlim(0, 110)
    ax.set_xlabel("Percentage (%)")
    ax.set_title("📊 Subject-wise Performance")
    ax.legend(loc="lower right", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


def chart_progress_over_time(student_id: int):
    """Line chart: Marks progress over time"""
    df = get_df("""
        SELECT DATE(r.submitted_at) as Date,
               AVG(r.marks * 100.0 / NULLIF(q.marks,0)) as AvgPct
        FROM   results r
        JOIN   quizzes q ON r.quiz_id = q.id
        WHERE  r.student_id = ?
        GROUP  BY DATE(r.submitted_at)
        ORDER  BY Date
    """, (student_id,))

    if df.empty or len(df) < 2:
        st.info("Progress chart ke liye zyada data chahiye.")
        return

    set_chart_style()
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(pd.to_datetime(df["Date"]), df["AvgPct"],
            marker="o", linewidth=2.5, markersize=6,
            color="#0f3460", markerfacecolor="#533483")
    ax.fill_between(pd.to_datetime(df["Date"]), df["AvgPct"],
                    alpha=0.15, color="#0f3460")
    ax.set_ylim(0, 110)
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Score (%)")
    ax.set_title("📈 Progress Over Time")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


def chart_grade_distribution(student_id: int):
    """Pie chart: Grade distribution"""
    df = detect_weak_subjects(student_id)
    if df.empty:
        return

    grade_counts = df["Grade"].value_counts()
    colors = {"A+": "#16a34a","A": "#22c55e","B": "#3b82f6",
              "C": "#f59e0b","D": "#f97316","F": "#ef4444"}
    chart_colors = [colors.get(g, "#6b7280") for g in grade_counts.index]

    set_chart_style()
    fig, ax = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax.pie(
        grade_counts.values, labels=grade_counts.index,
        autopct="%1.0f%%", colors=chart_colors,
        startangle=90, pctdistance=0.8,
        wedgeprops=dict(edgecolor="white", linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")
    ax.set_title("Grade Distribution")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


def chart_admin_overview():
    """Admin ke liye system analytics charts"""
    # Student enrollment per course
    df = get_df("""
        SELECT c.title, COUNT(e.student_id) as Students
        FROM courses c
        LEFT JOIN enrollments e ON c.id = e.course_id
        GROUP BY c.id
        ORDER BY Students DESC
    """)

    if df.empty:
        return

    set_chart_style()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Chart 1: Enrollments per course
    axes[0].bar(df["title"], df["Students"],
                color=["#0f3460","#533483","#e94560","#16213e","#0f3460","#533483"],
                edgecolor="white")
    axes[0].set_title("Enrollments per Course")
    axes[0].set_xlabel("Course")
    axes[0].set_ylabel("Students")
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=30, ha="right", fontsize=8)

    # Chart 2: Role distribution
    role_df = get_df("SELECT role, COUNT(*) as count FROM users GROUP BY role")
    axes[1].pie(role_df["count"], labels=role_df["role"].str.capitalize(),
                autopct="%1.0f%%",
                colors=["#0f3460","#533483","#e94560"],
                wedgeprops=dict(edgecolor="white", linewidth=2))
    axes[1].set_title("User Role Distribution")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


def chart_teacher_results(teacher_id: int):
    """Teacher ke courses ki results bar chart"""
    df = get_df("""
        SELECT c.title,
               COUNT(DISTINCT r.student_id) as Students,
               ROUND(AVG(r.marks * 100.0 / NULLIF(q.marks,0)),1) as AvgScore
        FROM   results r
        JOIN   courses c ON r.course_id = c.id
        JOIN   quizzes q ON r.quiz_id   = q.id
        WHERE  c.teacher_id = ?
        GROUP  BY c.id
    """, (teacher_id,))

    if df.empty:
        st.info("Abhi tak koi results nahi hain.")
        return

    set_chart_style()
    fig, ax = plt.subplots(figsize=(9, 4))
    x   = np.arange(len(df))
    w   = 0.35
    b1  = ax.bar(x - w/2, df["Students"], w, label="Students", color="#0f3460")
    b2  = ax.bar(x + w/2, df["AvgScore"], w, label="Avg Score %", color="#533483")
    ax.set_xticks(x)
    ax.set_xticklabels(df["title"], rotation=20, ha="right", fontsize=8)
    ax.set_title("📊 Course Performance Overview")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ═══════════════════════════════════════════════════════════
# SECTION 10: STUDENT PANEL
# Student ke liye tamam pages / features
# ═══════════════════════════════════════════════════════════

def render_student_dashboard():
    """Student ka main dashboard"""
    uid  = st.session_state.user["id"]
    name = st.session_state.user["name"]

    st.markdown(f"## 👋 Welcome back, **{name}**!")

    # ── KPI Metrics ──────────────────────────────────────
    enrolled = get_df(
        "SELECT COUNT(*) as c FROM enrollments WHERE student_id=?", (uid,))
    attempts = get_df(
        "SELECT COUNT(*) as c FROM results WHERE student_id=?", (uid,))
    results  = get_df("""
        SELECT COALESCE(SUM(r.marks),0) as earned,
               COALESCE(SUM(q.marks),0) as total
        FROM   results r JOIN quizzes q ON r.quiz_id=q.id
        WHERE  r.student_id=?
    """, (uid,))

    total_marks = results["total"].iloc[0] if not results.empty else 0
    earned      = results["earned"].iloc[0] if not results.empty else 0
    pct         = round(float(earned) / float(total_marks) * 100, 1) if total_marks > 0 else 0
    grade       = calculate_grade(pct)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Enrolled Courses", int(enrolled["c"].iloc[0]))
    col2.metric("📝 Quiz Attempts",    int(attempts["c"].iloc[0]))
    col3.metric("📊 Overall Score",    f"{pct}%")
    col4.metric("🏆 Grade",            grade)

    st.markdown("---")

    # ── Charts ───────────────────────────────────────────
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.markdown("### 📊 Subject-wise Performance")
        chart_subject_performance(uid)
    with col_r:
        st.markdown("### 🎯 Grade Distribution")
        chart_grade_distribution(uid)

    st.markdown("### 📈 Progress Over Time")
    chart_progress_over_time(uid)

    # ── AI Prediction ─────────────────────────────────────
    st.markdown("### 🤖 AI Performance Prediction")
    total_q = int(attempts["c"].iloc[0])
    total_available = get_df("""
        SELECT COUNT(q.id) as c FROM quizzes q
        JOIN enrollments e ON q.course_id=e.course_id
        WHERE e.student_id=?
    """, (uid,))
    avail = int(total_available["c"].iloc[0]) if not total_available.empty else 1
    comp_rate = round(min(total_q / avail, 1.0), 2) if avail > 0 else 0

    model, scaler = train_performance_model()
    result = predict_performance(model, scaler, pct, total_q, comp_rate)

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown(f"""
        <div class='card {"card-success" if result["status"]==1 else "card-danger"}'>
            <h3 style='text-align:center;'>🎯 Prediction</h3>
            <h2 style='text-align:center; font-size:2em;'>{result['prediction']}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col_p2:
        st.metric("✅ Pass Probability", f"{result['pass_prob']}%")
    with col_p3:
        st.metric("❌ Fail Probability", f"{result['fail_prob']}%")

    # ── Announcements ─────────────────────────────────────
    st.markdown("### 📢 Recent Announcements")
    ann_df = get_df("SELECT title, message, created_at FROM announcements ORDER BY id DESC LIMIT 3")
    for _, row in ann_df.iterrows():
        st.info(f"**{row['title']}** — {row['message']} *(📅 {row['created_at'][:10]})*")


def render_student_courses():
    """Student ke enrolled + available courses"""
    uid = st.session_state.user["id"]
    st.markdown("## 📚 My Courses")

    tab1, tab2 = st.tabs(["✅ Enrolled Courses", "🔍 Browse All Courses"])

    with tab1:
        df = get_df("""
            SELECT c.id, c.title, c.description, u.name as Teacher
            FROM   enrollments e
            JOIN   courses c ON e.course_id = c.id
            LEFT JOIN users u ON c.teacher_id = u.id
            WHERE  e.student_id = ?
        """, (uid,))

        if df.empty:
            st.info("Abhi tak kisi course mein enrolled nahi ho. Browse All Courses se enroll karo.")
        else:
            for _, row in df.iterrows():
                with st.expander(f"📖 {row['title']} — by {row['Teacher']}", expanded=False):
                    st.write(f"**Description:** {row['description']}")

                    # Lectures
                    lec_df = get_df(
                        "SELECT id, title FROM lectures WHERE course_id=?", (row["id"],))
                    if not lec_df.empty:
                        st.markdown("**📹 Lectures:**")
                        for _, lec in lec_df.iterrows():
                            if st.button(f"📄 {lec['title']}", key=f"lec_{lec['id']}"):
                                st.session_state.view_lecture = lec["id"]

                    # View selected lecture
                    if "view_lecture" in st.session_state:
                        l = get_df("SELECT * FROM lectures WHERE id=?",
                                   (st.session_state.view_lecture,))
                        if not l.empty and l.iloc[0]["course_id"] == row["id"]:
                            st.markdown("---")
                            st.markdown(l.iloc[0]["content"])

    with tab2:
        all_courses = get_df("""
            SELECT c.id, c.title, c.description, u.name as Teacher
            FROM   courses c
            LEFT JOIN users u ON c.teacher_id = u.id
        """)
        enrolled_ids = get_df(
            "SELECT course_id FROM enrollments WHERE student_id=?", (uid,))["course_id"].tolist()

        for _, row in all_courses.iterrows():
            col_c, col_btn = st.columns([4, 1])
            with col_c:
                st.markdown(f"**{row['title']}** — *{row['Teacher']}*")
                st.caption(row["description"] or "")
            with col_btn:
                if row["id"] in enrolled_ids:
                    st.markdown('<span class="badge badge-green">Enrolled ✓</span>',
                                unsafe_allow_html=True)
                else:
                    if st.button("Enroll", key=f"enroll_{row['id']}"):
                        try:
                            run_query(
                                "INSERT INTO enrollments (student_id,course_id) VALUES (?,?)",
                                (uid, row["id"]))
                            st.success(f"✅ '{row['title']}' mein enrolled ho gaye!")
                            st.rerun()
                        except Exception:
                            st.error("Already enrolled hai!")
            st.divider()


def render_student_quiz():
    """Student quiz attempt page"""
    uid = st.session_state.user["id"]
    st.markdown("## 📝 Quiz Section")

    # Get enrolled courses
    courses = get_df("""
        SELECT c.id, c.title FROM courses c
        JOIN enrollments e ON c.id=e.course_id
        WHERE e.student_id=?
    """, (uid,))

    if courses.empty:
        st.warning("Pehle kisi course mein enroll karo!")
        return

    selected_course = st.selectbox(
        "📚 Course chunen:",
        options=courses["id"].tolist(),
        format_func=lambda x: courses[courses["id"] == x]["title"].values[0]
    )

    if not selected_course:
        return

    # Get unattempted questions
    quizzes = get_df("""
        SELECT q.* FROM quizzes q
        WHERE q.course_id = ?
        AND   q.id NOT IN (
            SELECT quiz_id FROM results WHERE student_id=? AND course_id=?
        )
    """, (selected_course, uid, selected_course))

    if quizzes.empty:
        st.success("🎉 Is course ke tamam quizzes complete ho gaye hain!")

        # Show course result
        res = get_df("""
            SELECT SUM(r.marks) as earned, SUM(q.marks) as total
            FROM results r JOIN quizzes q ON r.quiz_id=q.id
            WHERE r.student_id=? AND r.course_id=?
        """, (uid, selected_course))
        if not res.empty and res["total"].iloc[0]:
            e = float(res["earned"].iloc[0])
            t = float(res["total"].iloc[0])
            p = round(e / t * 100, 1)
            g = calculate_grade(p)
            col1, col2, col3 = st.columns(3)
            col1.metric("Marks Earned", f"{e:.0f}/{t:.0f}")
            col2.metric("Percentage",   f"{p}%")
            col3.metric("Grade",         g)
        return

    st.markdown(f"**{len(quizzes)} questions remaining**")

    # Show first unattempted question
    q = quizzes.iloc[0]
    st.markdown("---")
    st.markdown(f"### Q: {q['question']}")

    answer = None
    if q["type"] == "mcq":
        options = {}
        for opt in ["A","B","C","D"]:
            val = q.get(f"option_{opt.lower()}")
            if val:
                options[opt] = f"{opt}) {val}"
        if options:
            answer = st.radio("Jawab chunen:", list(options.keys()),
                              format_func=lambda x: options[x],
                              key=f"quiz_{q['id']}")
        else:
            answer = st.radio("Jawab chunen:", ["A","B","C","D"],
                              key=f"quiz_{q['id']}")
    else:
        answer = st.text_area("Apna jawab likhein:", key=f"short_{q['id']}", height=100)

    col_sub, col_skip = st.columns([1, 5])
    with col_sub:
        if st.button("✅ Submit Answer"):
            if not answer:
                st.warning("Pehle jawab chunen!")
            else:
                # Evaluate
                if q["type"] == "mcq":
                    correct = evaluate_mcq(answer, q["correct_answer"])
                    marks   = float(q["marks"]) if correct else 0.0
                else:
                    score   = evaluate_short_answer(answer, q["correct_answer"])
                    marks   = round(float(q["marks"]) * score, 2)
                    correct = score > 0.5

                run_query("""INSERT INTO results (student_id,quiz_id,course_id,answer,marks)
                             VALUES (?,?,?,?,?)""",
                          (uid, q["id"], selected_course, answer, marks))

                if correct:
                    st.success(f"✅ Sahi jawab! +{marks} marks")
                else:
                    st.error(f"❌ Galat jawab. Sahi jawab: **{q['correct_answer']}**")

                import time; time.sleep(1)
                st.rerun()


def render_student_results():
    """Student ka performance aur results page"""
    uid = st.session_state.user["id"]
    st.markdown("## 📊 My Performance & Results")

    # Subject-wise summary
    weak_df = detect_weak_subjects(uid)
    if not weak_df.empty:
        st.markdown("### 📋 Subject-wise Report")
        display_df = weak_df[["Subject","Total_Attempts","Marks_Earned",
                               "Total_Marks","Percentage","Grade","Status"]].copy()
        display_df.columns = ["Subject","Attempts","Earned","Total","Percentage%","Grade","Status"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Suggestions
        st.markdown("### 💡 AI Improvement Suggestions")
        suggestions = get_suggestions(weak_df)
        for s in suggestions:
            st.markdown(f"- {s}")

    # Detailed result history
    st.markdown("### 📜 Quiz History")
    hist = get_df("""
        SELECT q.question, c.title as Course, r.answer,
               q.correct_answer, r.marks, q.marks as max_marks,
               r.submitted_at
        FROM results r
        JOIN quizzes q ON r.quiz_id=q.id
        JOIN courses c ON r.course_id=c.id
        WHERE r.student_id=?
        ORDER BY r.submitted_at DESC
        LIMIT 50
    """, (uid,))

    if not hist.empty:
        hist["Result"] = hist.apply(
            lambda x: "✅" if str(x["answer"]).upper() == str(x["correct_answer"]).upper() else "❌",
            axis=1
        )
        hist["Date"] = pd.to_datetime(hist["submitted_at"]).dt.strftime("%Y-%m-%d")
        st.dataframe(
            hist[["Course","question","answer","correct_answer","marks","max_marks","Result","Date"]],
            use_container_width=True, hide_index=True
        )


# ═══════════════════════════════════════════════════════════
# SECTION 11: TEACHER PANEL
# Teacher ke liye tamam features
# ═══════════════════════════════════════════════════════════

def render_teacher_dashboard():
    """Teacher ka main dashboard"""
    tid  = st.session_state.user["id"]
    name = st.session_state.user["name"]

    st.markdown(f"## 👨‍🏫 Teacher Dashboard — **{name}**")

    # Metrics
    my_courses = get_df(
        "SELECT COUNT(*) as c FROM courses WHERE teacher_id=?", (tid,))
    my_students = get_df("""
        SELECT COUNT(DISTINCT e.student_id) as c
        FROM enrollments e
        JOIN courses c ON e.course_id=c.id
        WHERE c.teacher_id=?
    """, (tid,))
    my_quizzes = get_df("""
        SELECT COUNT(*) as c FROM quizzes q
        JOIN courses c ON q.course_id=c.id
        WHERE c.teacher_id=?
    """, (tid,))

    col1, col2, col3 = st.columns(3)
    col1.metric("📚 My Courses",  int(my_courses["c"].iloc[0]))
    col2.metric("👨‍🎓 Students",   int(my_students["c"].iloc[0]))
    col3.metric("📝 Quizzes",     int(my_quizzes["c"].iloc[0]))

    st.markdown("---")
    st.markdown("### 📊 Course Performance Overview")
    chart_teacher_results(tid)


def render_teacher_courses():
    """Teacher course management page"""
    tid = st.session_state.user["id"]
    st.markdown("## 📚 Manage Courses")

    tab1, tab2 = st.tabs(["➕ Add Course", "📋 My Courses"])

    with tab1:
        st.markdown("### Create New Course")
        title = st.text_input("Course Title", placeholder="e.g. Advanced Python")
        desc  = st.text_area("Description",   placeholder="Course ka overview likhein...")
        if st.button("🚀 Create Course"):
            if title:
                run_query("INSERT INTO courses (title,description,teacher_id) VALUES (?,?,?)",
                          (title.strip(), desc.strip(), tid))
                st.success(f"✅ Course '{title}' successfully create ho gaya!")
                st.rerun()
            else:
                st.error("Course title required hai!")

    with tab2:
        courses = get_df(
            "SELECT id, title, description, created_at FROM courses WHERE teacher_id=?", (tid,))
        if courses.empty:
            st.info("Koi course nahi hai abhi tak.")
        else:
            for _, c in courses.iterrows():
                with st.expander(f"📖 {c['title']}", expanded=False):
                    st.write(f"**Description:** {c['description']}")
                    st.write(f"**Created:** {c['created_at'][:10]}")

                    # Enrolled students count
                    cnt = get_df(
                        "SELECT COUNT(*) as n FROM enrollments WHERE course_id=?", (c["id"],))
                    st.write(f"**👨‍🎓 Enrolled Students:** {int(cnt['n'].iloc[0])}")

                    # Add Lecture
                    st.markdown("---")
                    st.markdown("**➕ Add Lecture:**")
                    lec_title   = st.text_input("Lecture Title",   key=f"lt_{c['id']}")
                    lec_content = st.text_area("Lecture Content",  key=f"lc_{c['id']}", height=150)
                    if st.button("Add Lecture", key=f"addlec_{c['id']}"):
                        if lec_title:
                            run_query("INSERT INTO lectures (course_id,title,content) VALUES (?,?,?)",
                                      (c["id"], lec_title, lec_content))
                            st.success("✅ Lecture add ho gaya!")
                            st.rerun()

                    # Existing lectures
                    lecs = get_df(
                        "SELECT title FROM lectures WHERE course_id=?", (c["id"],))
                    if not lecs.empty:
                        st.markdown(f"**📹 Lectures ({len(lecs)}):** " +
                                    " | ".join(f"`{t}`" for t in lecs["title"]))


def render_teacher_quiz_creator():
    """Teacher quiz create karne ka page"""
    tid = st.session_state.user["id"]
    st.markdown("## 📝 Create Quiz Questions")

    courses = get_df(
        "SELECT id, title FROM courses WHERE teacher_id=?", (tid,))
    if courses.empty:
        st.warning("Pehle ek course banao!")
        return

    selected = st.selectbox("Course chunen:",
                            options=courses["id"].tolist(),
                            format_func=lambda x: courses[courses["id"] == x]["title"].values[0])

    tab_add, tab_view = st.tabs(["➕ Add Question", "📋 Existing Questions"])

    with tab_add:
        q_type = st.radio("Question Type:", ["mcq", "short"], horizontal=True,
                          format_func=lambda x: "MCQ (Multiple Choice)" if x=="mcq" else "Short Answer")
        question = st.text_area("Question:", height=80)
        marks    = st.number_input("Marks:", min_value=1, max_value=10, value=2)
        correct  = None

        if q_type == "mcq":
            col1, col2 = st.columns(2)
            with col1:
                oa = st.text_input("Option A:", key="oa")
                ob = st.text_input("Option B:", key="ob")
            with col2:
                oc = st.text_input("Option C:", key="oc")
                od = st.text_input("Option D:", key="od")
            correct = st.selectbox("Correct Answer:", ["A","B","C","D"])
        else:
            correct = st.text_input("Correct Answer (keywords):",
                                    placeholder="Main keywords likhein jaise: python, programming")

        if st.button("✅ Add Question"):
            if question and correct:
                if q_type == "mcq":
                    run_query("""INSERT INTO quizzes
                                 (course_id,question,type,option_a,option_b,option_c,option_d,correct_answer,marks)
                                 VALUES (?,?,?,?,?,?,?,?,?)""",
                              (selected, question, q_type, oa, ob, oc, od, correct, marks))
                else:
                    run_query("""INSERT INTO quizzes
                                 (course_id,question,type,correct_answer,marks)
                                 VALUES (?,?,?,?,?)""",
                              (selected, question, q_type, correct, marks))
                st.success("✅ Question add ho gaya!")
                st.rerun()
            else:
                st.error("Question aur correct answer required hain!")

    with tab_view:
        q_df = get_df("SELECT id, question, type, correct_answer, marks FROM quizzes WHERE course_id=?",
                      (selected,))
        if q_df.empty:
            st.info("Is course mein koi question nahi hai.")
        else:
            st.dataframe(q_df, use_container_width=True, hide_index=True)
            # Delete question
            del_id = st.number_input("Question ID delete karein:", min_value=0, step=1)
            if st.button("🗑️ Delete Question") and del_id:
                run_query("DELETE FROM quizzes WHERE id=? AND course_id=?", (del_id, selected))
                st.success(f"Question {del_id} delete ho gaya!")
                st.rerun()


def render_teacher_students():
    """Teacher apne students ki results dekhe"""
    tid = st.session_state.user["id"]
    st.markdown("## 👨‍🎓 Student Results")

    courses = get_df("SELECT id, title FROM courses WHERE teacher_id=?", (tid,))
    if courses.empty:
        st.info("Koi course nahi hai.")
        return

    selected = st.selectbox("Course chunen:",
                            options=courses["id"].tolist(),
                            format_func=lambda x: courses[courses["id"] == x]["title"].values[0])

    results = get_df("""
        SELECT u.name as Student, u.email,
               COUNT(r.id)           as Attempts,
               SUM(r.marks)          as Earned,
               SUM(q.marks)          as Total,
               ROUND(SUM(r.marks)*100.0/NULLIF(SUM(q.marks),0),1) as Percentage
        FROM results r
        JOIN users u   ON r.student_id = u.id
        JOIN quizzes q ON r.quiz_id    = q.id
        WHERE r.course_id = ?
        GROUP BY r.student_id
        ORDER BY Percentage DESC
    """, (selected,))

    if results.empty:
        st.info("Is course mein abhi tak koi result nahi hai.")
        return

    results["Grade"] = results["Percentage"].apply(calculate_grade)
    results["Status"] = results["Percentage"].apply(
        lambda p: "Pass ✅" if p >= 50 else "Fail ❌")

    st.dataframe(results, use_container_width=True, hide_index=True)

    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Class Average", f"{results['Percentage'].mean():.1f}%")
    col2.metric("🏆 Highest",        f"{results['Percentage'].max():.1f}%")
    col3.metric("📉 Lowest",         f"{results['Percentage'].min():.1f}%")


# ═══════════════════════════════════════════════════════════
# SECTION 12: ADMIN PANEL
# Admin ke liye system management
# ═══════════════════════════════════════════════════════════

def render_admin_dashboard():
    """Admin ka main dashboard"""
    st.markdown("## 👨‍💼 Admin Dashboard")

    # System metrics
    users    = get_df("SELECT role, COUNT(*) as c FROM users GROUP BY role")
    courses  = get_df("SELECT COUNT(*) as c FROM courses")
    results  = get_df("SELECT COUNT(*) as c FROM results")
    lectures = get_df("SELECT COUNT(*) as c FROM lectures")

    students_count = int(users[users["role"]=="student"]["c"].sum()) if not users.empty else 0
    teachers_count = int(users[users["role"]=="teacher"]["c"].sum()) if not users.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👨‍🎓 Students",  students_count)
    col2.metric("👨‍🏫 Teachers",  teachers_count)
    col3.metric("📚 Courses",   int(courses["c"].iloc[0]))
    col4.metric("📝 Quiz Attempts", int(results["c"].iloc[0]))

    st.markdown("---")
    st.markdown("### 📊 System Analytics")
    chart_admin_overview()

    # Recent activity
    st.markdown("### 🕐 Recent Quiz Activity")
    recent = get_df("""
        SELECT u.name as Student, c.title as Course,
               r.marks, r.submitted_at
        FROM results r
        JOIN users u   ON r.student_id=u.id
        JOIN courses c ON r.course_id=c.id
        ORDER BY r.submitted_at DESC
        LIMIT 15
    """)
    if not recent.empty:
        recent["submitted_at"] = pd.to_datetime(recent["submitted_at"]).dt.strftime("%Y-%m-%d %H:%M")
        st.dataframe(recent, use_container_width=True, hide_index=True)


def render_admin_users():
    """Admin user management page"""
    st.markdown("## 👥 User Management")

    tab1, tab2, tab3 = st.tabs(["👨‍🎓 Students", "👨‍🏫 Teachers", "➕ Add User"])

    with tab1:
        students = get_df("""
            SELECT u.id, u.name, u.email, u.created_at,
                   COUNT(DISTINCT e.course_id) as Courses,
                   COUNT(DISTINCT r.id)        as Attempts
            FROM   users u
            LEFT JOIN enrollments e ON u.id=e.student_id
            LEFT JOIN results r     ON u.id=r.student_id
            WHERE  u.role='student'
            GROUP  BY u.id
            ORDER  BY u.id
        """)
        st.write(f"**Total Students: {len(students)}**")
        st.dataframe(students, use_container_width=True, hide_index=True)

        # Delete student
        del_sid = st.number_input("Student ID delete karein:", min_value=0, step=1, key="del_student")
        if st.button("🗑️ Delete Student") and del_sid:
            run_query("DELETE FROM users WHERE id=? AND role='student'", (del_sid,))
            st.success(f"Student {del_sid} delete ho gaya!")
            st.rerun()

    with tab2:
        teachers = get_df("""
            SELECT u.id, u.name, u.email, u.created_at,
                   COUNT(DISTINCT c.id) as Courses
            FROM   users u
            LEFT JOIN courses c ON u.id=c.teacher_id
            WHERE  u.role='teacher'
            GROUP  BY u.id
        """)
        st.dataframe(teachers, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("### Add New User")
        a_name  = st.text_input("Full Name")
        a_email = st.text_input("Email")
        a_pass  = st.text_input("Password", type="password")
        a_role  = st.selectbox("Role", ["student","teacher","admin"])
        if st.button("✅ Create User"):
            if all([a_name, a_email, a_pass]):
                if register_user(a_name, a_email, a_pass, a_role):
                    st.success(f"✅ User '{a_name}' create ho gaya!")
                else:
                    st.error("Email already registered hai!")
            else:
                st.error("Tamam fields required hain!")


def render_admin_courses():
    """Admin course management"""
    st.markdown("## 📚 Course Management")

    all_courses = get_df("""
        SELECT c.id, c.title, c.description, u.name as Teacher,
               COUNT(DISTINCT e.student_id) as Students,
               COUNT(DISTINCT l.id)         as Lectures,
               COUNT(DISTINCT q.id)         as Quizzes
        FROM   courses c
        LEFT JOIN users u        ON c.teacher_id=u.id
        LEFT JOIN enrollments e  ON c.id=e.course_id
        LEFT JOIN lectures l     ON c.id=l.course_id
        LEFT JOIN quizzes q      ON c.id=q.course_id
        GROUP BY c.id
    """)
    st.dataframe(all_courses, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Courses", len(all_courses))
    if not all_courses.empty:
        col2.metric("Total Enrollments", int(all_courses["Students"].sum()))
        col3.metric("Total Quizzes",     int(all_courses["Quizzes"].sum()))

    # Delete course
    del_cid = st.number_input("Course ID delete karein:", min_value=0, step=1)
    if st.button("🗑️ Delete Course") and del_cid:
        run_query("DELETE FROM courses WHERE id=?", (del_cid,))
        st.success(f"Course {del_cid} delete ho gaya!")
        st.rerun()


def render_admin_analytics():
    """Admin ke liye advanced analytics"""
    st.markdown("## 📊 System Analytics")

    # Overall pass/fail stats
    results = get_df("""
        SELECT u.name as Student,
               ROUND(SUM(r.marks)*100.0/NULLIF(SUM(q.marks),0),1) as Percentage
        FROM results r
        JOIN users u   ON r.student_id=u.id
        JOIN quizzes q ON r.quiz_id=q.id
        WHERE u.role='student'
        GROUP BY r.student_id
    """)

    if results.empty:
        st.info("Abhi koi data nahi hai.")
        return

    results["Grade"]  = results["Percentage"].apply(calculate_grade)
    results["Status"] = results["Percentage"].apply(lambda p: "Pass" if p>=50 else "Fail")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 System Average", f"{results['Percentage'].mean():.1f}%")
    col2.metric("✅ Pass Rate",
                f"{(results['Status']=='Pass').mean()*100:.1f}%")
    col3.metric("🏆 Top Score",  f"{results['Percentage'].max():.1f}%")
    col4.metric("📉 Lowest",     f"{results['Percentage'].min():.1f}%")

    # Grade distribution chart
    st.markdown("### 🎓 Grade Distribution (All Students)")
    grade_cnt = results["Grade"].value_counts().reindex(["A+","A","B","C","D","F"], fill_value=0)
    set_chart_style()
    fig, ax = plt.subplots(figsize=(8, 3))
    colors = ["#16a34a","#22c55e","#3b82f6","#f59e0b","#f97316","#ef4444"]
    ax.bar(grade_cnt.index, grade_cnt.values, color=colors, edgecolor="white", linewidth=1.5)
    for i, (g, v) in enumerate(zip(grade_cnt.index, grade_cnt.values)):
        ax.text(i, v + 0.5, str(v), ha="center", fontweight="bold")
    ax.set_xlabel("Grade")
    ax.set_ylabel("Number of Students")
    ax.set_title("Grade Distribution Across All Students")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Top performers
    st.markdown("### 🏆 Top 10 Performers")
    top10 = results.nlargest(10, "Percentage")[["Student","Percentage","Grade"]]
    st.dataframe(top10, use_container_width=True, hide_index=True)

    # Subjects requiring attention
    st.markdown("### ⚠️ Subjects Needing Attention")
    course_perf = get_df("""
        SELECT c.title as Course,
               COUNT(DISTINCT r.student_id)                               as Students,
               ROUND(AVG(r.marks*100.0/NULLIF(q.marks,0)),1)              as AvgScore
        FROM results r
        JOIN quizzes q ON r.quiz_id=q.id
        JOIN courses c ON r.course_id=c.id
        GROUP BY c.id
        ORDER BY AvgScore
    """)
    if not course_perf.empty:
        course_perf["Status"] = course_perf["AvgScore"].apply(
            lambda s: "⚠️ Needs Attention" if s<60 else "✅ On Track")
        st.dataframe(course_perf, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════
# SECTION 13: SIDEBAR NAVIGATION
# Sidebar mein navigation links
# ═══════════════════════════════════════════════════════════

def render_sidebar():
    """Sidebar navigation render karo based on user role"""
    user = st.session_state.get("user")
    if not user:
        return

    with st.sidebar:
        st.markdown(f"""
        <div class='logo-area'>
            <div style='font-size:2.5em;'>🎓</div>
            <div style='font-size:1.1em; font-weight:700; color:white;'>Smart LMS</div>
            <div style='font-size:0.75em; color:#a0aec0;'>AI-Powered Learning</div>
        </div>
        """, unsafe_allow_html=True)

        # User info
        role_icons = {"student": "👨‍🎓", "teacher": "👨‍🏫", "admin": "👨‍💼"}
        st.markdown(f"""
        <div style='padding:12px; margin:8px 0; background:rgba(255,255,255,0.08);
                    border-radius:8px; border-left:3px solid #533483;'>
            <div style='font-size:0.85em; color:#a0aec0;'>Logged in as</div>
            <div style='font-weight:700; color:white;'>
                {role_icons.get(user['role'],'👤')} {user['name']}
            </div>
            <div style='font-size:0.75em; color:#718096;'>{user['role'].capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Navigation based on role
        role = user["role"]

        if role == "student":
            pages = {
                "🏠 Dashboard":    "dashboard",
                "📚 My Courses":   "courses",
                "📝 Take Quiz":    "quiz",
                "📊 My Results":   "results",
            }
        elif role == "teacher":
            pages = {
                "🏠 Dashboard":     "dashboard",
                "📚 Courses":       "courses",
                "📝 Create Quiz":   "quiz",
                "👨‍🎓 Students":     "students",
            }
        else:  # admin
            pages = {
                "🏠 Dashboard":    "dashboard",
                "👥 Users":        "users",
                "📚 Courses":      "courses",
                "📊 Analytics":    "analytics",
            }

        current = st.session_state.get("page", "dashboard")
        for label, page_key in pages.items():
            active = current == page_key
            btn_style = "primary" if active else "secondary"
            if st.button(label, key=f"nav_{page_key}", use_container_width=True,
                         type=btn_style):
                st.session_state.page = page_key
                # Clear any sub-states
                if "view_lecture" in st.session_state:
                    del st.session_state.view_lecture
                st.rerun()

        st.markdown("---")

        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        # Footer
        st.markdown("""
        <div style='position:absolute; bottom:20px; left:0; right:0;
                    text-align:center; color:#4a5568; font-size:0.7em;'>
            Smart LMS v1.0 | FYP Project<br>
            Built with ❤️ using Streamlit
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# SECTION 14: MAIN APP ROUTER
# Sahi page ko render karo
# ═══════════════════════════════════════════════════════════

def main():
    """Main application entry point"""

    # ── Initialize database ────────────────────────────────
    init_database()
    seed_dummy_data()

    # ── Initialize session state ───────────────────────────
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    # ── Auth check ─────────────────────────────────────────
    if not st.session_state.user:
        render_auth_page()
        return

    # ── Render sidebar ────────────────────────────────────
    render_sidebar()

    # ── Route to correct page ─────────────────────────────
    user = st.session_state.user
    role = user["role"]
    page = st.session_state.get("page", "dashboard")

    # ── STUDENT ROUTES ────────────────────────────────────
    if role == "student":
        if   page == "dashboard": render_student_dashboard()
        elif page == "courses":   render_student_courses()
        elif page == "quiz":      render_student_quiz()
        elif page == "results":   render_student_results()
        else:                     render_student_dashboard()

    # ── TEACHER ROUTES ────────────────────────────────────
    elif role == "teacher":
        if   page == "dashboard": render_teacher_dashboard()
        elif page == "courses":   render_teacher_courses()
        elif page == "quiz":      render_teacher_quiz_creator()
        elif page == "students":  render_teacher_students()
        else:                     render_teacher_dashboard()

    # ── ADMIN ROUTES ──────────────────────────────────────
    elif role == "admin":
        if   page == "dashboard": render_admin_dashboard()
        elif page == "users":     render_admin_users()
        elif page == "courses":   render_admin_courses()
        elif page == "analytics": render_admin_analytics()
        else:                     render_admin_dashboard()


# ══════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
