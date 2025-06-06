# Home.py
import streamlit as st

st.set_page_config(page_title="Dashboard Home", layout="wide")

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

st.markdown("---")
st.markdown("Made with 💜 by [Riva Gore](https://www.linkedin.com/in/rivagore/)", unsafe_allow_html=True)