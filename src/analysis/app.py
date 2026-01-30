import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import time
import re
import google.generativeai as genai
import os

# Setup for connecting to MinIO storage
MINIO_ENDPOINT = "127.0.0.1:9000"
AWS_ACCESS_KEY = "admin"
AWS_SECRET_KEY = "my-password"
BUCKET_NAME = "raw-data"
DATA_PATH = f"s3://raw-data/processed-data/**/*.parquet"

# Page layout and appearance
st.set_page_config(
    page_title="FinAI | RAG Pipeline",
    page_icon="hmC",
    layout="wide"
)

# Custom styling for the dashboard
st.markdown("""
<style>
    /* Gradient Header */
    .main-header {
        font-size: 2.5rem;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: -10px;
    }
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #262730;
        border: 1px solid #3b3c45;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
    }
    /* Highlighting */
    mark {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        padding: 2px 5px;
        border-radius: 4px;
    }
    /* Search Result Card */
    .result-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #00C9FF;
        margin-bottom: 10px;
        color: #31333F;
    }
    /* Dark mode text adjustment */
    @media (prefers-color-scheme: dark) {
        .result-card {
            background-color: #262730;
            border: 1px solid #3b3c45;
            border-left: 5px solid #00C9FF;
            color: #FAFAFA;
        }
    }
</style>
""", unsafe_allow_html=True)

# Create database connection to MinIO
@st.cache_resource
def get_db_connection():
    con = duckdb.connect(database=':memory:')
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute(f"""
        SET s3_region='us-east-1';
        SET s3_url_style='path';
        SET s3_endpoint='{MINIO_ENDPOINT}';
        SET s3_access_key_id='{AWS_ACCESS_KEY}';
        SET s3_secret_access_key='{AWS_SECRET_KEY}';
        SET s3_use_ssl=false;
    """)
    return con

con = get_db_connection()

# Sidebar controls
with st.sidebar:
    st.title("⚡ FinAI Analyst")
    st.divider()
    
    try:
        # Get list of available stock tickers from data
        tickers_df = con.execute(f"SELECT DISTINCT ticker FROM read_parquet('{DATA_PATH}')").df()
        ticker_list_raw = tickers_df['ticker'].tolist()
        ticker_list = sorted(ticker_list_raw)

        # Keep track of selected ticker
        if 'selected_ticker' not in st.session_state:
            st.session_state.selected_ticker = ticker_list[0]

        # Ticker selection dropdown
        st.subheader("Target Entity")
        st.selectbox(
            "Select Ticker", 
            ticker_list, 
            key="ticker_selector",
            on_change=lambda: setattr(st.session_state, 'selected_ticker', st.session_state.ticker_selector)
        )
        
        current_ticker = st.session_state.selected_ticker
        st.success(f"Locked to: **{current_ticker}**")
        
    except Exception as e:
        st.warning("⚠️ No data found in MinIO yet. Showing demo mode.")
        ticker_list = ["AAPL", "MSFT", "GOOG"]
        current_ticker = ticker_list[0]


# Main dashboard content

# Dashboard header
c1, c2 = st.columns([5, 1], vertical_alignment="center")
with c1:
    st.markdown('<div class="main-header">GenAI Financial Analyst</div>', unsafe_allow_html=True)
    st.caption(f" Analyzing SEC 10-K Filings for **{current_ticker}** via MinIO & DuckDB.")
with c2:
    st.success("System Online", icon="🟢")

st.divider()

# Data statistics section
stats_query = f"""
    SELECT 
        COUNT(*) as total_chunks,
        COUNT(CASE WHEN chunk_content LIKE '%[PHONE_REDACTED]%' THEN 1 END) as redacted_phone
    FROM read_parquet('{DATA_PATH}')
    WHERE ticker = '{current_ticker}'
"""
stats = con.execute(stats_query).df()
clean_count = stats['total_chunks'][0] - stats['redacted_phone'][0]
redacted_count = stats['redacted_phone'][0]

st.subheader("📊 Data Overview")
col_metrics, col_chart = st.columns([2, 1], gap="medium")

# Display metrics
with col_metrics:
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Total Document Chunks", f"{stats['total_chunks'][0]:,}")
    with m2:
        st.metric("Redacted PII Data", redacted_count)
    
    st.info("💡 **Analyst Note:** High redaction rates indicate sensitive regulatory disclosures.", icon="ℹ️")

# Create chart data
chart_data = pd.DataFrame({
        'Category': ['Clean Text', 'Redacted (PII)'],
        'Value': [clean_count, redacted_count]
    })

# Display pie chart
with col_chart:
    with st.container():
        base = alt.Chart(chart_data).encode(theta=alt.Theta("Value", stack=True))
        pie = base.mark_arc(outerRadius=75, innerRadius=45).encode(
            color=alt.Color("Category", scale=alt.Scale(range=['#00C9FF', '#FF4B4B'])),
            tooltip=["Category", "Value"]
        ).properties(
            height=180,
            padding={"top": 0, "bottom": 0}
        )
        st.altair_chart(pie, width='stretch')

# AI Chat interface section
st.write("") 
st.subheader(f"💬 Chat with {current_ticker} Documents")

# RAG search and Gemini AI section
st.divider()
st.subheader(f"🤖 Ask Gemini about {current_ticker}")

# Configure Gemini API (using hardcoded key in this version)
api_key = 'AIzaSyC_Rsv4P7uuaeho0itc5knNwKZd1ZY9j6c'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# Function to extract search keywords from user questions
def extract_search_terms(user_question):
    prompt = f"""
    You are a SQL search optimizer. 
    Convert this user question into a list of 2-3 most important keywords for a database search.
    Return ONLY the keywords separated by commas.Return ONLY the keywords in their singular form. Do not add quotes or brackets.
    
    User Question: "{user_question}"

    Example: 'risk', 'litigation'
    
    """
    response = model.generate_content(prompt)
    
    keywords = [k.strip() for k in response.text.split(',')]
    print("Extracted Keywords:", keywords)
    return keywords

# Handle user input and process queries
user_query = True
if user_query:
    if prompt := st.chat_input("Ex: What are the risks and litigations?"):
        
        # Extract search keywords using AI
        search_keywords = extract_search_terms(prompt)
        
        st.write(f"🔎 *Searching for terms:* `{search_keywords}`")

        # Build SQL query with OR logic for all keywords
        sql_filters = [f"chunk_content ILIKE '%{kw}%'" for kw in search_keywords]
        where_clause = " OR ".join(sql_filters)

        search_sql = f"""
            SELECT chunk_id, chunk_content 
            FROM read_parquet('{DATA_PATH}')
            WHERE ticker = '{current_ticker}' 
            AND ({where_clause})
            LIMIT 10
        """     
    
        results_df = con.execute(search_sql).df()
        print("Search SQL:", results_df)
        print("Results Found:", len(results_df))
    
        # Show retrieved context
        with st.expander("View Retrieved Context (Source Data)"):
            for text in results_df['chunk_content']:
                st.markdown(f"- {text[:200]}...")

        # Generate answer using Gemini
        if api_key:
            try:
                # Prepare context from search results
                context_text = "\n\n".join(results_df['chunk_content'].tolist())
                print("Context Text:", context_text)
                
                question = f'tell me about {", ".join(search_keywords)}'
                print("User Question for Gemini:", question)
                
                # Create prompt for Gemini
                prompt = f"""
                You are a senior financial analyst. 
                Answer the user's question based ONLY on the context provided below.
                If the answer is not in the context, say 'I cannot find that information in the reports.'
                
                CONTEXT:
                {context_text}
                
                USER QUESTION:
                {question}
                """
                
                # Get Gemini response
                with st.spinner("Gemini is analyzing the reports..."):
                    response = model.generate_content(prompt)
                print("Gemini Response:", response.text)
                    
                # Display the answer
                st.success("### Gemini Analysis")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Gemini API Error: {e}")
        else:
            st.info("💡 Enter your Google API Key above to unlock the AI analysis.")