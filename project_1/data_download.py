import logging
import yfinance as yf
from plotly import graph_objs as go
from datetime import date


logging.basicConfig(
    level=logging.INFO,
    filename="logging.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)


def fetch_stock_data(ticker, period=None, start=None, end=None):
    """
    This function retrieves data from the trading history

    :param ticker: str, the stock ticker symbol
    :param period: str, optional, the time period (e.g. '1d', '1mo', '1y')
    :param start: str, optional, start date in 'yyyy-mm-dd' format
    :param end: str, optional, end date in 'yyyy-mm-dd' format

    :return data: containing the stock data for the specified parameters
    """
    stock = yf.Ticker(ticker)
    # передаем временной отрезок в зависимости от того, что ввел пользователь
    if not period:
        data = stock.history(start=start, end=end)
        logging.info(
            "%s: Временной отрезок данных - промежуток с %r по %r",
            add_moving_average.__name__,
            start,
            end,
        )
    else:
        data = stock.history(period=period)
        logging.info(
            "%s: Временной отрезок данных - период %s",
            add_moving_average.__name__,
            period,
        )
    return data


def calculate_rsi(data, window=14):
    """
    Calculates the Relative Strength Index (RSI) for a given dataset.

    :param data: pd.DataFrame with a "Close" column containing closing prices.
    :param window: int, value specifying the window for calculating RSI.
    :return data: pd.DataFrame with an additional "RSI" column added.

    The RSI is a technical indicator used in financial analysis
    to evaluate the speed and change of price movements.
    """

    # рассчитываем приросты цен:
    delta = data["Close"].diff()
    # разделяем приросты на положительные и отрицательные:
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    # рассчитываем относительную силу:
    rs = gain / loss
    # RSI
    rsi = 100 - (100 / (1 + rs))
    logging.info(
        "%s: Произведен расчет RSI",
        calculate_rsi.__name__,
    )
    data["RSI"] = rsi
    return data


def add_moving_average(data, window_size=5):
    """
    Calculates the moving average of the closing prices in the input data.

    :param data: pd.DataFrame with a "Close" column containing closing prices.
    :param window_size: int, the size of the moving average window.
    :return data: pd.DataFrame with an additional column
    "Moving_Average" containing the calculated moving averages.
    """

    data["Moving_Average"] = data["Close"].rolling(window=window_size).mean()
    logging.info(
        "%s: Подсчитана скользящая средняя",
        add_moving_average.__name__
    )
    return data


def calculate_and_display_average_price(data):
    """
    This function calculates the average value
    of the closing prices and displays

    :param data: pd.DataFrame with a "Close" column containing closing prices.

    :return av_price: float, the average value of closing prices.
    """
    av_price = data["Close"].mean()
    logging.info(
        "%s: Среднее значение %s",
        calculate_and_display_average_price.__name__,
        {av_price}
    )
    return av_price


def notify_if_strong_fluctuations(data, treshold):
    """
    Checks for strong fluctuations in the data
    and notifies if the threshold is exceeded.

    :param data: pd.DataFrame The dataset containing high and low prices.
    :param treshold: float, the threshold for fluctuations.

    :return message: str, a notification if strong fluctuations are detected,
    otherwise no notifications are sent.

    Raises:
    ValueError: If the input threshold is not a float.

    The function takes a dataset with high and low
    prices and a threshold value.
    It calculates the difference between high and low prices
    and checks if the difference exceeds the given threshold.

    If strong fluctuations are detected, the function sends a notification
    with the date and the amount by which the threshold was exceeded.
    If no strong fluctuations are found, no notifications are sent.
    """
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
    for i in data["Low"]:
        for j in data["High"]:
            # находим разницу
            diff = j - i
            # если разница превышает порог, записываем в словарь
            if treshold < diff:
                # получаем дату (например, по High)
                low_key = data.index[data["High"] == j].tolist()
                # форматируем дату
                low_key = [date(2023, 10, 27)]
                date_format = f"{low_key[0].strftime('%d.%m.%Y')}"
                # date_format = f"{low_key[0].day}.
                # {low_key[0].month}.{low_key[0].year}"
                dct[date_format] = diff-treshold
    # если словарь не пуст, отправляем уведомление
    if len(dct) != 0:
        logging.info(
            "%s: Есть несколько сильных колебаний: %s",
            notify_if_strong_fluctuations.__name__,
            dct
        )
        for key, value in dct.items():
            return (f"Уведомление!\n {key} пробит порог {treshold} на {value}")
    else:
        logging.info(
            "%s: Сильных колебаний нет",
            notify_if_strong_fluctuations.__name__,
        )
        return "Уведомлений нет"


def export_data_to_csv(data, filename):
    """
    This function takes a Pandas DataFrame and saves it
    to a CSV file with the given filename.
    The index column is not included in the CSV file.

    :param data: pd.DataFrame containing the data to be exported.
    :param filename: str, name of the CSV file to be created.

    :return None
    """
    data.to_csv(filename, index=False)
    logging.info(
        "%s: Данные записаны в csv file",
        export_data_to_csv.__name__,
    )


def calculate_std(data):
    """
    Calculates the standard deviation of the closing price.

    :param data: pd.DataFrame with a "Close" column containing closing prices.

    :return std_dev: float, standard deviation of the closing price
    """

    std = data['Close'].std()
    logging.info(
        "%s: Подсчитано стандартное отклонение цены закрытия: %s",
        calculate_std.__name__,
        std
    )
    return std


def interactive_graph(data):
    """
    Creates an interactive chart of the closing price using Plotly.

    :param data: pd.DataFrame with a "Close" column containing closing prices.

    :return None, displays an interactive graph in the console.
    """

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['Close'],
            name='Цена закрытия'
        )
    )
    fig.update_layout(
        title=f'Цена закрытия',
        xaxis_title='Дата',
        yaxis_title='Цена закрытия',
    )
    fig.show()
    logging.info(
        "%s: Создан интерактивный график",
        interactive_graph.__name__,
    )
    average_close = data['Close'].mean()
    logging.info(
        "%s: Рассчитано среднее значение цены закрытия %s",
        interactive_graph.__name__,
        average_close
    )
    print(f'Среднее значение цены закрытия: {average_close}\n')
