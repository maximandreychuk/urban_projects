import logging
import yfinance as yf


logging.basicConfig(
    level=logging.INFO,
    filename="my_log.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s" ,
)

formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")

def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_and_display_average_price(data):
    # принимаем DataFrame и вычисляем среднее значение колонки 'Close'.
    logging.info(
        "%s: Среднее значение %s",
        calculate_and_display_average_price.__name__,
        {data["Close"].mean()}
    )
    print(f"Среднее значение за выбранный период - {data["Close"].mean()}")

def notify_if_strong_fluctuations(data, treshold):
    # проверка что treshold это float
    try:
        treshold = float(treshold)
        logging.info(
            "%s: Пользователь ввел число %s",
            notify_if_strong_fluctuations.__name__,
            treshold
        )
    except ValueError:
        logging.info(
            "%s: Пользователь ввел не число %s",
            notify_if_strong_fluctuations.__name__,
            treshold
        )
        return print("Вы ввели не число")
    # объявляем словарь для записи даты и разницы
    dct = {}
    # получаем минимальное и максимальное значения цены закрытия
    for i in data['Low']:
        for j in data['High']:
            # находим разницу
            diff = j - i
            # если разница превышает порог, записываем в словарь
            if treshold < diff:
                # получаем дату (например, по High)
                low_key = data.index[data['High'] == j].tolist()
                # форматируем дату
                date_format = f"{low_key[0].day}.{low_key[0].month}.{low_key[0].year}"
                dct[date_format] = diff-treshold
    # если словарь не пуст, отправляем уведомление
    if len(dct) != 0:
        logging.info(
            "%s: Есть несколько сильных колебаний: %s",
            notify_if_strong_fluctuations.__name__,
            data
        )
        for key, value in dct.items():
            print(f"Уведомление!\n {key} пробит порог {treshold} на {value}")
    else:
        logging.info(
            "%s: Сильных колебаний нет",
            notify_if_strong_fluctuations.__name__
        )

