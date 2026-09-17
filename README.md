# Expense Tracker

A Splitwise-style expense tracker that automatically categorizes expenses using a trained ML model, with real persistence and expense splitting between friends.

## Why I Built This

I wanted a project that went beyond a single Kaggle notebook — something that shows the full loop of shipping a model: building a dataset, training and evaluating it, and then actually serving it through a real API, database, and frontend. Expense categorization was a good fit because it's a genuine text classification problem with real ambiguity.

## Features

- Type a description like "Swiggy order" and get an automatically predicted category — no manual selection needed
- Expenses persist in a real SQLite database
- Add friends and split any expense between them
- Dashboard with totals, category breakdown chart, and full expense history
- Custom-designed frontend

## Tech Stack

- **ML:** scikit-learn (TF-IDF + Logistic Regression)
- **Backend:** FastAPI
- **Database:** SQLite + SQLAlchemy
- **Frontend:** Streamlit

## Architecture

```
User types expense description
        ↓
Streamlit frontend (app.py)
        ↓  HTTP request
FastAPI backend (main.py)
        ↓
TF-IDF vectorizer + Logistic Regression model (category_model.pkl)
        ↓
Predicted category + confidence score
        ↓
Saved to SQLite database (expenses.db) via SQLAlchemy models
        ↓
Retrieved and displayed back in the dashboard
```

Splitting works through a **junction table** (`Split`) connecting `Expense` and `Person` — each row represents one fact: "this person owes this much for this expense," correctly modeling the many-to-many relationship between expenses and people.

## The ML Part

**Dataset:** built synthetically (since real personal expense data isn't publicly available), combining template-based examples with hand-written natural-language sentences upto ~900 rows across 6 categories.

**First evaluation was misleading.** An initial test split scored ~99–100% accuracy was a red flag. The test set was too similar to training data, so the model was memorizing, not generalizing.

**Built an holdout set:** 20 genuinely novel examples, written to differ from anything in training, and deliberately never used to patch the training data afterward.

**Real results on the honest holdout:**
| Model | Accuracy |
|---|---|
| Naive Bayes | 65% |
| Logistic Regression (shipped) | **70%** |

With 6 classes, random guessing is ~17%, so this reflects learned signal while being honest that it's far from perfect for a project built in days on synthetic data.

**Confidence calibration was tested** Checked whether the model's confidence scores actually correlated with correctness — found only a weak correlation. "Flag low-confidence predictions for review" is a reasonable soft signal here, not a reliable hard filter.

**What would improve this further:** a feedback loop — logging user corrections when a prediction is wrong, and periodically retraining on that real data — would matter far more than further synthetic data tuning.

## Setup

```bash
git clone https://github.com/m4nasw1/expense-tracker.git
cd expense-tracker

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install fastapi uvicorn sqlalchemy python-multipart joblib scikit-learn streamlit requests

# terminal 1
uvicorn main:app --reload

# terminal 2
streamlit run app.py
```

Backend: `http://127.0.0.1:8000` (docs at `/docs`) · Frontend: `http://localhost:8501`

## Project Structure

```
expense-tracker-ml/
├── generate_dataset.py      # synthetic training data generator
├── holdout_test.py          # honest, never-patched evaluation set
├── model_training.ipynb     # model training, evaluation, comparison
├── category_model.pkl       # trained Logistic Regression model
├── tfidf_vectorizer.pkl     # fitted TF-IDF vectorizer
├── database.py              # SQLAlchemy engine/session setup
├── models.py                # Expense, Person, Split table definitions
├── main.py                  # FastAPI app and all endpoints
├── app.py                   # Streamlit frontend
└── .streamlit/config.toml   # theme configuration
```