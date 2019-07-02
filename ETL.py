
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

def extract(filename= PATH):

    import pandas as pd
    import numpy as np
    df = pd.read_csv(filename)
    print(df['ENTRIES'].describe())


if __name__ == "__main__":
    extract()