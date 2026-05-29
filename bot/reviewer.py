import os
import google.generativeai as genai
from github import Github

# Connect to Gemini AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# Connect to GitHub
gh = Github(os.environ["GITHUB_TOKEN"])
repo = gh.get_repo(os.environ["GITHUB_REPOSITORY"])
pr_number = int(os.environ["PR_NUMBER"])
pr = repo.get_pull(pr_number)

# Get the changed code
code_diff = ""
for file in pr.get_files():
    code_diff += f"\n\nFile: {file.filename}\n"
    code_diff += file.patch or "(binary file)"

# Ask Gemini to review
prompt = f"""
You are a senior software engineer doing a code review.
Review this code and give feedback on:
- Bugs or errors
- Code quality
- Security concerns
- Suggestions

Code changes:
{code_diff}
"""

response = model.generate_content(prompt)
review = response.text

# Post review as PR comment
pr.create_issue_comment(f"## 🤖 ReviewMate AI\n\n{review}")
print("✅ Review posted!")
