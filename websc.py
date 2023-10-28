import requests
from bs4 import BeautifulSoup
import random
import time
import csv
import sys

# Set the User-Agent header to mimic a web browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Initialize variables
page_number = 1

# change label here A-Z
label = sys.argv[1] 

base_url = 'https://www.1mg.com/drugs-all-medicines?label=' + label + '&page='

# Create a CSV file and write header row
csv_filename = 'medicine_data'+label+'.csv'
with open(csv_filename, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Medicine Name', 'Manufacturer', 'Medicine Type','Active Ingredient', 'MRP', 'Prescription Required'])

while True:
    # Create the URL for the current page
    url = base_url + str(page_number)

    # Send an HTTP GET request with the User-Agent header
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information for each product card on the page
        product_cards = soup.find_all('div', class_='style__product-card___1gbex')

        if not product_cards:
            # No more pages, exit the loop
            break

        for product_card in product_cards:
            # Extract the full product name and MRP as a single string
            product_name_mrp = product_card.find('div', class_='style__font-bold___1k9Dl').text
            # Split the product_name_mrp to separate the product name and MRP
            parts = product_name_mrp.split("MRP₹")
            product_name = parts[0].strip()
            mrp = parts[1].strip()

            # Extract prescription_required if found
            rx_element = product_card.find('div', class_='style__rx___3pKXG')
            prescription_required = rx_element.find('span').text if rx_element and rx_element.find('span') else 'Not specified'
            medicine_type = product_card.find_all('div', class_='style__padding-bottom-5px___2NrDR')[1].text
            manufacturer = product_card.find_all('div', class_='style__padding-bottom-5px___2NrDR')[2].text
            active_ingredient = product_card.find('div', class_='style__product-content___5PFBW').text

            # Print the extracted data for each product
            print(f"Product Name: {product_name}")
            print(f"MRP: {mrp}")
            print(f"Type: {medicine_type} ")
            print(f"Prescription Required: {prescription_required}")
            print(f"Manufacturer: {manufacturer}")
            print(f"Active Ingredient: {active_ingredient}")
            print()

            # Append data to the CSV file
            with open(csv_filename, mode='a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([product_name, manufacturer, medicine_type, active_ingredient, mrp,prescription_required])

        # Increment the page number for the next iteration
        page_number += 1

        # Add a random interval (between 3 and 10 seconds) before the next request
        interval = random.uniform(1, 5)
        print(f"Waiting for {interval:.2f} seconds before the next request...")
        time.sleep(interval)

    else:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
        break  # Exit the loop if there's an issue with a page request
