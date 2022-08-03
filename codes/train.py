from lightgbm import LGBMRegressor
import lightgbm as lgb
import os


# train lgb
def train_lgb(model_dir, data_dir, train_steps, eval_steps):
    """Train the model."""
    # Load the model
    model = LGBMRegressor.Boosting()

    # Create dataset lgb dataset
    train_data = lgb.Dataset(os.path.join(data_dir, 'train.csv'))
    eval_data = lgb.Dataset(os.path.join(data_dir, 'eval.csv'))

    # Create a trainig and evaluation function
    train_func = model.fit(train_data, epochs=train_steps)
    eval_func = model.evaluate(eval_data)

    # Save the model
    model.save_model(os.path.join(model_dir, 'model.txt'))

    # Return the training and evaluation function
    return train_func, eval_func