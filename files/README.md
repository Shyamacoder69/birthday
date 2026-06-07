# 🎂 National Birthday Aptitude Test

> A JEE-meets-escape-room-meets-meme-page birthday experience.

---

## Project Structure

```
birthday_app/
├── backend/
│   └── main.py          # FastAPI backend
├── frontend/
│   ├── app.py           # Streamlit frontend
│   └── assets/          # Drop your photos here
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI backend

```bash
cd birthday_app
uvicorn backend.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000  
API docs at: http://localhost:8000/docs

### 3. Start the Streamlit frontend (new terminal)

```bash
cd birthday_app
streamlit run frontend/app.py --server.port 8501
```

Frontend runs at: http://localhost:8501

---

## Adding Photos

Place your friend group photos in `frontend/assets/`:

```
frontend/assets/
├── photo1.jpg
├── photo2.jpg
└── group.jpg
```

Then update the gallery section in `frontend/app.py` to use `st.image()` with the local paths.

---

## Game Flow

```
Home → Physics → Maths → ML → AI Verification
     → Gallery → Poster → Gift → Rickroll → Final
```

Progress is saved in Streamlit session state. Users cannot skip missions.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/question/{level}` | Get question for level (physics/maths/ml) |
| POST | `/submit` | Submit answer, get result |
| GET | `/progress` | Available levels & achievements |
| GET | `/stats` | Game stats |
| GET | `/final_result` | Final mission complete data |
| GET | `/rickroll` | Rickroll endpoint |
| GET | `/achievements` | All achievements list |

---

## Achievements

| Achievement | How to earn |
|-------------|-------------|
| 🏆 Physics Survivor | Answer the physics question correctly |
| 🏆 Math Wizard | Answer the maths question correctly |
| 🏆 Machine Learning Engineer | Answer the ML question correctly |
| 🏆 National Asset | Complete AI verification |
| 🏆 Rickrolled | Open the birthday gift |
| 🎂 Birthday Boy | Complete the full journey |

---

## Deployment

### Option A: Local Network (share with friends)

```bash
streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Share your local IP: `http://YOUR_IP:8501`

### Option B: Cloud (Streamlit Community Cloud)

1. Push to GitHub
2. Go to share.streamlit.io
3. Deploy `frontend/app.py`
4. Deploy backend separately on Railway/Render
5. Update `API_BASE` in `frontend/app.py`

### Option C: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000 8501
CMD uvicorn backend.main:app --port 8000 & streamlit run frontend/app.py --server.port 8501
```

---

## Customisation

- **Birthday boy's name**: Search `app.py` for "Birthday" and update messages
- **Friend photos**: Replace placeholder divs in `page_gallery()` with `st.image()`  
- **Inside jokes**: Edit captions in the `captions` list in `page_gallery()`
- **Modi image**: Replace the Wikipedia URL in `page_ai_verification()` with any image URL

---

## Tech Stack

- **Backend**: FastAPI + Pydantic + Uvicorn
- **Frontend**: Streamlit + Custom CSS
- **Fonts**: Orbitron, Share Tech Mono, Rajdhani (Google Fonts)
- **State**: Streamlit session state

---

*Failure is acceptable. Disappointment is not.* 🎂
