# for creating model
# usage: python set_model.py
from recommendations import Recommendation
import os.path

if not os.path.isdir('models'):
    os.makedirs('models')
reco = Recommendation()
reco.calculateSimilarityOfItems(n=50)
