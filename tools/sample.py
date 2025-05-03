import requests

def get_temperature(city: str) -> str:
    """
    Returns the current temperature of the city using wttr.in (no API key required).
    
    :param city: the name of the city
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data["current_condition"][0]["temp_C"]
        return f"{temp}°C"
    except Exception as e:
        return f"Error retrieving temperature: {e}"

def get_bitcoin_value() -> str:
    """
    Returns the current value of Bitcoin in USD using CoinGecko (no API key required).
    """
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = data["bitcoin"]["usd"]
        return f"${price}"
    except Exception as e:
        return f"Error retrieving Bitcoin value: {e}"
