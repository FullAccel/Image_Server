import requests


# url = "http://114.70.23.79:8080"
url = "http://0.0.0.0:8080"
def send_url(user_id, homework_id,saved_paths):
    endpoint = f"/submission/{user_id}/{homework_id}"

    try:
        response = requests.post(url+endpoint, json={"image_urls": saved_paths})
        response.raise_for_status()
        print("Request successful!")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
