class FabStrategy():
    def __init__(self):
        self.size = 7
        self.size2 = 77
        self.size3 = 231
        self.size4 = 22
        self.size5 = 721

    def _sma(self, dataframe, size):
        return round(dataframe['Close'].rolling(size).mean(), 2)

    def load_data(self, df):
        self.df = df

    def create_objects(self):
        df = self.df
        self.price, self.low, self.high = df['Close'].values, df['Low'].values, df['High'].values
        self.green, self.orange, self.black = self._sma(df, self.size).values, self._sma(df,
                                                                                         self.size2).values, self._sma(
            df, self.size3).values
        self.cyan, self.red = self._sma(df, self.size4).values, self._sma(df, self.size5).values

    def rule_1_buy_enter(self, i):
        if self.green[i] > self.black[i] and self.orange[i] > self.black[i] and self.green[i] <= self.orange[
            i]:  # and self.black[i]>self.red[i]
            if self.green[i + 1] > self.orange[i + 1]:
                return True
        return False

    def rule_1_buy_exit(self, i):
        if self.green[i] > self.black[i] and self.orange[i] > self.black[i] and self.green[i] >= self.orange[i]:
            if self.green[i + 1] < self.orange[i + 1] or self.orange[i + 1] < self.black[i + 1]:
                return True
        return False

    def rule_1_short_enter(self, i):
        if self.green[i] < self.black[i] and self.orange[i] < self.black[i] and self.green[i] >= self.orange[
            i]:  # and self.black[i]>self.red[i]:
            if self.green[i + 1] < self.orange[i + 1]:
                return True
        return False

    def rule_1_short_exit(self, i):
        if self.green[i] < self.black[i] and self.orange[i] < self.black[i] and self.green[i] <= self.orange[i]:
            if self.green[i + 1] > self.orange[i + 1] or self.orange[i + 1] > self.black[i + 1]:
                return True
        return False

    def rule_2_buy_enter(self, i):
        if self.low[i] > self.black[i] and self.low[i - 1] > self.black[i - 1] and self.green[i] > self.black[i] and \
                self.orange[i] <= self.black[i]:
            if self.low[i + 1] <= self.black[i + 1] and ((self.orange[i] - self.orange[i - 3]) / 3) > (
                    (self.black[i] - self.black[i - 3]) / 3):
                return True
        return False

    def rule_2_buy_stop(self, i):
        if self.price[i] < self.black[i] and self.orange[i] <= self.black[i]:
            if self.price[i + 1] <= self.orange[i + 1] or self.green[i + 1] < self.black[i + 1]:
                return True
        return False

    def rule_2_short_enter(self, i):
        if self.high[i] < self.black[i] and self.high[i - 1] < self.black[i - 1] and self.green[i] < self.black[i] and \
                self.orange[i] >= self.black[i]:
            if self.high[i + 1] >= self.black[i + 1] and ((self.orange[i] - self.orange[i - 3]) / 3) < (
                    (self.black[i] - self.black[i - 3]) / 3):
                return True
        return False

    def rule_2_short_stop(self, i):
        if self.price[i] > self.black[i] and self.orange[i] >= self.black[i]:
            if self.price[i + 1] >= self.orange[i + 1] or self.green[i + 1] > self.black[i + 1]:
                return True
        return False

    def rule_3_buy_enter(self, i):
        if self.green[i] > self.black[i] and self.orange[i] <= self.black[i]:
            if self.orange[i + 1] > self.black[i + 1] and self.green[i + 1] > self.orange[i + 1]:
                return True
        return False

    def rule_3_short_enter(self, i):
        if self.green[i] < self.black[i] and self.orange[i] >= self.black[i]:
            if self.orange[i + 1] < self.black[i + 1] and self.green[i + 1] < self.orange[i + 1]:
                return True
        return False