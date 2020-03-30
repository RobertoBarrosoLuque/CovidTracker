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

def get_num_doctors():
    '''
    Create data frame for number of primary care physicians per state. Access census api for populations per state. 
    Source: "Centers for Disease Control and Prevention. Chronic Kidney Disease Surveillance System—United States. website. http://www.cdc.gov/ckd"

    Returns: 
      main_df: pandas dataframe
    '''
    file = "Primary_Care_Physicians_by_US_State_by_State_2013.xlsx"
    doctors = pd.read_excel("C:/Users/robal/Dropbox/U Chicago/CovidProject/Data/" + file, sheet_name='Data For Current Chart')

    pop_req = requests.get("https://api.census.gov/data/2019/pep/population?get=POP,NAME&for=state:*")
    pop_df = pd.DataFrame(pop_req.json()[1:])
    pop_df.columns = ["Population", "State_name", "State_num"]

    main_df = pop_df.merge(doctors, left_on="State_name", 
                           right_on="State")[["Population",
                           "Main Value","State"]]
    main_df.columns = ["Population", "Num_doctors", "State"]
    main_df = main_df.astype({'Population': 'int32',
                              "Num_doctors":   "int32", "State":"str"})

    main_df["doc_per_thousand"] = main_df.apply(lambda row: 
                                                row.Num_doctors/row.Population
                                                *100000, axis = 1)
    return main_df







