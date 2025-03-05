#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --time=10
#SBATCH --mem=1gb
#SBATCH -p dev_single

# Load python interpreter module:
module load devel/python/3.12.3_gnu_13.3

echo -e "We are in: "
pwd

echo -e "\nWe have the following environment:\n"
printenv

echo -e "\nPython3 is the following executable: "
which python3

echo -e "\nPython3 has the following version: "
python3 --version

echo -e "import numpy as np\nprint(f'Numpy has the following version{np.__version__}')" | python3
