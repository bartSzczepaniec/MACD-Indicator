import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.max_rows = 9999

def ema_value(day, value_data, period):
    ema_val = 0
    divisor = 0
    alfa = 2.0 / (period + 1)
    for i in range(0, period + 1):
        ema_val += value_data[day - i] * pow((1 - alfa), i)
        divisor += pow((1 - alfa), i)
    ema_val /= divisor
    return ema_val


if __name__ == '__main__':
    amount = 1000
    df = pd.read_csv('LVMHF.csv')
    df = df.head(amount)  # pobranie pierwszych 1000 wierszy z pliku .csv
    openValuesData = df[['Open']]
    closeValuesData = df[['Close']]
    # Wizualizacja danych wejściowych
    plt.plot(closeValuesData)
    plt.xlabel("Dni")
    plt.ylabel("Ceny akcji")
    plt.title("Ceny zamknięcia z 1000 dni")
    plt.show()

    closeValues = [data for data in closeValuesData['Close']]
    openValues = [data for data in openValuesData['Open']]
    macd = []
    signal = []
    for i in range(0, amount):
        if i >= 26:
            ema12 = ema_value(i, closeValues, 12)
            ema26 = ema_value(i, closeValues, 26)
            macd_val = ema12 - ema26
            macd.append(macd_val)
            if i >= 35:
                signal9_val = ema_value(i - 26, macd, 9)
                signal.append(signal9_val)

    macd = macd[-(amount - 35):]  # wyrównanie wykresów
    macdToPlot = np.array(macd)
    plt.plot(macdToPlot, label='MACD')
    signalToPlot = np.array(signal)
    plt.plot(signalToPlot, color='r', label='SIGNAL')

    plt.title("Wskaźnik MACD")
    plt.xlabel("Dni")
    plt.ylabel("Wartości wskaźników")
    plt.legend()
    plt.grid(True)
    plt.show()

    #zestawienie wynikow i wejscia razem
    closeValuesHelp = closeValues[-(amount - 35):]
    entryToPlot = np.array(closeValuesHelp)

    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Zestawienie cen akcji i wskaźnika MACD')

    ax1.plot(entryToPlot, label='Ceny')
    ax1.grid(True)
    ax1.set(ylabel='Ceny akcji')
    ax1.legend()

    ax2.plot(macdToPlot, label='MACD')
    ax2.plot(signalToPlot, color='r', label='SIGNAL')
    ax2.set(xlabel='Dni', ylabel='Wartości wskaźników')
    ax2.label_outer()
    ax2.grid(True)
    ax2.legend()
    plt.show()

    startingMoney = 1000 * openValues[0]
    shares = 0
    money = startingMoney
    print(f'Money on start: {money}')
    closeValues = closeValues[-(amount - 35):]
    openValues = openValues[-(amount - 35):]
    buySignal = False
    sellSignal = False
    for i in range(1, amount - 35):
        if buySignal:
            buySignal = False
            amountToBuy = 0
            priceOfBuying = 0
            while priceOfBuying + openValues[i] <= money:
                priceOfBuying += openValues[i]
                amountToBuy += 1
            if amountToBuy > 0:
                money -= priceOfBuying
                shares += amountToBuy
        if sellSignal:
            sellSignal = False
            money += closeValues[i] * shares
            shares = 0
        if macd[i - 1] > signal[i - 1] and macd[i] <= signal[i]:
            sellSignal = True
        if macd[i - 1] < signal[i - 1] and macd[i] >= signal[i]:
            buySignal = True
        if macd[i - 1] < 0 and macd[i] > 0:
            buySignal = True
        if macd[i - 1] > 0 and macd[i] < 0:
            sellSignal = True

    endingValue = money + shares * closeValues[-1]
    profit = endingValue / startingMoney
    print(f'Money on finish: {endingValue}')
    print(f'Profit: {profit}')


