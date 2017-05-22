
import pandas as pd

OUTPUT_DIR = '../intermediate_data'
studentVLE = pd.read_csv('dataset/studentVle.csv')

# VLE data per course

studentVleA = studentVLE[studentVLE.code_module == 'AAA']
studentVleA.to_csv(OUTPUT_DIR + '/VLE_A.csv')

studentVleB = studentVLE[studentVLE.code_module == 'BBB']
studentVleB.to_csv(OUTPUT_DIR + '/VLE_B.csv')

studentVleC = studentVLE[studentVLE.code_module == 'CCC']
studentVleC.to_csv(OUTPUT_DIR + '/VLE_C.csv')

studentVleD = studentVLE[studentVLE.code_module == 'DDD']
studentVleD.to_csv(OUTPUT_DIR + '/VLE_D.csv')

studentVleE = studentVLE[studentVLE.code_module == 'EEE']
studentVleE.to_csv(OUTPUT_DIR + '/VLE_E.csv')

studentVleF = studentVLE[studentVLE.code_module == 'FFF']
studentVleF.to_csv(OUTPUT_DIR + '/VLE_F.csv')

studentVleG = studentVLE[studentVLE.code_module == 'GGG']
studentVleG.to_csv(OUTPUT_DIR + '/VLE_G.csv')
