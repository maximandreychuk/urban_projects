import logging
import matplotlib.pyplot as plt
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    filename="logging.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)


def create_and_save_plot(
        data,
        ticker,
        period,
        std,
        start=None,
        end=None,
        filename=None,
        style="ggplot",
):
    """
    This function creates and saves a stock price based on the given data,
    ticker symbol, period, start and end dates, and filename.
    The user can choose the style of plotting

    :param data: pd.DataFrame, input data containing stock information
    :param ticker: str, ticker symbol of the stock
    :param period: str, time period for the stock data
    :param start: str, start date for the stock data (optional)
    :param end: str, end date for the stock data (optional)
    :param filename: str, name of the file to save the plot (optional)
    :param style: str, style to apply to the plot (default is 'ggplot')
    :param std: standard deviation of the closing price

    :return plot: Save the stock price chart as an image file

    The function plots two subplots:
    Close Price vs. Moving Average vs Standard deviation
    RSI (Relative Strength Index) with the upper and lower threshold lines.
    """
    try:
        plt.style.use(style)
        logging.info(
            "%s: Пользователь ввел валидный стиль",
            create_and_save_plot.__name__,
        )
    except OSError as e:
        logging.debug(
            "%s: Пользователь ввел не валидный стиль %s",
            create_and_save_plot.__name__,
            style
        )
        print(f"Что-то пошло не так: {e} \nГрафик выполнен в стиле ggplot")
        plt.style.use(style="ggplot")

    plt.figure(
        figsize=(
            12,
            6,
        )
    )
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            # subplot разделяет на два графика: первый
            plt.subplot(2, 1, 1)
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.title(
                f"Цена закрытия {ticker} ({period})"
                "\nСтандартное отклонение: {std:.2f}"
            )
            plt.plot(
                dates,
                data['Moving_Average'].values,
                label='Moving Average'
            )
            plt.legend()
            # subplot разделяет на два графика: второй
            plt.subplot(2, 1, 2)
            plt.plot(dates, data['RSI'].values, label='RSI', color='blue')
            plt.axhline(70, linestyle='--', alpha=0.5, color='red')
            plt.axhline(30, linestyle='--', alpha=0.5, color='green')
            plt.legend()
        else:
            print(
                "Информация о дате отсутствует "
                "или не имеет распознаваемого формата."
            )
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.subplot(2, 1, 1)
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.title(
                f"Цена закрытия {ticker} ({period})"
                "\nСтандартное отклонение: {std:.2f}"
            )
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(data['Date'], data['RSI'], label='RSI', color='blue')
        plt.axhline(70, linestyle='--', alpha=0.5, color='red')
        plt.axhline(30, linestyle='--', alpha=0.5, color='green')
        plt.legend()

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")

    if filename is None:
        if not period:
            filename = f"{ticker}_{start}_{end}_stock_price_chart.png"
        else:
            filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    logging.info(
        "%s: График сохранен как %r",
        create_and_save_plot.__name__,
        filename,
    )
    print(f"График сохранен как {filename}")
