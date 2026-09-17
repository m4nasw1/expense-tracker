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

response = requests.get(f"{API_URL}/expenses")
if response.status_code == 200:
    expenses = response.json()
    if expenses:
        st.dataframe(expenses, use_container_width=True)

        total = sum(e["amount"] for e in expenses)
        st.metric("Total spent", f"₹{total:.2f}")
    else:
        st.info("No expenses yet. Add one above!")
else:
    st.error("Could not fetch expenses.")