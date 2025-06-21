import requests, zipfile, io, os
from datetime import datetime, timedelta

# Create folder to store BSE Bhav Copies
os.makedirs("bhav_data_bse", exist_ok=True)

# Define date range
start_date = datetime(2020, 6, 1)
end_date = datetime.today() - timedelta(days=1)

# Get list of already downloaded files
downloaded_files = set(os.listdir("bhav_data_bse"))

# Format switch date
format_switch_date = datetime(2024, 7, 8)

# Loop through each date
while start_date <= end_date:
    # Skip weekends
    if start_date.weekday() >= 5:
        start_date += timedelta(days=1)
        continue

    date_str_old = start_date.strftime('%d%m%y')
    date_str_new = start_date.strftime('%Y%m%d')

    if start_date < format_switch_date:
        zip_name = f"EQ{date_str_old}_CSV.ZIP"
        csv_name = f"EQ{date_str_old}.CSV"
        url = f"https://www.bseindia.com/download/BhavCopy/Equity/{zip_name}"
    else:
        csv_name = f"BhavCopy_BSE_CM_0_0_0_{date_str_new}_F_0000.CSV"
        url = f"https://www.bseindia.com/download/BhavCopy/Equity/{csv_name}"

    # Skip if already downloaded
    if csv_name in downloaded_files:
        print(f"✅ Already downloaded: {csv_name}")
        start_date += timedelta(days=1)
        continue

    print(f"Downloading: {url}")

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            if start_date < format_switch_date:
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    z.extract(csv_name, path="bhav_data_bse")
            else:
                with open(os.path.join("bhav_data_bse", csv_name), "wb") as f:
                    f.write(response.content)
            print(f"✅ Saved: {csv_name}")
        else:
            print(f"❌ Not available for {start_date.strftime('%Y-%m-%d')} (likely a holiday)")
    except Exception as e:
        print(f"⚠️ Error on {start_date.strftime('%Y-%m-%d')}: {e}")

    start_date += timedelta(days=1)
