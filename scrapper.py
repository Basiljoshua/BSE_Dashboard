import requests
import os
from datetime import datetime

def download_bhav_copy(save_folder="data"):
    # Get today's date in YYYYMMDD format
    today = datetime.today().strftime("%Y%m%d")

    # Build the Bhav Copy URL based on observed pattern
    url = f"https://www.bseindia.com/download/BhavCopy/Equity/BhavCopy_BSE_CM_0_0_0_{today}_F_0000.CSV"
    print(url)

    print(f"📥 Trying to download: {url}")

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/138.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    
    if response.status_code != 200:
        print("❌ Bhav copy not available for today (maybe market holiday?)")
        return

    os.makedirs(save_folder, exist_ok=True)
    filename = today+".csv"
    save_path = os.path.join(save_folder, filename)

    with open(save_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Bhav copy saved to: {save_path}")

if __name__ == "__main__":
    download_bhav_copy()
