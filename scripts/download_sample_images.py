import os
import requests

image_folder = "data/product_images"
os.makedirs(image_folder, exist_ok=True)

print("Downloading 50 sample product images...")

for i in range(1, 51):
    url = f"https://picsum.photos/400/400?random={i}"
    file_path = os.path.join(image_folder, f"product_{i}.jpg")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {file_path}")
        else:
            print(f"Failed to download image {i} (status {response.status_code})")
    except Exception as e:
        print(f"Error downloading image {i}: {e}")

print("Done downloading images.")
