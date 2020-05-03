"""CSC 161 Project: Milestone II

Noe Reyes
Lab Section MW 3:25-4:40pm
Spring 2020
"""


def test_data(filename, col, day):
    """A test function to query the data you loaded into your program.

    Args:
        filename: A string for the filename containing the stock data,
                  in CSV format.

        col: A string of either "date", "open", "high", "low", "close",
             "volume", or "adj_close" for the column of stock market data to
             look into.

             The string arguments MUST be LOWERCASE!

        day: An integer reflecting the absolute number of the day in the
             data to look up, e.g. day 1, 15, or 1200 is row 1, 15, or 1200
             in the file.

    Returns:
        A value selected for the stock on some particular day, in some
        column col. The returned value *must* be of the appropriate type,
        such as float, int or str.
    """
    dateList, openList, highList, lowList, closeList, adjList, volList = parse(filename)
    if col == "date":
        return dateList[day]
    elif col == "open":
        return openList[day]
    elif col == "high":
        return highList[day]
    elif col == "low":
        return lowList[day]
    elif col == "close":
        return closeList[day]
    elif col == "volume":
        return volList[day]
    elif col == "adj_close":
        return adjList[day]


def parse(file):
    infile = open(file, "r")
    infile.readline()
    data = infile.readlines()
    dateList = [0]
    openList = [0]
    highList = [0]
    lowList = [0]
    closeList = [0]
    adjList = [0]
    volList = [0]
    for i in data:
        date, open_, high, low, close, adj, vol = i.split(",")
        dateList.append(date)
        openList.append(float(open_))
        highList.append(float(high))
        lowList.append(float(low))
        closeList.append(float(close))
        adjList.append(float(adj))
        volList.append(float(vol))

    return dateList, openList, highList, lowList, closeList, adjList, volList

# ------------ Milestone II ----------- #


def alg_moving_average(filename):
    """This function implements the moving average stock trading algorithm.

    The CSV stock data should be loaded into your program; use that data to
    make decisions using the moving average algorithm.

    Any bookkeeping setup from Milestone I should be called/used here.

    Algorithm:
    - Trading must start on day 21, taking the average of the previous 20 days.
    - You must buy shares if the current day price is 5%, or more, lower than the moving average.
    - You must sell shares if the current day price is 5% higher, or more than the moving average.
    - You must buy, or sell 10 stocks per transaction.
    - You are free to choose which column of stock data to use (open, close, low, high, etc)

    Args:
        A filename, as a string.

    Returns:
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """
    funds = 1000
    stocks = 0
    openList = prices_perday(filename)
    day = 0
    in_list = []

    while day <= 20:
        in_list.append(openList[day])
        day += 1

    average = sum(in_list)/len(in_list)

    moving_list = [average]

    for day in range(21, len(openList)+1):
        moving = []
        for i in range(day-20, day-1):
            moving.append(openList[i])

            moving_list.append(sum(moving)/20)

    for i in range(20, len(openList)):
        if openList[i] <= 0.95 * moving_list[i-20]:
            funds, stocks = transact(funds, stocks, 10, openList[i], buy=True, sell=False)
        elif openList[i] >= 0.95 * moving_list[i-20]:
            funds, stocks = transact(funds, stocks, 10, openList[i], buy=False, sell=True)
        elif i == len(openList):
            funds, stocks = transact(funds, stocks, stocks, openList[i], buy=False, sell=True)

    return funds, stocks

    # Last thing to do, return two values: one for the number of stocks you end up
    # owning after the simulation, and the amount of money you have after the simulation.
    # Remember, all your stocks should be sold at the end!
    return stocks_owned, cash_balance


def prices_perday(file):
    infile = open(file, "r")
    infile.readline()
    data = infile.readlines()
    openList = []

    for i in range(len(data)):
        open_ = data[i].split(",")
        openList.append(float(open_[1]))

    return openList


def transact(funds, stocks, qty, price, buy=False, sell=False):
    """A bookkeeping function to help make stock transactions.

       Args:
           funds: An account balance, a float; it is a value of how much money you have,
                  currently.

           stocks: An int, representing the number of stock you currently own.

           qty: An int, representing how many stock you wish to buy or sell.

           price: An float reflecting a price of a single stock.

           buy: This option parameter, if set to true, will initiate a buy.

           sell: This option parameter, if set to true, will initiate a sell.

       Returns:
           Two values *must* be returned. The first (a float) is the new
           account balance (funds) as the transaction is completed. The second
           is the number of stock now owned (an int) after the transaction is
           complete.

           Error condition #1: If the `buy` and `sell` keyword parameters are both set to true,
           or both false. You *must* print an error message, and then return
           the `funds` and `stocks` parameters unaltered. This is an ambiguous
           transaction request!

           Error condition #2: If you buy, or sell without enough funds or
           stocks to sell, respectively.  You *must* print an error message,
           and then return the `funds` and `stocks` parameters unaltered. This
           is an ambiguous transaction request!
    """
    float(funds)
    int(stocks)
    int(qty)
    float(price)

    if buy is True and sell is False:
        if qty*price > funds:

            return funds, stocks

        elif qty*price <= funds:
            funds = funds - (qty*price)
            stocks = stocks + qty

            return funds, stocks

    elif sell is True and buy is False:
        if qty > stocks:

            return funds, stocks

        elif qty <= stocks:
            funds = (qty*price) + funds
            stocks = stocks - qty

            return funds, stocks

    elif sell is True and buy is True or sell is False and buy is False:
        print("Ambigious transaction! Can't determine whether to buy or sell. No action performed.")

        return float(funds), int(stocks)


def main():
    filename = input("Enter a filename for stock data (CSV format): ")
    alg_funds, alg_stocks = alg_moving_average(filename)
    print("Stocks =", alg_stocks)
    print("Funds = ${0:0.2f}".format(alg_funds))

if __name__ == "__main__":
    main()

