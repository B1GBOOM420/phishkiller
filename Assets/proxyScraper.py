import requests


def scrape_proxies(api_url, file_name="proxies.txt"):
    """
    Download the proxy list from the API endpoint and save it to a file.
    Overwrite the file if it already exists.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        proxies = clean_proxies(response.text)
        save_proxies_to_file(proxies, file_name)
        print(f"Proxies downloaded and saved to {file_name}.")
    except requests.RequestException as e:
        print(f"Error downloading proxies: {e}")


def clean_proxies(proxies_text):
    """
    Remove leading and trailing whitespace from each line in the proxy list.
    """
    return "\n".join(line.strip() for line in proxies_text.splitlines() if line.strip())


def save_proxies_to_file(proxies, file_name):
    """
    Save the cleaned proxy list to a file, overwriting the file if it already exists.
    """
    with open(file_name, "w") as file:
        file.write(proxies)


# Example usage
api_url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=text&anonymity=Elite&timeout=1500"
scrape_proxies(api_url)
