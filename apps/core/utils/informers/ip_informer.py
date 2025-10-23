import urllib.request
import urllib.error
import json
from typing import Optional, Dict, Any


class IPInfoService:
    BASE_URL = "http://ip-api.com/json/"
    FIELDS = [
        'status', 'message', 'country', 'countryCode', 'region', 'regionName',
        'city', 'zip', 'lat', 'lon', 'timezone', 'isp', 'org', 'as',
        'mobile', 'proxy', 'hosting', 'query'
    ]

    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address

    def get_info(self) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{self.ip_address}" if self.ip_address else self.BASE_URL
        params = f"?fields={','.join(self.FIELDS)}"

        try:
            with urllib.request.urlopen(f"{url}{params}", timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

                if data.get('status') == 'fail':
                    raise ValueError(data.get('message', 'Unknown error'))

                return data

        except urllib.error.URLError as e:
            raise ValueError(f"Network error: {e.reason}")
        except json.JSONDecodeError:
            raise ValueError("Invalid API response")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")
