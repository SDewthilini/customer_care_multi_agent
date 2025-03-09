import streamlit as st
import time
from app import run_customer_support

st.set_page_config(
    page_title="Customer Support Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("Customer Support Agent")
st.markdown("This application processes customer queries and shows the agent's thinking process.")

# User input
query = st.text_area("Enter your customer query:", height=100)

# Create columns for displaying results
if query and st.button("Process Query"):
    # Display thinking process with a spinner
    with st.spinner("Processing query..."):
        # Show thinking process
        thinking_container = st.container()
        
        with thinking_container:
            st.subheader("Agent Thinking Process:")
            
            category_placeholder = st.empty()
            category_placeholder.text("⏳ Categorizing query...")
            time.sleep(1)  # Simulate processing time
            
            # Call the app but intercept at each step to show thinking
            # We'll use the actual app in the backend but show the steps visually
            result = run_customer_support(query)
            
            # Update with actual category
            category_placeholder.success(f"✅ Query categorized as: {result['category']}")
            
            sentiment_placeholder = st.empty()
            sentiment_placeholder.text("⏳ Analyzing sentiment...")
            time.sleep(1)  # Simulate processing time
            
            # Update with actual sentiment
            sentiment_emoji = "😊" if result['sentiment'] == "Positive" else "😐" if result['sentiment'] == "Neutral" else "😠"
            sentiment_placeholder.success(f"✅ Sentiment analyzed as: {result['sentiment']} {sentiment_emoji}")
            
            response_placeholder = st.empty()
            
            if result['sentiment'] == "Negative":
                response_placeholder.warning("⚠️ Negative sentiment detected. Escalating to human agent...")
            else:
                if result['category'] == "Technical":
                    response_placeholder.info("🔧 Generating technical support response...")
                elif result['category'] == "Billing":
                    response_placeholder.info("💰 Generating billing support response...")
                else:
                    response_placeholder.info("ℹ️ Generating general support response...")
            
            time.sleep(1.5)  # Simulate response generation time
            
        # Display final results in a nice format
        st.subheader("Results:")
        
        # Create three columns for the results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Category", result['category'])
            
        with col2:
            st.metric("Sentiment", result['sentiment'])
            
        with col3:
            if result['sentiment'] == "Negative":
                st.metric("Status", "Escalated")
            else:
                st.metric("Status", "Resolved")
        
        # Display the final response
        st.subheader("Response:")
        st.write(result['response'])
        
        # Optional: Add a divider and history section
        st.divider()
        
        # Store history in session state if it doesn't exist
        if 'history' not in st.session_state:
            st.session_state.history = []
        
        # Add current interaction to history
        st.session_state.history.append({
            "query": query,
            "category": result['category'],
            "sentiment": result['sentiment'],
            "response": result['response']
        })

# Display history if available
if 'history' in st.session_state and st.session_state.history:
    st.subheader("Previous Queries:")
    for i, interaction in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Query {len(st.session_state.history) - i}: {interaction['query'][:50]}..."):
            st.write(f"**Category:** {interaction['category']}")
            st.write(f"**Sentiment:** {interaction['sentiment']}")
            st.write(f"**Response:**")
            st.write(interaction['response'])

# Add a sidebar with information
with st.sidebar:
    st.header("About")
    st.write("""
    This customer support agent uses LangGraph and Groq to process customer queries.
    
    The workflow:
    1. Categorize the query (Technical, Billing, General)
    2. Analyze sentiment (Positive, Neutral, Negative)
    3. Route to appropriate handler or escalate if negative
    """)
    
    st.subheader("Sample Queries")
    sample_queries = [
        "How do I reset my password?",
        "I'd like to update my billing information",
        "Tell me about your services",
        "This product is terrible and doesn't work at all"
    ]
    
    for sample in sample_queries:
        if st.button(sample):
            # This will set the query but user still needs to click Process Query
            st.session_state.query = sample
            st.experimental_rerun()