import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Expense Tracker")
st.write("Track your expenses with automatic ML categorization")

st.header("Add a new expense")

with st.form("expense_form"):
    description = st.text_input("Description (e.g. 'Swiggy order')")
    amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
    submitted = st.form_submit_button("Add Expense")

    if submitted and description and amount > 0:
        response = requests.post(
            f"{API_URL}/expenses",
            json={"description": description, "amount": amount}
        )
        if response.status_code == 200:
            result = response.json()
            st.success(f"Added! Category: {result['category']} (confidence: {result['confidence']})")
        else:
            st.error("Something went wrong adding the expense.")

st.header("Your expenses")

expenses_response = requests.get(f"{API_URL}/expenses")
expenses = []
if expenses_response.status_code == 200:
    expenses = expenses_response.json()
    if expenses:
        st.dataframe(expenses, use_container_width=True)

        total = sum(e["amount"] for e in expenses)
        st.metric("Total spent", f"₹{total:.2f}")

        st.subheader("Spending by category")
        category_totals = {}
        for e in expenses:
            category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]

        st.bar_chart(category_totals)
    else:
        st.info("No expenses yet. Add one above!")
else:
    st.error("Could not fetch expenses.")

# ---- People management ----
st.header("People")

with st.form("person_form"):
    person_name = st.text_input("Friend's name")
    person_submitted = st.form_submit_button("Add Person")

    if person_submitted and person_name:
        response = requests.post(f"{API_URL}/people", json={"name": person_name})
        if response.status_code == 200:
            st.success(f"Added {person_name}!")
        else:
            st.error("Something went wrong adding this person.")

people_response = requests.get(f"{API_URL}/people")
people = []
if people_response.status_code == 200:
    people = people_response.json()
    if people:
        st.write("Current people:", ", ".join(p["name"] for p in people))
    else:
        st.info("No people added yet.")

# ---- Split an expense ----
st.header("Split an expense")

if expenses and people:
    expense_options = {f"#{e['id']} - {e['description']} (₹{e['amount']})": e["id"] for e in expenses}
    selected_expense_label = st.selectbox("Choose an expense to split", list(expense_options.keys()))
    selected_expense_id = expense_options[selected_expense_label]

    people_options = {p["name"]: p["id"] for p in people}
    selected_names = st.multiselect("Split between", list(people_options.keys()))

    if st.button("Split this expense"):
        if len(selected_names) < 2:
            st.warning("Pick at least 2 people to split between.")
        else:
            selected_ids = [people_options[name] for name in selected_names]
            response = requests.post(
                f"{API_URL}/expenses/{selected_expense_id}/split",
                json={"person_ids": selected_ids}
            )
            if response.status_code == 200:
                st.success(f"Split between {', '.join(selected_names)}!")
            else:
                st.error("Something went wrong splitting this expense.")
else:
    st.info("Add at least one expense and one person before splitting.")

# ---- Balances ----
st.header("Balances")

if people:
    balance_names = {p["name"]: p["id"] for p in people}
    selected_balance_name = st.selectbox("Check balance for", list(balance_names.keys()))
    selected_balance_id = balance_names[selected_balance_name]

    balance_response = requests.get(f"{API_URL}/people/{selected_balance_id}/balance")
    if balance_response.status_code == 200:
        balance_data = balance_response.json()
        st.metric(f"{balance_data['person']} owes", f"₹{balance_data['total_owed']:.2f}")
        if balance_data["breakdown"]:
            st.write("Breakdown:")
            st.dataframe(balance_data["breakdown"], use_container_width=True)
    else:
        st.error("Could not fetch balance.")
else:
    st.info("Add people first to see balances.")