def get_temperature(city: str) -> str:
    """
    Returns the current temperature of the city.
    
    :param city: the name of the city
    """
    
    if (city.lower() == "salvador"):
        return "28°C"
    elif (city.lower() == "aracajú"):
        return "27°C"
    elif (city.lower() == "maceió"):
        return "26°C"
    elif (city.lower() == "goiânia"):
        return "25°C"
        
    return "19°C"

def get_bitcoin_value() -> str:
    """
    Returns the current value of Bitcoin in USD.
    """
    return "$27,000"