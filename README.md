python
import os

# Fill in your GitHub credentials 
GITHUB_USERNAME = adityasingh121608-cell
GITHUB_EMAIL = adityasingh121608@gmail.com
GITHUB_TOKEN = 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
REPO_NAME = uac-system-capacity-analytics

# Configure Git user
!git config --global user.name "{adityasingh121608-cell}"
!git config --global user.email "{adityasingh121608#gmail.com}"

# Initialize local git repository
!git init

# Remove any existing origin to avoid conflicts
!git remote remove origin 2>/dev/null

# Set remote origin using your secure PAT
remote_url = f"https://{adityasingh121608-cell}:{GITHUB_TOKEN}@github.com/{adityasingh121608-cell}/{uac-system-capacity-analytics}.git"
!git remote add origin {remote_url}

# Stage required project files
!git add app.py requirements.txt README.md cleaned_uac_analytics.csv HHS_Unaccompanied_Alien_Children_Program.csv

# Commit changes
!git commit -m "feat: complete UAC care pipeline analytics and Streamlit app"

# Rename branch to main and push
!git branch -M main
!git push -u origin main --force

print(f"\n🚀 Successfully pushed to: https://github.com/{adityasingh121608-cell}/{uac-system-capacity-analytics}")
