import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("📊 Advising & Workshop Data Analysis Tool")

st.sidebar.header("Upload Data Files")
advising_file = st.sidebar.file_uploader("Upload Advising CSV", type="csv")
workshop_file = st.sidebar.file_uploader("Upload Workshop CSV", type="csv")

show_data = st.sidebar.checkbox("Show raw data preview", value=False)

if advising_file:
    df = pd.read_csv(advising_file)
    df['Date Scheduled'] = pd.to_datetime(df['Date Scheduled'], errors='coerce')
    df['Full Name'] = df['First Name'].str.strip().str.lower() + ' ' + df['Last Name'].str.strip().str.lower()

    if show_data:
        st.subheader("📋 Advising Data Preview")
        st.dataframe(df.head())

    st.header("📈 Advising Metrics")
    total_appointments = len(df)
    unique_students = df['Student Number'].nunique()
    repeat_students = df['Student Number'].value_counts().gt(1).sum()
    appointments_by_calendar = df['Calendar'].value_counts()
    type_counts = df['Type'].value_counts()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", total_appointments)
    col2.metric("Unique Students", unique_students)
    col3.metric("Repeat Students", repeat_students)

    st.subheader("📆 Appointments by Month")
    df['Month'] = df['Date Scheduled'].dt.to_period('M').astype(str)
    month_counts = df['Month'].value_counts().sort_index()
    st.bar_chart(month_counts)

    st.subheader("📊 Appointment Type Breakdown")
    st.bar_chart(type_counts)

    st.subheader("📑 Advisor vs Appointment Category")
    if 'Category' in df.columns:
        advisor_category = pd.crosstab(df['Calendar'], df['Category'])
        st.dataframe(advisor_category)

if workshop_file:
    dfw = pd.read_csv(workshop_file)
    dfw['Date Scheduled'] = pd.to_datetime(dfw['Date Scheduled'], errors='coerce')
    dfw['Date Rescheduled'] = pd.to_datetime(dfw['Date Rescheduled'], errors='coerce')
    dfw['Writing Stage'] = dfw['Where in the writing process are you? '].str.lower().fillna('')
    dfw['Current Major'] = dfw['What is your current major?'].str.strip().str.title()
    dfw['Applied Before'] = dfw['Have you applied to the Allen School before? '].str.lower().str.strip()

    if show_data:
        st.subheader("📋 Workshop Data Preview")
        st.dataframe(dfw.head())

    st.header("📈 Workshop Metrics")
    total_w_appointments = len(dfw)
    unique_majors = dfw['Current Major'].nunique()
    rescheduled = dfw['Date Rescheduled'].notnull().sum()
    applied_yes = (dfw['Applied Before'] == 'yes').sum()
    applied_no = (dfw['Applied Before'] == 'no').sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", total_w_appointments)
    col2.metric("Unique Majors", unique_majors)
    col3.metric("Rescheduled Appointments", rescheduled)

    col4, col5 = st.columns(2)
    col4.metric("Applied Before", applied_yes)
    col5.metric("Not Applied Before", applied_no)

    st.subheader("🧠 Writing Stage Breakdown")
    stage_series = dfw['Writing Stage'].str.split(',').explode().str.strip()
    stage_counts = stage_series.value_counts()
    st.bar_chart(stage_counts)

    st.subheader("🎓 Major Distribution")
    major_counts = dfw['Current Major'].value_counts()
    st.bar_chart(major_counts)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
