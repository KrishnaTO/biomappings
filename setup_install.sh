#!/bin/sh

# Use pip from current environment
if [[ "$CONDA_DEFAULT_ENV" == "base" ]]; then
    CONDA_DIR=$(conda info | awk -F':' '/active env location/ { print $2 }')
    LOCAL_PIP=$CONDA_DIR/bin/pip
else
    LOCAL_PIP=$(which pip)
fi

# Install dependencies
$LOCAL_PIP install -U pyobo gilda indra rdflib

# Install biomappings from current repo
su $USER -c "$LOCAL_PIP install -e ."