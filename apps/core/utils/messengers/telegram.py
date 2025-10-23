import json
import urllib.request
import urllib.error
import urllib.parse


class TelegramMessenger:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

    def send_message(self, chat_id, message):
        url = f"{self.base_url}sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message
        }

        data_bytes = json.dumps(data).encode('utf-8')

        try:
            request = urllib.request.Request(
                url,
                data=data_bytes,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode('utf-8'))

        except urllib.error.HTTPError as e:
            error_message = e.read().decode('utf-8')
            raise Exception(f"HTTP Error {e.code}: {error_message}")
        except Exception as e:
            raise Exception(f"Error sending message: {str(e)}")
