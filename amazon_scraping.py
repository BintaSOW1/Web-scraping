import requests
from bs4 import BeautifulSoup
import csv

# Part 1: Web Scraping
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
page_count = 20

data = []
session = requests.Session()

for page_number in range(1, page_count + 1):
    url = f"{base_url}&page={page_number}"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")



    products = soup.find_all("div", class_="s-result-item")
    for product in products:
        product_url = product.find("a", class_="a-link-normal")
        product_name = product.find("span", class_="a-text-normal")
        product_price = product.find("span", class_="a-offscreen")
        rating = product.find("span", class_="a-icon-alt")
        num_reviews = product.find("span", class_="a-size-base")
        #asin_element= product.find("span", class_="a-text-bold"),             
        #manufacturer_element = product.find("span", class_="a-text-bold") 

        if product_url:
            product_url = "https://www.amazon.in" + product_url.get("href")

            if product_name:
                product_name = product_name.text.strip()
            else:
                product_name = "N/A"

            if product_price:
                product_price = product_price.text.strip()
            else:
                product_price = "N/A"

            if rating:
                rating = rating.text.strip().split()[0]
            else:
                rating = "N/A"

            if num_reviews:
                num_reviews = num_reviews.text.strip().replace(",", "")
            else:
                num_reviews = "N/A"


            item_data = {
                "Product URL": product_url,
                "Product Name": product_name,
                "Product Price": product_price,
                "Rating": rating,
                "Number of Reviews": num_reviews,
                "Description": " ",       
                "ASIN": " ",            
                "Manufacturer": " "     
            }

            data.append(item_data)

# Part 2: Enhancing Product Data
for item in data:
    product_url = item["Product URL"]
    product_response = requests.get(product_url)
    product_soup = BeautifulSoup(product_response.text, "html.parser")

    #code to extract Description, ASIN, Product Description, Manufacturer ...
    product_description = product_soup.find("meta", attrs={"name": "description"})
    if product_description:
        product_description = product_description.get("content")

    asin_element = product_soup.find("th", string="ASIN")
    if asin_element:
        asin_element = asin_element.find_next("td").text.strip()

    manufacturer_element = product_soup.find("a", href=lambda href: href and "seller=" in href)
    if manufacturer_element:
        manufacturer_element = manufacturer_element.get_text(strip=True)

    item["Description"] = product_description if product_description else "N/A"
    item["ASIN"] = asin_element if asin_element else "N/A"
    item["Manufacturer"] = manufacturer_element if manufacturer_element else "N/A"

# Export to CSV
csv_filename = "amazon_product_dat.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews", "Description", "ASIN", "Manufacturer"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Data has been scraped and exported to {csv_filename}")

