
import pandas as pd

'''
Obtaining features from vle (virtual learning environment) table.
Feature engineering:
* total number of clicks on vle resources per period
* unique resource accessed by a student per day summed over the time period
* other things to try later:
    - type of resource accessed (dummies)
    - early registration for the course

'''


def clean_vle_checkpoint(days_range):
    # reading vle table for course 'BBB'
    studentVleB = pd.read_csv('../intermediate_data/VLE_B.csv')

    # collecting total number of clicks and number of unique resources accessed
    # per student per day
    s = studentVleB.groupby(['code_module','code_presentation','id_student',
                            'date']).agg({'id_site':pd.Series.nunique,
                            'sum_click':sum})

    # selecting data for relevant time perion (days_range)
    s = s.reset_index()
    if days_range is not None:
        first_day, last_day = days_range
        if first_day is None:
            first_day = -30
        s = s[(s['date'] >= first_day) & (s['date'] < last_day)]

    # grouping the number of clicks and variety of resources accessed by
    # student per period (days_range)
    s2 = s.groupby(['code_module','code_presentation',
                    'id_student']).agg({'id_site':sum, 'sum_click':sum})

    # grouping by student id and course (module), taking only the recent result
    # for each student-course combination
    vle = s2.reset_index().groupby(['id_student']).last().reset_index()
    vle = vle.rename(columns = {'id_site':'access_variety' + str(days_range),
                                'sum_click': 'sum_click' + str(days_range)})
    vle = vle.drop('code_module', axis = 1)

    return vle
