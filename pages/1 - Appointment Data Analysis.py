import streamlit as st
import pandas as pd
import nltk

from collections import Counter
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

nltk.download('stopwords')
default_stopwords = set(stopwords.words('english'))

st.set_page_config(layout="wide", page_title="Advising Data Analysis")
st.title("\U0001F4CA Advising Data Analysis Tool")

st.sidebar.header("Upload Data Files")
advising_file = st.sidebar.file_uploader("\U0001F4C1 Upload Advising CSV", type="csv")
show_data = st.sidebar.checkbox("\U0001F441 Show raw data preview", value=False)

if advising_file:
    df = pd.read_csv(advising_file, dtype=str)
    df.columns = df.columns.str.strip()
    topic_cols = [col for col in df.columns if "What would you like to talk about?" in col]
    df['What would you like to talk about?'] = df[topic_cols].astype(str).agg(' '.join, axis=1)

    df['Date Scheduled'] = pd.to_datetime(df['Date Scheduled'], errors='coerce')
    df['Full Name'] = df['First Name'].str.strip().str.lower() + ' ' + df['Last Name'].str.strip().str.lower()
    df['In-Person'] = df['Type'].astype(str).str.contains('IN PERSON', case=False, na=False).map({True: 'In Person', False: 'Virtual'})

    df['Student Number'] = df['Student Number'].astype(str).str.strip()
    df = df[df['Student Number'].notna() & (df['Student Number'] != '')]

    advisors = df['Calendar'].dropna().unique().tolist()
    types = df['Type'].dropna().unique().tolist()
    with st.expander("\U0001F50D Filter Options"):
        selected_advisors = st.multiselect("Filter by Advisor", advisors, default=advisors)
        selected_types = st.multiselect("Filter by Appointment Type", types, default=types)

    df = df[df['Calendar'].isin(selected_advisors) & df['Type'].isin(selected_types)]
    df['topic_clean'] = df['What would you like to talk about?'].astype(str).str.lower().str.replace(r'[^a-z\s]', ' ', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()

    category_keywords = {
        "Internships": ["internship", "internships", "practical experience", "recruitment"],
        "Applications / Essays": ["essay", "application", "apply", "personal statement", "application review"],
        "Course Planning": ["course", "registration", "class", "winter", "spring", "plan", "planning"],
        "Resume / Career": ["resume", "career", "job", "fair", "job searching"],
        "Research": ["research", "undergraduate research", "lab", "390r", "a i m s"],
        "Admissions": ["admission", "transfer", "undeclared", "paul allen", "allen school"],
    }

    def categorize(text):
        if pd.isna(text): return "Other"
        for cat, kws in category_keywords.items():
            if any(kw in text for kw in kws):
                return cat
        return "Other"

    df['Category'] = df['topic_clean'].apply(categorize)

    if show_data:
        with st.expander("\U0001F4CB Preview Advising Data"):
            st.dataframe(df.head(), use_container_width=True)

    st.header("\U0001F4CA Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", len(df))
    col2.metric("Unique Students", df['Student Number'].nunique())
    col3.metric("Repeat Students", df['Student Number'].value_counts().gt(1).sum())

    st.subheader("Appointments by Day of Week")
    df['Weekday'] = pd.Categorical(df['Date Scheduled'].dt.day_name(), categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], ordered=True)
    weekday_counts = df['Weekday'].value_counts().sort_index()
    st.bar_chart(weekday_counts, color="#8a2be2")

    st.subheader("Appointments by Month")
    df['Month'] = df['Date Scheduled'].dt.to_period('M').astype(str)
    month_counts = df['Month'].value_counts().sort_index()
    st.bar_chart(month_counts, color="#8a2be2")

    st.subheader("Virtual vs In Person")
    st.bar_chart(df['In-Person'].value_counts(), color="#8a2be2")

    st.header("\U0001F464 By Advisor")
    st.subheader("Monthly Load per Advisor")
    advisor_month = pd.crosstab(index=df['Month'], columns=df['Calendar'])
    advisor_month = advisor_month.sort_index()
    styled = advisor_month.style.highlight_max(axis=0, props="background-color: rgba(138, 43, 226, 0.2); font-weight: bold;")
    st.dataframe(styled, use_container_width=True)

    st.subheader("Appointments by Advisor and Category")
    advisor_category = pd.crosstab(index=df['Calendar'], columns=df['Category'])
    styled_category = advisor_category.style.highlight_max(axis=1, props="background-color: rgba(138, 43, 226, 0.2); font-weight: bold;")
    st.dataframe(styled_category, use_container_width=True)

    st.header("\U0001F501 Repeat Visits")
    repeat_df = df[df['Student Number'].duplicated(keep=False)]
    if not repeat_df.empty:
        time_gaps = repeat_df.groupby('Student Number')['Date Scheduled'].agg(['min', 'max'])
        time_gaps['Days Between'] = (time_gaps['max'] - time_gaps['min']).dt.days
        st.metric("Average Gap (Days)", f"{time_gaps['Days Between'].mean():.1f}")
        st.metric("Shortest Gap", time_gaps['Days Between'].min())
        st.metric("Longest Gap", time_gaps['Days Between'].max())
    else:
        st.info("Not enough repeat visits to calculate gaps.")

    st.subheader("Frequency of Repeat Visits")
    repeat_freq = df['Student Number'].value_counts().value_counts().sort_index()
    st.bar_chart(repeat_freq.rename_axis("Visits").reset_index(name="Student Count").set_index("Visits"), color="#8a2be2")

    st.subheader("Repeat vs First-Time by Advisor")
    df['Repeat Status'] = df['Student Number'].duplicated(keep=False).map({True: 'Repeat', False: 'First-Time'})
    repeat_status = pd.crosstab(df['Calendar'], df['Repeat Status'])
    st.bar_chart(repeat_status, color=["#b19cd9", "#8a2be2"])

    st.header("\U0001F5E3 Topic Analysis")
    st.subheader("Topic Word Cloud")
    text = ' '.join(df['topic_clean'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Purples', max_font_size=120, prefer_horizontal=1.0).generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    st.subheader("Appointments by Topic Category")
    category_counts = df['Category'].value_counts()
    st.bar_chart(category_counts, color="#8a2be2")

    st.subheader("Most Frequent Words in Topics")
    custom_stopwords = default_stopwords.union({
        'course', 'courses', 'planning', 'plan', 'class', 'classes', 'quarter',
        'school', 'year', 'i', 'my', 'in', 'to',
        'for', 'and', 'the', 'a', 'about', 'would', 'like', 'want', 'need', 'know',
        'next', 'soon', 'future', 'help', 'thing', 'something', 'nan', 'get',
        'going', 'schedule', 'appointment', 'just', 'see', 'talk', 'cse', 'spring', 'degree', 
        'take', 'winter', 'fall', 'autumn', 'summer', 'double', 'academic', 'science', 
    })
    words = ' '.join(df['topic_clean'].dropna()).split()
    filtered_words = [w for w in words if w.isalpha() and w not in custom_stopwords and len(w) > 2]
    word_counts = Counter(filtered_words)
    common_words = pd.DataFrame(word_counts.most_common(15), columns=["Word", "Frequency"])
    st.bar_chart(common_words.set_index("Word"), color="#8a2be2")
    st.dataframe(common_words, use_container_width=True)
