
# Fatima
# TODO StationNames

# aaron's td

# TODO enries per time exits per time


def extract(filename= 'turnstile_190629.txt'):
    """

    :param filename: week's file name
    :return: Pandas DataFrame of the MTA week's data with a datetime object in place of the date & time objects
    """


    import pandas as pd
    df = pd.read_csv(filename)

    return df



def transform(df):
    import pandas as pd
    from datetime import datetime

    #DateTime transform
    dt_format = '%m/%d/%Y %H:%M:%S'
    working = []

    for _, row in enumerate(df.values):
        working.append(datetime.strptime(row[6]+' '+row[7], dt_format))
    df['datetime'] = pd.DataFrame(working)
    df.drop(columns=['DATE', 'TIME'], inplace=True)
    df.to_pickle('.DateTime_transformed.pickle')

    #column names
    df.columns = df.columns.str.strip()

    #delta turnstiles
    cols_diff = ["ENTRIES", "EXITS"]
    cols_add = ["TURNSTILE_ENTRIES", "TURNSTILE_EXITS"]
    df[cols_add] = df.groupby(by=["STATION", "C/A", "SCP", "LINENAME"])[cols_diff].diff()
    df.to_pickle('.Turnstile_transformed.pickle')

    return df


if __name__ == "__main__":
    transform(extract())