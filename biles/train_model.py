import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Sample data (replace with data from your database)
data = {
    "price": [1000, 0, 100000, 0, 0, 0, 28000, 670028, 120000, 13000, 10000, 11207230, 10000],
    "net": [128, 0, 10000, 0, 0, 0, 402, 3069, 900, 128, 1200, 1052996, 9000],
    "top": [131, 0, 18000, 0, 0, 0, 609, 4385, 930, 131, 1680, 1378558, 9300],
    "is_paid": [False, False, False, False, False, False, False, False, False, True, False, False, False],
    "done": [False, True, False, False, False, False, False, False, False, True, False, False, True]
}

df = pd.DataFrame(data)

# Convert boolean values to 0 and 1 for model compatibility
df['is_paid'] = df['is_paid'].astype(int)
df['done'] = df['done'].astype(int)

# Features and target
X = df[['price', 'net', 'top']]  # Features
y = df['done']  # Target: Predict whether the bill is done (0 or 1)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
