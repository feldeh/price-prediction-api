from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import xgboost as xgb
from random import *
import pandas as pd
import numpy as np
from pathlib import Path


def split_house_apartment(df):
    df_h = df[df['type'] == 'HOUSE']
    df_a = df[df['type'] == 'APARTMENT']
    df_h = df_h.drop('type', axis=1)
    df_a = df_a.drop('type', axis=1)

    return df_h, df_a


def split_train_test(df, random_state):
    X, y = df.drop('price', axis=1), df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state)

    return X_train, X_test, y_train, y_test


def scale_features(X_train, X_test):

    scaler = MinMaxScaler()
    scaled_X_train = scaler.fit_transform(X_train)
    scaled_X_test = scaler.transform(X_test)

    df_scaled_X_train = pd.DataFrame(scaled_X_train, columns=X_train.columns)
    df_scaled_X_test = pd.DataFrame(scaled_X_test, columns=X_test.columns)

    return df_scaled_X_train, df_scaled_X_test


def regression_train_eval(X_train, X_test, y_train, y_test, prop_type):

    scaled_X_train, scaled_X_test = scale_features(X_train, X_test)

    model = LinearRegression()
    model.fit(scaled_X_train, y_train)
    y_pred = model.predict(X_test)

    # weights associated with each features
    # print("Coefficients: \n", model.coef_)

    print(f'    LINEAR REGRESSION {prop_type} model:')
    print("        Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
    print("        Training score: %.2f" % model.score(scaled_X_train, y_train))
    print("        Test score: %.2f" % model.score(scaled_X_test, y_test))

    # plt.scatter(y_test, y_pred, color="black")
    # plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="blue")
    # plt.title(f'{prop_type}')
    # plt.xlabel("Actual Price")
    # plt.ylabel("Predicted Price")
    # plt.show()


def linear_reg(df, prop_type, random_state):
    X_train, X_test, y_train, y_test = split_train_test(df, random_state)
    regression_train_eval(X_train, X_test, y_train, y_test, prop_type)


def main_linear(df, df_h, df_a):
    linear_reg_features = ['price', 'region', 'province', 'netHabitableSurface', 'bedroomCount', 'hasDoubleGlazing', 'condition', 'hasSwimmingPool',
                           'bathroomCount', 'showerRoomCount', 'parkingCountIndoor', 'hasGarden', 'gardenSurface', 'hasTerrace', 'hasLift', 'kitchen', 'latitude', 'longitude']
    df_a = df_a[linear_reg_features]
    df_h = df_h[linear_reg_features]
    df = df[linear_reg_features]

    df_a = pd.get_dummies(df_a)
    df_h = pd.get_dummies(df_h)
    df = pd.get_dummies(df)
    random_state = randint(1, 1000)
    print(f'RANDOM STATE: {random_state}')
    linear_reg(df, 'FULL dataset', random_state)
    linear_reg(df_h, 'HOUSE dataset', random_state)
    linear_reg(df_a, 'APARTMENT dataset', random_state)


def xgb_train_eval(X_train, X_test, y_train, y_test, prop_type):

    # scale features
    scaled_X_train, scaled_X_test = scale_features(X_train, X_test)

    model = xgb.XGBRegressor()
    model.fit(scaled_X_train, y_train)
    y_pred = model.predict(scaled_X_test)

    print(f'    XGBOOST REGRESSION {prop_type} model:')
    print("        Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
    print("        Training score: %.2f" % model.score(scaled_X_train, y_train))
    print("        Test score: %.2f" % model.score(scaled_X_test, y_test))

    # plt.scatter(y_test, y_pred, color="black")
    # plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="blue")
    # plt.title(f'{prop_type}')
    # plt.xlabel("Actual Price")
    # plt.ylabel("Predicted Price")
    # plt.show()


def xgb_reg(df, prop_type, random_state):
    X_train, X_test, y_train, y_test = split_train_test(df, random_state)
    xgb_train_eval(X_train, X_test, y_train, y_test, prop_type)


def main_xgb(df, df_h, df_a):
    xgb_features = ['price', 'region', 'province', 'district', 'netHabitableSurface', 'bedroomCount', 'hasDoubleGlazing', 'condition', 'hasSwimmingPool', 'bathroomCount',
                    'showerRoomCount', 'parkingCountIndoor', 'hasGarden', 'gardenSurface', 'hasTerrace', 'hasLift', 'kitchen', 'latitude', 'longitude', 'constructionYear']
    df_a = df_a[xgb_features]
    df_h = df_h[xgb_features]
    df = df[xgb_features]

    df_a = pd.get_dummies(df_a)
    df_h = pd.get_dummies(df_h)
    df = pd.get_dummies(df)

    random_state = randint(1, 1000)
    print("===========================================")
    print(f'RANDOM STATE: {random_state}')
    xgb_reg(df, 'FULL dataset', random_state)
    xgb_reg(df_h, 'HOUSE dataset', random_state)
    xgb_reg(df_a, 'APARTMENT dataset', random_state)
