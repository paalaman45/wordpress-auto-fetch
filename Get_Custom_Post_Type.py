import requests
import csv
import time


def validate_post_type(domain, post_type):
    """Check if the custom post type exists in the WordPress API."""
    api_url = f"https://{domain}/wp-json/wp/v2/types"
    response = requests.get(api_url)

    if response.status_code == 200:
        available_types = response.json().keys()
        return post_type in available_types
    return False


def fetch_custom_posts(domain, post_type, output_file):
    """Fetch posts of a specific custom post type and save to CSV."""
    print(f"Fetching '{post_type}' posts from {domain}...")
    api_url = f"https://{domain}/wp-json/wp/v2/{post_type}"
    posts = []
    page_number = 1

    while True:
        response = requests.get(api_url, params={"status": "publish", "per_page": 50, "page": page_number})

        if response.status_code == 429:  # Handle rate limits
            print("Rate limit exceeded. Retrying in 10 seconds...")
            time.sleep(10)
            continue

        if response.status_code != 200:
            print(f"Failed to fetch posts: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        posts.extend(data)
        page_number += 1
        time.sleep(1)  # Prevent hitting API rate limits too quickly

    if posts:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Title", "Link", "Meta Title", "Meta Description"])

            for post in posts:
                meta_title = post.get('yoast_head_json', {}).get('title', 'N/A')
                meta_description = post.get('yoast_head_json', {}).get('description', 'N/A')
                writer.writerow([post['id'], post['title']['rendered'], post['link'], meta_title, meta_description])

        print(f"Successfully saved {len(posts)} '{post_type}' posts to {output_file}")
    else:
        print(f"No published '{post_type}' posts found.")


if __name__ == "__main__":
    print("Welcome! This script fetches WordPress custom post type entries.")

    domain = input("Enter the WordPress domain (without https://): ").strip()
    if not domain:
        print("Invalid domain. Please enter a valid WordPress domain.")
        exit()

    # Validate custom post type
    while True:
        post_type = input("Enter the custom post type (e.g., posts, pages, portfolio, etc.): ").strip()
        if validate_post_type(domain, post_type):
            break
        else:
            print(f"Invalid post type '{post_type}'. Please enter a valid custom post type.")

    output_file = input("Enter the output CSV file name: ").strip()
    if not output_file.endswith(".csv"):
        output_file += ".csv"

    fetch_custom_posts(domain, post_type, output_file)
