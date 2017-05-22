
import pandas as pd

# ** features from vle table
# * early registration for the course-presentation - later
# * interaction variety per period
# * total clicks per period
# * resource dummies - later


def clean_vle_checkpoint(days_range):
    studentVleB = pd.read_csv('../intermediate_data/VLE_B.csv')

    # * collecting total number of clicks and number of unique resources accessed
    # per student per day
    s = studentVleB.groupby(['code_module','code_presentation','id_student', 'date']).agg({'id_site':pd.Series.nunique, 'sum_click':sum})
    s = s.reset_index()
    if days_range is not None:
        first_day, last_day = days_range
        if first_day is None:
            first_day = -30
        s = s[(s['date'] >= first_day) & (s['date'] < last_day)]

    # * grouping the number of clicks and variety of resources accessed by student per period (course or checkpoint)
    s2 = s.groupby(['code_module','code_presentation','id_student']).agg({'id_site':sum, 'sum_click':sum})

    # group by student id and course (module), take only the recent result
    # for each student - course combination
    vle = s2.reset_index().groupby(['id_student']).last().reset_index()
    vle = vle.rename(columns = {'id_site':'access_variety'+str(days_range), 'sum_click': 'sum_click' + str(days_range)})
    vle = vle.drop('code_module', axis = 1)

    return vle
