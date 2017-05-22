
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import roc_curve, auc

import matplotlib.pyplot as plt

INTERMEDIATE_DATA = '../intermediate_data'

# Baseline Classifier

def run_baseline(X_train, X_test, y_train, y_test):
    bl = DummyClassifier()
    bl.fit(X_train, y_train)
    predictions = bl.predict(X_test)
    print 'Baseline Classifier'
    print np.mean(cross_val_score(bl, X_train, y_train, cv = 5, scoring='recall'))

    accuracy = np.mean([predictions == np.array(y_test)])
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    print classification_report(y_test, predictions)

    return accuracy, precision, recall

# Random Forest Classifier

def run_rf(X_train, X_test, y_train, y_test):
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    predictions = rf.predict(X_test)

    print 'Random Forest Classifier'
    print np.mean(cross_val_score(rf, X_train, y_train, cv = 5, scoring='f1'))

    accuracy = np.mean([predictions == np.array(y_test)])
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    print classification_report(y_test, predictions)
    y_proba_rf = rf.predict_proba(X_test)

    return accuracy, precision, recall, y_proba_rf


# KNN Classifier

def run_knn(X_train, X_test, y_train, y_test):
    knn = KNeighborsClassifier()
    knn.fit(X_train, y_train)
    predictions_knn = knn.predict(X_test)

    print 'KNN Classifier'
    print np.mean(cross_val_score(knn, X_train, y_train, cv = 5, scoring='f1'))

    accuracy = np.mean([predictions_knn == np.array(y_test)])
    precision = precision_score(y_test, predictions_knn)
    recall = recall_score(y_test, predictions_knn)
    print classification_report(y_test, predictions_knn)
    y_proba_knn = knn.predict_proba(X_test)

    return accuracy, precision, recall, y_proba_knn

# GradientBoostingClassifier

def run_gb(X_train, X_test, y_train, y_test):
    gb = GradientBoostingClassifier()
    gb.fit(X_train, y_train)
    predictions = gb.predict(X_test)

    print 'Gradient Boosting Classifier'
    print np.mean(cross_val_score(gb, X_train, y_train, cv = 5, scoring='f1'))

    print np.mean(cross_val_score(gb, X_train, y_train, cv = 5, scoring='recall'))

    accuracy = np.mean([predictions == np.array(y_test)])
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    print classification_report(y_test, predictions)
    y_proba_gb = gb.predict_proba(X_test)

    return accuracy, precision, recall, y_proba_gb

# LR Classifier

def run_lr(X_train_l, X_test_l, y_train_l, y_test_l):
    lr = LogisticRegression()
    lr.fit(X_train_l, y_train_l)
    predictions_lr = lr.predict(X_test_l)

    # print cross_val_score(lr, X_train, y_train, scoring='f1')

    accuracy = np.mean([predictions_lr == np.array(y_test_l)])
    precision = precision_score(y_test_l, predictions_lr)
    recall = recall_score(y_test_l, predictions_lr)
    print classification_report(y_test_l, predictions_lr)
    y_proba_lr = lr.predict_proba(X_test_l)

    return accuracy, precision, recall, y_proba_lr



############################################################

ml_file = INTERMEDIATE_DATA + '/table-ch2.csv'

df = pd.read_csv(ml_file)
df_l = df.drop(['Lower Than A Level', '0-35'], axis = 1)

y = df['final_result']
X = df.drop(['final_result'], axis = 1)
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 123)

y_l = df_l['final_result']
X_l = df_l.drop(['final_result'], axis = 1)
X_train_l, X_test_l, y_train_l, y_test_l = train_test_split(X_l,y_l, random_state = 123)

baseline_scores = run_baseline(X_train, X_test, y_train, y_test)
rf_scores = run_rf(X_train, X_test, y_train, y_test)
knn_scores = run_knn(X_train, X_test, y_train, y_test)
gb_scores = run_gb(X_train, X_test, y_train, y_test)
lr_scores = run_lr(X_train_l, X_test_l, y_train_l, y_test_l)

print ml_file

print baseline_scores
print rf_scores
print knn_scores
print gb_scores
print lr_scores



# plotting roc curve for different models

fpr, tpr, thresholds = roc_curve(y_test, rf_scores[3][:, 1])
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label='ROC (area = %0.2f)' % (roc_auc))

fpr, tpr, thresholds = roc_curve(y_test, gb_scores[3][:, 1])
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label='ROC (area = %0.2f)' % (roc_auc))

fpr, tpr, thresholds = roc_curve(y_test, knn_scores[3][:, 1])
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label='ROC (area = %0.2f)' % (roc_auc))

fpr, tpr, thresholds = roc_curve(y_test_l, lr_scores[3][:, 1])
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label='ROC (area = %0.2f)' % (roc_auc))

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.plot([0, 1], [0, 1], linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.show()
