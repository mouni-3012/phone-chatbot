import streamlit as st
import pandas as pd

# -------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="📱 Phone Deals Agent",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("📱 Phone Deals Agent")
st.markdown("Search phones by **brand**, **model**, **type** (new/used/refurbished), or **price range**.")

# -------------------------------------------------------------
# Sidebar – Settings
# -------------------------------------------------------------
st.sidebar.markdown("### Settings")
price_min = st.sidebar.number_input("Minimum Price ($)", min_value=0, value=0)
price_max = st.sidebar.number_input("Maximum Price ($)", min_value=0, value=1000)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "[GitHub Repository](https://github.com/mouni-3012/phone-chatbot)",
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# Load CSV Data
# -------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("phonesdata.csv")

phones = load_data()

# -------------------------------------------------------------
# Chat Input
# -------------------------------------------------------------
query = st.chat_input("Type a phone model, brand, or type…")

if query:
    st.chat_message("user").markdown(query)

    # Filter phones by search text
    mask = (
        phones["model"].str.contains(query, case=False) |
        phones["brand"].str.contains(query, case=False) |
        phones["type"].str.contains(query, case=False)
    )

    # Apply price filters
    filtered = phones[mask]
    filtered = filtered[(filtered["price"] >= price_min) & (filtered["price"] <= price_max)]

    if not filtered.empty:
        st.chat_message("assistant").markdown(
            f"Here are some matches for **{query}** "
            f"between **${price_min}–${price_max}**:"
        )

        for _, row in filtered.iterrows():
            st.chat_message("assistant").markdown(
                f"**ID:** {row.id}\n"
                f"**Brand/Model:** {row.brand} {row.model}\n"
                f"**Type:** {row.type}\n"
                f"**Price:** ${row.price}\n"
                f"**Condition:** {row.condition}"
            )
    else:
        st.chat_message("assistant").markdown("No phones match your search.")

# -------------------------------------------------------------
# Optional – Display Full Table
# -------------------------------------------------------------
st.markdown("---")
if st.checkbox("Show full phone catalog"):
    st.dataframe(phones)
