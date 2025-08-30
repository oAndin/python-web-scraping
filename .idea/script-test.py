import requests
import re
import pandas as pd

def extract_ean_barcode(html_text):
    """
    Extracts the EAN barcode from the HTML content of a product page.

    This function uses a regular expression to find a 12 to 14-digit number
    that follows the keyword "ean" in a case-insensitive manner. It is
    designed to handle various formats and separators.

    Args:
        html_text (str): The HTML content of the product page.

    Returns:
        str: The first EAN barcode found, or None if no barcode is found.
    """
    # Regex to find "ean" (case-insensitive) followed by a colon, equals sign,
    # or other separators, and then capture a 12-14 digit number.
    pattern = re.compile(r'"ean"\s*[:=]\s*"?(\d{12,14})"?', re.IGNORECASE)
    match = pattern.search(html_text)

    if match:
        return match.group(1)

    # A more general pattern if the first one fails
    pattern = re.compile(r'ean\D*(\d{12,14})', re.IGNORECASE)
    match = pattern.search(html_text)
    if match:
        return match.group(1)

    return None

def main():
    """
    Main function to scrape EAN barcodes from a list of URLs and save them
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

    print("Starting barcode scraping process...")
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            html_content = response.text
            barcode = extract_ean_barcode(html_content)

            if barcode:
                results.append({'url': url, 'barcode': barcode})
                print(f"SUCCESS: Found barcode {barcode} for {url}")
            else:
                results.append({'url': url, 'barcode': 'Not Found'})
                print(f"INFO: No barcode found for {url}")

        except requests.exceptions.RequestException as e:
            print(f"ERROR: Could not fetch URL {url}. Reason: {e}")
            results.append({'url': url, 'barcode': 'Request Error'})

    # --- Output Generation ---

    # 1. Text File Output
    try:
        with open('barcodes.txt', 'w') as f:
            for item in results:
                f.write(f"{item['url']}, {item['barcode']}\n")
        print("\nSuccessfully created barcodes.txt")
    except IOError as e:
        print(f"ERROR: Could not write to barcodes.txt. Reason: {e}")

    # 2. Excel File Output
    try:
        df = pd.DataFrame(results)
        df.to_excel('barcodes.xlsx', index=False, header=["URL", "Barcode"])
        print("Successfully created barcodes.xlsx")
    except Exception as e:
        print(f"ERROR: Could not write to barcodes.xlsx. Reason: {e}")

if __name__ == "__main__":
    main()
