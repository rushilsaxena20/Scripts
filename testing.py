import requests
import json

def listusers():
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer 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',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    qp = {
        # 'filter': '2fa_disabled',
        'per_page': 100,
        'page': 0
    }
    i=1
    users = 0
    flag = True
    while flag:
        qp['page']=i
        response = requests.get('https://api.github.com/orgs/MoEngage/members', headers=headers, params=qp)
        if len(response.json())==0:
            flag = False
        users = users+len(response.json())
        for name in response.json():
            print(name['login'])
        i=i+1
    print(users, i)
# If a users is present or not, update the GUI (for team).
# Build Harness pipeline.
# invite user to a github team

#-------------------------- Check if a user is present in org or not -------------------------------  
def checkuser():
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer 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',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    username = 'umangmoe'
    response = requests.get(f'https://api.github.com/orgs/MoEngage/members/{username}', headers=headers)
    if response.status_code == 404:
        print('User not present in org.')
    elif response.status_code == 302:
        print('please check auth token')
    else:
        print('User is org member')
    # if 'User does not exist or is not a member of the organization' in json.loads(response.text)['message']:
    #     print('User not present in org.')
    # else:
    #     print('user present')

def inviteuser(email):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer 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',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    data = {"email":"","role":"direct_member","team_ids":[]}
    data['email'] = email
    print(data)
    response = requests.post('https://api.github.com/orgs/MoEngage/invitations', headers=headers, data=json.dumps(data))
    print(response.text)

# inviteuser("jayant.choudhary@moengage.com")
# listusers()
def listteams(team_name):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer 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',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    qp = {
        # 'filter': '2fa_disabled',
        'per_page': 100,
        'page': 1
    }
    i = 1
    flag = True
    count = 0
    team_slug=""
    while flag:
        qp['page']=i
        teams = requests.get('https://api.github.com/orgs/MoEngage/teams', headers=headers, params=qp)
        if len(teams.json()) == 0:
            flag = False
            break
        for team in teams.json():
            count = count+1
            # if team['name'] == team_name:
            #     team_slug = team['slug']
            #     flag = False
            #     break
        i = i+1
    print(team_slug, count)

# listteams('Infra Requests')
# listusers()
listteams('haha')