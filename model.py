from connection import engine
import pandas as pd
import dask.dataframe as dd
from dask_ml.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PowerTransformer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
import pickle

# --- 🚀 Fetch Data from Snowflake ---
def fetch_cleaned_data():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM crypto_market_cleaned;", conn)
    return df

df = fetch_cleaned_data()

# Convert to Dask DataFrame for efficient processing
ddf = dd.from_pandas(df, npartitions=4)

# --- 🚀 Feature Selection ---
features = ["market_cap", "total_volume", "circulating_supply"]
target = "price_change_percentage_24h"

# Train-Test Split
X = ddf[features]
y = ddf[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

# Convert to Pandas (since Scikit-Learn doesn’t support Dask)
X_train = X_train.compute()
X_test = X_test.compute()
y_train = y_train.compute()
y_test = y_test.compute()

# --- 🚀 Outlier Removal ---
def remove_outliers(df, threshold=3):
    return df[(np.abs((df - df.mean()) / df.std()) < threshold).all(axis=1)]

X_train = remove_outliers(X_train)
y_train = y_train.loc[X_train.index]  # Keep labels aligned

# --- 🚀 Data Augmentation (Gaussian Noise) ---
def augment_data(X, y, noise_level=0.01, copies=3):
    X_aug = []
    y_aug = []
    
    for _ in range(copies):
        noise = np.random.normal(0, noise_level, X.shape)  # Generate noise
        X_aug.append(X + noise)  # Add noise to features
        y_aug.append(y + np.random.normal(0, noise_level * np.std(y)))  # Add noise to target
    
    X_aug.append(X)  # Include original data
    y_aug.append(y)
    
    return np.vstack(X_aug), np.hstack(y_aug)

X_train_aug, y_train_aug = augment_data(X_train.values, y_train.values)

# --- 🚀 Feature Engineering (Normalization) ---
scaler = PowerTransformer()
X_train_aug = scaler.fit_transform(X_train_aug)
X_test = scaler.transform(X_test)

# --- 🚀 Hyperparameter Tuning for RandomForest ---
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

rf = RandomForestRegressor(random_state=42)
random_search = RandomizedSearchCV(rf, param_grid, n_iter=10, cv=3, random_state=42, n_jobs=-1)
random_search.fit(X_train_aug, y_train_aug)

# --- 🚀 Train Best Model ---
best_model = random_search.best_estimator_
y_pred = best_model.predict(X_test)

# --- 🚀 Evaluation ---
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error (MAE): {mae:.4f}")

# --- 🚀 Save Model ---
with open("crypto_price_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

print("✅ Model saved successfully!")
