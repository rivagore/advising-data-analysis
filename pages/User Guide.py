# User Guide.py
import streamlit as st

st.set_page_config(page_title="User Guide", layout="wide")

st.title("📖 Dashboard User Guide")

st.markdown("""
Welcome to the **Advising & Workshop Dashboard** user guide. This guide will help you understand how to use the dashboard effectively.

---

### 🧭 Navigation
Use the sidebar to navigate between:
- **Project Analysis**: Advising appointment insights
- **Workshop Analysis**: Workshop submissions and trends
- **Home**: Overview and dashboard description

---

### 📁 Project Analysis Page

This page displays data from advising appointments.
- **Upload CSV**: Use the file uploader in the sidebar
- **Filters**: Select advisors and appointment types to narrow your view
- **Category Tagging**: Appointments are automatically categorized using keyword matching
- **Repeat Metrics**: View frequency of visits, timelines, and student behavior over time
- **Topic Word Cloud**: Shows most common discussion topics, with filler words removed

---

### 🧾 Workshop Analysis Page

This page shows data from workshop submissions.
- **Upload CSV**: Use the file uploader in the sidebar
- **Essay Stage Funnel**: Visualize students' writing progress
- **Application Status**: Cross-analyze writing stage vs Allen School application history
- **Major & Reschedule Trends**: Understand academic background and behavior

---

### 📊 Charts & Tables
- You can hover over any chart to see tooltips
- Click column headers in tables to sort data
- Most tables are interactive and scrollable

---

### 💡 Tips
- Refresh the app if filters or uploads don’t load
- Ensure date fields in your CSV are properly formatted (`YYYY-MM-DD`)
- Use full-screen mode for better visibility on wide charts

Need help? Reach out to your project maintainer or Streamlit support.
""")

st.markdown("---")
st.markdown("Made with 💜 by [Riva Gore](https://www.linkedin.com/in/rivagore/)", unsafe_allow_html=True)