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

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use('Agg')

if advising_file:
    st.markdown("## 📁 Advising Data Overview")
    st.markdown("### 🗂 Advising Data Analysis")
    df = pd.read_csv(advising_file)
    df['Date Scheduled'] = pd.to_datetime(df['Date Scheduled'], errors='coerce')
    df['Full Name'] = df['First Name'].str.strip().str.lower() + ' ' + df['Last Name'].str.strip().str.lower()

    # Filters
    advisors = df['Calendar'].dropna().unique().tolist()
    types = df['Type'].dropna().unique().tolist()
    with st.expander("🔍 Filter Options"):
        selected_advisors = st.multiselect("Filter by Advisor", advisors, default=advisors)
        selected_types = st.multiselect("Filter by Appointment Type", types, default=types)

    df = df[df['Calendar'].isin(selected_advisors) & df['Type'].isin(selected_types)]

    if show_data:
        with st.expander("📋 Preview Advising Data"):
            st.dataframe(df.head(), use_container_width=True)

    st.markdown("### 📊 General Appointment Stats")

    st.subheader("🗓️ Appointments by Day of Week")
    df['Weekday'] = df['Date Scheduled'].dt.day_name()
    weekday_counts = df['Weekday'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    st.bar_chart(weekday_counts)

    st.markdown("### 📆 Advisor Activity Overview")
    st.subheader("🧾 Monthly Load per Advisor")
    df['Month'] = df['Date Scheduled'].dt.strftime('%B %Y')
    advisor_month = pd.crosstab(index=df['Month'], columns=df['Calendar']).copy()
    advisor_month = advisor_month.loc[~advisor_month.index.duplicated(keep='first')]
    styled = advisor_month.style.highlight_max(axis=0, props="background-color: rgba(138, 43, 226, 0.2); font-weight: bold;")
    st.dataframe(styled, use_container_width=True, hide_index=False)

    st.subheader("🧑‍🎓 Repeat Visitors Timeline")
    timeline_df = df.copy()
    timeline_df['Month'] = timeline_df['Date Scheduled'].dt.to_period('M').astype(str)
    timeline_counts = timeline_df[timeline_df['Student Number'].duplicated(keep=False)].groupby('Month')['Student Number'].nunique()
    st.line_chart(timeline_counts)

    st.subheader("📊 First-time vs Repeat Students by Advisor")
    repeat_flags = df.duplicated(subset='Student Number', keep=False)
    df['Repeat Status'] = repeat_flags.map({True: 'Repeat', False: 'First-Time'})
    grouped = df.groupby(['Calendar', 'Repeat Status']).size().unstack(fill_value=0)
    st.dataframe(grouped, use_container_width=True)

    if 'topic_clean' in df.columns:
        st.markdown("### 🗣 Topic Content Insights")
    st.subheader("🌥 Topic Word Cloud")
        text = ' '.join(df['topic_clean'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

    st.markdown("### 🔁 Repeat Visit Metrics")
    st.subheader("⏱️ Average Time Between Repeat Visits")
    repeat_df = df[df['Student Number'].duplicated(keep=False)]
    gaps = repeat_df.groupby('Student Number')['Date Scheduled'].agg(['min', 'max'])
    gaps['Days Between'] = (gaps['max'] - gaps['min']).dt.days
    st.write(f"Average gap: {gaps['Days Between'].mean():.1f} days")
    st.write(f"Shortest gap: {gaps['Days Between'].min()} days")
    st.write(f"Longest gap: {gaps['Days Between'].max()} days")
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
    if not df['Date Scheduled'].isna().all():
        df['Month'] = df['Date Scheduled'].dt.strftime('%B %Y')
        month_counts = df['Month'].value_counts().sort_index()
        st.bar_chart(month_counts)
    else:
        st.warning("No valid dates found after filtering. Please adjust filters or check data.")

    st.subheader("📅 Appointments by Day of Week")
    df['Weekday'] = df['Date Scheduled'].dt.day_name()
    weekday_counts = df['Weekday'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    st.bar_chart(weekday_counts)

    st.subheader("📋 Appointments by Advisor and Category")
    if 'Category' in df.columns:
        advisor_category = pd.crosstab(index=df['Calendar'], columns=df['Category']).copy()
        advisor_category = advisor_category.loc[~advisor_category.index.duplicated(keep='first')]
        st.dataframe(advisor_category, use_container_width=True)

    st.subheader("🧾 Monthly Load per Advisor")
    advisor_month = pd.crosstab(index=df['Month'], columns=df['Calendar']).copy()
    advisor_month = advisor_month.loc[~advisor_month.index.duplicated(keep='first')]
    styled = advisor_month.style.highlight_max(axis=0, props="background-color: rgba(138, 43, 226, 0.2); font-weight: bold;")
    st.dataframe(styled, use_container_width=True, hide_index=False)

    st.subheader("🔁 Frequency of Repeat Visits")
    repeat_freq = df['Student Number'].value_counts().value_counts().sort_index()
    repeat_freq_df = repeat_freq.rename_axis("Visits").reset_index(name="Student Count")
    st.bar_chart(repeat_freq_df.set_index("Visits"))

    st.subheader("🧠 Most Frequent Words in Topics")
if 'topic_clean' in df.columns:
    words = ' '.join(df['topic_clean'].dropna()).split()
    common_words = pd.Series(Counter(words)).value_counts().head(15)
    common_words_df = common_words.rename_axis("word").reset_index(name="frequency")
    st.dataframe(common_words_df, use_container_width=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=common_words_df, y="word", x="frequency", ax=ax, palette="Purples_d")
    ax.set_title("Top 15 Words in Topics")
    st.pyplot(fig)

    st.subheader("📅 New vs Returning Students by Advisor")
    df['is_repeat'] = df.duplicated(subset='Student Number', keep=False)
    new_vs_repeat = pd.crosstab(df['Calendar'], df['is_repeat'])
    st.bar_chart(new_vs_repeat)

    st.subheader("🧪 Average Time Between Repeat Visits")
    df_sorted = df.sort_values(['Student Number', 'Date Scheduled'])
    repeat_intervals = df_sorted[df_sorted.duplicated(subset='Student Number', keep=False)]
    time_gaps = repeat_intervals.groupby('Student Number')['Date Scheduled'].agg(['min', 'max'])
    time_gaps['days_between'] = (time_gaps['max'] - time_gaps['min']).dt.days
    if not time_gaps.empty:
        avg_gap = int(time_gaps['days_between'].mean())
        min_gap = int(time_gaps['days_between'].min())
        max_gap = int(time_gaps['days_between'].max())
        st.metric("Average Gap (Days)", avg_gap)
        st.metric("Shortest Gap", min_gap)
        st.metric("Longest Gap", max_gap)
    else:
        st.info("Not enough repeat visits to calculate time gaps.")

    
    st.subheader("🧠 Most Frequent Words in Topics")
    if 'topic_clean' in df.columns:
        words = ' '.join(df['topic_clean'].dropna()).split()
        common_words = pd.Series(Counter(words)).value_counts().head(15)
        common_words_df = common_words.rename_axis("word").reset_index(name="frequency")
        st.bar_chart(common_words_df.set_index("word"))

if workshop_file:
    st.markdown("## 🧾 Workshop Data Overview")
    st.markdown("### 🧾 Workshop Data Analysis")
    dfw = pd.read_csv(workshop_file)
    dfw['Date Scheduled'] = pd.to_datetime(dfw['Date Scheduled'], format='%Y-%m-%d', errors='coerce')
    dfw['Date Rescheduled'] = pd.to_datetime(dfw['Date Rescheduled'], format='%Y-%m-%d', errors='coerce')
    dfw['Writing Stage'] = dfw['Where in the writing process are you? '].str.lower().fillna('')
    dfw['Current Major'] = dfw['What is your current major?'].str.strip().str.title()
    dfw['Applied Before'] = dfw['Have you applied to the Allen School before? '].str.lower().str.strip()

    if show_data:
        with st.expander("📋 Preview Workshop Data"):
            st.dataframe(dfw.head(), use_container_width=True)

    st.markdown("### 📊 Workshop Summary Stats")
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
    st.markdown("### ✍️ Essay Progress and Support")
    st.subheader("📚 Writing Stage Breakdown")

    st.subheader("🔻 Writing Stage Funnel")
    funnel_counts = stage_series.value_counts().reindex([
        'i am just getting started',
        'i have brainstormed but not yet drafted',
        'i have a draft',
        'i am nearly done'
    ]).fillna(0)
    st.bar_chart(funnel_counts)
    stage_series = dfw['Writing Stage'].str.split(',').explode().str.strip()
    stage_counts = stage_series.value_counts()
    st.bar_chart(stage_counts)

    st.markdown("### 🎓 Student Academic Backgrounds")
    st.subheader("🎓 Major Representation")
    major_counts = dfw['Current Major'].value_counts()
    st.bar_chart(major_counts)

    st.markdown("### 📝 Writing Stage vs. Allen School Application")
    st.subheader("📊 Writing Stage vs Application Status")
    exploded_df = dfw[['Applied Before']].copy()
    exploded_df['Writing Stage'] = dfw['Writing Stage']
    exploded_df = exploded_df.dropna(subset=['Writing Stage'])
    exploded_df = exploded_df.assign(Writing_Stage=exploded_df['Writing Stage'].str.split(',')).explode('Writing_Stage')
    exploded_df['Writing_Stage'] = exploded_df['Writing_Stage'].str.strip()
    stage_vs_applied = pd.crosstab(exploded_df['Writing_Stage'], exploded_df['Applied Before'])
    st.dataframe(stage_vs_applied.copy(), use_container_width=True)

    st.markdown("### 📆 Rescheduling Behavior")
    st.subheader("⏳ Time Between Scheduling and Rescheduling")
    dfw['Days Rescheduled'] = (dfw['Date Rescheduled'] - dfw['Date Scheduled']).dt.days
    lead_time_dist = dfw['Days Rescheduled'].dropna()
    lead_time_df = lead_time_dist.value_counts().sort_index().rename_axis("days").reset_index(name="count")
    st.bar_chart(lead_time_df.set_index("days"))

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
