#!/bin/bash

# Use pip from current environment
if [[ "$CONDA_DEFAULT_ENV" == "base" ]]; then
    LOCAL_PY=$(which python)
    echo "Using base env"
else
    eval $(conda shell.bash hook)
    CONDA_DIR=$(conda info | awk -F':' '/active env location/ { print $2 }')
    LOCAL_PY=$CONDA_DIR/bin/python
    echo "using python from $LOCAL_PY"
fi

# Run script
su $USER -m -c "echo $PWD; $LOCAL_PY scripts/generate_csv_mappings_multiple.py"
