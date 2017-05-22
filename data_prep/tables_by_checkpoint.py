
import pandas as pd
import sys

# * create tables for different checkpoint periods (month1 - ch1, month2 - ch2,
# month4 - ch3, month6 - ch4, month8 - ch5)

INTERMEDIATE_DATA = '../intermediate_data'
INPUT_FILE = INTERMEDIATE_DATA + '/main_table_ml.csv'

def csv_fname(checkpoint):
    return INTERMEDIATE_DATA + '/table-ch' + str(checkpoint) + '.csv'

checkpoints_periods = [30, 60, 120, 180, 240]

date_columns = ['date_submitted-a1', 'date_submitted-a2', 'date_submitted-a3',
    'date_submitted-a4', 'date_submitted-a5', 'date_submitted-a6']

assessment_prefixes = ['date_submitted', 'is_banked', 'score',
    'late_submit_days', 'late_submit', 'passed']

vle_prefixes = ['access_variety', 'sum_click']

vle_suffixes = [
    ['(210, 240)', '(180, 210)'],
    ['(150, 180)', '(120, 150)'],
    ['(60, 90)', '(90, 120)'],
    ['(30, 60)']
]

# checkpoint 5

df = pd.read_csv(INPUT_FILE)
df = df[(df['date_submitted-a1'] < 240) & (df['date_submitted-a2'] < 240)
    & (df['date_submitted-a3'] < 240) & (df['date_submitted-a4'] < 240)
    & (df['date_submitted-a5'] < 240) & (df['date_submitted-a6'] < 240)]

df5 = df.drop(date_columns + ['access_varietyNone', 'sum_clickNone'], axis = 1)

df5.to_csv(csv_fname(5), index = False)

# checkpoint 4

df = df.drop([p+s for p in vle_prefixes for s in vle_suffixes[0]], axis = 1)
df = df.drop([p + '-a6' for p in assessment_prefixes], axis = 1)
df = df.drop([p + '-a5' for p in assessment_prefixes], axis = 1)

period = 180
df = df[(df['date_submitted-a1'] < period) & (df['date_submitted-a2'] < period)
    & (df['date_submitted-a3'] < period) & (df['date_submitted-a4'] < period)]

df4 = df.drop(date_columns[:-2] + ['access_varietyNone', 'sum_clickNone'], axis = 1)

df4.to_csv(csv_fname(4), index = False)


# checkpoint 3

df = df.drop([p+s for p in vle_prefixes for s in vle_suffixes[1]], axis = 1)
df = df.drop([p + '-a4' for p in assessment_prefixes], axis = 1)

period = 120
df = df[(df['date_submitted-a1'] < period) & (df['date_submitted-a2'] < period)
    & (df['date_submitted-a3'] < period)]

df3 = df.drop(date_columns[:-3] + ['access_varietyNone', 'sum_clickNone'], axis = 1)
df3.to_csv(csv_fname(3), index = False)


# checkpoint 2

df = df.drop([p+s for p in vle_prefixes for s in vle_suffixes[2]], axis = 1)
df = df.drop([p + '-a3' for p in assessment_prefixes], axis = 1)

period = 60
df = df[(df['date_submitted-a1'] < period) & (df['date_submitted-a2'] < period)]

df2 = df.drop(date_columns[:-4] + ['access_varietyNone', 'sum_clickNone'], axis = 1)
df2.to_csv(csv_fname(2), index = False)


# checkpoint 1

df = df.drop([p+s for p in vle_prefixes for s in vle_suffixes[3]], axis = 1)
df = df.drop([p + '-a2' for p in assessment_prefixes], axis = 1)

period = 30
df = df[(df['date_submitted-a1'] < period)]

df1 = df.drop(date_columns[:-5] + ['access_varietyNone', 'sum_clickNone'], axis = 1)
df1.to_csv(csv_fname(1), index = False)
