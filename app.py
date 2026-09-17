import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# ---- Warm Light Theme Styling ----
st.markdown("""
<style>
    /* Direct @font-face declarations for reliable font loading */
    @font-face {
        font-family: 'DM Sans';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/dmsans/v17/rP2Yp2ywxg089UriI5-g4vlH9VoD8Cmcqbu0-K6z9mXg.woff2) format('woff2');
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }
    @font-face {
        font-family: 'DM Sans';
        font-style: normal;
        font-weight: 500;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/dmsans/v17/rP2Yp2ywxg089UriI5-g4vlH9VoD8Cmcqbu0-K6z9mXg.woff2) format('woff2');
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }
    @font-face {
        font-family: 'DM Sans';
        font-style: normal;
        font-weight: 600;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/dmsans/v17/rP2Yp2ywxg089UriI5-g4vlH9VoD8Cmcqbu0-K6z9mXg.woff2) format('woff2');
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }
    @font-face {
        font-family: 'DM Sans';
        font-style: normal;
        font-weight: 700;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/dmsans/v17/rP2Yp2ywxg089UriI5-g4vlH9VoD8Cmcqbu0-K6z9mXg.woff2) format('woff2');
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }
    @font-face {
        font-family: 'DM Serif Display';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/dmserifdisplay/v17/-nFnOHM81r4j6k0gjAW3mujVU2B2G_Bx0vrx52g.woff2) format('woff2');
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }
    /* Global base typography */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #20201E !important;
    }

    .stApp {
        background-color: #F5F3EE !important;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3.5rem;
        max-width: 980px;
    }

    /* Headings with DM Serif Display */
    h1, h1 *, h2, h2 *, h3, h3 *,
    h1 [class*="st-"], h2 [class*="st-"], h3 [class*="st-"],
    span[data-heading-text],
    .serif-heading, .serif-heading * {
        font-family: 'DM Serif Display', Georgia, serif !important;
        font-weight: 400 !important;
        color: #20201E !important;
        letter-spacing: -0.4px !important;
    }

    h1, h1 *, h1 [class*="st-"] {
        font-size: 2.6rem !important;
        margin-bottom: 0.15rem !important;
        line-height: 1.15 !important;
    }

    h2, h2 *, h2 [class*="st-"] {
        font-size: 1.55rem !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0.75rem !important;
    }

    h3, h3 *, h3 [class*="st-"] {
        font-size: 1.25rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.6rem !important;
    }

    [data-testid="stCaptionContainer"] {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1.05rem !important;
        color: #6A6965 !important;
        margin-bottom: 1.5rem !important;
    }

    /* Forms */
    div[data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2DFD7 !important;
        border-radius: 16px !important;
        padding: 24px 28px !important;
        box-shadow: 0 2px 10px rgba(32, 32, 30, 0.03) !important;
    }

    /* Form Inputs */
    .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {
        background-color: #FAFAFA !important;
        border: 1px solid #D2CDC2 !important;
        border-radius: 9px !important;
        color: #20201E !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #315C4A !important;
        box-shadow: 0 0 0 2px rgba(49, 92, 74, 0.15) !important;
    }

    /* Buttons */
    .stButton button, .stFormSubmitButton button {
        background-color: #315C4A !important;
        color: #FFFFFF !important;
        border: 1px solid #315C4A !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        padding: 10px 22px !important;
        box-shadow: 0 2px 6px rgba(49, 92, 74, 0.2) !important;
        transition: all 0.15s ease-in-out !important;
    }

    .stButton button:hover, .stFormSubmitButton button:hover {
        background-color: #27493A !important;
        border-color: #27493A !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(49, 92, 74, 0.28) !important;
        color: #FFFFFF !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        border-bottom: 1px solid #E2DFD7 !important;
        padding-bottom: 2px !important;
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 9px !important;
        padding: 10px 18px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        color: #6A6965 !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.15s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #EAE6DF !important;
        color: #20201E !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #DCE5DD !important;
        color: #315C4A !important;
    }

    /* Standard Metric styling */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2DFD7 !important;
        border-left: 4px solid #315C4A !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        box-shadow: 0 2px 8px rgba(32, 32, 30, 0.04) !important;
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        font-weight: 600 !important;
        color: #6A6965 !important;
    }

    div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] * {
        font-family: 'DM Serif Display', Georgia, serif !important;
        font-size: 2.2rem !important;
        font-weight: 400 !important;
        color: #20201E !important;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #E2DFD7 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(32, 32, 30, 0.02) !important;
    }

    /* Alert boxes */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        font-family: 'DM Sans', sans-serif !important;
        border: 1px solid #E2DFD7 !important;
        background-color: #FFFFFF !important;
    }

    hr {
        border-color: #E2DFD7 !important;
        margin: 1.5rem 0 !important;
    }

    /* Custom Dashboard Card */
    .stat-card {
        background-color: #FFFFFF;
        border: 1px solid #E2DFD7;
        border-left: 4px solid #315C4A;
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 2px 8px rgba(32, 32, 30, 0.03);
        margin-bottom: 0.75rem;
    }

    .stat-card.debt {
        border-left-color: #B84C3A;
    }

    .stat-card-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #6A6965;
        margin-bottom: 6px;
    }

    .stat-card-value {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 2.3rem;
        font-weight: 400;
        color: #20201E;
        line-height: 1.1;
        margin-bottom: 4px;
    }

    .stat-card-value.income {
        color: #315C4A;
    }

    .stat-card-value.debt {
        color: #B84C3A;
    }

    .stat-card-sub {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        color: #8C8B85;
    }

    /* Person Chips */
    .chips-wrap {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 8px;
        margin-top: 10px;
    }

    .person-chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #DCE5DD;
        color: #315C4A;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid #C9D6CB;
    }

    .person-chip-avatar {
        width: 20px;
        height: 20px;
        background-color: #315C4A;
        color: #FFFFFF;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.72rem;
        font-weight: 700;
    }

    /* Split Calculation Box */
    .split-calc-box {
        background-color: #FFFFFF;
        border: 1px solid #DCE5DD;
        border-radius: 12px;
        padding: 14px 18px;
        margin: 12px 0 16px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
        box-shadow: 0 1px 4px rgba(32, 32, 30, 0.02);
    }

    .split-calc-item {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.92rem;
        color: #5C5B56;
    }

    .split-calc-highlight {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 1.4rem;
        color: #315C4A;
    }

    /* Warm Empty States */
    .empty-card {
        background-color: #FFFFFF;
        border: 1px dashed #D2CDC2;
        border-radius: 16px;
        padding: 38px 24px;
        text-align: center;
        margin: 20px 0;
    }

    .empty-card-icon {
        font-size: 2.2rem;
        margin-bottom: 8px;
    }

    .empty-card-title {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 1.25rem;
        color: #20201E;
        margin-bottom: 4px;
    }

    .empty-card-text {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: #6A6965;
        max-width: 380px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# ---- Reusable Helpers ----
def render_empty_state(icon: str, title: str, text: str):
    st.markdown(f"""
    <div class="empty-card">
        <div class="empty-card-icon">{icon}</div>
        <div class="empty-card-title">{title}</div>
        <div class="empty-card-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)

def prepare_expense_df(data):
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"])
    if "confidence" in df.columns:
        # Convert float ratio (e.g. 0.64) to integer 0-100 for progress column
        df["confidence"] = (df["confidence"] * 100).round()
    return df

# Shared column configuration for expenses tables
EXPENSE_TABLE_CONFIG = {
    "id": st.column_config.NumberColumn("ID", width="small"),
    "description": st.column_config.TextColumn("Description"),
    "amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
    "category": st.column_config.TextColumn("Category"),
    "confidence": st.column_config.ProgressColumn(
        "ML Confidence", min_value=0, max_value=100, format="%d%%"
    ),
    "created_at": st.column_config.DatetimeColumn("Date", format="D MMM YYYY, h:mm a"),
}

# ---- Page Header ----
st.title("💰 Expense Tracker")
st.caption("Track your spending, split with friends.")

# Fetch shared data once, used across tabs
expenses_response = requests.get(f"{API_URL}/expenses")
expenses = expenses_response.json() if expenses_response.status_code == 200 else []

people_response = requests.get(f"{API_URL}/people")
people = people_response.json() if people_response.status_code == 200 else []

tab_add, tab_dashboard, tab_split, tab_balances = st.tabs(
    ["➕ Add Expense", "📊 Dashboard", "🧾 Split", "⚖️ Balances"]
)

# ---- Tab 1: Add Expense ----
with tab_add:
    st.subheader("Add a new expense")
    with st.form("expense_form"):
        description = st.text_input("Description", placeholder="e.g. Swiggy dinner, Uber ride, Groceries")
        amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
        submitted = st.form_submit_button("Add Expense", use_container_width=True)

        if submitted and description and amount > 0:
            response = requests.post(
                f"{API_URL}/expenses",
                json={"description": description, "amount": amount}
            )
            if response.status_code == 200:
                result = response.json()
                st.session_state["last_added"] = result
                st.rerun()
            else:
                st.error("Something went wrong adding the expense.")

    if "last_added" in st.session_state:
        last = st.session_state.pop("last_added")
        st.markdown(f"""
        <div style="background-color: #DCE5DD; border: 1px solid #C9D6CB; border-radius: 12px; padding: 14px 18px; margin: 14px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
            <div>
                <span style="font-weight: 600; color: #315C4A;">Expense Added:</span>
                <span style="color: #20201E; margin-left: 6px;">{last.get('description', '')} (₹{last.get('amount', 0):.2f})</span>
            </div>
            <div>
                <span style="background-color: #315C4A; color: #FFFFFF; font-size: 0.82rem; font-weight: 600; padding: 4px 12px; border-radius: 12px; margin-right: 6px;">
                    {last.get('category', 'Uncategorized')}
                </span>
                <span style="color: #5C5B56; font-size: 0.85rem; font-weight: 500;">
                    {int(last.get('confidence', 0) * 100)}% confidence
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if expenses:
        st.subheader("Recent expenses")
        df_recent = prepare_expense_df(expenses[-5:][::-1])
        st.dataframe(
            df_recent,
            column_config=EXPENSE_TABLE_CONFIG,
            use_container_width=True,
            hide_index=True
        )
    else:
        render_empty_state(
            icon="💳",
            title="No Expenses Logged Yet",
            text="Enter a description and amount above to record your first expense with automatic ML categorization."
        )

# ---- Tab 2: Dashboard ----
with tab_dashboard:
    if expenses:
        col1, col2 = st.columns(2)
        total = sum(e["amount"] for e in expenses)

        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-label">Total Spent</div>
                <div class="stat-card-value income">₹{total:.2f}</div>
                <div class="stat-card-sub">Sum of all recorded transactions</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-label">Number of Expenses</div>
                <div class="stat-card-value">{len(expenses)}</div>
                <div class="stat-card-sub">Total entries in ledger</div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("Spending by category")
        category_totals = {}
        for e in expenses:
            category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]
        st.bar_chart(category_totals, color="#315C4A")

        st.subheader("All expenses")
        df_all = prepare_expense_df(expenses)
        st.dataframe(
            df_all,
            column_config=EXPENSE_TABLE_CONFIG,
            use_container_width=True,
            hide_index=True
        )
    else:
        render_empty_state(
            icon="📊",
            title="No Data Available for Dashboard",
            text="Add expenses in the first tab to view financial metrics, charts, and transaction history."
        )

# ---- Tab 3: Split ----
with tab_split:
    st.subheader("Add a group member")
    with st.form("person_form"):
        person_name = st.text_input("Friend's name", placeholder="e.g. Alice, Bob, Riya")
        person_submitted = st.form_submit_button("Add Member", use_container_width=True)
        if person_submitted and person_name:
            response = requests.post(f"{API_URL}/people", json={"name": person_name})
            if response.status_code == 200:
                st.session_state["person_added"] = person_name
                st.rerun()
            else:
                st.error("Something went wrong adding this person.")

    if "person_added" in st.session_state:
        p_name = st.session_state.pop("person_added")
        st.success(f"Added **{p_name}** to group members!")

    if people:
        chips_html = "".join([
            f'<span class="person-chip"><span class="person-chip-avatar">{p["name"][:1].upper()}</span>{p["name"].title()}</span>'
            for p in people
        ])
        st.markdown(f"""
        <div style="margin-top: 14px; margin-bottom: 24px;">
            <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; color: #6A6965; margin-bottom: 8px;">
                Current Members ({len(people)})
            </div>
            <div class="chips-wrap">{chips_html}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        render_empty_state(
            icon="👥",
            title="No Group Members Yet",
            text="Add friends above to enable shared expense splitting and balance settlements."
        )

    st.divider()
    st.subheader("Split an expense")

    if expenses and people:
        expense_options = {f"#{e['id']} - {e['description']} (₹{e['amount']})": e["id"] for e in expenses}
        selected_expense_label = st.selectbox("Choose an expense to split", list(expense_options.keys()))
        selected_expense_id = expense_options[selected_expense_label]

        people_options = {p["name"]: p["id"] for p in people}
        selected_names = st.multiselect("Split between", list(people_options.keys()))

        # Dynamic split calculation preview
        selected_expense_obj = next((e for e in expenses if e["id"] == selected_expense_id), None)
        if selected_expense_obj and selected_names:
            num_people = len(selected_names)
            total_amt = selected_expense_obj["amount"]
            per_person_amt = round(total_amt / num_people, 2)
            st.markdown(f"""
            <div class="split-calc-box">
                <div class="split-calc-item">
                    Splitting <strong>₹{total_amt:.2f}</strong> among <strong>{num_people} {'members' if num_people > 1 else 'member'}</strong>
                </div>
                <div class="split-calc-highlight">
                    ₹{per_person_amt:.2f} <span style="font-size: 0.85rem; font-family: 'DM Sans', sans-serif; color: #6A6965;">/ person</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Split this expense", use_container_width=True):
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
        render_empty_state(
            icon="🧾",
            title="Splitting Unavailable",
            text="Add at least one expense and one member before creating a split."
        )

# ---- Tab 4: Balances ----
with tab_balances:
    st.subheader("Check a balance")
    if people:
        balance_names = {p["name"]: p["id"] for p in people}
        selected_balance_name = st.selectbox("Check balance for", list(balance_names.keys()))
        selected_balance_id = balance_names[selected_balance_name]

        balance_response = requests.get(f"{API_URL}/people/{selected_balance_id}/balance")
        if balance_response.status_code == 200:
            balance_data = balance_response.json()
            total_owed = balance_data.get("total_owed", 0.0)
            person_display = balance_data.get("person", selected_balance_name).title()
            breakdown_list = balance_data.get("breakdown", [])

            col1, col2 = st.columns([1, 1])
            with col1:
                if total_owed > 0:
                    st.markdown(f"""
                    <div class="stat-card debt">
                        <div class="stat-card-label">{person_display} Owes</div>
                        <div class="stat-card-value debt">₹{total_owed:.2f}</div>
                        <div class="stat-card-sub">Total outstanding across shared splits</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-card-label">{person_display} Balance</div>
                        <div class="stat-card-value income">₹0.00</div>
                        <div class="stat-card-sub">All shared expenses are settled</div>
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                status_label = "Pending Settlement" if total_owed > 0 else "All Settled"
                badge_style = (
                    "background-color: #F8EBE8; color: #B84C3A; border: 1px solid #E8C8C2;"
                    if total_owed > 0
                    else "background-color: #DCE5DD; color: #315C4A; border: 1px solid #C9D6CB;"
                )
                st.markdown(f"""
                <div class="stat-card" style="border-left: 4px solid {'#B84C3A' if total_owed > 0 else '#315C4A'};">
                    <div class="stat-card-label">Account Status</div>
                    <div style="margin: 6px 0 8px 0;">
                        <span style="{badge_style} font-weight: 600; font-size: 0.85rem; padding: 4px 12px; border-radius: 16px; display: inline-block;">
                            {status_label}
                        </span>
                    </div>
                    <div class="stat-card-sub">
                        {len(breakdown_list)} split transaction{'s' if len(breakdown_list) != 1 else ''} recorded
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if breakdown_list:
                st.subheader("Expense breakdown")
                b_df = pd.DataFrame(breakdown_list)
                if expenses:
                    expense_lookup = {e["id"]: e.get("description", f"Expense #{e['id']}") for e in expenses}
                    b_df["description"] = b_df["expense_id"].map(expense_lookup).fillna("Split Expense")
                    b_df = b_df[["expense_id", "description", "amount"]]
                    b_config = {
                        "expense_id": st.column_config.NumberColumn("Expense ID", width="small"),
                        "description": st.column_config.TextColumn("Expense Description"),
                        "amount": st.column_config.NumberColumn("Amount Owed", format="₹%.2f"),
                    }
                else:
                    b_config = {
                        "expense_id": st.column_config.NumberColumn("Expense ID", width="small"),
                        "amount": st.column_config.NumberColumn("Amount Owed", format="₹%.2f"),
                    }
                st.dataframe(b_df, column_config=b_config, use_container_width=True, hide_index=True)
            else:
                render_empty_state(
                    icon="🎉",
                    title="No Outstanding Debts",
                    text=f"{person_display} has no unpaid split expenses on record."
                )
        else:
            st.error("Could not fetch balance.")
    else:
        render_empty_state(
            icon="⚖️",
            title="No Balance Information",
            text="Add group members in the 'Split' tab to track member balances and settlements."
        )