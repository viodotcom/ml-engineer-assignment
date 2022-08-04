def train_data_gen(config_file):
    """
    Generate training data for the model.
    """
    # Load the config file
    config = yaml.load(open(config_file))

    # Generate the data

    # Split the data into train and eval
    train_data = data.sample(frac=0.8, random_state=0)
    eval_data = data.drop(train_data.index)

    # Save the train and eval data
    train_data.to_csv(config['data_dir'] + '/train.csv', index=False)
    eval_data.to_csv(config['data_dir'] + '/eval.csv', index=False)

    # Return the training and evaluation function
    return 


def test_data_gen(config_file):
    """
    Generate test data for the model.
    """
    # Load the config file
    config = yaml.load(open(config_file))

    # Generate the data


    # Save the test data
    data.to_csv(config['data_dir'] + '/test.csv', index=False)

    # Return the test data
    return
