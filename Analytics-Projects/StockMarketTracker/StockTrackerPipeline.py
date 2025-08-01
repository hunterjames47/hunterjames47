# Databricks notebook source
import os
import time
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from io import BytesIO

# COMMAND ----------

load_dotenv(override=True)

# COMMAND ----------

storage_account_name = os.getenv("STORAGE_ACCOUNT_NAME")
container_name = os.getenv("STORAGE_CONTAINER_NAME")
sas_token=os.getenv("Storage_SAS_Token")

# COMMAND ----------

blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net",
    credential=sas_token
)

# COMMAND ----------

blob_name = "market_data.parquet"
container_client = blob_service_client.get_container_client(container_name)

# COMMAND ----------

try:
    blob_client = container_client.get_blob_client(blob_name)
    blob_props = blob_client.get_blob_properties()
    
    # Check size first
    if blob_props.size > 0:
        stream = BytesIO()
        stream.write(blob_client.download_blob().readall())
        stream.seek(0)
        df = pd.read_parquet(stream)
    else:
        display("Blob exists but is empty. Initializing empty DataFrame.")
        df = pd.DataFrame()
except ResourceNotFoundError:
    display("Blob does not exist. Initializing empty DataFrame.")
    df = pd.DataFrame()

# COMMAND ----------

api_key = os.getenv("Polygon_API_Key")
today = date.today()
TwoYrAgo = today - relativedelta(years=2)


# COMMAND ----------

def get_polygon_data(ticker, start, end):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}?adjusted=true&sort=asc&apiKey={api_key}"
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Error fetching {ticker}: {r.text}")
        return pd.DataFrame()
    data = r.json().get("results", [])
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["t"], unit="ms")
    df = df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"})
    df = df[["date", "open", "high", "low", "close", "volume"]]
    df["ticker"] = ticker
    return df

# COMMAND ----------

if not df.empty:
    LastLoad = df['date'].max()
else:
    LastLoad = None
maxDate = df['date'].max() if LastLoad else pd.Timestamp(TwoYrAgo)
start_date = maxDate.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

# COMMAND ----------

tickers = {
    "stocks": ["AAPL", "MSFT", "SPY", "QQQ", "TSLA", "NVDA", "AMZN", "META"],
    "cryptos": ["X:BTCUSD", "X:ETHUSD"]
}

# COMMAND ----------

display(f"LastLoad: {LastLoad}")
display(f"maxDate: {maxDate}")
display(f"start_date: {start_date}")
display(f"end_date: {end_date}")

# COMMAND ----------

all_new_data = []
call_count = 0

for category, t_list in tickers.items():
    for t in t_list:
        display(f"Fetching {t} from {start_date} to {end_date}")
        df = get_polygon_data(t, start_date, end_date)
        if not df.empty:
            df["category"] = category
            all_new_data.append(df)
        call_count += 1
        if call_count >= sum(len(v) for v in tickers.values()):
            display("All tickers have been collected")
            break
        # Pause after every 5 API calls (free tier limit)
        if call_count % 5 == 0:
            display("Reached 5 calls, pausing for 60 seconds...")
            time.sleep(60)
        else:
            time.sleep(0.25) 

# COMMAND ----------

if all_new_data:
    new_df = pd.concat(all_new_data)
    updated_df = pd.concat([df, new_df], ignore_index=True).drop_duplicates()

    parquet_buffer = BytesIO()
    updated_df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)

    # Upload (overwrites existing blob)
    container_client.upload_blob(
        name=blob_name,
        data=parquet_buffer,
        overwrite=True,
        metadata={"updated_by": "databricks_script"}
    )
    display(f"Added {len(new_df)} new rows to {blob_name}.")
else:
    display("No new data to append.")