from src.data_cleaning import clean_data
from src.data_cleaning import clean_data
from pathlib import Path
import pandas as pd
from src.model import *


def main():
    raw_data_path = Path.cwd() / "data" / "raw" / "properties_data.csv"
    df = pd.read_csv(raw_data_path)
    clean_df = clean_data(df)
    df_h, df_a = split_house_apartment(clean_df)
    main_linear(clean_df, df_h, df_a)
    main_xgb(clean_df, df_h, df_a)


if __name__ == "__main__":
    main()
