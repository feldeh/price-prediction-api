import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
import xgboost as xgb
import joblib

from src.utils.data_cleaning import clean_data


def preprocess_data(X_train):

    # numerical features transformer
    numerical_features = X_train.select_dtypes(exclude=['object']).columns
    numerical_pipeline = Pipeline([('minmax', MinMaxScaler())])

    # categorical features transformer
    categorical_features = X_train.select_dtypes(include=['object']).columns
    categorical_pipeline = Pipeline([('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=True))])

    transformer = ColumnTransformer(
        [("categorical_preprocessing", categorical_pipeline, categorical_features),
         ("numerical_preprocessing", numerical_pipeline, numerical_features)]
    )

    return transformer


def train_model(X_train, y_train):

    transformer = preprocess_data(X_train)

    ml_pipeline = Pipeline([('preprocessing', transformer),
                            ('xgboost', xgb.XGBRegressor())])

    model = ml_pipeline.fit(X_train, y_train)

    return model


def eval_model(model, X, y):

    cv_results = cross_validate(model, X, y, scoring=['neg_mean_squared_error', 'r2'], return_train_score=True)
    print(f"Cross validation results: {cv_results}")

    scores = cross_val_score(model, X, y)
    print(f"Mean accuracy score: {scores.mean():.2f}+/-{scores.std():.2f}")


def train_eval_save_model():

    raw_data_path = Path.cwd() / "datasets" / "raw" / "properties_data.csv"
    df = pd.read_csv(raw_data_path)
    clean_df = clean_data(df)

    xgb_features = ['region', 'province', 'district', 'netHabitableSurface', 'bedroomCount',
                    'hasDoubleGlazing', 'condition', 'hasSwimmingPool', 'bathroomCount',
                    'showerRoomCount', 'parkingCountIndoor', 'hasGarden', 'gardenSurface',
                    'hasTerrace', 'hasLift', 'kitchen', 'latitude', 'longitude'
                    ]

    clean_df = clean_df[xgb_features + ['price']]

    X = clean_df.drop('price', axis=1)
    y = clean_df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)

    eval_model(model, X, y)

    model_path = Path.cwd() / "models" / "model.pkl"

    joblib.dump(model, model_path)


if __name__ == '__main__':
    train_eval_save_model()
