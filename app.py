import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(layout="wide", page_title="Advising & Workshop Dashboard")
st.title("📊 Advising & Workshop Data Analysis Tool")

st.sidebar.header("Upload Data Files")
advising_file = st.sidebar.file_uploader("📁 Upload Advising CSV", type="csv")
workshop_file = st.sidebar.file_uploader("📁 Upload Workshop CSV", type="csv")

show_data = st.sidebar.checkbox("👁 Show raw data preview", value=False)

st.markdown("""
<style>
    .metric-label {
        font-weight: bold;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

if advising_file:
    st.markdown("### 🗂 Advising Data Analysis")
    df = pd.read_csv(advising_file)
    df['Date Scheduled'] = pd.to_datetime(df['Date Scheduled'], errors='coerce')
    df['Full Name'] = df['First Name'].str.strip().str.lower() + ' ' + df['Last Name'].str.strip().str.lower()

    if show_data:
        with st.expander("📋 Preview Advising Data"):
            st.dataframe(df.head(), use_container_width=True)

    st.subheader("🔢 Summary Metrics")
    total_appointments = len(df)
    unique_students = df['Student Number'].nunique()
    repeat_students = df['Student Number'].value_counts().gt(1).sum()
    appointments_by_calendar = df['Calendar'].value_counts()
    type_counts = df['Type'].value_counts()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", total_appointments)
    col2.metric("Unique Students", unique_students)
    col3.metric("Repeat Students", repeat_students)

    st.markdown("---")
    st.subheader("📆 Appointments Over Time")
    df['Month'] = df['Date Scheduled'].dt.to_period('M').astype(str)
    month_counts = df['Month'].value_counts().sort_index()
    st.bar_chart(month_counts)

    st.subheader("⏰ Appointments by Hour")
    df['Hour'] = df['Date Scheduled'].dt.hour
    st.bar_chart(df['Hour'].value_counts().sort_index())

    st.subheader("📊 Type of Appointments")
    st.bar_chart(type_counts)

    st.subheader("📋 Appointments by Advisor and Category")
    if 'Category' in df.columns:
        advisor_category = pd.crosstab(df['Calendar'], df['Category'])
        st.dataframe(advisor_category, use_container_width=True)

    st.subheader("🧾 Monthly Load per Advisor")
    advisor_month = pd.crosstab(df['Month'], df['Calendar'])
    st.dataframe(advisor_month, use_container_width=True)

    st.subheader("🔁 Frequency of Repeat Visits")
    repeat_freq = df['Student Number'].value_counts().value_counts().sort_index()
    repeat_freq_df = repeat_freq.rename_axis("Visits").reset_index(name="Student Count")
    st.bar_chart(repeat_freq_df.set_index("Visits"))

    st.subheader("🧠 Most Frequent Words in Topics")
    if 'topic_clean' in df.columns:
        words = ' '.join(df['topic_clean'].dropna()).split()
        common_words = pd.Series(Counter(words)).value_counts().head(15)
        common_words_df = common_words.rename_axis("word").reset_index(name="frequency")
        st.bar_chart(common_words_df.set_index("word"))

if workshop_file:
    st.markdown("### 🧾 Workshop Data Analysis")
    dfw = pd.read_csv(workshop_file)
    dfw['Date Scheduled'] = pd.to_datetime(dfw['Date Scheduled'], errors='coerce')
    dfw['Date Rescheduled'] = pd.to_datetime(dfw['Date Rescheduled'], errors='coerce')
    dfw['Writing Stage'] = dfw['Where in the writing process are you? '].str.lower().fillna('')
    dfw['Current Major'] = dfw['What is your current major?'].str.strip().str.title()
    dfw['Applied Before'] = dfw['Have you applied to the Allen School before? '].str.lower().str.strip()

    if show_data:
        with st.expander("📋 Preview Workshop Data"):
            st.dataframe(dfw.head(), use_container_width=True)

    st.subheader("🔢 Workshop Summary")
    total_w_appointments = len(dfw)
    unique_majors = dfw['Current Major'].nunique()
    rescheduled = dfw['Date Rescheduled'].notnull().sum()
    applied_yes = (dfw['Applied Before'] == 'yes').sum()
    applied_no = (dfw['Applied Before'] == 'no').sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", total_w_appointments)
    col2.metric("Unique Majors", unique_majors)
    col3.metric("Rescheduled", rescheduled)

    col4, col5 = st.columns(2)
    col4.metric("Applied Before", applied_yes)
    col5.metric("Not Applied Before", applied_no)

    st.markdown("---")
    st.subheader("📚 Writing Stage Breakdown")
    stage_series = dfw['Writing Stage'].str.split(',').explode().str.strip()
    stage_counts = stage_series.value_counts()
    st.bar_chart(stage_counts)

    st.subheader("🎓 Major Representation")
    major_counts = dfw['Current Major'].value_counts()
    st.bar_chart(major_counts)

    st.subheader("📊 Writing Stage vs Application Status")
    stage_vs_applied = pd.crosstab(stage_series, dfw['Applied Before'])
    st.dataframe(stage_vs_applied, use_container_width=True)

    st.subheader("⏳ Time Between Scheduling and Rescheduling")
    dfw['Days Rescheduled'] = (dfw['Date Rescheduled'] - dfw['Date Scheduled']).dt.days
    lead_time_dist = dfw['Days Rescheduled'].dropna()
    lead_time_df = lead_time_dist.value_counts().sort_index().rename_axis("days").reset_index(name="count")
    st.bar_chart(lead_time_df.set_index("days"))

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
