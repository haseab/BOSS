from datetime import datetime
import pandas as pd
import numpy as np


class FabStrategy:
    """
    This is a set of rules that specify to buy/sell/short/close whenever the market fulfills those conditions.

    Attributes
    -----------
    All attributes are moving average size. There are currently 5 different Moving average sizes that are
    listed as attributes.


    NOTE: The reason why the moving averages are colors is to avoid hardcoding the MA. Also it is used to distinguish
    between different MA's on a graph

    price:  closing price of minute candle
    green:  size1 moving average
    orange: size2 moving average
    black:  size3 moving average
    blue:   size4 moving average
    red:    size5 moving average

    Methods
    ------------
    load_data
    update_moving_averages
    update_objects

    rule_1_buy_enter
    rule_1_buy_exit
    rule_1_short_enter
    rule_1_short_exit
    rule_2_buy_enter
    rule_2_buy_stop
    rule_2_short_enter
    rule_2_short_stop
    rule_3_buy_enter
    rule_3_short_enter

    Please look at each method for descriptions
    """

    def __init__(self, debug=False):
        """Initializing moving average sizes"""
        self.size1 = 7
        self.size2 = 77
        self.size3 = 231
        self.size4 = 200
        self.size5 = 721
        self.debug = debug

    def _sma(self, series: pd.Series, size: int) -> pd.Series:
        """
        Simple moving average (MA)

        Parameters
        ------------
        series: pd.Series object containing Close values of an asset.
        size: the size of the moving average (how many points it should take the average of)

        Ex. _sma(pd.Series([2,3,5,6,8,10]), 2) -> [NaN, 2.5, 4.0, 5.5, 7.0, 9.0]
        Ex.  _sma(pd.Series([2,3,5,6,8,10]), 6) -> [NaN, NaN, NaN, NaN, NaN, 5.67]

        Returns pd.Series of moving average data, rounded to the nearest hundreth.
        """
        return round(series.rolling(size).mean(), 2)

    def load_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Passes a dataframe object and adds it as an instance variable.
        """
        self.df = df

    def update_moving_averages(self) -> None:
        """
        Creates/updates all required moving averages (MA's) needed to run trading strategy successfully

        Parameters: None
        :return None
        """
        self.price, self.low, self.high = self.df['Close'].values, self.df['Low'].values, self.df['High'].values
        self.green, self.orange, self.black = self._sma(self.df["Close"], self.size1).values, self._sma(
            self.df["Close"], self.size2).values, self._sma(self.df["Close"], self.size3).values

        self.blue, self.red = self._sma(self.df['Close'],self.size4).values, self._sma(self.df['Close'],self.size5).values

    def _update_objects(self, open_price: float, high_price: float, low_price: float, close_price: float) -> None:
        """
        WORK IN PROGRESS - Instead of creating new objects every time, the objects can be updated.
        This is a little more complex and more prone to error.
        """
        self.price.append(close_price)
        self.low.append(low_price)
        self.high.append(high_price)
        self.green.append(sum(np.append(self.green[-self.size1 + 1:].astype("float"), [close_price])) / self.size1)
        self.orange.append(sum(np.append(self.orange[-self.size2 + 1:].astype("float"), [close_price])) / self.size2)
        self.black.append(sum(np.append(self.black[-self.size3 + 1:].astype("float"), [close_price])) / self.size3)

    def rule_1_buy_enter(self, i: int) -> bool:
        """
        In Plain English: If 7 MA (Green) just crosses above 77 MA (Orange) and both are > 231 MA (Black), BUY.

        Parameters
        -----------
        i: the current index in the data. Ex. -1 is the latest point and 0 is the first point in the dataset.

        """
        if self.green[i - 1] > self.blue[i - 1] and self.orange[i - 1] > self.blue[i - 1] and self.green[i - 1] <= \
                self.orange[i - 1] and self.price[i-1]>self.red[i-1]:
            if self.green[i] > self.orange[i]:
                if self.debug == True:
                    print(str(datetime.now())[:19], self.price[i], "Rule 1 Buy Enter")
                return True
        return False

    def rule_1_buy_exit(self, i: int) -> bool:
        """
        In Plain English: If 7 MA (Green) just crosses below 77 MA (Orange) and both are > 231 MA (Black), CLOSE.

        Parameters
        -----------
        i: the current index in the data. Ex. -1 is the latest point and 0 is the first point in the dataset.

        """
        if self.green[i - 1] > self.black[i - 1] and self.orange[i - 1] > self.black[i - 1] and self.green[i - 1] >= \
                self.orange[i - 1]:
            if self.green[i] < self.orange[i] or self.orange[i] < self.black[i]:
                if self.debug == True:
                    print(str(datetime.now())[:19], self.price[i], "Rule 1 Buy Exit")
                return True
        return False

    def rule_1_short_enter(self, i: int) -> bool:
        """
        In Plain English: If 7 MA (Green) just crosses below 77 MA (Orange) and both are < 231 MA (Black), SHORT.

        Parameters
        -----------
        i: the current index in the data. Ex. -1 is the latest point and 0 is the first point in the dataset.

        """
        if self.green[i - 1] < self.black[i - 1] and self.orange[i - 1] < self.black[i - 1] and self.green[i - 1] >= \
                self.orange[i - 1] and self.price[i-1]>self.red[i-1]:
            if self.green[i] < self.orange[i]:
                if self.debug == True:
                    print(str(datetime.now())[:19], self.price[i], "Rule 1 Short Enter")
                return True
        return False

    def rule_1_short_exit(self, i: int) -> bool:
        """
        In Plain English: If 7 MA (Green) just crosses above 77 MA (Orange) and both are < 231 MA (Black), CLOSE.

        Parameters
        -----------
        i: the current index in the data. Ex. -1 is the latest point and 0 is the first point in the dataset.

        """
        if self.green[i - 1] < self.black[i - 1] and self.orange[i - 1] < self.black[i - 1] and self.green[i - 1] <= \
                self.orange[i - 1]:
            if self.green[i] > self.orange[i] or self.orange[i] > self.black[i]:
                if self.debug == True:
                    print(str(datetime.now())[:19], self.price[i], "Rule 1 Short Exit")
                return True
        return False

    def rule_2_buy_enter(self, i: int, sensitivity: int = 0) -> bool:
        """
        In Plain English: If Price passes above 231 MA (Black) and then comes back down to touch the 231 MA (Black), BUY.

        Parameters
        -----------
        i: the current index in the data. Ex. -1 is the latest point and 0 is the first point in the dataset.
        sensitivity: how far from the moving average should you enter. The larger the value, the further and less sensitive.

        """
        if self.low[i - 1] > self.black[i - 1] and self.low[i - 2] > self.black[i - 2] and self.green[i - 1] > \
                self.black[i - 1] and self.orange[i - 1] <= self.black[i - 1]:
            if self.low[i] <= (self.black[i] * (1 + sensitivity)) and (
                    (self.orange[i - 1] - self.orange[i - 4]) / 3) > ((self.black[i - 1] - self.black[i - 4]) / 3):
                if self.debug == True:
                    print(str(datetime.now())[:19], self.price[i], "Rule 2 Buy Enter")
                return True
        return False

    def rule_2_buy_stop(self, i: int) -> bool:
        """
        In Plain English: (After Rule 2 Buy), If 7 MA (Green) crosses below 231 MA (Black), CLOSE.

        Parameters
        -----------
        i: the current index in the data. Ex. -1 is the latest point and 0 is the first point in the dataset.

        """
        if self.low[i - 1] < self.black[i - 1] and self.orange[i - 1] <= self.black[i - 1] and self.green[i - 1] > \
                self.black[i - 1]:
            if self.green[i] < self.black[i]:
                if self.debug == True:
                    print(str(datetime.now())[:19], self.price[i], "Rule 2 Buy Stop")
                return True
        return False

    def rule_2_short_enter(self, i: int, sensitivity: int = 0) -> bool:
        """
        In Plain English: If Price passes below 231 MA (Black) and then comes back up to touch the 231 MA (Black), SHORT.

        Parameters
        -----------
        i: the current index in the data. Ex. -1 is the latest point and 0 is the first point in the dataset.
        sensitivity: how far from the moving average should you enter. The larger the value, the further and less sensitive.

        """
        if self.high[i - 1] < self.black[i - 1] and self.high[i - 2] < self.black[i - 2] and self.green[i - 1] < \
                self.black[i - 1] and self.orange[i - 1] >= self.black[i - 1]:
            if self.high[i] >= (self.black[i] / (1 + sensitivity)) and (
                    (self.orange[i - 1] - self.orange[i - 4]) / 3) < ((self.black[i - 1] - self.black[i - 4]) / 3):
                if self.debug == True:
                    print(str(datetime.now())[:19], self.price[i], "Rule 2 Short Enter")
                return True
        return False

    def rule_2_short_stop(self, i: int) -> bool:
        """
        In Plain English: (After Rule 2 Short), If 7 MA (Green) crosses above 231 MA (Black), CLOSE.

        Parameters
        -----------
        i: the current index in the data. Ex. -1 is the latest point and 0 is the first point in the dataset.

        """
        if self.high[i - 1] > self.black[i - 1] and self.orange[i - 1] >= self.black[i - 1] and self.green[i - 1] < \
                self.black[i - 1]:
            if self.green[i] > self.black[i]:
                if self.debug == True:
                    print(str(datetime.now())[:19], self.price[i], "Rule 2 Short Stop")
                return True
        return False

    def rule_3_buy_enter(self, i: int) -> bool:
        """
        In Plain English: If 77 MA > 231 MA (a.k.a. Orange > Black), BUY.

        Parameters
        -----------
        i: the current index in the data. Ex. -1 is the latest point and 0 is the first point in the dataset.

        """
        if self.green[i - 1] > self.black[i - 1] and self.orange[i - 1] <= self.black[i - 1]:
            if self.orange[i] > self.black[i] and self.green[i] > self.orange[i]:
                if self.debug == True:
                    print(str(datetime.now())[:19], self.price[i], "Rule 3 Buy Enter")
                return True
        return False

    def rule_3_short_enter(self, i: int) -> bool:
        """
        In Plain English: If 77 MA < 231 MA (a.k.a. Orange < Black), SHORT.

        Parameters
        -----------
        i: the current index in the data. Ex. -1 is the latest point and 0 is the first point in the dataset.

        """
        if self.green[i - 1] < self.black[i - 1] and self.orange[i - 1] >= self.black[i - 1]:
            if self.orange[i] < self.black[i] and self.green[i] < self.orange[i]:
                if self.debug == True:
                    print(str(datetime.now())[:19], self.price[i], "Rule 3 Short Enter")
                return True
        return False