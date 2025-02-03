import requests

def send_push_notification_to_admin(player_id, message):
    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        'Authorization': 'Basic YOUR_REST_API_KEY',  # کلید REST API خود را وارد کنید
        'Content-Type': 'application/json'
    }
    payload = {
        "app_id": "YOUR_ONESIGNAL_APP_ID",  # شناسه اپلیکیشن OneSignal خود را وارد کنید
        "include_player_ids": [player_id],
        "headings": {"en": "New Message from Expert"},
        "contents": {"en": message}
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
