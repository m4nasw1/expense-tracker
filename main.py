from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

# Load the trained model + vectorizer once, when the server starts
# (not on every request - that would be slow and wasteful)
model = joblib.load("category_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

@app.get("/")
def read_root():
    return {"message": "Expense tracker API is running"}

# Pydantic model: defines the "shape" of data this endpoint expects
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