import requests

def checkrepo(repos):
    badrep=[]
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer <token>',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    for repo in repos:
        response = requests.get(f'https://api.github.com/repos/MoEngage/{repo}', headers=headers)
        if response.status_code == 404:
            badrep.append(repo)
        if len(badrep)!=0:
            print(badrep)

repos = ['rushil','eventstore-poc']
checkrepo(repos)