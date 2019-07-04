
# Fatima
# TODO StationNames

# aaron's td

# TODO enries per time exits per time

##assumptions:
##  keeping duplicates, they look to be audits back at same timestamp


def extract(filename= 'turnstile_190629.txt'):
    """

    :param filename: week's file name
    :return: Pandas DataFrame of the MTA week's data with a datetime object in place of the date & time objects
    """

    import pandas as pd

    df = pd.read_csv(filename, parse_dates=[['DATE', 'TIME']], keep_date_col=True)
    df.to_pickle('.DateTime_transformed.pickle')

    return df



def transform(df):
    import pandas as pd
    from datetime import datetime

    #DateTime transform


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
    cols_diff = ["ENTRIES", "EXITS"]
    cols_add = ["TURNSTILE_ENTRIES", "TURNSTILE_EXITS"]
    #TODO update the entries to reverse the 'daily previous' as they look to be counting backwards for a few days

    df[cols_add] = df.groupby(by=["STATION", "C/A", "SCP", "LINENAME"])[cols_diff].diff()
    df["entries_cumsum"] = df.groupby(by=["STATION", "C/A", "SCP", "LINENAME"])["TURNSTILE_ENTRIES"].cumsum()
    df["exits_cumsum"] = df.groupby(by=["STATION", "C/A", "SCP", "LINENAME"])["TURNSTILE_EXITS"].cumsum()
    df['sum_people'] = df['TURNSTILE_ENTRIES'] + df['TURNSTILE_EXITS']
    df.to_pickle('.Turnstile_transformed.pickle')
    print('transformed into .Turnstile_transformed.pickle')


if __name__ == "__main__":
    transform(extract())