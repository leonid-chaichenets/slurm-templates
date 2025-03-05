#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --time=10
#SBATCH --mem=1gb
#SBATCH -p dev_single

# To protect email addresses and to not put them literally into this script,
# export SLURM_EMAIL and call sbatch --mail-user=$SLURM_EMAIL <script>.
#SBATCH --mail-type=START,END

pyenv versions

echo -e "We are in: "
pwd

echo -e "\nWe have the following environment:\n"
printenv

echo -e "\nPython3 is the following executable: "
which python3

#./gpu_test.py
