# Streamlit Cloud Deployment Guide

## Step 1: Create a New GitHub Repository

1. Go to https://github.com/new
2. Sign in with your GitHub account (Devmurthy)
3. Fill in the details:
   - **Repository name**: `AI-Agent-for-Automated-Website-Testing`
   - **Description**: `AI-powered website testing agent using LangGraph, OpenAI, and Playwright`
   - **Visibility**: Select **Public** (required for free Streamlit Cloud)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

## Step 2: Push Code to Your New Repository

After creating the repository, GitHub will show you commands. Use these:

```bash
cd "/Users/nklakshminarasimhamurthy/Desktop/infosys springboard"

# Add your new repository as a remote (replace YOUR_USERNAME with your GitHub username)
git remote add personal https://github.com/YOUR_USERNAME/AI-Agent-for-Automated-Website-Testing.git

# Push to your new repository
git push personal main
```

## Step 3: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click **"Sign in"** and authorize with GitHub
3. Click **"New app"**
4. Select your repository: `YOUR_USERNAME/AI-Agent-for-Automated-Website-Testing`
5. Set **Main file path**: `streamlit_app.py`
6. Click **"Advanced settings"**
7. Add **Secrets**:
   - Key: `OPENAI_API_KEY`
   - Value: (your OpenAI API key)
8. Click **"Deploy"**

## Alternative: Use Existing Repository

If you have access to the organization repository:
- Repository URL: `https://github.com/springboardmentor1029a-source/AI-Agent-for-Automated-Website-Testing`
- Make sure you're logged into GitHub with an account that has access to this organization
