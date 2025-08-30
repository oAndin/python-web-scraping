import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def extract_product_name(soup):
    """
    Extracts the product name from the BeautifulSoup object of a product page.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the product page.

    Returns:
        str: The product name, or 'Not Found' if not found.
    """
    try:
        # VTEX platform often uses this class for the product name
        name_element = soup.find('h1', class_='vtex-store-components-3-x-productNameContainer')
        if name_element:
            return name_element.text.strip()
        return 'Not Found'
    except Exception:
        return 'Not Found'

def extract_product_price(soup):
    """
    Extracts the product price from the BeautifulSoup object of a product page.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the product page.

    Returns:
        str: The product price, or 'Not Found' if not found.
    """
    try:
        # Find the container for the price
        price_container = soup.find('span', class_='vtex-store-components-3-x-currencyContainer')
        if price_container:
            # Extract the integer and fraction parts of the price
            integer_part = price_container.find('span', class_='vtex-store-components-3-x-currencyInteger').text
            fraction_part = price_container.find('span', class_='vtex-store-components-3-x-currencyFraction').text
            # Combine the parts to form the full price
            return f"R$ {integer_part},{fraction_part}"

        # Fallback to the old method if the new one fails
        price_element = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue')
        if price_element:
            return price_element.text.strip()

        return 'Not Found'
    except Exception:
        return 'Not Found'

def extract_ean_barcode(html_text):
    """
    Extracts the EAN barcode from the HTML content of a product page.

    This function uses a regular expression to find a 12 to 14-digit number
    that follows the keyword "ean" in a case-insensitive manner.

    Args:
        html_text (str): The HTML content of the product page.

    Returns:
        str: The first EAN barcode found, or 'Not Found' if no barcode is found.
    """
    # Regex to find "ean" followed by separators and a 12-14 digit number.
    # This pattern is more specific and less prone to false positives.
    pattern = re.compile(r'"ean"\s*:\s*"(\d{12,14})"', re.IGNORECASE)
    match = pattern.search(html_text)
    if match:
        return match.group(1)

    # A more general pattern if the first one fails
    pattern = re.compile(r'ean\D*(\d{12,14})', re.IGNORECASE)
    match = pattern.search(html_text)
    if match:
        return match.group(1)

    return 'Not Found'

def main():
    """
    Main function to scrape product data from a list of URLs and save it
    to .txt and .xlsx files.
    """
    # Predefined list of URLs to process
    urls = [
        "https://www.paguemenos.com.br/inalador-nebulizador-pague-menos-portatil-ultrassonico-mesh-nb1100/p?skuId=100141",
        "https://www.paguemenos.com.br/fralda-pampers-confort-sec-giga-tamanho-xxg-com-60-unidades/p",
        "https://www.paguemenos.com.br/fralda-pampers-confort-sec-xxg-56-unidades-o17a490578845z57/p",
        "https://www.paguemenos.com.br/fralda-pampers-confort-sec-p-72-unidades/p",
        # Add more URLs here
    ]

    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("Starting product data scraping process...")
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'lxml')

            # Extract all required data points
            name = extract_product_name(soup)
            price = extract_product_price(soup)
            barcode = extract_ean_barcode(html_content)

            result_data = {
                'url': url,
                'product_name': name,
                'price': price,
                'barcode': barcode
            }
            results.append(result_data)

            print(f"SUCCESS: Scraped '{name}' from {url}")

        except requests.exceptions.RequestException as e:
            print(f"ERROR: Could not fetch URL {url}. Reason: {e}")
            results.append({
                'url': url,
                'product_name': 'Request Error',
                'price': 'Request Error',
                'barcode': 'Request Error'
            })

    # --- Output Generation ---

    # 1. Text File Output
    try:
        with open('barcodes.txt', 'w', encoding='utf-8') as f:
            # Write header
            f.write("URL, Product Name, Price, Barcode\n")
            for item in results:
                f.write(f"{item['url']}, {item['product_name']}, {item['price']}, {item['barcode']}\n")
        print("\nSuccessfully created barcodes.txt")
    except IOError as e:
        print(f"ERROR: Could not write to barcodes.txt. Reason: {e}")

    # 2. Excel File Output
    try:
        df = pd.DataFrame(results)
        # Ensure correct column order
        df = df[['url', 'product_name', 'price', 'barcode']]
        df.to_excel('barcodes.xlsx', index=False, header=["URL", "Product Name", "Price", "Barcode"])
        print("Successfully created barcodes.xlsx")
    except Exception as e:
        print(f"ERROR: Could not write to barcodes.xlsx. Reason: {e}")

if __name__ == "__main__":
    main()
