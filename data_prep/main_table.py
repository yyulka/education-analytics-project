import pandas as pd


class MainTable(object):
    def __init__(self, demogr_csv):
        self.data = pd.read_csv(demogr_csv)

    def append_vle(self, vle):
        data_full = pd.merge(self.data, vle, how='left', on=['id_student', 'code_presentation'])
        self.data = data_full.fillna(0)

    def append_assessment(self, assessment):
        d = pd.merge(self.data, assessment,  how = 'left', on = ['id_student', 'code_presentation'])
        self.data = d.fillna(0)

    def get_ml_data(self):
        data = self.data.drop(['id_student', 'code_module', 'code_presentation', 'region', 'highest_education', 'age_band',
                          'first_attempt', 'Unnamed: 0'], axis = 1)
        return data

    def save(self, basename):
        self.data.to_csv(basename + '.csv', index = False)
        self.get_ml_data().to_csv(basename + '_ml.csv', index = False)
