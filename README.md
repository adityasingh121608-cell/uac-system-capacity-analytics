python
import os

# --- Fill in your GitHub credentials ---
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"
GITHUB_EMAIL = "YOUR_GITHUB_EMAIL"
GITHUB_TOKEN = "YOUR_COPIED_GHP_TOKEN"
REPO_NAME = "uac-system-capacity-analytics"

# Configure Git user
!git config --global user.name "{GITHUB_USERNAME}"
!git config --global user.email "{GITHUB_EMAIL}"

# Initialize local git repository
!git init

# Remove any existing origin to avoid conflicts
!git remote remove origin 2>/dev/null

# Set remote origin using your secure PAT
remote_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
!git remote add origin {remote_url}

# Stage required project files
!git add app.py requirements.txt README.md cleaned_uac_analytics.csv HHS_Unaccompanied_Alien_Children_Program.csv

# Commit changes
!git commit -m "feat: complete UAC care pipeline analytics and Streamlit app"

# Rename branch to main and push
!git branch -M main
!git push -u origin main --force

print(f"\n🚀 Successfully pushed to: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
