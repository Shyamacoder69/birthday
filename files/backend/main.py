from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI(title="National Birthday Aptitude Test API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Data models ───────────────────────────────────────────────────────────────

class AnswerSubmission(BaseModel):
    level: str
    answer: str
    session_id: Optional[str] = "default"

class ProgressUpdate(BaseModel):
    session_id: Optional[str] = "default"
    completed_levels: list[str] = []
    achievements: list[str] = []
    score: int = 0

# ── In-memory game data ───────────────────────────────────────────────────────

QUESTIONS = {
    "physics": {
        "mission": "MISSION 1 : PHYSICS",
        "preamble": "For the sake of this question,\nassume Modiji's development is constant.",
        "question": (
            "A stone is thrown vertically upward with an initial velocity of 20 m/s.\n\n"
            "Ignoring air resistance, corruption, and Twitter arguments,\n\n"
            "find the maximum height attained by the stone.\n\n"
            "Take g = 10 m/s²."
        ),
        "options": {"A": "5 m", "B": "10 m", "C": "20 m", "D": "40 m"},
        "correct": "C",
        "hints": [
            "Use kinematics.",
            "At the highest point, velocity becomes zero.",
            "Even development cannot defeat gravity.",
        ],
        "wrong_responses": [
            "Newton is disappointed.",
            "Gravity still works.",
            "Please consult Einstein.",
        ],
        "correct_response": "Excellent. Newton and Modiji are proud of you.",
        "achievement": "Physics Survivor",
    },
    "maths": {
        "mission": "MISSION 2 : MATHEMATICS",
        "preamble": "Assume Modiji's development follows a perfectly linear function.",
        "question": (
            "If f(x) = 2x + 16\n\n"
            "and the nation demands f(x) = 56,\n\n"
            "find x."
        ),
        "options": {"A": "10", "B": "20", "C": "30", "D": "40"},
        "correct": "B",
        "hints": [
            "Subtract before dividing.",
            "Development may be linear.",
            "Trust mathematics.",
        ],
        "wrong_responses": [
            "Euler refuses to comment.",
            "Arithmetic has left the chat.",
            "Even calculators need help.",
        ],
        "correct_response": "Mathematics approves.",
        "achievement": "Math Wizard",
    },
    "ml": {
        "mission": "MISSION 3 : MACHINE LEARNING",
        "preamble": (
            "A state-of-the-art AI model is trained to predict whether someone secretly loves Modiji.\n\n"
            "Features: Favourite colour, Favourite food, Sleep schedule, "
            "Number of memes shared, Browser history.\n\n"
            "Target: Modiji Fan = Yes or No."
        ),
        "question": "Which algorithm is most appropriate for this binary classification problem?",
        "options": {
            "A": "Linear Regression",
            "B": "Logistic Regression",
            "C": "K-Means",
            "D": "PCA",
        },
        "correct": "B",
        "hints": [
            "The output has only two classes.",
            "Think classification.",
            "Sigmoid is your friend.",
        ],
        "wrong_responses": [
            "Gradient descent diverged.",
            "Model overfitted.",
            "Validation accuracy: 0%.",
        ],
        "correct_response": "The AI approves.",
        "achievement": "Machine Learning Engineer",
    },
}

ACHIEVEMENTS_META = {
    "Physics Survivor":        {"emoji": "🏆", "desc": "Survived Newton's wrath"},
    "Math Wizard":             {"emoji": "🏆", "desc": "Euler nods in approval"},
    "Machine Learning Engineer": {"emoji": "🏆", "desc": "Model converged"},
    "National Asset":          {"emoji": "🏆", "desc": "AI-verified Modiji fan"},
    "Rickrolled":              {"emoji": "🏆", "desc": "Never gonna give you up"},
    "Birthday Boy":            {"emoji": "🎂", "desc": "Survived another year of engineering"},
}

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "message": "National Birthday Aptitude Test API",
        "status": "Candidate detected. Age verification pending.",
        "version": "1.0.0",
    }


@app.get("/question/{level}")
def get_question(level: str):
    if level not in QUESTIONS:
        raise HTTPException(status_code=404, detail=f"Level '{level}' not found.")
    q = QUESTIONS[level]
    return {
        "level": level,
        "mission": q["mission"],
        "preamble": q["preamble"],
        "question": q["question"],
        "options": q["options"],
        "hints": q["hints"],
        "achievement": q["achievement"],
    }


@app.post("/submit")
def submit_answer(submission: AnswerSubmission):
    level = submission.level.lower()
    if level not in QUESTIONS:
        raise HTTPException(status_code=404, detail=f"Level '{level}' not found.")

    q = QUESTIONS[level]
    is_correct = submission.answer.upper() == q["correct"]

    if is_correct:
        return {
            "correct": True,
            "message": q["correct_response"],
            "achievement": q["achievement"],
            "score_delta": 100,
        }
    else:
        return {
            "correct": False,
            "message": random.choice(q["wrong_responses"]),
            "achievement": None,
            "score_delta": 0,
        }


@app.get("/progress")
def get_progress():
    return {
        "levels": list(QUESTIONS.keys()),
        "total_levels": len(QUESTIONS),
        "achievements_available": list(ACHIEVEMENTS_META.keys()),
    }


@app.get("/stats")
def get_stats():
    return {
        "total_questions": len(QUESTIONS),
        "max_score": len(QUESTIONS) * 100,
        "achievements_total": len(ACHIEVEMENTS_META),
        "difficulty": "JEE-level (Modiji edition)",
    }


@app.get("/final_result")
def final_result():
    return {
        "status": "MISSION COMPLETE",
        "results": {
            "Physics": "PASSED",
            "Maths": "PASSED",
            "Machine Learning": "PASSED",
            "AI Verification": "PASSED",
        },
        "stats": {
            "Friendship": "∞",
            "Modiji Loyalty": "100%",
            "Age": "+1",
        },
        "message": (
            "Happy Birthday!\n\n"
            "Thanks for being an amazing friend.\n\n"
            "May your code compile.\n"
            "May your exams be easy.\n"
            "May your bugs disappear.\n"
            "And may you survive another year of engineering.\n\n"
            "❤️"
        ),
        "final_achievement": "Birthday Boy",
    }


@app.get("/rickroll")
def rickroll():
    return {
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1",
        "message": "Congratulations. You have successfully been Rickrolled.",
        "achievement": "Rickrolled",
    }


@app.get("/achievements")
def get_achievements():
    return {
        "achievements": [
            {"name": k, "emoji": v["emoji"], "description": v["desc"]}
            for k, v in ACHIEVEMENTS_META.items()
        ]
    }
