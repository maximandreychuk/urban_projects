import matplotlib.pyplot as plt
import pandas as pd



def create_and_save_plot(data, ticker, period, start, end, filename=None):
    plt.figure(figsize=(10, 6))
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            # subplot разделяет на два графика: первый
            plt.subplot(2, 1, 1)
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
            plt.legend()
            # subplot разделяет на два графика: второй
            plt.subplot(2, 1, 2)
            plt.plot(dates, data['RSI'].values, label='RSI', color='blue')
            plt.axhline(70, linestyle='--', alpha=0.5, color='red')
            plt.axhline(30, linestyle='--', alpha=0.5, color='green')
            plt.legend()
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.subplot(2, 1, 1)
        plt.plot(data['Date'], data['Close'], label='Close Price')
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
    print(f"График сохранен как {filename}")
