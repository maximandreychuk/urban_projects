import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_and_display_average_price(data):
    # принимаем DataFrame и вычисляем среднее значение колонки 'Close'.
    print(f"Среднее значение за выбранный период - {data["Close"].mean()}")

def notify_if_strong_fluctuations(data, treshold):
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
        for key, value in dct.items():
            print(f"Уведомление!\n {key} пробит порог {treshold} на {value}")

    print(data['High'],  data['Low'] )

