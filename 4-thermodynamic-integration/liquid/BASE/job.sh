#!/bin/bash
#SBATCH --ntasks=8              # total number of tasks across all nodes
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1       # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=300M      # memory per cpu-core (4G is default)
#SBATCH --time=01:00:00         # total run time limit (HH:MM:SS)
#SBATCH --job-name="EL-MYTEMPK" 
#SBATCH --constraint=cascade,skylake

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

pwd; hostname; date

module purge
module load intel/2021.1.2
module load intel-mpi/intel/2021.1.1
module load anaconda3/2021.5
module load fftw/intel-2021.1/intel-mpi/3.3.9

############################################################################
# Variables definition
############################################################################
LAMMPS_HOME=/home/ppiaggi/Programs/Lammps/lammps-git-cpu-2/build5
LAMMPS_EXE=${LAMMPS_HOME}/lmp_della
############################################################################

############################################################################
# Run
############################################################################
# Number of partitions
srun $LAMMPS_EXE -in start.lmp

date
