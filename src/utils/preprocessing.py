from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


def preprocess_data(X, y):
    xgb_features = ['region', 'province', 'district', 'netHabitableSurface', 'bedroomCount',
                    'hasDoubleGlazing', 'condition', 'hasSwimmingPool', 'bathroomCount',
                    'showerRoomCount', 'parkingCountIndoor', 'hasGarden', 'gardenSurface',
                    'hasTerrace', 'hasLift', 'kitchen', 'latitude', 'longitude', 'constructionYear']

    X = X[xgb_features]

    # split the dataset into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # numerical features
    numerical_features = X.select_dtypes(exclude=['object']).columns
    numerical_pipeline = Pipeline([('minmax', MinMaxScaler())])

    # categorical features
    categorical_features = X.select_dtypes(include=['object']).columns
    categorical_pipeline = Pipeline([('onehot', OneHotEncoder(handle_unknown='ignore'))])

    transformer = ColumnTransformer(
        [("categorical_preprocessing", categorical_pipeline, categorical_features),
         ("numerical_preprocessing", numerical_pipeline, numerical_features)]
    )

    return X_train, X_test, y_train, y_test, transformer
