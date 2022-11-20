#!/usr/bin/bash
if [ $# -ne 0 ]
then
    echo "Usage: ./generate_payments.sh no arguments"
    exit 1
fi

python3 generate_payments.py