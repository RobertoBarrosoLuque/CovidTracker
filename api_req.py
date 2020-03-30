import requests
from datetime import datetime
import pandas as pd
import numpy as np
import seaborn as sns
from pandas.io.json import json_normalize

def get_daily_cases():
    '''
    Make api request to covidtracking project and download most 
    recent data. Convert json into pandas dataframe

    Returns:
    - daily_cases: pandas dataframe
    '''
    data_json = requests.get("https://covidtracking.com/api/states/daily")
    daily_cases = json_normalize(data_json.json())
    daily_cases['date'] = daily_cases['date'].apply(lambda row:
                                                    datetime.strptime(str(row),
                                                    '%Y%m%d'))
    return daily_cases

#sns.relplot(x="date", y="positive", hue="state", 
#           kind="line", legend=False,data=daily_cases)
 