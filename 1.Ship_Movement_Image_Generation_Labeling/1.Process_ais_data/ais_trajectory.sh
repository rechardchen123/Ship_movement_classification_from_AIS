#!/bin/bash -l
# Batch script to run a serial job on Legion with the upgraded
# software stack under SGE.

# 1. Force bash as the executing shell.
#$ -S /bin/bash

# 2. Request ten minutes of wallclock time (format hours:minutes:seconds).
#$ -l h_rt=0:40:0

# 3. Request 4 gigabyte of RAM (must be an integer)
#$ -l mem=4G

# 4. Request 15 gigabyte of TMPDIR space (default is 10 GB)
#$ -l tmpfs=15G

# 5. Set the name of the job.
#$ -N AIS_data_process

#6. Select the MPI parallel environment and 16 processes.
#$ -pe mpi 8

# 7. Set the working directory to somewhere in your scratch space.  This is
# a necessary step with the upgraded software stack as compute nodes cannot
# write to $HOME.
#$ -wd /home/ucesxc0/Scratch/output/ais_data_process

#8. run the application
module load python3/recommended
./first_read_and_process_data.py







