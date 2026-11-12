import pytest

from exchange import ExchangeError, process_result


def test_valid_record():
    record = {"date": "2026-11-05", "amount": "1250.50", "status": "success"}
    assert process_result(record) == {"date": "2026-11-05", "amount": 1250.5, "status": "success"}


def test_field_aliases_normalized():
    a = process_result({" Дата ": "2026-11-05", "Сумма": "100", "Статус": "успешно"})
    b = process_result({"date": "2026-11-05", "amount": "100", "status": "success"})
    assert a == b


def test_empty_required_field():
    with pytest.raises(ExchangeError, match="обязательное поле"):
        process_result({"date": "   ", "amount": "100", "status": "success"})


def test_invalid_format():
    with pytest.raises(ExchangeError):
        process_result({"date": "2026-11-05", "amount": "сто рублей", "status": "success"})


def test_value_converted():
    result = process_result({"date": "05.11.2026", "amount": "1 250,50", "status": "в обработке"})
    assert result == {"date": "2026-11-05", "amount": 1250.5, "status": "pending"}


def test_error_message_names_field():
    with pytest.raises(ExchangeError, match="Поле «status»"):
        process_result({"date": "2026-11-05", "amount": "100", "status": "неизвестно"})
