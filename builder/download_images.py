import os
import csv
import re
import requests
import time
from urllib.parse import quote

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '../dist/gift_ideas_1200.csv')
IMAGES_DIR = os.path.join(BASE_DIR, '../dist/images')
MAX_ITEMS = None # Process all

def clean_filename(name):
    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')
    return clean_name

def download_image(name, save_path):
    encoded_name = quote(name)
    url = f"https://image.pollinations.ai/prompt/{encoded_name}?width=600&height=450&nologo=true"
    
    max_retries = 5
    base_delay = 20
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30, stream=True)
            if response.status_code == 429:
                delay = base_delay * (2 ** attempt)
                print(f"Rate limited (429). Retrying in {delay} seconds... (Attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
                continue
                
            response.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            delay = base_delay * (2 ** attempt)
            print(f"Network error: {e}. Retrying in {delay} seconds... (Attempt {attempt+1}/{max_retries})")
            time.sleep(delay)
        except Exception as e:
            print(f"Failed to download {name} due to unexpected error: {e}")
            return False
            
    return False

def main():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    items_processed = 0
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 5:
                continue
            
            if row[0].lower() == 'id' or not row[0].isdigit():
                continue

            if MAX_ITEMS is not None and items_processed >= MAX_ITEMS:
                break
            
            name = row[4]
            filename = clean_filename(name) + '.jpg'
            save_path = os.path.join(IMAGES_DIR, filename)

            if os.path.exists(save_path):
                print(f"Skipping {name} (already downloaded)")
                continue

            print(f"Generating and downloading image for: {name}")
            success = download_image(name, save_path)
            if success:
                print(f"Successfully downloaded image for {name}")
            else:
                print(f"Failed to download image for {name}")
            
            # Sleep 10 seconds to avoid 429 Too Many Requests
            time.sleep(10)
            items_processed += 1

    print("Finished downloading images.")

if __name__ == '__main__':
    main()
