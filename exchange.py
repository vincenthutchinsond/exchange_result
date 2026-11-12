"""Обработка результатов обмена данными между системами."""
from datetime import datetime

# Допустимые варианты названий полей -> каноническое название
FIELD_ALIASES = {
    "date": "date", "дата": "date",
    "amount": "amount", "сумма": "amount",
    "status": "status", "статус": "status",
}
REQUIRED_FIELDS = ("date", "amount", "status")
DATE_FORMATS = ("%Y-%m-%d", "%d.%m.%Y")
STATUSES = {
    "success": "success", "успешно": "success",
    "error": "error", "ошибка": "error",
    "pending": "pending", "в обработке": "pending",
}


class ExchangeError(ValueError):
    """Некорректная запись результата обмена."""


def normalize_fields(record):
    """Приводит названия полей к единому виду и убирает лишние пробелы."""
    result = {}
    for key, value in record.items():
        name = FIELD_ALIASES.get(str(key).strip().lower())
        if name:
            result[name] = value.strip() if isinstance(value, str) else value
    return result


def parse_date(value):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    raise ExchangeError(
        f"Поле «date»: ожидается дата ГГГГ-ММ-ДД или ДД.ММ.ГГГГ, получено «{value}».")


def parse_amount(value):
    text = str(value).replace(" ", "").replace(" ", "").replace(",", ".")
    try:
        amount = float(text)
    except ValueError:
        raise ExchangeError(f"Поле «amount»: ожидается число, получено «{value}».") from None
    if amount < 0:
        raise ExchangeError(f"Поле «amount»: сумма не может быть отрицательной, получено «{value}».")
    return round(amount, 2)


def parse_status(value):
    status = STATUSES.get(str(value).lower())
    if status is None:
        raise ExchangeError(
            f"Поле «status»: ожидается «успешно», «ошибка» или «в обработке», получено «{value}».")
    return status


def process_result(record):
    """Нормализует, проверяет и преобразует запись результата обмена."""
    data = normalize_fields(record)
    for field in REQUIRED_FIELDS:
        if data.get(field) in (None, ""):
            raise ExchangeError(f"Поле «{field}»: обязательное поле не заполнено.")
    return {
        "date": parse_date(data["date"]),
        "amount": parse_amount(data["amount"]),
        "status": parse_status(data["status"]),
    }
