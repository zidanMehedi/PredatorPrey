import pandas as pd

def filter(lst, winSize):
	window_size = winSize
	numbers_series = pd.Series(lst)
	windows = numbers_series.rolling(window_size)
	moving_averages = windows.mean()
	moving_averages_list = moving_averages.tolist()
	without_nans = moving_averages_list[window_size - 1:]

	return without_nans