import requests

url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    
    "ids": "bitcoin,ethereum,binancecoin", 
    "vs_currencies": "usd"
}

response = requests.get(url, params=params)
data = response.json()

print(" Курси криптовалют до USD:\n")

btc = data["bitcoin"]["usd"]
eth = data["ethereum"]["usd"]
bnb = data["binancecoin"]["usd"]

print("BTC:", data["bitcoin"]["usd"])
print("ETH:", data["ethereum"]["usd"])
print("BNB:", data["binancecoin"]["usd"])


print(f" Bitcoin (BTC): ${btc}")
print(f" Ethereum: ${eth}")
print(f" Binancecoin: ${bnb}")