from stock_data_ai import train_regression_model

def predict_price_movement(model, current_price, features):
    predicted_price = model.predict(features)
    if predicted_price > current_price:
        return "up"
    else:
        return "down"
