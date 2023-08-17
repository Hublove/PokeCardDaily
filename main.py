from select import select
import tweepy
import keys
import requests
import json
import math
import random
import requests
from time import sleep
from currency_converter import CurrencyConverter



#pokemon_cards = Card.where(q='supertype:pokemon',  page=1, pageSize=10, select='id')


#api_url = "https://api.pokemontcg.io/v2/cards?page=1&pageSize=1&select=id,name,images,tcgplayer&q=supertype:pokemon"
api_url_names = "https://api.pokemontcg.io/v2/cards?select=id&q=supertype:pokemon"
headers =  {"X-Api-Key":"e414e9e0-8582-45d6-9e1f-1b0b95adaf81"}

# print(pokemon_cards)

used_cards = {}



def api():
    auth = tweepy.OAuthHandler(keys.api_key, keys.api_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)

    return tweepy.API(auth)

def tweet(api: tweepy.API, card: dict, image_path=None):

    c = CurrencyConverter()
    img_data = requests.get(card["image"]).content
    with open('pokemon.jpg', 'wb') as handler:
        handler.write(img_data)
    msg = "『 " + card["name"] + " 』" + "\n\n"
    prices = [""] * 5
    for x in card["prices"]:
        match x:
            case "normal":
                price_US = card["prices"]["normal"]["market"]
                price_EURO = round(c.convert(price_US, 'USD', 'EUR'), 2)
                price_CAD = round(c.convert(price_US, 'USD', 'CAD'), 2)
                prices[0] = "\U0001f5ff | Normal: \U0001f1fa\U0001f1f8 $" + str(price_US) + " | \U0001f1ea\U0001f1fa $" + str(price_EURO) + " | \U0001f1e8\U0001f1e6 $" + str(price_CAD) + "\n"
            case "holofoil":
                price_US = card["prices"]["holofoil"]["market"]
                price_EURO = round(c.convert(price_US, 'USD', 'EUR'), 2)
                price_CAD = round(c.convert(price_US, 'USD', 'CAD'), 2)
                prices[1] = "\U0001f4bf | Holofoil: \U0001f1fa\U0001f1f8 $" + str(price_US) + " | \U0001f1ea\U0001f1fa $" + str(price_EURO) + " | \U0001f1e8\U0001f1e6 $" + str(price_CAD) + "\n"
            case "reverseHolofoil":
                price_US = card["prices"]["reverseHolofoil"]["market"]
                price_EURO = round(c.convert(price_US, 'USD', 'EUR'), 2)
                price_CAD = round(c.convert(price_US, 'USD', 'CAD'), 2)
                prices[2] = "\U0001f4c0 | Reverse Holofoil: \U0001f1fa\U0001f1f8 $" + str(price_US) + " | \U0001f1ea\U0001f1fa $" + str(price_EURO) + " | \U0001f1e8\U0001f1e6 $" + str(price_CAD) + "\n"
            case "1stEditionHolofoil" :
                price_US = card["prices"]["1stEditionHolofoil"]["market"]
                price_EURO = round(c.convert(price_US, 'USD', 'EUR'), 2)
                price_CAD = round(c.convert(price_US, 'USD', 'CAD'), 2)
                prices[3] = "\U0001faa9 | 1st Edition Holofoil: \U0001f1fa\U0001f1f8 $" + str(price_US) + " | \U0001f1ea\U0001f1fa $" + str(price_EURO) + " | \U0001f1e8\U0001f1e6 $" + str(price_CAD) + "\n"
            case "1stEditionNormal":
                price_US = card["prices"]["1stEditionNormal"]["market"]
                price_EURO = round(c.convert(price_US, 'USD', 'EUR'), 2)
                price_CAD = round(c.convert(price_US, 'USD', 'CAD'), 2)
                prices[4] = "\U0001f48e | 1st Edition Normal: \U0001f1fa\U0001f1f8 $" + str(price_US) + " | \U0001f1ea\U0001f1fa $" + str(price_EURO) + " | \U0001f1e8\U0001f1e6 $" + str(price_CAD) + "\n"
            case "1stEdition":
                price_US = card["prices"]["1stEdition"]["market"]
                price_EURO = round(c.convert(price_US, 'USD', 'EUR'), 2)
                price_CAD = round(c.convert(price_US, 'USD', 'CAD'), 2)
                prices[5] = "\U0001f48e | 1st Edition: \U0001f1fa\U0001f1f8 $" + str(price_US) + " | \U0001f1ea\U0001f1fa $" + str(price_EURO) + " | \U0001f1e8\U0001f1e6 $" + str(price_CAD) + "\n"
            case "unlimited":
                price_US = card["prices"]["unlimited"]["market"]
                price_EURO = round(c.convert(price_US, 'USD', 'EUR'), 2)
                price_CAD = round(c.convert(price_US, 'USD', 'CAD'), 2)
                prices[6] = "\U0001f48e | Unlimited: \U0001f1fa\U0001f1f8 $" + str(price_US) + " | \U0001f1ea\U0001f1fa $" + str(price_EURO) + " | \U0001f1e8\U0001f1e6 $" + str(price_CAD) + "\n"
    for y in prices:
        msg += y

    msg += "\n\U0001f6d2 | " + card["url"] + "\n"

    # Generate hashtags
    hashtags = ["#" + card["name"].replace(" ", "").replace("'", "").replace("-", "")]

    # a = card["name"].split(" ")
    # for x in a:
    #     if "#"+x not in hashtags:
    #         hashtags += ["#"+x]
    # b = card["name"].split("-")
    # for x in b:
    #     if "#"+x not in hashtags:
    #         hashtags += ["#"+x]
    hashtags += ["#Pokemon", "#PokemonTCG"]
    # print(hashtags)
    msg += "\n"+ " ".join(hashtags)


    if image_path:
        api.update_status_with_media(msg, image_path)
    else:
        api.update_status(msg)

    print('Tweeted successfully!')

def get_card(pageSize: int, numOfCards: int):
    lookingForCard = True

    while lookingForCard:

        # Choose rand card
        randNum = random.randrange(numOfCards)
        index = randNum % pageSize 
        pageNum = str(math.floor((randNum / pageSize) + 1))

        print("index: " + str(index))
        print("pageNum: " + str(pageNum))

        # Get the randomly selected card
        api_url_data = "https://api.pokemontcg.io/v2/cards?page=" + pageNum + "&select=id,name,images,tcgplayer&q=supertype:pokemon"
        card_response = requests.get(api_url_data, headers=headers)
        card_data = card_response.json()

        if card_data["data"][index]["id"] not in used_cards:
            lookingForCard = False
        else:
            print("Card " + card_data["data"][index]["id"] + " has already been used")
        
        
    # Get only the data that is needed
    card = {}
    card["name"] = card_data["data"][index]["name"]
    card["image"] = card_data["data"][index]["images"]["large"]
    card["prices"] = card_data["data"][index]["tcgplayer"]["prices"]
    card["url"] = card_data["data"][index]["tcgplayer"]["url"]

    # Mark card as used
    used_cards[card_data["data"][index]["id"]] = None
    with open("usedCards.txt", "a") as usedCardsFile:
        usedCardsFile.write(card_data["data"][index]["id"] + "\n")
    
    return card

if __name__ == '__main__':
    try:
        with open("usedCards.txt", "r") as f:
            for line in f:
                used_cards[line.strip("\n")] = None
        print(used_cards)
        
    except:
        print("No used cards on file")

    api = api()

    while True:
        # Get range for randomly drawing a card
        pokemon_cards_response = requests.get(api_url_names, headers=headers)
        pokemon_cards = pokemon_cards_response.json()
        pageSize = pokemon_cards["pageSize"]
        numOfCards = pokemon_cards["totalCount"]
        print("numOfCards: " + str(numOfCards))

        # Get and tweet card
        card = get_card(pageSize, numOfCards)
        tweet(api, card, "pokemon.jpg")
        sleep(1800)

