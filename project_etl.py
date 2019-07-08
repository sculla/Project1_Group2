#!/anaconda3/envs/metis/bin/python

# assumptions:
# keeping duplicates, they look to be audits back at same timestamp, and count is low.
# negative rates do not meet expectations and are filtered out.
# higher than 60 people per turnstile per minute are unrealistic, and are filtered out.
# the immediate week before the gala was used to show the most recent data.

"""
project_etl.py is a package which contains methods that extract,
transform and load MTA data into a pandas DataFrame for ease
of use.

Expected usages include:

Jupyter Notebook:

from project_etl import load
df = load(True, filename='http://web.mta.info/developers/data/nyct/turnstile/turnstile_190629.txt')
>Forcing through a new extract and transformation!
>transformed into .Turnstile_transformed.pickle
>Loaded forced new copy of data from .Turnstile_transformed.pickle!

Command Line to generate .pickle:

python3 project_etl.py http://web.mta.info/developers/data/nyct/turnstile/turnstile_190629.txt
>Forcing through a new extract and transformation!
>transformed into .Turnstile_transformed.pickle
>Loaded forced new copy of data from .Turnstile_transformed.pickle!

"""
from os import path
import pandas as pd

def _extract(filename=''):
    """
    Extract file and output pickle of the loaded csv into a pickle, optional return of the df.

    :param filename: week's file name or path
    :return: Pandas DataFrame of the MTA week's data with addition of datetime object from
    date & time strings.

    """

    if filename == '':
        raise AttributeError("Filename cannot be blank, please provide file name/link.")

    extracted_df = pd.read_csv(filename, parse_dates=[['DATE', 'TIME']], keep_date_col=True)
    extracted_df.to_pickle('.DateTime_transformed.pickle')
    return extracted_df

def _transform(loaded_df):

    """
    Transform a loaded python data frame from the MTA website, via _extract()

    :param loaded_df: data frame passed from _extract()
    :return: transformed data frame, with new columns for turnstile statistics.
    """

    #column names
    loaded_df.columns = loaded_df.columns.str.strip()
    loaded_df["DAY"] = loaded_df["DATE_TIME"].dt.day_name()

    #delta turnstiles
    cols_diff = ["ENTRIES", "EXITS", "DATE_TIME"]
    cols_add = ["TURNSTILE_ENTRIES", "TURNSTILE_EXITS", "TIME_DELTA"]
    loaded_df[cols_add] = loaded_df.groupby(by=["STATION", "C/A", "SCP", "LINENAME"])\
        [cols_diff].diff()
    loaded_df["entries_cumsum"] = loaded_df.groupby(by=["STATION", "C/A", "SCP", "LINENAME"])\
        ["TURNSTILE_ENTRIES"].cumsum()
    loaded_df["exits_cumsum"] = loaded_df.groupby(by=["STATION", "C/A", "SCP", "LINENAME"])\
        ["TURNSTILE_EXITS"].cumsum()

    #sum
    loaded_df['sum_people'] = loaded_df['TURNSTILE_ENTRIES'] + loaded_df['TURNSTILE_EXITS']

    #rates
    loaded_df["TIME_IN_HOURS"] = loaded_df['TIME_DELTA'].astype('timedelta64[h]')
    loaded_df["TURNSTILE_SUM_RATE"] = loaded_df["sum_people"] / loaded_df["TIME_IN_HOURS"]

    #2 step masking to avoid Pandas SettingwithCopyWarning
    mask = (loaded_df["TURNSTILE_SUM_RATE"] < 3600)
    polished_df = loaded_df[mask]
    mask = (polished_df["TURNSTILE_SUM_RATE"] > 0)
    polished_df = polished_df[mask]

    #last few bits before export
    polished_df.drop(['ENTRIES', 'EXITS'], axis=1, inplace=True)
    polished_df.to_pickle('.Turnstile_transformed.pickle')
    print('transformed into .Turnstile_transformed.pickle')
    return polished_df

def load(force=False, filename=''):

    """
    Load through a MTA .txt file as a pandas dataframe.

    :param force: Bool to force through a new extraction and transformation of a data set,
        or load the saved pickle.
    :param filename: file name to load, can be website, or a local text file in same directory.
    :return: Pandas DataFrame of the MTA data which has been transformed by _transform()
    """

    if force:
        print('Forcing through a new extract and transformation!')
        loaded_df = _transform(_extract(filename))
        print('Loaded forced new copy of data from .Turnstile_transformed.pickle!')

    elif path.exists('.Turnstile_transformed.pickle'):
        print('Loaded old pickle of data from .Turnstile_transformed.pickle!')
        loaded_df = pd.read_pickle('.Turnstile_transformed.pickle')

    else:
        print('Loading a new copy of data for {}'.format(filename))
        loaded_df = _transform(_extract(filename))
        print('Loaded new copy of data from .Turnstile_transformed.pickle!')
    return loaded_df

def top_20(transformed_df):

    """
    This function is a top 20 on a stick, for each week that we wish to view.

    :param transformed_df: a dataframe passed from load()
    :return: a printed list of the top 20 stations for the period.
    """

    daily_riders = transformed_df.groupby(by=["STATION", "LINENAME"])\
        ["TURNSTILE_ENTRIES", "TURNSTILE_EXITS"].sum().reset_index()
    top_stations = daily_riders.sort_values(by=["TURNSTILE_ENTRIES"], ascending=False)
    top_20_stations = top_stations[:20]
    print(top_20_stations['STATION'])

if __name__ == "__main__":
    import sys
    #Command line force argv
    if len(sys.argv) > 1 and (sys.argv[1] in ['True', 'true']):
        load(force=True, filename=sys.argv[2])

    #Command line python3 project_etl.py {html link or .txt file from MTA}
    elif len(sys.argv) > 1 and (str(sys.argv[1])[-4:] == '.txt'):
        print('loading from '+ str(sys.argv[1]))
        load(force=True, filename=sys.argv[1])
    else:
        load()
