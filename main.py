from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import joblib

from database import engine, SessionLocal, Base
from models import Expense

# Create the actual database tables (if they don't already exist)
Base.metadata.create_all(bind=engine)

app = FastAPI()

model = joblib.load("category_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Dependency: gives each request its own database session, and
# guarantees it's closed afterward, even if an error happens
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Expense tracker API is running"}

class ExpenseInput(BaseModel):
    description: str

@app.post("/predict-category")
def predict_category(expense: ExpenseInput):
    text_vec = vectorizer.transform([expense.description])
    prediction = model.predict(text_vec)[0]
    probabilities = model.predict_proba(text_vec)[0]
    confidence = float(max(probabilities))
    return {
        "description": expense.description,
        "predicted_category": prediction,
        "confidence": round(confidence, 2)
    }

# New: input shape for creating an actual saved expense
class ExpenseCreate(BaseModel):
    description: str
    amount: float

@app.post("/expenses")
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    # Reuse the same ML logic to auto-predict the category
    text_vec = vectorizer.transform([expense.description])
    prediction = model.predict(text_vec)[0]
    probabilities = model.predict_proba(text_vec)[0]
    confidence = float(max(probabilities))

    db_expense = Expense(
        description=expense.description,
        amount=expense.amount,
        category=prediction,
        confidence=round(confidence, 2)
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()