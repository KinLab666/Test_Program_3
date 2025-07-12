import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Token ",
    "X-Secret": ""
}

headers_party = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Token "
}

@app.post("/standardize_phone")
async def standardize_phone(phone: str):

    DADATA_URL = "https://cleaner.dadata.ru/api/v1/clean/phone"

    data = [phone]
    try:
        response = requests.post(DADATA_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()[0]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к DaData: {str(e)}")

@app.post("/standardize_party")
async def standardize_party(query: str):

    DADATA_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"

    data = [query]
    try:
        response = requests.post(DADATA_URL, json=data, headers=headers_party)
        response.raise_for_status()
        result = response.json()[0]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к DaData: {str(e)}")
