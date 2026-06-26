#!/bin/bash

# ===========================================
# GitHub Push Script (with Token)
# ===========================================

# Usage:
#   ./push_to_github.sh YOUR_GITHUB_TOKEN
#
# Example:
#   ./push_to_github.sh ghp_xxxxxxxxxxxxxxxxxxxx

if [ -z "$1" ]; then
    echo "❌ Error: GitHub token is required"
    echo ""
    echo "Usage:"
    echo "  ./push_to_github.sh YOUR_GITHUB_TOKEN"
    echo ""
    echo "Example:"
    echo "  ./push_to_github.sh ghp_xxxxxxxxxxxxxxxxxxxx"
    exit 1
fi

GITHUB_TOKEN=$1
REPO_URL="https://github.com/vjtechspot/AI-Agent.git"

echo "🚀 Pushing AI-Agent project to GitHub..."
echo ""

# Configure git
git config user.email "vjtechspot@gmail.com"
git config user.name "vjtechspot"

# Add all changes
git add .

# Commit
git commit -m "Fix: Updated agent to modern AgentSession, fixed dashboard API, added trunk cleanup script, improved error handling" || echo "No new changes to commit"

# Push using token
echo ""
echo "📤 Pushing to GitHub..."
git push https://$GITHUB_TOKEN@github.com/vjtechspot/AI-Agent.git main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "   Repository: https://github.com/vjtechspot/AI-Agent"
else
    echo ""
    echo "❌ Push failed. Please check your token and try again."
fi