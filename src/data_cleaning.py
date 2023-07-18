import pandas as pd
import numpy as np
from pathlib import Path


def outliers_removal(df, variables):
    IQR = df[variables].quantile(0.75) - df[variables].quantile(0.25)

    upper_limit = df[variables].quantile(0.75) + 1.5 * IQR
    lower_limit = df[variables].quantile(0.25) - 1.5 * IQR

    df = df[(df[variables] < upper_limit) & (df[variables] > lower_limit)]

    return df


def data_cleaner(df):

    # replace values which contains only [.,-] characters with NaN
    df['number'].replace(r'^[.,-]+$', np.nan, regex=True, inplace=True)
    # remove trailing [.,-] characters
    df['number'].replace(r'[.,-]+$', '', regex=True, inplace=True)

    # drop duplicate rows
    df.drop_duplicates(subset=['latitude', 'longitude', 'price', 'street', 'postalCode', 'number'], inplace=True)

    # drop columns
    col_to_drop = ['URL',
                   'Status',
                   'creationDate',
                   'lastModificationDate',
                   'transactionType',
                   'transactionSubtype',
                   'country',
                   'isSubjectToVat',
                   'box',
                   'number',
                   'street',
                   'isFurnished',
                   'floor',
                   'floorCount',
                   'land',
                   'toiletCount',
                   'epcScore',
                   'primaryEnergyConsumptionPerSqm',
                   'bookmarkCount',
                   'viewCount',
                   'locality',
                   'facadeCount'
                   ]
    df.drop(col_to_drop, axis=1, inplace=True)

    # drop rows
    df.dropna(how='any', subset=['price', 'netHabitableSurface', 'region'], inplace=True)

    df.drop(df[(df['type'] == 'APARTMENT_GROUP') | (df['type'] == 'HOUSE_GROUP')].index, inplace=True)

    # cast from float to str
    float_col = ['postalCode', 'constructionYear']
    df[float_col] = df[float_col].convert_dtypes().astype('Int64').astype('str')

    # data imputation
    bool_col = ['hasGarden', 'hasTerrace', 'hasSwimmingPool', 'hasAirConditioning', 'hasLift', 'hasDoubleGlazing']
    df[bool_col] = df[bool_col].fillna(False)

    num_col = ['terraceSurface', 'gardenSurface', 'parkingCountIndoor', 'bathroomCount', 'showerRoomCount', 'bedroomCount']
    df[num_col] = df[num_col].fillna(0)

    obj_col = ['heatingType', 'condition', 'kitchen']
    df[obj_col] = df[obj_col].fillna('no_info')

    df['saleType'] = df['saleType'].fillna('normalSale')

    df['subtype'] = df['subtype'].fillna(df['type'])

    # data recoding
    df.loc[(df['kitchen'] == 'HYPER_EQUIPPED') | (df['kitchen'] == 'USA_HYPER_EQUIPPED'), 'kitchen'] = 'SUPER_EQUIPPED'
    df.loc[df['kitchen'] == 'USA_SEMI_EQUIPPED', 'kitchen'] = 'SEMI_EQUIPPED'
    df.loc[df['kitchen'] == 'USA_INSTALLED', 'kitchen'] = 'INSTALLED'
    df.loc[df['kitchen'] == 'USA_UNINSTALLED', 'kitchen'] = 'NOT_INSTALLED'

    return df


raw_data_path = Path.cwd() / "data" / "raw" / "properties_data.csv"
df = pd.read_csv(raw_data_path)

clean_df = data_cleaner(df)

clean_data_path = Path.cwd() / "data" / "clean" / "clean_data.csv"
clean_df.to_csv(clean_data_path, index=False)
