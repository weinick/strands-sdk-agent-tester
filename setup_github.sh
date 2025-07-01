#!/bin/bash

# GitHub Repository Setup Helper Script
# This script helps you push your Strands SDK project to GitHub

echo "🚀 Strands SDK Agent Tester - GitHub Setup Helper"
echo "=================================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Please run 'git init' first."
    exit 1
fi

# Check if there are commits
if ! git log --oneline -n 1 > /dev/null 2>&1; then
    echo "❌ No commits found. Please make an initial commit first."
    exit 1
fi

echo "✅ Git repository is ready!"
echo ""

# Get repository URL from user
echo "📝 Please provide your GitHub repository details:"
echo ""
read -p "GitHub username: " username
read -p "Repository name (default: strands-sdk-agent-tester): " repo_name

# Set default repository name if not provided
if [ -z "$repo_name" ]; then
    repo_name="strands-sdk-agent-tester"
fi

# Construct repository URL
repo_url="https://github.com/$username/$repo_name.git"

echo ""
echo "🔗 Repository URL: $repo_url"
echo ""

# Confirm before proceeding
read -p "Is this correct? (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "❌ Setup cancelled."
    exit 1
fi

echo ""
echo "🚀 Setting up GitHub remote and pushing..."
echo ""

# Add remote origin
echo "📡 Adding remote origin..."
if git remote add origin "$repo_url" 2>/dev/null; then
    echo "✅ Remote origin added successfully!"
else
    echo "⚠️  Remote origin already exists, updating..."
    git remote set-url origin "$repo_url"
fi

# Set main branch
echo "🌿 Setting main branch..."
git branch -M main

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
if git push -u origin main; then
    echo ""
    echo "🎉 SUCCESS! Your project has been pushed to GitHub!"
    echo ""
    echo "🔗 Your repository is now available at:"
    echo "   https://github.com/$username/$repo_name"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Visit your repository on GitHub"
    echo "   2. Add topics: ai, agents, streamlit, aws-bedrock, openai, anthropic, python"
    echo "   3. Consider adding a LICENSE file"
    echo "   4. Star the repository if you like it! ⭐"
    echo ""
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "   1. Repository exists on GitHub"
    echo "   2. You have push permissions"
    echo "   3. Your GitHub credentials are configured"
    echo ""
    echo "💡 You can also try pushing manually:"
    echo "   git remote add origin $repo_url"
    echo "   git branch -M main"
    echo "   git push -u origin main"
fi
