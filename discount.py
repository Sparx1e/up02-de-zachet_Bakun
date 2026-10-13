"""Алгоритм расчёта цены со скидкой 25%."""
from datetime import datetime, timedelta
from config import DB_PATH
import sqlite3


def get_previous_month_range(date):
    """
    Возвращает (начало, конец) предыдущего месяца.
    :param date: дата расчёта
    :return: (start_date, end_date) в формате YYYY-MM-DD
    """
    # первое число текущего месяца
    first_day = date.replace(day=1)
    # последний день предыдущего месяца
    last_day_prev = first_day - timedelta(days=1)
    # первое число предыдущего месяца
    first_day_prev = last_day_prev.replace(day=1)
    # вернуть две даты в формате YYYY-MM-DD
    return (first_day_prev.strftime("%Y-%m-%d"), last_day_prev.strftime("%Y-%m-%d"))
pass

def has_orders_in_previous_month(product_id, date):
    """
    Есть ли заказы товара в предыдущем месяце?
    :param product_id: id товара
    :param date: дата расчёта
    :return: True / False
    """
    # получить диапазон предыдущего месяца
    start, end = get_previous_month_range(date)
    # открыть соединение
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # выполнить SQL
    cur.execute(
        "SELECT COUNT(*) FROM Заказ WHERE товар_id = ? AND дата BETWEEN ? AND ?",
        (product_id, start, end)
    )
    # получить счётчик
    count = cur.fetchone()[0]
    conn.close()
    # вернуть результат
    return count > 0
pass

def calculate_price_with_discount(product_id, price, date):
    """
    Рассчитывает цену со скидкой 25%.
    :param product_id: id товара
    :param price: базовая цена
    :param date: дата расчёта
    :return: цена со скидкой или без
    """
    # если есть заказы — вернуть цену без скидки
    if has_orders_in_previous_month(product_id, date):
        return price
    # иначе — цена × 0.75
    return price * 0.75
pass