import requests
import json

# Your GitHub token;
GITHUB_TOKEN = ""

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# List of organizations
response1 = requests.get("https://api.github.com/user/orgs", headers=headers)
if response1.status_code == 200:
    org_data = json.loads(response1.text)
    orgs = [org["login"] for org in org_data]
else:
    print("Failed to fetch organizations.")
    exit(1)


# Loop through each organization
for org in orgs:
    # Fetch repositories in the current organization
    response = requests.get(f"https://api.github.com/orgs/{org}/repos", headers=headers)
    #print(response.text)
    repos = json.loads(response.text)
    
    # Loop through each repository
    for repo in repos:
        repo_name = repo["name"]
        
        # Define your content
        with open('/Users/gauravarora/Documents/commit.txt', 'r') as f:
            pre_commit_content = f.read()

        
        # Base64 encode your content
        import base64
        encoded_content = base64.b64encode(pre_commit_content.encode()).decode()
        
        # Data to create a new file
        data = {
            "message": "Adding pre-commit hook",
            "content": encoded_content
        }
        
        # Create or update the file. currently its create file in root of project
        response = requests.put(
            f"https://api.github.com/repos/{org}/{repo_name}/contents/pre-commit.yaml",
            headers=headers,
            data=json.dumps(data)
        )
        #print(response.text)
        
        if response.status_code in [200, 201]:
            print(f"Successfully updated pre-commit hook in {repo_name}")
        else:
            print(f"Failed to update pre-commit hook in {repo_name}")
