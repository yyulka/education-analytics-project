
import pandas as pd
import numpy as np

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
#from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.dummy import DummyClassifier

INTERMEDIATE_DATA = '../intermediate_data'

models_to_run = [
    # Random Forest Classifier
    (RandomForestClassifier(),
        {'n_estimators': [10, 50, 100, 500],
        'max_features': ['sqrt', 'log2', 'auto'],
        'min_samples_leaf': [1, 2, 10, 50]
        }
    ),

# KNN Classifier
    (KNeighborsClassifier(),
        {'n_neighbors': [5, 10, 15],
        'weights': ['uniform', 'distance'],
        }
    ),

# GradientBoostingClassifier
    (GradientBoostingClassifier(),
        {'learning_rate': [0.05, 0.02, 0.01],
        'max_depth': [3, 6],
        'max_features': ['sqrt', 'log2'],
        'n_estimators': [50, 100, 500]
        }
    )]

def grid_search(models_to_run, score, X_train, y_train):

    for model, params in models_to_run:
        gs = GridSearchCV(model, params, n_jobs = 2, scoring = score, cv = 3)
        g = gs.fit(X_train, y_train)
        print '\n======={}======='.format(model.__class__.__name__)
        print 'Best parameters {}'.format(g.best_params_)
        print 'Best score {}'.format(g.best_score_)



def print_cv_score(model,score, X_train, y_train):
    print '\n======={}======='.format(model.__class__.__name__)
    print "Score: {}".format(np.mean(cross_val_score(model, X_train, y_train, cv = 5, scoring=score)))

def print_scores(models, score, X_train, y_train):
    for model in models:
        print_cv_score(model, score, X_train, y_train)


if __name__ == '__main__':

    ml_file = INTERMEDIATE_DATA + '/table-ch2.csv'

    df = pd.read_csv(ml_file)

    y = df['final_result']
    X = df.drop(['final_result'], axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 123)

    grid_search(models_to_run, 'recall', X_train, y_train)


    rf = RandomForestClassifier(max_features='auto', n_estimators = 50, min_samples_leaf = 2)
    knn = KNeighborsClassifier()
    gb = GradientBoostingClassifier()

    models = [rf, knn, gb]

    print_scores(models, 'recall', X_train, y_train)
