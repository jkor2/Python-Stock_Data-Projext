import getDate
import yfinance as yf


class Main:
    def __init__(self, stock="SPY", current_date=getDate.get_current_date(), past_date=getDate.seven_days_ago()):
        self._stock = stock
        self._current_date = current_date
        self._past_date = past_date
        self._active_data = []

    def load_data(self):
        """
        Returns default data
        """

        data = yf.download(self._stock, start=self._past_date,
                           end=self._current_date)

        data_list_of_dicts = data.reset_index().to_dict(orient='records')
        self.set_active_data(data_list_of_dicts)

    def set_active_data(self, data):
        """
        Updates the hashed data
        """
        self._hashed_data = data
        return True

    def get_active_data(self):
        """
        Gets the hashed data
        """
        return self._hashed_data


main = Main()
main.load_data()
