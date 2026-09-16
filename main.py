from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import joblib

from database import engine, SessionLocal, Base
from models import Expense, Person, Split

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

class PersonCreate(BaseModel):
    name: str

@app.post("/people")
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    db_person = Person(name=person.name)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.get("/people")
def get_people(db: Session = Depends(get_db)):
    return db.query(Person).all()

class SplitRequest(BaseModel):
    person_ids: list[int]  # who is splitting this expense

@app.post("/expenses/{expense_id}/split")
def split_expense(expense_id: int, split_request: SplitRequest, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        return {"error": "Expense not found"}

    num_people = len(split_request.person_ids)
    share = round(expense.amount / num_people, 2)

    created_splits = []
    for person_id in split_request.person_ids:
        db_split = Split(
            expense_id=expense.id,
            person_id=person_id,
            amount_owed=share
        )
        db.add(db_split)
        created_splits.append(db_split)

    db.commit()
    for s in created_splits:
        db.refresh(s)

    return created_splits

@app.get("/people/{person_id}/balance")
def get_person_balance(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        return {"error": "Person not found"}

    splits = db.query(Split).filter(Split.person_id == person_id).all()
    total_owed = sum(s.amount_owed for s in splits)

    return {
        "person": person.name,
        "total_owed": round(total_owed, 2),
        "breakdown": [
            {"expense_id": s.expense_id, "amount": s.amount_owed}
            for s in splits
        ]
    }