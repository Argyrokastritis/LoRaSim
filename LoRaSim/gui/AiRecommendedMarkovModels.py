import pandas as pd
import numpy as np
from hmmlearn import hmm

class AiRecommendedMarkovModels:
    """
    A class representing a collection of AI recommended Markov models.
    """

    def __init__(self):
        pass

    def generate_models(self):
        # Load data from Markov models.csv file
        data = pd.read_csv('Markov models.csv')

        # Extract transition and emission probabilities from data
        X = data[['P00', 'P01', 'P10', 'P11']].values

        # Train a Hidden Markov Model using the Baum-Welch algorithm
        model = hmm.MultinomialHMM(n_components=2, n_iter=1000)
        model.fit(X)

        # Generate new Markov models using the trained model
        new_models = []
        for i in range(10):
            # Generate a new sequence of hidden states
            hidden_states = model.predict(X)

            # Generate a new sequence of observations
            observations = model.sample(X.shape[0])[0]

            # Compute transition and emission probabilities from new sequences
            P00 = np.sum((hidden_states[:-1] == 0) & (hidden_states[1:] == 0)) / np.sum(hidden_states[:-1] == 0)
            P01 = np.sum((hidden_states[:-1] == 0) & (hidden_states[1:] == 1)) / np.sum(hidden_states[:-1] == 0)
            P10 = np.sum((hidden_states[:-1] == 1) & (hidden_states[1:] == 0)) / np.sum(hidden_states[:-1] == 1)
            P11 = np.sum((hidden_states[:-1] == 1) & (hidden_states[1:] == 1)) / np.sum(hidden_states[:-1] == 1)

            # Add new Markov model to list
            new_models.append({'Title': f'Model {i+1}', 'Description': f'This is a new Markov model generated by the AI algorithm.', 'P00': P00, 'P01': P01, 'P10': P10, 'P11': P11})

        # Save new Markov models to AI recommended Markov models.csv file
        new_data = pd.DataFrame(new_models)
        new_data.to_csv('AI recommended Markov models.csv', index=False)

        print("New Markov models generated and saved to 'AI recommended Markov models.csv'!")
