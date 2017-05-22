
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.metrics import classification_report
import statsmodels.api as sm

INTERMEDIATE_DATA = '../intermediate_data'

# LR Classifier

def run_lr(X_train_l, X_test_l, y_train_l, y_test_l):
    lr = LogisticRegression()
    lr.fit(X_train_l, y_train_l)
    predictions_lr = lr.predict(X_test_l)

    accuracy = np.mean([predictions_lr == np.array(y_test_l)])
    precision = precision_score(y_test_l, predictions_lr)
    recall = recall_score(y_test_l, predictions_lr)
    print classification_report(y_test_l, predictions_lr)

    return accuracy, precision, recall

# LR with statsmodels

def run_lr_sm(X_train_l, X_test_l, y_train_l, y_test_l):
    logit = sm.Logit(y_train_l, X_train_l)
    result = logit.fit()

    print result.summary()


if __name__ == '__main__':

    lr_file = INTERMEDIATE_DATA + '/table-ch2.csv'

    df = pd.read_csv(lr_file)

    df_l = df.drop(['0-35', 'Post Graduate Qualification'], axis = 1)

    y_l = df_l['final_result']
    X_l = df_l.drop(['final_result'], axis = 1)
    X_train_l, X_test_l, y_train_l, y_test_l = train_test_split(X_l,y_l, random_state = 123)

    lr_scores = run_lr(X_train_l, X_test_l, y_train_l, y_test_l)
    lr_summary = run_lr_sm(X_train_l, X_test_l, y_train_l, y_test_l)

    print 'File used: {}'.format(lr_file)
    print 'Sklearn LR scores: {}'.format(lr_scores)
    print lr_summary
