#!/bin/bash

# Script to push code to your personal GitHub repository
# Replace YOUR_USERNAME with your actual GitHub username

echo "🚀 Pushing code to GitHub..."
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required!"
    exit 1
fi

# Repository name
REPO_NAME="AI-Agent-for-Automated-Website-Testing"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "📦 Repository URL: ${REPO_URL}"
echo ""

# Check if personal remote already exists
if git remote | grep -q "personal"; then
    echo "⚠️  Personal remote already exists. Removing it..."
    git remote remove personal
fi

# Add personal remote
echo "➕ Adding personal remote..."
git remote add personal "${REPO_URL}"

# Push to personal repository
echo "📤 Pushing to your personal repository..."
git push personal main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to: ${REPO_URL}"
    echo ""
    echo "🌐 Next steps:"
    echo "1. Go to: https://streamlit.io/cloud"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select repository: ${GITHUB_USERNAME}/${REPO_NAME}"
    echo "5. Set main file: streamlit_app.py"
    echo "6. Add OPENAI_API_KEY in secrets"
    echo "7. Deploy!"
else
    echo ""
    echo "❌ Push failed. Make sure:"
    echo "1. The repository exists at: ${REPO_URL}"
    echo "2. You have push access"
    echo "3. You're authenticated with GitHub"
fi
