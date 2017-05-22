
import pandas as pd

DATASET_INPUT = '../dataset/studentInfo.csv'
OUTPUT_BASENAME = '../intermediate_data/dataCourse-'

# target variable:
# 1. failure vs success (exclude withdrawal)
# other options to explore later:
# 2. withdrawal vs not (remove those who dropped before start date)
# 3. distinction vs not (exclude withdrawn)


# ** demographics table cleaning steps
# * data per student (student_id)
# * convert target variables to binary
# * convert age band into dummies
# * drop regions (use imd band instead)
# * imd_band - convert into categories
# * gender to binary
# * disability status to binary
# * studied credits - keep as is
# * highest_education - dummify
# * first_attempt as a binary
# * group by student id and course (module), take only the most recent result


def preliminary_cleaning():

    # reading the original file
    studentInfo = pd.read_csv(DATASET_INPUT)
    df_new1 = studentInfo[studentInfo.final_result != 'Withdrawn']

    # * disability status to binary
    disability_mask = {'N': 0, 'Y': 1}
    df_new1.loc[:,'disability'] = df_new1['disability'].map(disability_mask)

    # * gender to binary
    gender_mask = {'F': 0, 'M': 1}
    df_new1.loc[:,'gender'] = df_new1['gender'].map(gender_mask)

    # * imd_band - convert into categories
    df_new1.loc[:,'imd_band'] = df_new1.imd_band.astype(str)
    imd_mask = {'0-10%':1,'10-20':2,'20-30%':3,'30-40%':4,'40-50%':5,'50-60%':6,'60-70%':7,'70-80%':8,'80-90%': 9,'90-100%': 10}
    df_new1.loc[:,'imd_band'] = df_new1['imd_band'].map(imd_mask)

    # * convert target variables to binary
    result_mask = {'Pass': 0, 'Fail': 1, 'Distinction': 0}
    df_new1.loc[:,'final_result'] = df_new1['final_result'].map(result_mask)

    # * first_attempt as a binary
    df_new1.loc[:,'first_attempt'] = (df_new1['num_of_prev_attempts'] == 0)

    # group by student id and course (module), take only the recent result
    # for each student - course combination
    df_grouped = df_new1.groupby(['id_student', 'code_module']).last().reset_index()

    # * first_attempt as a binary
    first_attempt_mask = {True: 1, False: 0}
    df_grouped.loc[:,'first_attempt'] = df_grouped['first_attempt'].map(first_attempt_mask)

    # * convert highest_education to dummies
    dummies1 = pd.get_dummies(df_grouped['highest_education'])

    # * convert age band to dummies
    dummies2 = pd.get_dummies(df_grouped['age_band'])

    # * preliminary data file
    data = pd.concat([df_grouped, dummies1, dummies2], axis=1)
    data = data.dropna()

    return data

def drop_some_columns(data):
    # * drop unnecessary columns
    data1 = data.drop(['id_student', 'code_module', 'code_presentation', 'region', 'highest_education', 'age_band',
                      'first_attempt'], axis = 1)
    return data1

def drop_dummy(data):
    # * drop one dummy (for logistic regression)
    return data.drop(['Lower Than A Level', '0-35'], axis = 1)

def data_for_course(data, course):
    # * data for one course only (B in this case since it is the largest one)
    dataCourse = data[data.code_module == course]
    return dataCourse

def prepare_course_data(data, course):
    dataCourse = data_for_course(data, course)
    dataCourse_ml = drop_some_columns(dataCourse)
    dataCourse_lr = drop_dummy(dataCourse_ml)

    dataCourse.to_csv(OUTPUT_BASENAME + course + '.csv')
    dataCourse_ml.to_csv(OUTPUT_BASENAME + course + '_ml.csv', index = False)
    dataCourse_lr.to_csv(OUTPUT_BASENAME + course + '_lr.csv', index = False)


########################################################

if __name__ == '__main__':

    clean_data = preliminary_cleaning()
    ml_input = drop_some_columns(clean_data)
    lr_input = drop_dummy(ml_input)

    # clean_data.to_csv('tmp2/clean_data.csv')
    # ml_input.to_csv('tmp2/ml_input.csv', index = False)
    # lr_input.to_csv('tmp2/lr_input.csv', index = False)

    prepare_course_data(clean_data, 'BBB')
