#!/usr/bin/env python
"""
Fast Model Training Script
Trains the Random Forest model and saves all artifacts
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import sys

print("=" * 70)
print("HOUSE PRICE PREDICTION - MODEL TRAINING")
print("=" * 70)

# Step 1: Load Data
print("\n[1/7] Loading dataset...")
try:
    df = pd.read_csv('model/house_prices_train.csv')
    print(f"✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
except FileNotFoundError:
    print("✗ ERROR: house_prices_train.csv not found in model/ directory")
    sys.exit(1)

# Step 2: Select Features
print("\n[2/7] Selecting features...")
selected_features = ['OverallQual', 'GrLivArea', 'TotalBsmtSF', 'GarageCars', 'FullBath', 'YearBuilt']
target = 'SalePrice'

print(f"✓ Features: {selected_features}")
print(f"✓ Target: {target}")

# Step 3: Handle Missing Values
print("\n[3/7] Handling missing values...")
df_processed = df[selected_features + [target]].copy()
df_processed = df_processed.dropna()
print(f"✓ Dataset after removing missing values: {df_processed.shape[0]} rows")

# Step 4: Prepare Data
print("\n[4/7] Preparing data...")
X = df_processed[selected_features]
y = df_processed[target]

# CRITICAL: Split BEFORE scaling (no data leakage!)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"✓ Train set: {X_train.shape[0]} samples")
print(f"✓ Test set: {X_test.shape[0]} samples")

# Step 5: Scale Features (ONLY on training data)
print("\n[5/7] Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"✓ Scaler fitted on training data only")

# Step 6: Train Model
print("\n[6/7] Training Random Forest Regressor...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_scaled, y_train)
print(f"✓ Model trained successfully")

# Step 7: Evaluate Model
print("\n[7/7] Evaluating model...")
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)

train_mae = mean_absolute_error(y_train, y_train_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
train_mse = mean_squared_error(y_train, y_train_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
train_rmse = np.sqrt(train_mse)
test_rmse = np.sqrt(test_mse)
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

print("\n" + "=" * 70)
print("MODEL EVALUATION METRICS")
print("=" * 70)
print("\nTRAINING METRICS:")
print(f"  MAE:  ${train_mae:,.2f}")
print(f"  MSE:  ${train_mse:,.2f}")
print(f"  RMSE: ${train_rmse:,.2f}")
print(f"  R²:   {train_r2:.4f}")

print("\nTEST METRICS:")
print(f"  MAE:  ${test_mae:,.2f}")
print(f"  MSE:  ${test_mse:,.2f}")
print(f"  RMSE: ${test_rmse:,.2f}")
print(f"  R²:   {test_r2:.4f}")

# Feature Importance
print("\nFEATURE IMPORTANCE:")
feature_importance = pd.DataFrame({
    'feature': selected_features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.iterrows():
    print(f"  {row['feature']:20s}: {row['importance']:.4f}")

# Save Artifacts
print("\n" + "=" * 70)
print("SAVING MODEL ARTIFACTS")
print("=" * 70)

model_path = 'model/house_price_model.pkl'
scaler_path = 'model/scaler.pkl'
features_path = 'model/selected_features.pkl'

joblib.dump(model, model_path)
print(f"✓ Model saved: {model_path}")

joblib.dump(scaler, scaler_path)
print(f"✓ Scaler saved: {scaler_path}")

joblib.dump(selected_features, features_path)
print(f"✓ Features saved: {features_path}")

# Verify Reloading
print("\n" + "=" * 70)
print("VERIFYING MODEL ARTIFACTS")
print("=" * 70)

loaded_model = joblib.load(model_path)
loaded_scaler = joblib.load(scaler_path)
loaded_features = joblib.load(features_path)

y_test_pred_reloaded = loaded_model.predict(loaded_scaler.transform(X_test))
reloaded_r2 = r2_score(y_test, y_test_pred_reloaded)

print(f"✓ Model reloaded successfully")
print(f"✓ Scaler reloaded successfully")
print(f"✓ Features reloaded successfully")
print(f"✓ R² match: {abs(reloaded_r2 - test_r2) < 1e-6}")

print("\n" + "=" * 70)
print("✓ TRAINING COMPLETE - ALL ARTIFACTS SAVED")
print("=" * 70)
print("\nYou can now run:")
print("  python app.py")
print("\nThen visit: http://localhost:5000")
