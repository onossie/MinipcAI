from sklearn.linear_model import LogisticRegression
import numpy as np

def prepare_training_data(candles):
    prices = [float(c[2]) for c in candles]
    X = []
    y = []
    for i in range(2, len(prices)):
        X.append([prices[i-1], prices[i-2]])
        y.append(1 if prices[i] > prices[i-1] else 0)
    return np.array(X), np.array(y)

def train_model(candles):
    X, y = prepare_training_data(candles)
    if len(X) < 10:
        return None
    model = LogisticRegression()
    model.fit(X, y)
    return model

def predict_trade(model, candles):
    if model is None or len(candles) < 3:
        return None
    prices = [float(c[2]) for c in candles]
    X_pred = np.array([[prices[-1], prices[-2]]])
    return model.predict(X_pred)[0]
