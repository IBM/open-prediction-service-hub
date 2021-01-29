import numpy as np
import pandas as pd
from openapi_server.common import get_feature_names, get_label_name
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# Load the file to Pandas DataFrame using code below
features = get_feature_names()
label = get_label_name()
df = pd.read_csv(
    './data/miniloan-payment-default-cases-v2.0.csv',
    header=0,
    delimiter=r'\s*,\s*',
    engine='python'
).replace(
    [np.inf, -np.inf], np.nan
).dropna().loc[:, features + [label]]

# Train / test split
split_data = np.split(df.sample(frac=1, random_state=42), [int(.8*len(df)), int((.8+.18)*len(df))])
train_data = split_data[0]
test_data = split_data[1]
predict_data = split_data[2]

clf = SGDClassifier(loss="log", penalty="l2", random_state=42, tol=1e-3)
scaler = StandardScaler()

pipeline = Pipeline([
    ('standardize', scaler),
    ("classifier", clf)
])


x_train_data = train_data.loc[:, features]
y_train_data = train_data.loc[:, label]

pipeline.fit(x_train_data, y_train_data)


def predict_proba(data):
    return pipeline.predict_proba(data)[0]
