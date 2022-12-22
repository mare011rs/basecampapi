import requests
import os
import datetime
import credentials
import json

keys = json.loads(credentials.get_credentials())

def get_access_token():
    client_id = keys['basecamp_client_id']
    client_secret = keys['basecamp_client_secret']
    redirect_url = keys['basecamp_redirect_uri']
    refresh_token = keys['basecamp_refresh_token']
    
    refresh_token_url = f"https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token={refresh_token}&client_id={client_id}&redirect_uri={redirect_url}&client_secret={client_secret}"
    access_token = requests.post(refresh_token_url).json()['access_token']
    return access_token

account_id = "3694081"
project_id = "######" # Enter project id
message_board_id = "######" # Enter message board id
base_url = f"https://3.basecampapi.com/{account_id}"

def get_sgid(path):
    attachments_url = f"{base_url}/attachments.json?name={path}"
    file_size = os.path.getsize(path)
    img_headers = {
        'Authorization': 'Bearer '+ get_access_token(),
        "Content-Type": "image/png",
        "Content-Length": str(file_size)
        }
    
    with open(path, "rb") as img_content:
        image_sgid = requests.post(attachments_url, headers=img_headers, data=img_content).json()['attachable_sgid']
        
    return image_sgid

class metrics:
    date = datetime.date.today() - datetime.timedelta(1)
    day_of_month = date.day
    year_month = date.strftime('%B %Y')
    bc_post_name = f"Daily Metrics - {year_month}"

def create_bc_post():
    url = f"{base_url}/buckets/{project_id}/message_boards/{message_board_id}/messages.json"
    headers = {
        "Authorization": "Bearer " + get_access_token(),
        "Content-Type": "application/json"
    }
    
    content = "<p><strong>Daily metrics for "+metrics.year_month+" will be posted in the comment section.</strong></p><br> \
    <p>Explore metrics in the <a href='https://ed8a34f1.us2a.app.preset.io/superset/dashboard/p/GRypvmnXzMl/'>KPI Dashboard</a>.<p> \
    <p>Learn about metrics on the <a href='https://docs.fishingbooker.org/data/daily-metrics'>documentation page</a>.</p><br> \
    <p>🚀 <em><span style='color: rgb(17, 138, 15);'>Boosts</span> are encouraged!</em></p> \
    <p>💬 <em><span style='color: rgb(207, 0, 0);'>Comment</span> only if necessary to avoid spamming everyone in the company.</em></p><br> \
    <p><em>If you notice something wrong with the metrics, you can ping me or write in Data team's <a href='https://3.basecamp.com/3694081/buckets/22348834/todolists/5214969729'>Inbox</a> or <a href='https://3.basecamp.com/3694081/buckets/22348834/chats/3779965909'>Campfire</a>.</em></p>"
    
    data = str('{"subject": "'+metrics.bc_post_name+'", "content": "'+content+'", "status": "active"}').encode()

    requests.post(url, headers=headers, data=data)

def post_metrics():
    message_board_url = f"{base_url}/buckets/{project_id}/message_boards/{message_board_id}/messages.json"
    headers = {
        "Authorization": "Bearer " + get_access_token(),
        "Content-Type": "application/json"
    }
    messages = requests.get(message_board_url, headers=headers).json()
    
    if not(any(msg['subject'] == metrics.bc_post_name for msg in messages)):
        create_bc_post()
        messages = requests.get(message_board_url, headers=headers).json()
        
    for msg in messages:
        if msg['subject'] == metrics.bc_post_name:
            message_id = msg['id']
    
    comment_url = f"{base_url}/buckets/{project_id}/recordings/{message_id}/comments.json"
    
    images = []
    for file in sorted(os.listdir("/tmp/images")):
        if file.endswith(".png"):
            image = {
                "name": os.path.basename(file),
                "sgid": get_sgid(f"/tmp/images/{file}")
            }
            images.append(image)
    
    content = ''
    for image in images:
        content += "<bc-attachment sgid='"+image['sgid']+"'></bc-attachment> \
            <br> \
            "
    content += "- <a href='https://ed8a34f1.us2a.app.preset.io/superset/dashboard/p/GRypvmnXzMl/'>KPI Dashboard</a> <br> \
        - <a href='https://datastudio.google.com/reporting/8c88333b-a69b-47ae-8dcd-9163a8732b09'>Additional metrics dashboard</a> <br> \
        - <a href='https://docs.fishingbooker.org/data/daily-metrics'>Metrics documentation</a> <br><br> \
        <em style='color: rgb(102, 102, 102);'>This is an automated post. If you notice something wrong with the metrics, you can ping me or write in Data team's <a href='https://3.basecamp.com/3694081/buckets/22348834/todolists/5214969729'>Inbox</a> or <a href='https://3.basecamp.com/3694081/buckets/22348834/chats/3779965909'>Campfire</a>.</em>"
    
    requests.post(comment_url, headers=headers, data='{"content": "'+content+'"}')