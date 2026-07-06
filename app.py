import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Social Media Sentiment & Trend Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Social Media Sentiment & Trend Tracker")
st.markdown("Analyzing live tech conversations, sentiment patterns, and keyword trends over time.")
st.markdown("---")


@st.cache_data
def load_data():
    try:
        data = pd.read_csv("processed_sentiment_data.csv")
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        return data
    except FileNotFoundError:
        st.error("Error: 'processed_sentiment_data.csv' not found. Please make sure the file is in the same folder as app.py.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    
    st.sidebar.header("🎛️ Control Panel Filters")
    
    
    all_classes = ['All'] + list(df['Sentiment_Class'].unique())
    selected_class = st.sidebar.selectbox("Filter by Sentiment Category:", all_classes)
    
   
    search_query = st.sidebar.text_input("🔍 Search Keywords in Titles:", "").lower()
    
   
    filtered_df = df.copy()
    if selected_class != 'All':
        filtered_df = filtered_df[filtered_df['Sentiment_Class'] == selected_class]
    if search_query:
        filtered_df = filtered_df[filtered_df['Raw_Title'].str.lower().str.contains(search_query)]

  
    total_items = len(filtered_df)
    pos_count = len(filtered_df[filtered_df['Sentiment_Class'] == 'Positive'])
    neg_count = len(filtered_df[filtered_df['Sentiment_Class'] == 'Negative'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tracked Items", total_items)
    col2.metric("Positive Volume", pos_count, delta=f"{(pos_count/max(total_items,1))*100:.1f}%")
    col3.metric("Negative Volume", neg_count, delta=f"-{(neg_count/max(total_items,1))*100:.1f}%", delta_color="inverse")
    
    st.markdown("---")

    
    graph_col1, graph_col2 = st.columns(2)
    
    with graph_col1:
        st.subheader("📈 Overall Sentiment Class Distribution")
        class_counts = filtered_df['Sentiment_Class'].value_counts().reset_index()
        class_counts.columns = ['Category', 'Count']
        
        
        fig_pie = px.pie(class_counts, values='Count', names='Category', 
                         color='Category',
                         color_discrete_map={'Positive':'#2ecc71', 'Neutral':'#f1c40f', 'Negative':'#e74c3c'},
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with graph_col2:
        st.subheader("⏳ Sentiment Score Intensity Over Time")
        
        fig_scatter = px.scatter(filtered_df, x='Timestamp', y='Sentiment_Score',
                                 color='Sentiment_Class',
                                 hover_data=['Raw_Title'],
                                 color_discrete_map={'Positive':'#2ecc71', 'Neutral':'#f1c40f', 'Negative':'#e74c3c'},
                                 title="Post Mood Trend Matrix")
        st.plotly_chart(fig_scatter, use_container_width=True)

    
    st.markdown("---")
    st.subheader("📋 Detailed Live Stream Feed Inspection Log")
    st.dataframe(filtered_df[['Timestamp', 'Raw_Title', 'Sentiment_Class', 'Sentiment_Score']], use_container_width=True)

else:
    st.warning("Please add data to initialize dashboard components.")