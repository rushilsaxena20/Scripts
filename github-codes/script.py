from github import Github
import sys
from github import GithubException
import requests
import get_secret

def repoaccess(token, org_name, repo_name, user_name, permission):
     # Authenticate with the GitHub API
    g = Github(token)

    # Get the organization object
    org = g.get_organization(org_name)

     # Get the user object
    user = g.get_user(user_name)
    
    repos = repo_name.strip("[]").replace(" ","").split(",")

    for repo in repos:
    # Get the repository object
        print(type(repo))
        repo = org.get_repo(repo)
        try:
            if permission == 'read':
                repo.add_to_collaborators(user, permission='read')
            elif permission == 'write':
                repo.add_to_collaborators(user, permission='write')
            else:
                print(f"Invalid permission level: {permission}")
            print(f"{permission.capitalize()} access granted to {user_name} for {repo}")
        except GithubException as e:
            print(f"Failed to grant {permission} access to {user_name} for {repo}: {e}")

def teamAccess(org_name, user_name, team_name, token):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    qp = {
        # 'filter': '2fa_disabled',
        'per_page': 100,
        'page': 1
    }
    data = '{"role":"member"}'
    i = 1
    flag = True
    count = 0
    team_slug=""
    while flag:
        qp['page']=i
        teams = requests.get(f'https://api.github.com/orgs/{org_name}/teams', headers=headers, params=qp)
        if len(teams.json()) == 0:
            flag = False
            break
        for team in teams.json():
            count = count+1
            if team['name'] == team_name:
                team_slug = team['slug']
                flag = False
                break
        i = i+1
    print(team_slug)
    response = requests.put(f'https://api.github.com/orgs/{org_name}/teams/{team_slug}/memberships/{user_name}', headers=headers, data=data)
    print(response.text)


# def main(token, org_name, team_name, user_name, permission, team_access):
#     if team_access.lower() == 'yes':
#         teamAccess(token, org_name, team_name, user_name)
#     else:
#         repoaccess()

if __name__ == '__main__':
    ACCESS_TOKEN = get_secret.get_secret('rushil_gh_token')
    print(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    if sys.argv[1] == 'yes':
        teamAccess('MoEngage', sys.argv[3], sys.argv[5], ACCESS_TOKEN)
    else:
        repoaccess(ACCESS_TOKEN, 'MoEngage', sys.argv[2], sys.argv[3], sys.argv[4])
    # main(ACCESS_TOKEN, 'MoEngage', sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])