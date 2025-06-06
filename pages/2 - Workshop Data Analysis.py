import streamlit as st
import pandas as pd
import nltk

from collections import Counter
from nltk.corpus import stopwords

nltk.download('stopwords')
default_stopwords = set(stopwords.words('english'))

st.set_page_config(layout="wide", page_title="Workshop Data Analysis")
st.title("📊 Workshop Data Analysis Tool")

st.sidebar.header("Upload Data Files")

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

    # st.markdown("### 🎓 Student Academic Backgrounds")
    # st.subheader("🎓 Major Representation")
    # major_counts = dfw['Current Major'].value_counts()
    # st.bar_chart(major_counts)
    st.markdown("### 🎓 Student Academic Backgrounds")
    st.subheader("🎓 Major Representation")

    # Normalize major names
    dfw['Current Major'] = dfw['Current Major'].str.lower().str.strip()
    dfw['Current Major'] = dfw['Current Major'].replace(
        to_replace=r'(pre[\s\-]?sciences|presciences|premajor)', value='Pre-Sciences', regex=True
    )
    dfw['Current Major'] = dfw['Current Major'].str.title()

    # Generate pie chart for major distribution
    major_counts = dfw['Current Major'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(major_counts, labels=major_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Purples_r(range(len(major_counts))))
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown("### 📝 Writing Stage vs. Allen School Application")
    st.subheader("📊 Writing Stage vs Application Status")
    exploded_df = dfw[['Applied Before']].copy()
    exploded_df['Writing Stage'] = dfw['Writing Stage']
    exploded_df = exploded_df.dropna(subset=['Writing Stage'])
    exploded_df = exploded_df.assign(Writing_Stage=exploded_df['Writing Stage'].str.split(',')).explode('Writing_Stage')
    exploded_df['Writing_Stage'] = exploded_df['Writing_Stage'].str.strip()
    stage_vs_applied = pd.crosstab(exploded_df['Writing_Stage'], exploded_df['Applied Before'])
    st.dataframe(stage_vs_applied.copy(), use_container_width=True)

st.markdown("---")
st.markdown("Made with 💜 by [Riva Gore](https://www.linkedin.com/in/rivagore/)", unsafe_allow_html=True)

