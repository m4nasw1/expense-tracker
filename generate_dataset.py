"""
Generates a synthetic (description -> category) dataset for training
the expense auto-categorization model.

Why synthetic data? Real personal expense data is private and hard to
source publicly. We simulate realistic merchant/description patterns
instead, which is a common bootstrapping strategy for this kind of problem.
"""

import pandas as pd
import random

random.seed(42)  # reproducibility - good habit to mention in interviews

# ---- Base vocabulary per category ----
# Mix of real merchant names + generic phrasing + casual/short forms,
# so the model learns patterns, not just exact strings.

CATEGORY_DATA = {
    "Food": {
        "merchants": ["Swiggy", "Zomato", "McDonald's", "Domino's Pizza", "Starbucks",
                      "KFC", "Cafe Coffee Day", "Local restaurant", "Pizza Hut", "Subway",
                      "Biryani place", "Street food stall", "Bakery", "Ice cream shop"],
        "templates": [
            "{merchant} order", "Lunch at {merchant}", "Dinner - {merchant}",
            "{merchant} delivery", "Food order from {merchant}", "Coffee at {merchant}",
            "{merchant} payment", "Snacks - {merchant}", "Breakfast {merchant}",
            "{merchant}", "Ordered food via {merchant}"
        ],
        "hard_examples": [
            "paid for biryani at new restaurant", "grabbed a quick bite downtown",
            "ordered biryani via a food app", "split a pizza with roommates",
            "bought groceries for the week", "vegetables from the local market",
            "milk and bread from the corner store", "weekend brunch with family"
        ]
    },
    "Transport": {
        "merchants": ["Uber", "Ola", "Rapido", "Metro card recharge", "IndianOil petrol pump",
                      "Shell petrol pump", "Bus ticket", "Train ticket - IRCTC", "Parking fee",
                      "BluSmart", "Fastag", "Toll plaza", "Auto rickshaw"],
        "templates": [
            "{merchant} ride", "{merchant} trip", "Cab - {merchant}", "{merchant}",
            "Fuel - {merchant}", "{merchant} recharge", "{merchant} booking",
            "Travel - {merchant}", "{merchant} fare"
        ],
        "hard_examples": [
            "recharged fastag for toll", "grabbed a cab to airport", "paid toll on highway",
            "filled petrol tank on the way home", "monthly parking pass renewal",
            "flight ticket booking for work trip", "auto fare to the station",
            "car service and oil change"
        ]
    },
    "Shopping": {
        "merchants": ["Amazon", "Flipkart", "Myntra", "Zara", "H&M", "Decathlon",
                      "Local mall purchase", "Reliance Trends", "Nike store", "Ajio",
                      "Electronics store", "Furniture shop"],
        "templates": [
            "{merchant} order", "Purchase from {merchant}", "{merchant} shopping",
            "Bought clothes - {merchant}", "{merchant}", "Online order - {merchant}",
            "{merchant} purchase", "Shoes from {merchant}"
        ],
        "hard_examples": [
            "bought a birthday gift for mom", "new phone case online", "shoes for the trek",
            "home decor items for the living room", "bought a laptop bag",
            "new headphones from an online store", "festive season shopping spree"
        ]
    },
    "Bills": {
        "merchants": ["Electricity board", "Airtel postpaid", "Jio recharge", "Wifi bill - ACT",
                      "Water bill", "Gas cylinder booking", "Netflix subscription",
                      "Spotify subscription", "House rent", "Maintenance fee", "Insurance premium"],
        "templates": [
            "{merchant} payment", "{merchant}", "Monthly {merchant}", "{merchant} bill paid",
            "Paid {merchant}", "{merchant} due", "{merchant} auto-debit"
        ],
        "hard_examples": [
            "electricity board late payment", "monthly gym membership fee",
            "annual insurance premium payment", "broadband internet renewal",
            "society maintenance for the month", "credit card bill payment",
            "mobile recharge for the month", "streaming service auto-renewal"
        ]
    },
    "Entertainment": {
        "merchants": ["PVR Cinemas", "INOX", "BookMyShow", "Concert tickets", "Gaming - Steam",
                      "PlayStation Store", "Bowling alley", "Amusement park", "Club entry"],
        "templates": [
            "{merchant} tickets", "{merchant}", "Movie - {merchant}", "{merchant} booking",
            "Night out - {merchant}", "{merchant} purchase", "Tickets via {merchant}"
        ],
        "hard_examples": [
            "watched a movie with friends", "weekend concert tickets", "arcade night out",
            "stand-up comedy show tickets", "video game purchase on sale",
            "amusement park entry tickets", "karaoke night with friends"
        ]
    },
    "Other": {
        "merchants": ["ATM withdrawal", "Bank transfer", "Gift to friend", "Donation",
                      "Medical store", "Pharmacy", "Stationery shop", "Haircut - salon",
                      "Miscellaneous", "Cash withdrawal"],
        "templates": [
            "{merchant}", "{merchant} payment", "Paid for {merchant}", "{merchant} expense",
            "Sent money - {merchant}"
        ],
        "hard_examples": [
            "medicine from the pharmacy", "donated to a charity fund", "paid the doctor's fee",
            "sent money to a friend", "haircut at the salon", "school fees for sibling",
            "lost and had to pay a late fine"
        ]
    }
}

def generate_examples(n_per_category=150):
    rows = []
    for category, data in CATEGORY_DATA.items():
        # 1. Templated examples (merchant + template combinations)
        for _ in range(n_per_category):
            merchant = random.choice(data["merchants"])
            template = random.choice(data["templates"])
            desc = template.format(merchant=merchant)

            # add some casing/typo variety so model doesn't overfit to exact casing
            r = random.random()
            if r < 0.15:
                desc = desc.lower()
            elif r < 0.25:
                desc = desc.upper()

            rows.append({"description": desc, "category": category})

        # 2. Hand-written natural-language examples, repeated with slight
        # case variation so they carry meaningful weight in training too,
        # without just being a single rare occurrence each.
        for hard_desc in data["hard_examples"]:
            for _ in range(4):
                desc = hard_desc
                r = random.random()
                if r < 0.2:
                    desc = desc.capitalize()
                rows.append({"description": desc, "category": category})

    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate_examples(n_per_category=120)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle
    df.to_csv("expenses_dataset.csv", index=False)
    print(f"Generated {len(df)} rows")
    print(df["category"].value_counts())
    print("\nSample rows:")
    print(df.head(10))