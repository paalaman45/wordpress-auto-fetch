import requests
import csv

# WooCommerce API credentials
store_url = ""
consumer_key = ""
consumer_secret = ""

# API Endpoint for products
endpoint = f"{store_url}/wp-json/wc/v3/products"

# Request parameters to fetch only published products
params = {
    "status": "publish",
    "per_page": 100  # Adjust as needed (max 100 per request)
}

# Make the request
response = requests.get(endpoint, params=params, auth=(consumer_key, consumer_secret))

if response.status_code == 200:
    products = response.json()

    # Define CSV file name
    csv_file = "woocommerce_products.csv"

    # Open CSV file for writing
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["ID", "Name", "Category", "Tags", "Short Description", "Description", "Product Link"])

        # Write product data
        for product in products:
            product_id = product.get("id")
            name = product.get("name")
            categories = ", ".join([cat["name"] for cat in product.get("categories", [])])
            tags = ", ".join([tag["name"] for tag in product.get("tags", [])])
            short_desc = product.get("short_description").strip()  # Remove unwanted whitespace
            description = product.get("description").strip()
            product_link = product.get("permalink")

            writer.writerow([product_id, name, categories, tags, short_desc, description, product_link])

    print(f"Data saved to {csv_file}")

else:
    print(f"Failed to fetch data. Status Code: {response.status_code}")
    print(response.text)
