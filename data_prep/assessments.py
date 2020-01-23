
import pandas as pd
DATASET_DIR = '../dataset'

'''
Obtaining features from assessment table.
Feature engineering:
* assessment scores
* assessment passed (y/n)
* late sumbission (y/n)
* days after deadline

'''


# Clean assessment table and add some features

def clean_assessment():

    assessments = pd.read_csv(DATASET_DIR + '/assessments.csv')
    studentAssessment = pd.read_csv(DATASET_DIR + '/studentAssessment.csv')

    assessments_all = pd.merge(assessments, studentAssessment,
                                on = 'id_assessment')

    assessments_all = assessments_all[assessments_all.score != '?']
    assessments_all['score'] = assessments_all['score'].astype(int)
    assessments_all['passed'] = (assessments_all['score'] > 40)
    passed_mask = {True: 1, False: 0}
    assessments_all.loc[:,'passed'] = assessments_all['passed'].map(passed_mask)

    assessments_all['score_weighted'] = assessments_all['weight']/100 * assessments_all['score']

    assessments_all = assessments_all[assessments_all.date != '?']
    assessments_all.loc[:,'date'] = assessments_all['date'].astype(int)

    assessments_all['late_submit'] = ((assessments_all['date_submitted']
                                        - assessments_all['date']) > 0)
    late_mask = {True: 1, False: 0}
    assessments_all.loc[:,'late_submit'] = assessments_all['late_submit'].map(late_mask)

    assessments_all['late_submit_days'] = (assessments_all['date_submitted']
                                            - assessments_all['date'])

    return assessments_all

# create student assessment table for course BBB

def create_assessmentsBBB(data, codes, name):

    assessmentsB = data[data['code_module'] == 'BBB']

    assessmentB = assessmentsB[(assessmentsB['id_assessment'].isin(codes))]

    assessmentB = assessmentB.groupby(['id_student']).last().reset_index()
    assessmentB = assessmentB.drop(['code_module', 'id_assessment',
                                    'assessment_type', 'date', 'weight',
                                    'score_weighted'], axis = 1)
    assessmentB.columns = [col + '-' + name for col in assessmentB.columns]
    assessmentB = assessmentB.rename(columns = {'id_student'+ '-'
                                    + name:'id_student', 'code_presentation'
                                    + '-' + name: 'code_presentation'})
    return assessmentB
