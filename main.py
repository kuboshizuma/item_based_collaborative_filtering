# for recommendation
# usage: python main.py :user_id
from recommendations import Recommendation
import sys

def main(user_id):
    reco = Recommendation()
    print(reco.getRecommendItems(user_id)[0:50])

if __name__ == '__main__':
    params = sys.argv
    if len(params) < 2:
        sys.exit("Warning: Add a argument for user_id.")
    else:
        main(params[1])
