import os

nums = ['15', '30', '39', '54', '63', '81', '103']#, '133', '330', '351', '402']
#nums = ['63', '81', '103']#, '133', '243', '330', '351', '402']
basis_sets = ['cc-pvdz',  'cc-pvtz', 'aug-cc-pvdz', 'aug-cc-pvtz', 'cc-pvqz', 'aug-cc-pvqz']
options = ['DFJK', 'SYMM_JK']
tests = []

for basis in basis_sets:
    for num in nums:
        for option in options:
            test = 'protein_' + num + '_atoms_' + option + '_' + basis
            tests.append(test)

def check(fil_name):
    
    if fil_name not in os.listdir('.'):
        return False
    with open(fil_name, 'r') as fil:
        for lin in fil:
            if 'beer' in lin: 
                return True
    
    return False 

for test in tests:
    os.chdir('/theoryfs2/ds/bakr/chem/matt_tests/scaled_geoms/hex15_tests/'+test)
    if check(test+'.out'):
        continue
    psi4 = '/theoryfs2/ds/schieber/Gits/mspsi4/objdir3/stage/usr/local/psi4/bin/psi4 -n 6 '
    os.system(psi4 + test+'.in') 
