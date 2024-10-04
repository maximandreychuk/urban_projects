import data_download as dd
import data_plotting as dplt

import datetime as dt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца) или \nнажмите Enter, чтобы ввести даты начала и окончания ")
    if not period:
        start = input("Введите конкретную дату начала для данных в формате YYYY-MM-DD (например, ""2020-01-01"")")
        end = input("Введите конкретную дату окончания для данных в формате YYYY-MM-DD (например, ""2022-12-31"")")
    else:
        start, end = None, None
    treshold = input("Введите порог для данных (например, 10.2): ")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period=period, start=start, end=end)
    # Notification of strong fluctuations
    print(dd.notify_if_strong_fluctuations(stock_data, treshold))
    # Calculates and outputs the average closing price of shares for a given period.
    print(f"Среднее значение за выбранный период - {dd.calculate_and_display_average_price(stock_data)}")
    # Calculate RSI
    stock_data = dd.calculate_rsi(stock_data)
    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)
    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker=ticker, period=period, start=start, end=end)
    # Writing data to csv file
    dd.export_data_to_csv(stock_data,f"{ticker}_data_{dt.date.today()}.csv")



if __name__ == "__main__":
    main()
