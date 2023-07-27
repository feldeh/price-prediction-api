import pandas as pd
import numpy as np
from pathlib import Path


def first_clean_data(df):

    print(f"Raw data shape: {df.shape}")

    # replace values which contains only [.,-] characters with NaN
    df['number'].replace(r'^[.,-]+$', np.nan, regex=True, inplace=True)
    # remove trailing [.,-] characters
    df['number'].replace(r'[.,-]+$', '', regex=True, inplace=True)

    # drop duplicate rows
    df.drop_duplicates(subset=['latitude', 'longitude', 'price', 'street', 'postalCode', 'number'], inplace=True)

    # drop columns
    col_to_drop = ['URL',
                   'id',
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
                   'parkingCountOutdoor',
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
                   'facadeCount',
                   ]
    df.drop(col_to_drop, axis=1, inplace=True)

    # drop rows
    df.dropna(how='any', subset=['price', 'netHabitableSurface', 'region', 'latitude'], inplace=True)

    df.drop(df[(df['type'] == 'APARTMENT_GROUP') | (df['type'] == 'HOUSE_GROUP')].index, inplace=True)
    df.drop(df[df['subtype'] == 'MIXED_USE_BUILDING'].index, inplace=True)
    df.drop(df[df['saleType'] == 'publicSale'].index, inplace=True)

    # data imputation
    bool_col = ['hasGarden', 'hasTerrace', 'hasSwimmingPool', 'hasAirConditioning', 'hasLift', 'hasDoubleGlazing']
    df[bool_col] = df[bool_col].fillna(False)

    num_col = ['terraceSurface', 'gardenSurface', 'parkingCountIndoor', 'bathroomCount', 'showerRoomCount', 'bedroomCount']
    df[num_col] = df[num_col].fillna(0)

    obj_col = ['heatingType', 'condition', 'kitchen']
    df[obj_col] = df[obj_col].fillna('NO_INFO')

    df['saleType'] = df['saleType'].fillna('normalSale')

    df['subtype'] = df['subtype'].fillna(df['type'])

    # type casting
    float_col = ['postalCode', 'constructionYear']
    df[float_col] = df[float_col].astype('str')
    df['constructionYear'] = df['constructionYear'].fillna('NO_INFO')

    boolean_col = ['hasLift', 'hasGarden', 'hasTerrace', 'fireplaceExists', 'hasSwimmingPool', 'hasAirConditioning', 'hasDoubleGlazing']
    df[boolean_col] = df[boolean_col].astype(int)

    # data recoding
    df.loc[(df['kitchen'] == 'HYPER_EQUIPPED') | (df['kitchen'] == 'USA_HYPER_EQUIPPED'), 'kitchen'] = 'SUPER_EQUIPPED'
    df.loc[df['kitchen'] == 'USA_SEMI_EQUIPPED', 'kitchen'] = 'SEMI_EQUIPPED'
    df.loc[df['kitchen'] == 'USA_INSTALLED', 'kitchen'] = 'INSTALLED'
    df.loc[df['kitchen'] == 'USA_UNINSTALLED', 'kitchen'] = 'NOT_INSTALLED'

    df.loc[(df['heatingType'] == 'PELLET') | (df['heatingType'] == 'WOOD') | (df['heatingType'] == 'SOLAR') | (df['heatingType'] == 'CARBON'), 'heatingType'] = 'OTHER'

    return df


def iqr_outliers(df, col, upper_multiplier=1.5, lower_multiplier=1.5):
    IQR = df[col].quantile(0.75) - df[col].quantile(0.25)

    upper_limit = df[col].quantile(0.75) + upper_multiplier * IQR
    lower_limit = df[col].quantile(0.25) - lower_multiplier * IQR

    df = df[(df[col] < upper_limit) & (df[col] > lower_limit)]

    return df


def remove_outliers(df):

    df['pricePerSqm'] = df['price'] / df['netHabitableSurface']

    df_h = df[df['type'] == 'HOUSE']
    df_h = iqr_outliers(df_h, 'price')
    df_h = iqr_outliers(df_h, 'pricePerSqm')
    df_h = iqr_outliers(df_h, 'netHabitableSurface')

    df_a = df[df['type'] == 'APARTMENT']
    df_a = iqr_outliers(df_a, 'price')
    df_a = iqr_outliers(df_a, 'pricePerSqm')
    df_a = iqr_outliers(df_a, 'pricePerSqm')

    df = pd.concat([df_h, df_a], ignore_index=True)

    df.drop('pricePerSqm', axis=1, inplace=True)

    print(f"Cleaned data shape: {df.shape}")

    return df


def clean_data(df):

    first_clean_df = first_clean_data(df)
    outlier_clean_df = remove_outliers(first_clean_df)

    outlier_clean_df.to_csv(Path.cwd() / "data" / "clean" / "clean_data.csv", index=False)
    outlier_clean_df.to_pickle(Path.cwd() / "data" / "clean" / "clean_data.pkl")

    return outlier_clean_df
