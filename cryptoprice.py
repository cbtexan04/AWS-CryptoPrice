import difflib
import json
import requests

JSON_FILE = "data/cryptotickers.json"

def get_price(name):
    cryptos = json.load(JSON_FILE)

    name, ticker = get_key_value(name, cryptos)
    if not name:
        raise KeyError('currency not found')

    api_link = "https://min-api.cryptocompare.com/data/price?fsym={0}&tsyms=USD".format(ticker)
    api_response = requests.get(api_link)
    price = api_response.json().get("USD", 'Unavailable')

    return price

def currency_supported(name):
    cryptos = json.load(JSON_FILE)

    crypto_name, crypto_symbol = get_key_and_value_match(name, cryptos)
    if not crypto_name:
        return False

def get_key_value(key_word, dictionary):
    """
    Takes a key word and finds the key or value inside the dictionary which
    matches it and returns the corresponding key and value pair. If there is
    no direct match, the nearest key or value is then found.
    Dictionary is expected to be with lower case keys and upper case values.
    """
    reverse_dictionary = {dictionary[k]: k for k in dictionary}
    if key_word in dictionary:
        key = key_word
        value = dictionary[key_word]
    elif key_word in reverse_dictionary:
        key = reverse_dictionary[key_word]
        value = key_word
    else:
        all_names = {k.lower(): k for k in dictionary.keys()}
        all_names.update({v.lower(): v for v in dictionary.values()})
        closest_guesses = difflib.get_close_matches(key_word.lower(), all_names)
        if len(closest_guesses) > 0:
            closest_guess = all_names[closest_guesses[0]]
            if closest_guess in dictionary.keys():
                key = closest_guess
                value = dictionary[closest_guess]
            elif closest_guess in reverse_dictionary.keys():
                key = reverse_dictionary[closest_guess]
                value = closest_guess

    return key, value
