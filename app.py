import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Advising & Workshop Data Analysis Tool")

uploaded_file = st.file_uploader("Upload your advising CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    st.subheader("🔍 Preview of Uploaded Data")
    st.dataframe(df.head())

    if 'Date Scheduled' in df.columns:
        df['Date'] = pd.to_datetime(df['Date Scheduled'], errors='coerce')
        df.set_index('Date', inplace=True)

        st.subheader("📈 Appointments Over Time")
        fig, ax = plt.subplots()
        df.resample('W').size().plot(ax=ax, title='Appointments Per Week')
        st.pyplot(fig)

    if 'Category' in df.columns:
        st.subheader("📋 Appointments by Category")
        fig2, ax2 = plt.subplots()
        df['Category'].value_counts().plot(kind='bar', ax=ax2)
        st.pyplot(fig2)

    if 'What would you like to talk about?' in df.columns:
        st.subheader("🧠 Top Words from Student Topics")
        all_text = ' '.join(df['What would you like to talk about?'].dropna().str.lower())
        top_words = pd.Series(all_text.split()).value_counts().head(15)
        fig3, ax3 = plt.subplots()
        top_words.plot(kind='bar', ax=ax3)
        st.pyplot(fig3)
