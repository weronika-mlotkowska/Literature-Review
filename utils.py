import requests
from typing import Dict
import os
import json

API_KEY = '' #your API key
Insttoken='' #your Institution Token

HEADERS = {
    "Accept": "application/json",
    "X-ELS-APIKey": API_KEY,
    "X-ELS-Insttoken":Insttoken
}

def get_work(doi:str,url:str) -> Dict:
    if not API_KEY:
        raise ValueError("API_KEY and/or Insttoken must be set before running.")
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        return data
    except Exception as e:
        print(f"Error fetching work for {doi}: {str(e)}")
        if r.status_code == 401 :
            raise Exception("401 Client Error: Invalid authentication credentials (API key or Institution Token).")
        
class JSONResultWriter():
    def write(self, report: Dict[str, object], file_name: str,directory:str) -> None:
        if not os.path.exists(directory):
            os.makedirs(directory)
        output_file = os.path.join(directory, file_name)
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)