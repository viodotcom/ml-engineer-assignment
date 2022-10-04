import sklearn


def inference(input_data):
    """
    Inference function for the model.
    """
    # Load the model
    model = sklearn.externals.joblib.load('model.txt')
    # Make a prediction
    prediction = model.predict(input_data)
    return prediction
