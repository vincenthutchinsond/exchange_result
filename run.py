"""Обработка файла с результатами обмена."""
import json

from exchange import process_result

with open("data/results.json", encoding="utf-8") as f:
    records = json.load(f)

for i, record in enumerate(records, 1):
    print(i, process_result(record))
