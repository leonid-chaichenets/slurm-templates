#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --time=10
#SBATCH --mem=1gb
#SBATCH -p dev_single

# Test the module commands:
module avail system/example/1.0
module whatis system/example/1.0
module help system/example/1.0

# Load the module
module load system/example/1.0

# Upon loading the module, the executable file top-words.sh is in $PATH
# and the environment variable EXAMPLE_EXA_DIR is set.

# Copy the example data into the current working directory
if [ ! "x$EXAMPLE_EXA_DIR" == "x" ]; then
    cp -r ${EXAMPLE_EXA_DIR}/* .
else
  echo "EXAMPLE_EXA_DIR is not set"
  exit 0
fi


# Like in regular bwhpc-examples, the software provided by the module is used
# on the example data. This shows how the software ca be used.

# Show us where we are and what we know.
pwd
hostname
printenv

# Count all words in Othello
echo "Count all words in Othello" > examples_result.txt
top-words.sh shakespeare-plays-flat-text/othello.txt >> examples_result.txt

# Count words that are longer than 3 characters
echo "Count all words in Othello with length >= 3" >> examples_result.txt
top-words.sh shakespeare-plays-flat-text/othello.txt 3 >> examples_result.txt

# Count words with length between 5 and 10 characters
echo "Count all words in Othello with length >=5 and <=10" >> examples_result.txt
top-words.sh shakespeare-plays-flat-text/othello.txt 5 10 >> examples_result.txt

echo "success"
