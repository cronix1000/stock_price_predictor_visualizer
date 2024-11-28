from stock_data_ai import train_regression_model

def predict_price_movement(model, features):
    """Predict the price movement based on the given features."""
    prediction = model.predict(features)

    return prediction