import random

def predict_demand():
    # simulate AI / forecasting output
    base = 500
    trend = random.randint(-50, 150)
    noise = random.randint(-20, 20)

    prediction = base + trend + noise
    return prediction