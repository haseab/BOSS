class FabStrategy():
    def __init__(self):
        self.size1 = 7
        self.size2 = 77
        self.size3 = 231
        self.size4 = 22
        self.size5 = 721

    def _sma(self, dataframe, size):
        return round(dataframe['Close'].rolling(size).mean(), 2)

    def load_data(self, df):
        self.df = df

    def create_objects(self):
        self.price, self.low, self.high = self.df['Close'].values, self.df['Low'].values, self.df['High'].values
        self.green, self.orange, self.black = self._sma(self.df, self.size1).values, self._sma(self.df,
                                                                                               self.size2).values, self._sma(
            self.df, self.size3).values
        self.cyan, self.red = self._sma(self.df, self.size4).values, self._sma(self.df, self.size5).values

    def update_objects(self, open_price, high_price, low_price, close_price):
        self.price.append(close_price)
        self.low.append(low_price)
        self.high.append(high_price)
        self.green.append(sum(np.append(self.green[-self.size1 + 1:].astype("float"), [close_price])) / self.size1)
        self.orange.append(sum(np.append(self.orange[-self.size2 + 1:].astype("float"), [close_price])) / self.size2)
        self.black.append(sum(np.append(self.black[-self.size3 + 1:].astype("float"), [close_price])) / self.size3)

    def rule_1_buy_enter(self, i):
        if self.green[i - 1] > self.black[i - 1] and self.orange[i - 1] > self.black[i - 1] and self.green[i - 1] <= \
                self.orange[i - 1]:  # and self.black[i-1]>self.red[i-1]
            if self.green[i] > self.orange[i]:
                print("Rule 1 Buy Enter")
                return True
        return False

    def rule_1_buy_exit(self, i):
        if self.green[i - 1] > self.black[i - 1] and self.orange[i - 1] > self.black[i - 1] and self.green[i - 1] >= \
                self.orange[i - 1]:
            if self.green[i] < self.orange[i] or self.orange[i] < self.black[i]:
                print("Rule 1 Buy Exit")
                return True
        return False

    def rule_1_short_enter(self, i):
        if self.green[i - 1] < self.black[i - 1] and self.orange[i - 1] < self.black[i - 1] and self.green[i - 1] >= \
                self.orange[i - 1]:  # and self.black[i-1]>self.red[i-1]:
            if self.green[i] < self.orange[i]:
                print("Rule 1 Short Enter")
                return True
        return False

    def rule_1_short_exit(self, i):
        if self.green[i - 1] < self.black[i - 1] and self.orange[i - 1] < self.black[i - 1] and self.green[i - 1] <= \
                self.orange[i - 1]:
            if self.green[i] > self.orange[i] or self.orange[i] > self.black[i]:
                print("Rule 1 Short Exit")
                return True
        return False

    def rule_2_buy_enter(self, i, sensitivity):
        if self.low[i - 1] > self.black[i - 1] and self.low[i - 2] > self.black[i - 2] and self.green[i - 1] > \
                self.black[i - 1]:  # and self.orange[i-1]<=self.black[i-1]:
            if self.low[i] <= (self.black[i] * (1 + sensitivity)) and (
                    (self.orange[i - 1] - self.orange[i - 4]) / 3) > ((self.black[i - 1] - self.black[i - 4]) / 3):
                print("Rule 2 Buy Enter")
                return True
        return False

    def rule_2_buy_stop(self, i):
        if self.price[i - 1] < self.black[i - 1] and self.orange[i - 1] <= self.black[i - 1] and self.green[i - 1] > \
                self.black[i - 1]:
            if self.green[i] < self.black[i]:
                print("Rule 2 Buy Stop")
                return True
        return False

    def rule_2_short_enter(self, i, sensitivity):
        if self.high[i - 1] < self.black[i - 1] and self.high[i - 2] < self.black[i - 2] and self.green[i - 1] < \
                self.black[i - 1]:  # and self.orange[i-1]>=self.black[i-1]:
            if self.high[i] >= (self.black[i] / (1 + sensitivity)) and (
                    (self.orange[i - 1] - self.orange[i - 4]) / 3) < ((self.black[i - 1] - self.black[i - 4]) / 3):
                print("Rule 2 Short Enter")
                return True
        return False

    def rule_2_short_stop(self, i):
        if self.price[i - 1] > self.black[i - 1] and self.orange[i - 1] >= self.black[i - 1] and self.green[i - 1] < \
                self.black[i - 1]:
            if self.green[i] > self.black[i]:
                print("Rule 2 Short Stop")
                return True
        return False

    def rule_3_buy_enter(self, i):
        if self.green[i - 1] > self.black[i - 1] and self.orange[i - 1] <= self.black[i - 1]:
            if self.orange[i] > self.black[i] and self.green[i] > self.orange[i]:
                print("Rule 3 Buy Enter")
                return True
        return False

    def rule_3_short_enter(self, i):
        if self.green[i - 1] < self.black[i - 1] and self.orange[i - 1] >= self.black[i - 1]:
            if self.orange[i] < self.black[i] and self.green[i] < self.orange[i]:
                print("Rule 3 Short Enter")
                return True
        return False