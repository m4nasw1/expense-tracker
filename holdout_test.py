"""
HONEST holdout test set.

Rule: no matter what fails here, we do NOT add similar examples to
generate_dataset.py to "fix" it. This file exists to give us a truthful
read on generalization. If the model does poorly here, the fix is either
(a) genuinely better/more diverse training data added for good reason,
not just to patch this specific list, or (b) accepting the limitation
and building the confidence-threshold/correction-loop system around it.
"""

HOLDOUT_EXAMPLES = [
    # Food - unusual phrasing, no obvious merchant name
    ("split the dinner bill with coworkers", "Food"),
    ("bought some fruit from a vendor", "Food"),
    ("late night snack run", "Food"),
    ("caterer for a small get-together", "Food"),

    # Transport - regional/slang terms, no direct keyword overlap with training
    ("shared auto to college", "Transport"),
    ("booked a self-drive car for the weekend", "Transport"),
    ("bike service at the garage", "Transport"),
    ("air ticket refund minus cancellation fee", "Transport"),

    # Shopping
    ("new curtains for the bedroom", "Shopping"),
    ("bought a watch as a treat for myself", "Shopping"),
    ("replaced a broken phone screen", "Shopping"),

    # Bills
    ("landlord asked for the deposit top-up", "Bills"),
    ("annual domain renewal for a side project", "Bills"),
    ("cable TV package renewal", "Bills"),

    # Entertainment
    ("theme park season pass", "Entertainment"),
    ("paid for a friend's game night entry", "Entertainment"),
    ("live music show downtown", "Entertainment"),

    # Other
    ("vet visit for the dog", "Other"),
    ("paid a fine for late library return", "Other"),
    ("contributed to a wedding gift pool", "Other"),
]

if __name__ == "__main__":
    for text, label in HOLDOUT_EXAMPLES:
        print(f"{text:50s} -> (expected: {label})")
    print(f"\nTotal holdout examples: {len(HOLDOUT_EXAMPLES)}")