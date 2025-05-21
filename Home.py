# Home.py
import streamlit as st

st.set_page_config(page_title="Dashboard Home", layout="wide")

# ---- Sidebar Style ----
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background-color: #f8f4ff;
    padding: 2rem 1rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] p {
    color: #4B0082;
    font-family: 'Segoe UI', sans-serif;
}

span[data-baseweb="tag"] {
    background-color: rgba(138, 43, 226, 0.2) !important;
    color: #4B0082 !important;
    font-weight: 600;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---- Sidebar Content ----
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Purple_circle.svg/1024px-Purple_circle.svg.png", width=80)
    st.title("📊 Data Dashboard")
    st.markdown("Navigate to a dataset below:")
    st.markdown("### 🗂 Sections")
    st.markdown("- 📁 Project Analysis\n- 🧾 Workshop Analysis\n- 📖 User Guide")
    st.markdown("### ℹ️ Info")
    st.caption("Built with ❤️ using Streamlit")

# ---- Main Content ----
st.title("👋 Welcome to the Advising & Workshop Dashboard")

st.markdown("""
This interactive dashboard was developed to help staff and advisors:

- 📈 Monitor student engagement with advising and workshops
- 🗂 Analyze patterns in appointment types, categories, and repeat visits
- 🧠 Explore topic content and identify student needs
- 📝 Examine application prep stages and workshop attendance

The dashboard is split into the following areas:

### 📁 Project Analysis
View and analyze advising appointment data, including category tagging, student repeat behavior, advisor load over time, and common topics.

### 🧾 Workshop Analysis
Review trends from workshop submissions, including student majors, writing stages, and rescheduling behavior.

### 📖 User Guide *(coming soon)*
Step-by-step guide on how to use all the filters, interpret charts, and export insights.

Use the sidebar to begin exploring!
""")