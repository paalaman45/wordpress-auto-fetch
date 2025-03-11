import requests
import csv

def fetch_media_images(domain, output_file):
    api_url = f"https://{domain}/wp-json/wp/v2/media"
    media_items = []
    page_number = 1

    while True:
        response = requests.get(api_url, params={"per_page": 50, "page": page_number})

        if response.status_code != 200:
            print(f"Failed to fetch media: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        media_items.extend(data)
        page_number += 1

    if media_items:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Image URL", "Alternative Text"])

            for media in media_items:
                if media.get('media_type') == 'image':
                    image_url = media.get('source_url', 'N/A')
                    writer.writerow([media['id'], media['title']['rendered'], image_url, media['alt_text']])

        print(f"Successfully saved {len(media_items)} media items to {output_file}")
    else:
        print("No media items found.")

if __name__ == "__main__":
    domain = input("Enter the WordPress domain (without https://): ")
    output_file = input("Enter the output CSV file name: ")

    fetch_media_images(domain, output_file)
