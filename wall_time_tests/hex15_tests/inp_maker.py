import os

systems = [270, 280, 305, 310, 315, 335, 340, 350, 370, 385, 390, 395]

base_dir = '/theoryfs2/ds/bakr/chem/matt_tests/scaled_geoms/'
for s in systems:
    with open(base_dir + str(s) + '/test_' + str(s) + '.xyz', 'r') as fil:
        lines = fil.readlines()
        natoms = lines[0]
        geom = lines[2:]
    for basis in ['cc-pvdz', 'aug-cc-pvdz', 'cc-pvtz', 'aug-cc-pvtz', 'cc-pvqz', 'aug-cc-pvqz']:
        for option in ['DFJK', 'SYMM_JK']:
            new_direct = 'protein_' + natoms.split()[0] + '_atoms_' + option + '_' + basis
            try: 
                os.mkdir(new_direct)
            except:
                pass
            with open(new_direct + '/protein_' + natoms.split()[0] + '_atoms_' + option + '_' + basis + '.in', 'w') as inp_fil:
                inp_fil.write('memory 60 Gb\n\n')
                inp_fil.write('molecule protein_' + natoms.split()[0] + ' {\n')
                inp_fil.write('0 1\n')
                for line in geom:
                    inp_fil.write(line)
                inp_fil.write('}\n\n')
                inp_fil.write('set {\n')
                inp_fil.write('basis ' + basis + '\n')
                inp_fil.write('scf_type df\n')
                inp_fil.write('guess sad\n')
                inp_fil.write('DF_SCF_TYPE '+ option + '\n')
                inp_fil.write('}\n\n')
                inp_fil.write("energy('HF')\n")
