# item_based_collaborative_filtering

## Requirements

- Python 3.5
- click ( for progress bar )
- scikit-learn ( only for saving model )
- numpy
- scipy

## Installation

```
$ git clone https://github.com/kuboshizuma/item_based_collaborative_filtering
```


```
$ pip install -r requirements.txt
```

## Preparation

[MovieLens](http://grouplens.org/datasets/movielens/) datasets is used in this implementation.
For demo you need to download this datasets.

Click the following button below, and you can download datasets soon.

[Download datasets](http://files.grouplens.org/datasets/movielens/ml-100k.zip)

After that, unzip the datasets and put the directory in top directory, naming it `datasets`. 

## Documentation



### Create model

This command takes a few tens of seconds to complete.

```
$ python set_model.py
```

### Display recommend items

```
$ python main.py (user_id)
```

for example

```
$ python main.py 24
```
