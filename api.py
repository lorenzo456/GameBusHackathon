import json
import requests

def post_walk_activity(steps: int):
    url = "https://api.healthyw8.gamebus.eu/v2/activities?dryrun=false&fields=personalPoints"
    
    with open('walk_activity.json', 'r') as file:
        data = json.load(file)
        data['propertyInstances'] = [{"property":20,"value":steps}]
        
    with open('walk_activity.json', 'w') as file:
        json.dump(data, file)

    payload = {}
    files=[
        ('activity', ('walk_activity.json', open('walk_activity.json', 'rb'), 'application/json'))
    ]
    #update value in walk_activity.json

    headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZ2FtZWJ1c19hcGkiXSwidXNlcl9uYW1lIjoibC5qLmphbWVzK2FnZW50czFAdHVlLm5sIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIiwidHJ1c3QiLCJkZWxldGU6YWN0aXZpdHkiXSwiZXhwIjoxODIzMDg5ODU1LCJhdXRob3JpdGllcyI6WyJVU0VSIl0sImp0aSI6IlJ1ZzFpd201RGEzY19NLUtIVF84aFZMQTJiWSIsImNsaWVudF9pZCI6ImdhbWVidXNfc3R1ZGlvX2FwcCJ9.mjkXdOCfhxHFtPGrLfFvivU3SvKGzhDnKY8QHKpwIK9SHbzbKgQLIEMdvzprU6bAeTl9IhSQmXUCYlkyKtXVIGqIfGF7yZ1pFu-MNAoePRDPt1rjr6NMoEgKCAvCGTNK7Of5cM0MJS2UWs3fr9kMRXlFeKu8XtipG5kha9kwqsflh_L1Flw_4PZc73EfK0igCJ9PNHQBNFLIG1SwVgS0Qsw0S4V9GMQtOWRq1Fzt7IUlAcKTHVpMPnw6lNVvFX3PlYKCxm3GNjw0K-YI7iQSNJYZ1_BYPuP3EJwt13FyOi8XLH_3OqX9HrzRS8hWhXJbFFTih5nUieciHjtaaJthsw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
