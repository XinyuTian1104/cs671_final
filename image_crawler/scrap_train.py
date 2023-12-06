import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from tqdm import tqdm

# Create a directory to store the downloaded images
os.makedirs('../downloaded_images', exist_ok=True)

def download_image(url, index):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # This will raise an exception for HTTP errors

        # Naming the image based on the index
        file_extension = url.split('.')[-1].strip()
        name = f"{index}.{file_extension}"

        # Save the image
        with open(os.path.join('downloaded_images', name), 'wb') as file:
            file.write(response.content)
        return f"Image {index} downloaded successfully."
    except Exception as e:
        return f"Error downloading image {index}: {e}"

def main():
    with open('train_picture_url.txt', 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    # Using ThreadPoolExecutor to download images in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Create a list to hold the futures
        futures = {executor.submit(download_image, url, index): index for index, url in enumerate(urls)}

        # Iterate over the futures as they complete (i.e., when downloads finish)
        for future in as_completed(futures):
            print(future.result())

if __name__ == "__main__":
    main()
