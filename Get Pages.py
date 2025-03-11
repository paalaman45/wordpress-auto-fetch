import requests
import csv


def fetch_published_pages(domain, output_file):
    print("Processing...")
    api_url = f"https://{domain}/wp-json/wp/v2/pages"
    pages = []
    page_number = 1

    while True:
        response = requests.get(api_url, params={"status": "publish", "per_page": 50, "page": page_number})

        if response.status_code != 200:
            print(f"Failed to fetch pages: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        pages.extend(data)
        page_number += 1

    if pages:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Title", "Link", "Meta Title", "MetaDescription"])

            for page in pages:
                meta_title = page.get('yoast_head_json', {}).get('title', 'N/A')
                meta_description = page.get('yoast_head_json', {}).get('description', 'N/A')
                writer.writerow([page['id'], page['title']['rendered'], page['link'], meta_title, meta_description])

        print(f"Successfully saved {len(pages)} pages to {output_file}")
    else:
        print("No published pages found.")

if __name__ == "__main__":
    print("Welcome, this simple code will fetch the WordPress Sites Pages")
    domain = input("Enter the WordPress domain (without https://): ")
    output_file = input("Enter the output CSV file name: ")

    fetch_published_pages(domain, output_file)
