
import pandas as pd

DATASET_INPUT = '../dataset/studentInfo.csv'
OUTPUT_BASENAME = '../intermediate_data/dataCourse-'
cols_to_drop = ['id_student', 'code_module', 'code_presentation', 'region',
                'highest_education', 'age_band', 'first_attempt']
dummies_to_drop = ['Lower Than A Level', '0-35']



'''
Initial cleaning of the demographic table.

Target variable: failure vs success
(excluding "Withdrawn").

Features cleaning and transformations:
* target variable to binary
* age band to dummies
* drop regions (use imd band instead)
* imd_band to categories
* gender to binary
* disability status to binary
* studied credits - keep as is
* highest_education to dummies
* first_attempt as a binary
* group by student id and course (module), take only the most recent result
'''

def clean_data(input_path):

    # reading the original file
    student_info = pd.read_csv(input_path)
    d = student_info.loc[student_info['final_result'] != 'Withdrawn']

    # disability status to binary
    disability_mask = {'N': 0, 'Y': 1}
    d.loc[:,'disability'] = d['disability'].map(disability_mask)

    # gender to binary
    gender_mask = {'F': 0, 'M': 1}
    d.loc[:,'gender'] = d['gender'].map(gender_mask)

    # imd_band - convert into categories
    d.loc[:,'imd_band'] = d.imd_band.astype(str)
    imd_mask = {'0-10%':1,'10-20':2,'20-30%':3,'30-40%':4,'40-50%':5,'50-60%':6,
                '60-70%':7,'70-80%':8,'80-90%': 9,'90-100%': 10}
    d.loc[:,'imd_band'] = d['imd_band'].map(imd_mask)

    # convert target variables to binary
    result_mask = {'Pass': 0, 'Fail': 1, 'Distinction': 0}
    d.loc[:,'final_result'] = d['final_result'].map(result_mask)

    # first_attempt as a binary
    d.loc[:,'first_attempt'] = (d['num_of_prev_attempts'] == 0)

    # group by student id and course (module), take only the recent result
    # for each student - course combination
    df_grouped = d.groupby(['id_student', 'code_module']).last().reset_index()

    # first_attempt as a binary
    first_attempt_mask = {True: 1, False: 0}
    df_grouped.loc[:,'first_attempt'] = df_grouped['first_attempt'].map(first_attempt_mask)

    # convert highest_education to dummies
    education_dummies = pd.get_dummies(df_grouped['highest_education'])

    # convert age band to dummies
    age_dummies = pd.get_dummies(df_grouped['age_band'])

    # preliminary data file
    data = pd.concat([df_grouped, education_dummies, age_dummies], axis=1)
    data = data.dropna()

    return data

def data_for_course(data, course):
    # data for one course only (course with code BBB in this case since it is
    # the largest one)
    return data.loc[data['code_module'] == course]

def prepare_course_data(data, course, output_path):
    dataCourse = data_for_course(data, course)
    # drop some columns
    dataCourse_ml = dataCourse.drop(cols_to_drop, axis = 1)
    # drop one dummy for each variable (for logistic regression)
    dataCourse_lr = dataCourse_ml.drop(dummies_to_drop, axis = 1)

    dataCourse.to_csv(output_path + course + '.csv')
    dataCourse_ml.to_csv(output_path + course + '_ml.csv', index = False)
    dataCourse_lr.to_csv(output_path + course + '_lr.csv', index = False)


########################################################

if __name__ == '__main__':

    clean_data = clean_data(DATASET_INPUT)
    prepare_course_data(clean_data, 'BBB', OUTPUT_BASENAME)
