import sys
import os
from sec_edgar_downloader import Downloader

# 1. Setup - The SEC requires a User-Agent string with a valid email
# Replace with your actual email (it's for their internal logging only)
EMAIL_ADDRESS = "s1032190676@gmail.com" 
ORG_NAME = "Personal-Portfolio-Project"

def download_10k_reports():
    # Initialize the downloader
    # It will download files to a folder named "sec-edgar-filings"
    # dl = Downloader(ORG_NAME, EMAIL_ADDRESS, "./data/minio_data/raw-data")
    dl = Downloader(ORG_NAME, EMAIL_ADDRESS, "C:\Project\compliance-llm-pipeline")


    tickers = ["NFLX"]
    
    print(f"Starting download for: {tickers}")
    
    for ticker in tickers:
        try:
            print(f"Downloading 10-K for {ticker}...")
            # Limit to the last 2 years (2023-2024) to keep it light
            dl.get("10-K", ticker, limit=2) 
            print(f"Successfully downloaded {ticker}")
        except Exception as e:
            print(f"Error downloading {ticker}: {e}")

if __name__ == "__main__":
    download_10k_reports()