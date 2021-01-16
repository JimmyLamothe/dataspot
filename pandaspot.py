import pandas as pd
import numpy as np

with open('data/user_artists.csv', 'r') as csv_file:
    user_artists = pd.read_csv(csv_file)

print(user_artists.head())
