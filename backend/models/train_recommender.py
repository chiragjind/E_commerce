import numpy as np
import pandas as pd

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 1) Generate synthetic users, products, and interactions
NUM_USERS = 50
NUM_PRODUCTS = 5   # we already have 5 products in DB

np.random.seed(42)

user_ids = np.random.randint(1, NUM_USERS + 1, size=200)
product_ids = np.random.randint(1, NUM_PRODUCTS + 1, size=200)

# actions: view = 0, click = 1, buy = 2 (higher = more interest)
actions = np.random.choice([0, 1, 2], size=200, p=[0.6, 0.3, 0.1])

data = pd.DataFrame({
    "user_id": user_ids,
    "product_id": product_ids,
    "action_score": actions
})

print("Sample of synthetic interaction data:")
print(data.head())
print("\nData shape:", data.shape)



# 2) Prepare data for training
X = data[["user_id", "product_id"]]
y = data["action_score"]

# 3) Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4) Train XGBoost model
model = XGBRegressor(
    n_estimators=60,
    max_depth=4,
    learning_rate=0.1,
    subsample=0.9,
    colsample_bytree=0.9
)

model.fit(X_train, y_train)

# 5) Evaluate
preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
print("\nXGBoost trained. Test MSE:", mse)

# 6) Save model
model.save_model("models/xgb_model.json")
print("Saved model to models/xgb_model.json")


from sklearn.neural_network import MLPRegressor

# 7) Simple Neural Network (MLP)
nn_model = MLPRegressor(
    hidden_layer_sizes=(64, 32),
    activation='relu',
    solver='adam',
    max_iter=500
)

nn_model.fit(X_train, y_train)

# 8) Evaluate NN
nn_preds = nn_model.predict(X_test)
nn_mse = mean_squared_error(y_test, nn_preds)
print("\nNeural Network trained. Test MSE:", nn_mse)

# 9) Save NN model
import pickle
with open("models/nn_model.pkl", "wb") as f:
    pickle.dump(nn_model, f)

print("Saved model to models/nn_model.pkl")


