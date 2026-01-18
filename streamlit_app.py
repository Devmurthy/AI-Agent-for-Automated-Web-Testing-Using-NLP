"""
Streamlit Deployment App for AI Website Testing Agent
This provides an alternative deployment option using Streamlit
"""

import streamlit as st
import os
import subprocess
from dotenv import load_dotenv

# Install Playwright browsers if needed (for Streamlit Cloud)
try:
    from playwright.sync_api import sync_playwright
    # Check if browsers are installed
    result = subprocess.run(['playwright', 'install', '--dry-run', 'chromium'], 
                          capture_output=True, text=True, timeout=10)
    if 'chromium' in result.stdout.lower() or result.returncode != 0:
        # Browsers not installed, install them
        subprocess.run(['playwright', 'install', 'chromium'], 
                      capture_output=True, timeout=300)
except Exception as e:
    st.warning(f"Playwright browser installation check failed: {e}")

from ai_agent import AIWebsiteTester

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Agent - Automated Website Testing",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize AI agent
@st.cache_resource
def get_ai_agent():
    """Initialize and cache the AI agent"""
    try:
        agent = AIWebsiteTester()
        return agent, None
    except Exception as e:
        return None, str(e)

# Main title
st.title("🤖 AI Agent for Automated Website Testing")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📋 About")
    st.markdown("""
    This AI-powered testing agent uses:
    - **LangGraph** for workflow orchestration
    - **OpenAI GPT** for natural language understanding
    - **Playwright** for browser automation
    
    Simply describe what you want to test in plain English!
    """)
    
    st.header("⚙️ Settings")
    browser = st.selectbox("Browser", ["chrome", "firefox", "webkit"], index=0)
    
    st.markdown("---")
    st.markdown("**Note:** OpenAI API key required in `.env` file")

# Initialize agent
ai_agent, error = get_ai_agent()

if error:
    st.error(f"❌ Error initializing AI Agent: {error}")
    st.info("💡 The agent will work in fallback mode without OpenAI API")
    ai_agent = None
else:
    st.success("✅ AI Agent initialized successfully!")

# Main form
st.header("🧪 Run Test")

with st.form("test_form"):
    website_url = st.text_input(
        "Website URL",
        placeholder="https://amazon.com",
        help="Enter the website URL you want to test"
    )
    
    test_instruction = st.text_area(
        "Test Instruction (Natural Language)",
        placeholder="go to website and search for iphone 15",
        height=100,
        help="Describe what you want to test in plain English"
    )
    
    submitted = st.form_submit_button("🚀 Run Test", use_container_width=True)

# Run test when form is submitted
if submitted:
    if not ai_agent:
        st.error("AI Agent not available. Please check your configuration.")
    elif not website_url or not test_instruction:
        st.warning("⚠️ Please fill in both Website URL and Test Instruction")
    else:
        # Validate URL
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        # Show progress
        with st.spinner("🔄 Running test... This may take a few moments"):
            try:
                # Run the test
                result = ai_agent.run_test(website_url, test_instruction, browser)
                
                # Display results
                st.markdown("---")
                st.header("📊 Test Results")
                
                # Status
                if result.get("status") == "success":
                    st.success(f"✅ Test Passed")
                else:
                    st.error(f"❌ Test Failed")
                
                # Test details
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Website", result.get("websiteUrl", "N/A"))
                with col2:
                    st.metric("Browser", result.get("browser", "N/A"))
                
                st.markdown(f"**Test Instruction:** {result.get('testInstruction', 'N/A')}")
                
                # Results
                if result.get("results"):
                    st.subheader("📋 Results")
                    for res in result["results"]:
                        st.markdown(f"- {res}")
                
                # Validations
                if result.get("validations"):
                    st.subheader("✅ Validations")
                    for val in result["validations"]:
                        status_icon = "✅" if val.get("status") == "pass" else "⚠️" if val.get("status") == "warning" else "❌"
                        st.markdown(f"{status_icon} **{val.get('type', 'N/A')}**: {val.get('message', 'N/A')}")
                
                # Screenshots
                if result.get("screenshots"):
                    st.subheader("📸 Screenshots")
                    screenshots = result["screenshots"]
                    # Filter duplicates
                    seen = set()
                    unique_screenshots = []
                    for ss in screenshots:
                        if ss.get("name") and ss.get("name") not in seen and ss.get("base64"):
                            seen.add(ss.get("name"))
                            unique_screenshots.append(ss)
                    
                    if unique_screenshots:
                        cols = st.columns(min(len(unique_screenshots), 3))
                        for idx, screenshot in enumerate(unique_screenshots):
                            with cols[idx % len(cols)]:
                                st.image(
                                    f"data:image/png;base64,{screenshot.get('base64')}",
                                    caption=screenshot.get("name", f"Screenshot {idx + 1}"),
                                    use_container_width=True
                                )
                
                # Performance metrics
                if result.get("performance"):
                    st.subheader("⚡ Performance Metrics")
                    perf = result["performance"]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Load Time", f"{perf.get('loadTime', 0)}ms")
                    with col2:
                        st.metric("Page Size", f"{perf.get('pageSize', 'N/A')}KB")
                
                # Error details
                if result.get("error"):
                    st.error(f"❌ Error: {result.get('error')}")
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("**Built with:** LangGraph + OpenAI GPT + Playwright + Streamlit")
