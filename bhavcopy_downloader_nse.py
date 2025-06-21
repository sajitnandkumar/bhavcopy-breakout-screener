import requests, os
from datetime import datetime, timedelta

# Create folder to store NSE Bhav Copies
os.makedirs("bhav_data_nse", exist_ok=True)

# Define date range
start_date = datetime(2020, 6, 1)
end_date = datetime.today() - timedelta(days=1)

# Get list of already downloaded files
downloaded_files = set(os.listdir("bhav_data_nse"))

# Loop through each date
while start_date <= end_date:
    # Skip weekends
    if start_date.weekday() >= 5:
        start_date += timedelta(days=1)
        continue

    date_str = start_date.strftime('%d%m%y')
    yyyy = start_date.strftime('%Y')
    mmm = start_date.strftime('%b').upper()
    file_name = f"cm{date_str}bhav.csv"
    url = f"https://www1.nseindia.com/content/historical/EQUITIES/{yyyy}/{mmm}/{file_name}"

    # Skip if already downloaded
    if file_name in downloaded_files:
        print(f"✅ Already downloaded: {file_name}")
        start_date += timedelta(days=1)
        continue

    print(f"Downloading: {url}")

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            with open(os.path.join("bhav_data_nse", file_name), "wb") as f:
                f.write(response.content)
            print(f"✅ Saved: {file_name}")
        else:
            print(f"❌ Not available for {start_date.strftime('%Y-%m-%d')} (likely a holiday)")
    except Exception as e:
        print(f"⚠️ Error on {start_date.strftime('%Y-%m-%d')}: {e}")

    start_date += timedelta(days=1)
