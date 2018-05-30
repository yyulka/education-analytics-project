
import main_table
import vle
import assessments
import sys

INTERMEDIATE_DATA = '../intermediate_data'

'''
Importing data from vle and assessment tables and preparing them for joining
with the main table.

'''


def add_vles(mt):
    clean_vle = vle.clean_vle_checkpoint(days_range = None)
    mt.append_vle(clean_vle)

    clean_vle_ch1 = vle.clean_vle_checkpoint((None, 30))
    mt.append_vle(clean_vle_ch1)

    for i in range(1, 8):
        days_range = (30*i, 30*(i+1))
        print "Appending " + str(days_range)
        vle_data = vle.clean_vle_checkpoint(days_range)
        mt.append_vle(vle_data)
        print len(mt.data)


def add_assessments(mt):
    a1codes = [14984, 14996, 15008, 15020]
    a2codes = [14985, 14997, 15009, 15021]
    a3codes = [14986, 14998, 15010, 15022]
    a4codes = [14987, 14999, 15011, 15023]
    a5codes = [14988, 15000, 15012, 15024]
    a6codes = [14989, 15001, 15013]

    codes = [a1codes, a2codes, a3codes, a4codes, a5codes, a6codes]
    names = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']
    code_names = zip(codes, names)

    clean_assessment = assessments.clean_assessment()

    for code, name in code_names:
        assessment = assessments.create_assessmentsBBB(clean_assessment, code, name)
        print 'Appending ' + str(code)
        print 'Assessment size: ' + str(len(assessment))
        print 'MT size before:' + str(len(mt.data))
        mt.append_assessment(assessment)
        print 'MT size after:' + str(len(mt.data))



if __name__ == '__main__':
    mt = main_table.MainTable(INTERMEDIATE_DATA + '/dataCourse-BBB.csv')
    add_vles(mt)
    add_assessments(mt)
    print mt.data.head()
    mt.save(INTERMEDIATE_DATA + '/main_table')
