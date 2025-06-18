from fastapi import FastAPI, Request
import requests
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

app = FastAPI()

TOKEN = "7665195851:AAFt129lOBsOyaShByPlIjzyBqWJUrpPfUg"
CHAT_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id: str, text: str, buttons=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if buttons:
        payload["reply_markup"] = {
            "keyboard": buttons,
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
    requests.post(f"{CHAT_URL}/sendMessage", json=payload)

def get_crypto_rates():
    result = {}
    days = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3, 0, -1)]

  
    cg_ids = {"BTC": "bitcoin", "ETH": "ethereum", "SHIB": "shiba-inu"}
    coingecko_data = {}
    for symbol, coin_id in cg_ids.items():
        history = []
        for day in days:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/history?date={datetime.strptime(day, '%Y-%m-%d').strftime('%d-%m-%Y')}"
            try:
                res = requests.get(url).json()
                price = res["market_data"]["current_price"]["usd"]
                history.append({"date": day, "price": price})
            except:
                history.append({"date": day, "price": None})
        coingecko_data[symbol] = history
    result["coingecko"] = coingecko_data

    paprika_ids = {"BTC": "btc-bitcoin", "ETH": "eth-ethereum", "SHIB": "shib-shiba-inu"}
    paprika_data = {}
    for symbol, coin_id in paprika_ids.items():
        url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
        try:
            res = requests.get(url).json()
            price = res["quotes"]["USD"]["price"]
            paprika_data[symbol] = [{"date": datetime.now().strftime("%Y-%m-%d"), "price": price}]
        except:
            paprika_data[symbol] = [{"date": datetime.now().strftime("%Y-%m-%d"), "price": None}]
    result["coinpaprika"] = paprika_data

    def get_binance_price(symbol):
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            return float(requests.get(url).json()["price"])
        except:
            return None

    binance_data = {
        "BTC": [{"date": datetime.now().strftime("%Y-%m-%d"), "price": get_binance_price("BTCUSDT")}],
        "ETH": [{"date": datetime.now().strftime("%Y-%m-%d"), "price": get_binance_price("ETHUSDT")}],
        "SHIB": [{"date": datetime.now().strftime("%Y-%m-%d"), "price": get_binance_price("SHIBUSDT")}]
    }
    result["binance"] = binance_data
    return result

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    message = data.get("message", {})
    chat_id = str(message.get("chat", {}).get("id"))
    text = message.get("text", "")

    if text == "/start":
        buttons = [["📊 Курс валют зараз"], ["📈 Зміни за останні 3 дні"]]
        send_message(chat_id, "Привіт! Вибери, що ти хочеш подивитись:", buttons)

    elif text == "📊 Курс валют зараз":
        rates = get_crypto_rates()
        msg = "*Курси криптовалют на даний момент:*"
        for api, coins in rates.items():
            msg += f"\n*{api.upper()}*"
            for coin, history in coins.items():
                today = history[-1]
                price = today['price']
                msg += f"{coin}: ${price:.6f}\n" if isinstance(price, float) else f"{coin}: ошибка\n"
        send_message(chat_id, msg)

    elif text == "📈 Зміни за останні 3 дні":
        rates = get_crypto_rates()
        msg = "*Зміни за останні 3 дні:*"
        for api, coins in rates.items():
            msg += f"\n*{api.upper()}*"
            for coin, history in coins.items():
                msg += f"{coin}:"
                for h in history:
                    price_str = f"${h['price']:.6f}" if isinstance(h['price'], float) else "помилка"
                    msg += f"  {h['date']}: {price_str}\n"
        send_message(chat_id, msg)

    else:
        send_message(chat_id, "Натисніть на старт /start щоб обрати дію")

    return JSONResponse({"ok": True})
