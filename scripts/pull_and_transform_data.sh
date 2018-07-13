#!/bin/bash

# Control script for both pulling data and transforming to RDF encoding
# 6.18.18

# Argument check
if [ "$#" -ne 3 ]
then
    >&2 echo "Usage: run_me query size [cancer.gov | clinicaltrials.gov]"
    exit 1
fi

# Clear ./results folder
rm results/*

# Pull data using given arguments
./pull_data.sh $@

# Transform data to RDF encoding
if [ -f results/ec_criteria.txt ]
then
    python ttl_transform.py results/gen_info.txt results/mesh_diseases.txt results/ec_criteria.txt
else
    python ttl_transform.py results/gen_info.txt results/mesh_diseases.txt
fi

# Print results
echo "Done! Files contained in results dir"
echo "General info contained in results/gen_info.txt"
echo "MeSH diseases contained in results/mesh_diseases.txt"
echo "Eligibility criteria contained in results/ec_criteria.txt"
echo "RDF encoding contained in results/results.ttl"
echo -e "KNIME log printed to .internal/knime.log\n"
echo -e "Thank you!"
