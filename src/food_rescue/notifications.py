import requests


def send_food_rescue_notification(topic_name: str, food_message: str):
    requests.post(f"https://ntfy.sh/zomato_{topic_name}",
    data=food_message.encode(encoding='utf-8'))

def get_notification_link(topic_name: str, ):
    return f"https://ntfy.sh/zomato_{topic_name}"

