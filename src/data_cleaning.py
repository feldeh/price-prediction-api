import pandas as pd
import numpy as np
from pathlib import Path

raw_data_path = Path.cwd() / "data" / "raw" / "properties_data.csv"
df = pd.read_csv(raw_data_path)

# drop columns
col_to_drop = ['URL',
               'Status',
               'creationDate',
               'lastModificationDate',
               'fireplaceExists',
               'showerRoomCount',
               'hasDoubleGlazing',
               'transactionType',
               'transactionSubtype',
               'saleType',
               'country',
               'hasAirConditioning',
               'isSubjectToVat',
               'parkingCountOutdoor']
df.drop(col_to_drop, axis=1, inplace=True)

# drop rows with missing values
df.dropna(how='any', subset=['price', 'netHabitableSurface', 'region'], inplace=True)

# replace values which contains only [.,-] characters with NaN
df['number'].replace(r'^[.,-]+$', np.nan, regex=True, inplace=True)
# remove trailing [.,-] characters
df['number'].replace(r'[.,-]+$', '', regex=True, inplace=True)
# drop duplicates
df.drop_duplicates(subset=['latitude', 'longitude', 'price', 'street', 'postalCode', 'number'], inplace=True)

# impute missing values to False
df[['hasGarden', 'hasTerrace', 'hasSwimmingPool']] = df[['hasGarden', 'hasTerrace', 'hasSwimmingPool']].fillna(False)
# impute missing values to 0
df['parkingCountIndoor'] = df['parkingCountIndoor'].fillna(0)

# cast from float to str
df['postalCode'] = df['postalCode'].astype(str)

IQR = df['price'].quantile(0.75) - df['price'].quantile(0.25)

upper_limit = df['price'].quantile(0.75) + 1.5 * IQR
lower_limit = df['price'].quantile(0.25) - 1.5 * IQR

df = df[(df['price'] < upper_limit) & (df['price'] > lower_limit)]

clean_data_path = Path.cwd() / "data" / "clean" / "clean_data.csv"
df.to_csv(clean_data_path, index=False)
