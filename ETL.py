#!/anaconda3/envs/metis/bin/python

#comment

# Fatima
# TODO StationNames

# aaron's td

# TODO enries per time exits per time

##assumptions:
##  keeping duplicates, they look to be audits back at same timestamp


def extract(filename=''):
    """
    extract file and output pickle of the loaded csv into a pickle, optional return of the df.

    :param filename: week's file name
    :return: Pandas DataFrame of the MTA week's data with a datetime object in place of the date & time objects
    """

    import pandas as pd

    if filename == '':
        raise ValueError("Filename cannot be blank")

    df = pd.read_csv(filename, parse_dates=[['DATE', 'TIME']], keep_date_col=True)
    df.to_pickle('.DateTime_transformed.pickle')

    return df



def transform(df):
    import pandas as pd
    import numpy as np

    #column names
    df.columns = df.columns.str.strip()

    ##Duplicates as recovery audits OK to keep

    #mask = ["C/A", "UNIT", "SCP", "STATION", "datetime"]
    #(df.groupby(mask)).ENTRIES.count().reset_index().sort_values('ENTRIES', ascending=False).head()
    # mask2 = ((df["C/A"] == "R229") & \
    #          (df["UNIT"] == "R143") & \
    #          (df["SCP"] == "01-00-00") & \
    #          (df["STATION"] == "28 ST")) & \
    #         (df['datetime'] == '2019-06-27 17:00:00')
    # df[mask2].head()
    # for val in df[mask2].values:
    #     print(val)
    # ['R229' 'R143' '01-00-00' '28 ST' '6' 'IRT' '06/27/2019' '17:00:00'
    #  'REGULAR' 1795575 2546673 Timestamp('2019-06-27 17:00:00') 898.0 354.0
    #  15110.0]
    # ['R229' 'R143' '01-00-00' '28 ST' '6' 'IRT' '06/27/2019' '17:00:00'
    #  'RECOVR AUD' 1795575 2546672 Timestamp('2019-06-27 17:00:00') 0.0 - 1.0
    #  15110.0]

    #delta turnstiles
    cols_diff = ["ENTRIES", "EXITS", "DATE_TIME"]
    cols_add = ["TURNSTILE_ENTRIES", "TURNSTILE_EXITS", "TIME_DELTA"]
    #TODO update the entries to reverse the 'daily previous' as they look to be counting backwards for a few days

    df[cols_add] = df.groupby(by=["STATION", "C/A", "SCP", "LINENAME"])[cols_diff].diff()
    df["entries_cumsum"] = df.groupby(by=["STATION", "C/A", "SCP","LINENAME"])["TURNSTILE_ENTRIES"].cumsum()
    df["exits_cumsum"] = df.groupby(by=["STATION", "C/A", "SCP", "LINENAME"])["TURNSTILE_EXITS"].cumsum()
    df['sum_people'] = df['TURNSTILE_ENTRIES'] + df['TURNSTILE_EXITS']\

    #FATIMA'S

    df["TIME_IN_HOURS"] = df["TIME_DELTA"] / np.timedelta64(1, "h")
    df["TURNSTILE_SUM_RATE"] = df["sum_people"] / df["TIME_IN_HOURS"]


    df.to_pickle('.Turnstile_transformed.pickle')
    print('transformed into .Turnstile_transformed.pickle')

def load(force=False, filename=''):
    from os import path
    import pandas as pd
    import numpy as np


    if force:
        print('Forcing through a new extract and transformation!')
        df = transform(extract(filename))
        print('Loaded forced new copy of data from .Turnstile_transformed.pickle!')
        return df

    elif path.exists('.Turnstile_transformed.pickle'):
        print('Loaded old pickle of data from .Turnstile_transformed.pickle!')
        return pd.read_pickle('.Turnstile_transformed.pickle')

    else:
        print('Loading a new copy of data for {}'.format(filename))
        df = transform(extract(filename))
        print('Loaded new copy of data from .Turnstile_transformed.pickle!')
        return df


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and (sys.argv[1] in ['True', 'true']):
        load(force=True, filename='turnstile_190629.txt')
    elif len(sys.argv) > 1 and (sys.argv[1][-4:] == '.txt'):
        print('loading from '+ sys.argv[1])
        load(force=True, filename= sys.argv[1])
    else:
        load()