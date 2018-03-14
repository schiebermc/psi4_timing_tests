import os

nums = ['15', '30', '39', '54', '63', '81', '103']#, '133', '330', '351', '402']
basis_sets = ['cc-pvdz',  'cc-pvtz', 'aug-cc-pvdz', 'aug-cc-pvtz', 'cc-pvqz', 'aug-cc-pvqz']
basis_names = {'cc-pvdz':'DZ',  'cc-pvtz':'TZ', 'aug-cc-pvdz':'aDZ', 'aug-cc-pvtz':'aTZ', 'cc-pvqz':'QZ', 'aug-cc-pvqz':'aQZ'}
options = ['DFJK', 'SYMM_JK']
tests = []

for basis in basis_sets:
    for option in options:
        for num in nums:
            test = 'protein_' + num + '_atoms_' + option + '_' + basis
            tests.append(test)


data = {}
for test in tests:
    
    if test + '.out' not in os.listdir(test):
        continue
    
    disk = ''
    
    with open(test + '/' + test + '.out', 'r') as outfile:
        for lin in outfile:
            if 'Number of basis function:' in lin:
                nbf = lin.split()[-1]
                if test not in data:
                    data[test] = {'nbf': {'primary': nbf}}
                else:
                    data[test]['nbf']['aux'] = nbf 
            if 'Algorithm:' in lin or 'AO_core?' in lin:
                ls = lin.split()[-1]
                if ls == '0' or ls == 'Disk': 
                    disk = '$^{\dagger}$'
            if 'Total Energy = ' in lin:
                energy = lin.split()[-1]
                data[test]['energy'] = energy 

    if test not in data:
        continue
    elif 'energy' not in data[test]:
        continue
 
    with open(test + '/timer.dat', 'r') as times: 
        for lin in times:
            if 'Wall Time:' in lin:
                time = str(round(float(lin.split()[-2]),1))
                data[test]['time'] = time+disk
            if 'JK: JK                      :' in lin:
                time = lin.split()[-3]
                time = time.replace('w','')
                time = str(round(float(time),1))
                data[test]['JKtime'] = time+disk
            if 'JK: J                       :' in lin or 'DFH: compute_J              :' in lin:
                time = lin.split()[-3]
                time = time.replace('w','')
                time = str(round(float(time),1))
                data[test]['Jtime'] = time+disk
            if 'JK: K                       :' in lin or 'DFH: compute_K              :' in lin:
                time = lin.split()[-3]
                time = time.replace('w','')
                time = str(round(float(time),1))
                data[test]['Ktime'] = time+disk

#print("%65s %50s" % ("Test", "Time (s)"))
#print("%65s         %10s   %10s    %10s    %10s    %10s    %10s    %10s    %10s    %22s" % ("", "SYMMJK(Tot)", "DFJK(Tot)", "Speedup", "SYMMJK(JK)", "DFJK(JK)", "SYMMJK(J)", "DFJK(J)", "SYMMJK(K)", "DFJK(K)"))
labels = ["NBF", "AUX", "Basis", "Atoms", "SYMMJK(Tot)", "DFJK(Tot)", "Speedup", "SYMMJK(JK)", "DFJK(JK)", "SYMMJK(J)", "DFJK(J)", "SYMMJK(K)", "DFJK(K)"]
print("%4s %4s %3s %3s %19s %19s %7s %19s %19s %19s %19s %19s %19s" % tuple(labels))
bynbf = [[int(data[dfjk]['nbf']['aux'])*int(data[dfjk]['nbf']['primary']), dfjk] for dfjk in data.keys() if 'DFJK' in dfjk]
bynbf.sort()

for test in bynbf:

    dfjk = test[1]
    num = test[1].split('_')[1]
    basis = test[1].split('_')[-1]
    symmjk = 'protein_' + num + '_atoms_SYMM_JK_' + basis
    try:

        speedup = float(data[dfjk]['time'].replace('$^{\dagger}$',''))/float(data[symmjk]['time'].replace('$^{\dagger}$',''))
        speedup = str(round(speedup,1))
        values = [data[dfjk]['nbf']['primary'], data[dfjk]['nbf']['aux'], basis_names[basis], num, data[symmjk]['time'], 
                  data[dfjk]['time'], speedup, data[symmjk]['JKtime'], data[dfjk]['JKtime'], data[symmjk]['Jtime'], 
                  data[dfjk]['Jtime'], data[symmjk]['Ktime'], data[dfjk]['Ktime']]
        print("%4s %4s %5s %5s %19s %19s %7s %19s %19s %19s %19s %19s %19s" % tuple(values))
         
 
#        print("NBF: %4s (Primary), %4s (Aux); Basis: %3s; Atoms: %3s %10s %10s %10s %10s %10s %10s %10s %10s %10s" % (data[dfjk]['nbf']['primary'],data[dfjk]['nbf']['aux'],basis_names[basis],num,data[symmjk]['time'],data[dfjk]['time'],speedup,data[symmjk]['JKtime'],data[dfjk]['JKtime'],data[symmjk]['Jtime'],data[dfjk]['Jtime'],data[symmjk]['Ktime'],data[dfjk]['Ktime']))
    except:
        pass


#for basis in basis_sets:
#    for num in nums:
#        dfjk = 'protein_' + num + '_atoms_DFJK_' + basis
#        symmjk = 'protein_' + num + '_atoms_SYMM_JK_' + basis
#        try:
#            diff = abs(float(data[dfjk]['energy']) - float(data[symmjk]['energy'])) 
#            print("NBF: %5s (Primary), %5s (Aux); Basis: %11s; Atoms: %3s         %10s    %10s    %10s    %10s    %10s    %10s    %10s    %10s    %22s" % (data[dfjk]['nbf']['primary'],data[dfjk]['nbf']['aux'],basis,num,data[dfjk]['time'],data[symmjk]['time'],data[dfjk]['JKtime'],data[symmjk]['JKtime'],data[dfjk]['Jtime'],data[symmjk]['Jtime'],data[dfjk]['Ktime'],data[symmjk]['Ktime'], str(diff)))
#        except:
#            pass
