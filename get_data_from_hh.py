import pandas as pd
import requests

url = "https://api.hh.ru/vacancies"

params = {
    "date_to": "2024-04-07",
    "date_from": "2024-01-07",
    "page": 0,
    "per_page": 100,
    "text": "Bi",
    "area": "113",
    "currency": "RUR"
}
result = requests.get(url, params=params).json()

pages = result["pages"]

array_vacancy = []
array_vacancy.extend(result["items"])
for page in range(1, pages):
    params["page"] = page
    result_vacancies = requests.get(url, params).json()
    array_vacancy.extend(result_vacancies['items'])

for vacancy in array_vacancy:
    result_vacancy = requests.get(vacancy["url"]).json()
    while "error" in result_vacancy:
        result_vacancy = requests.get(vacancy["url"]).json()
    vacancy["description"] = result_vacancy["description"]
    vacancy["key_skills"] = result_vacancy["key_skills"]
    if "url" in vacancy["employer"]:
        result_employer = requests.get(vacancy["employer"]["url"]).json()
        vacancy["industries"] = result_employer["industries"]

df = pd.DataFrame.from_records(array_vacancy)
df.to_json("hh.json")
