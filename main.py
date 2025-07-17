import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Token ",
    "X-Secret": ""
}

@app.post("/standardize_phone")
async def standardize_phone(phone: str):

    DADATA_URL = "https://cleaner.dadata.ru/api/v1/clean/phone"

    data = [phone]
    try:
        response = requests.post(DADATA_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()[0]

        if not result:
            raise HTTPException(status_code=404, detail="Номер не найден")

        return result
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к DaData: {str(e)}")

@app.post("/standardize_party")
async def standardize_party(query: str):

    DADATA_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"

    data = {"query" : query}
    try:
        response = requests.post(DADATA_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json().get("suggestions")

        if not result:
            raise HTTPException(status_code=404, detail="Организация не найдена")

        return result[0]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к DaData: {str(e)}")

@app.get("/currency_rate")
def currency_rate(currency: str):

    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()["Valute"][f"{currency}"]["Value"]

        if not result:
            raise HTTPException(status_code=404, detail="валюта не найдена")

        return {f"{currency}": result}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к cbr-xml-daily: {str(e)}")
