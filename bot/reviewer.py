 import os
from google import genai
from github import Github, Auth

def main():
    # Auth
    token = os.environ["GITHUB_TOKEN"]
    gemini_key = os.environ["GEMINI_API_KEY"]
    repo_name = os.environ["REPO_NAME"]
    pr_number = int(os.environ["PR_NUMBER"])

    # Gemini setup (new SDK)
    client = genai.Client(api_key=gemini_key)

    # GitHub setup (new auth style)
    auth = Auth.Token(token)
    g = Github(auth=auth)

    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    # Get diff
    files = pr.get_files()
    diff_text = ""
    for f in files:
        diff_text += f"\n### {f.filename}\n"
        if f.patch:
            diff_text += f.patch

    prompt = f"""You are a senior code reviewer. Review this pull request diff and provide:
1. A brief summary of what changed
2. Any bugs or issues you spot
3. Suggestions for improvement
4. Overall assessment (Approve / Request Changes)

Here is the diff:
{diff_text}
"""

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    review_body = response.text
    pr.create_issue_comment(f"## 🤖 ReviewMate AI Review\n\n{review_body}")
    print("Review posted successfully!")

if __name__ == "__main__":
    main()
