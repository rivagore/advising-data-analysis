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
    appointments_by_calendar = df['Calendar'].value_counts().reset_index()
    appointments_by_calendar.columns = ['Calendar', 'Count']
    type_counts = df['Type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", total_appointments)
    col2.metric("Unique Students", unique_students)
    col3.metric("Repeat Students", repeat_students)

    st.subheader("📆 Appointments by Month")
    df['Month'] = df['Date Scheduled'].dt.to_period('M').astype(str)
    month_counts = df['Month'].value_counts().reset_index().sort_values('index')
    month_counts.columns = ['Month', 'Count']
    chart = alt.Chart(month_counts).mark_bar().encode(
        x=alt.X('Month:N', sort=None, axis=alt.Axis(labelAngle=0)),
        y='Count:Q'
    ).properties(title='Appointments Scheduled per Month')
    st.altair_chart(chart, use_container_width=True)

    st.subheader("📊 Appointment Type Breakdown")
    type_chart = alt.Chart(type_counts).mark_bar().encode(
        x=alt.X('Type:N', axis=alt.Axis(labelAngle=0)),
        y='Count:Q'
    ).properties(title='Appointment Type Counts')
    st.altair_chart(type_chart, use_container_width=True)

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
    stage_counts = stage_series.value_counts().reset_index()
    stage_counts.columns = ['Stage', 'Count']
    stage_chart = alt.Chart(stage_counts).mark_bar().encode(
        x=alt.X('Stage:N', axis=alt.Axis(labelAngle=0)),
        y='Count:Q'
    ).properties(title='Writing Stage Counts')
    st.altair_chart(stage_chart, use_container_width=True)

    st.subheader("🎓 Major Distribution")
    major_counts = dfw['Current Major'].value_counts().reset_index()
    major_counts.columns = ['Major', 'Count']
    major_chart = alt.Chart(major_counts).mark_bar().encode(
        x=alt.X('Major:N', axis=alt.Axis(labelAngle=0)),
        y='Count:Q'
    ).properties(title='Majors Attending Workshops')
    st.altair_chart(major_chart, use_container_width=True)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")