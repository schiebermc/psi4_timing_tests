for j in input_symm_jk.dat input_dfjk.dat
    do
        for i in 64
            do
                /theoryfs2/ds/schieber/Gits/mspsi4/objdir/stage/usr/local/psi4/bin/psi4 -n$i $j
            done
    done

