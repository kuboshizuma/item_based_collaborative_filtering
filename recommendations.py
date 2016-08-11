from math import sqrt
import click # for progress bar
from sklearn.externals import joblib # for saving model
import os.path
import sys

class Recommendation(object):
    # load datasets and convert them to dict
    def __init__(self, path='datasets'):
        # load title of movies { { movie_id: movie_title }, ...}
        movies={}
        for line in open(path+'/u.item', encoding='latin-1'):
            movie_id, movie_title = line.split('|')[0:2]
            movies[movie_id] = movie_title

        # load ratings { { user_id: { movie_title: rating, ... }, ... } }
        self.ratings = {}
        for line in open(path+'/u.data'):
            user_id, movie_id, rating, timestamp = line.split('\t')
            self.ratings.setdefault(user_id, {})
            self.ratings[user_id][movies[movie_id]] = float(rating)


    # calculate pearson correlation for similarity measure
    def __pearsonCorrelation(self, person1, person2):
        # get common items in both
        both_rated = {}
        for item in self.ratings[person1]:
            if item in self.ratings[person2]: both_rated[item] = 1

        number_of_both_rated = len(both_rated)

        # return 0 if there is no common item in both
        if number_of_both_rated==0: return 0

        # each person's sum of ratings
        sum_of_person1_rate = sum([self.ratings[person1][item] for item in both_rated])
        sum_of_person2_rate = sum([self.ratings[person2][item] for item in both_rated])

        # each person's sum of squared ratings
        sum_of_person1_squared_rate = sum([pow(self.ratings[person1][item], 2) for item in both_rated])
        sum_of_person2_squared_rate = sum([pow(self.ratings[person2][item], 2) for item in both_rated])

        # sum of product of each person's ratings
        sum_of_product_of_both_rate = sum([self.ratings[person1][item]*self.ratings[person2][item] for item in both_rated])

        # (pearson correlation) = numerator / denominator
        numerator = sum_of_product_of_both_rate - (sum_of_person1_rate * sum_of_person2_rate / number_of_both_rated)
        denominator = sqrt((sum_of_person1_squared_rate-pow(sum_of_person1_rate, 2)/number_of_both_rated)*(sum_of_person2_squared_rate-pow(sum_of_person2_rate, 2)/number_of_both_rated))

        if denominator == 0: return 0
        return numerator/denominator


    # get somethig similar to one target
    def __topSimilarRanking(self, target, n=10):
        scores =[(self.__pearsonCorrelation(target, other), other) for other in self.ratings if other!=target]
        scores.sort(reverse=True)
        return scores[0:n]


    # user_id: { movie_title: rating, ... } => movie_title: { user_id: rating, ... }
    def __transformRatings(self):
        result = {}
        for person in self.ratings:
            for item in self.ratings[person]:
                result.setdefault(item, {})
                result[item][person] = self.ratings[person][item]
        self.ratings = result


    # calculate similarity between items and save created model
    def calculateSimilarityOfItems(self, n=10):
        result = {}

        # convert ratings
        self.__transformRatings()

        # display progress bar because it needs time
        with click.progressbar(self.ratings) as bar:
            for item in bar:
                # in this case, calculate similarity of "items" not users
                scores = self.__topSimilarRanking(item, n=n)
                result[item] = scores
        # save model
        joblib.dump(result, "models/item_match")
        return result


    # recommend items to one person
    def getRecommendItems(self, user):
        if not user in self.ratings: sys.exit("Waring: The user cannot be found.")
        if not os.path.isfile("models/item_match"): sys.exit("Warning: cannot find model. You can use set_model.py for creating model.")

        # load model
        item_model = joblib.load("models/item_match")
        if len(item_model) == 0: sys.exit("Waring: No item match. Check your datasets.")

        user_ratings = self.ratings[user]
        scores = {}
        total_similarity = {}

        for (item, rating) in user_ratings.items():
            for (similarity, compared_item) in item_model[item]:
                # skip if this user already evaluated this item
                if compared_item in user_ratings: continue

                if not similarity == 0:
                    # similarity * rating for each item
                    scores.setdefault(compared_item, 0)
                    scores[compared_item] += similarity*rating

                    # sum of similarity for normalization
                    total_similarity.setdefault(compared_item, 0)
                    total_similarity[compared_item] += similarity

        rankings = [(score/total_similarity[item], item) for item, score in scores.items()]

        rankings.sort(reverse=True)
        return rankings
