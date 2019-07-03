
PATH = 'turnstile_190629.txt'

# RangeIndex: 205963 entries, 0 to 205962
# Data columns (total 11 columns):
# C/A                                                                     205963 non-null object
# UNIT                                                                    205963 non-null object
# SCP                                                                     205963 non-null object
# STATION                                                                 205963 non-null object
# LINENAME                                                                205963 non-null object
# DIVISION                                                                205963 non-null object
# DATE                                                                    205963 non-null object
# TIME                                                                    205963 non-null object
# DESC                                                                    205963 non-null object
# ENTRIES                                                                 205963 non-null int64
# EXITS                                                                   205963 non-null int64
# dtypes: int64(2), object(9)
# memory usage: 17.3+ MB



def extract(filename= 'turnstile_190629.txt'):
    """

    :param filename: week's file name
    :return: Pandas DataFrame of the MTA week's data with a datetime object in place of the date & time objects
    """

    from datetime import datetime

    #Fatima
    #TODO StationNames


    #aaron's td

    #TODO enries per time exits per time

    import pandas as pd
    df = pd.read_csv(filename)
    dt_format = '%m/%d/%Y %H:%M:%S'
    working = []
    for _, row in enumerate(df.values):
        working.append(datetime.strptime(row[6]+' '+row[7], dt_format))
    df['datetime'] = pd.DataFrame(working)
    df.drop(columns=['DATE','TIME'], inplace=True)
    return df



if __name__ == "__main__":
    df = extract()
    print(df.columns)