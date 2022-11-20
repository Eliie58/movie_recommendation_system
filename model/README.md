# K Nearest Neighbors Model

In this folder are all the necessary resources to train and use KNN for movie recommendation.

## Setup

To setup the environemnt:
* Create a new conda env
* Install the requirements from requirements.txt

## Training the model

The model should be trained on the movie ratings dataset.
The used dataset is under data/ratings.csv.

To train the model on the default dataset, run the following command:
```
python train.py
```

To train the model on a different dataset, run the following command from a python terminal:
```
from train import build_model
build_model(data_path: str, model_path: str = 'models/model.joblib')
```

## Inference

Once the model is trained, you can start using it to get movie recommendations.
From a python terminal:
```
from inference import get_neighbors
get_neighbors(movie_ids=[1,2], k=6)
```
You can also specify the model to be used, by passing it as a parameter to the function 
```
get_neighbors(movie_ids=[1,2], model=model, k=6)
```
