# This scripts uses the PLUMED driver to calculate the distribution of the environment
# similarity kernel in the liquid and the bcc phases

conda activate plumed-masterclass-2022

echo "# Sigma  Overlap"
# Use sigma values from 0.01 to 0.12 in steps of 0.01
for sigma in `seq 0.01 0.01 0.12`
do
        for phase in bcc liquid
        do
		cd $phase
                sed "s/replace/$sigma/g" ../plumed-base.dat > plumed.dat
                mpiexec plumed driver --plumed plumed.dat --mf_dcd out.dcd > plumed.out
		cp histo histo-$sigma
		cd ..
        done
	# Calculate the overlap using a python script
        overlap=`python script.py`
        echo $sigma $overlap
done
