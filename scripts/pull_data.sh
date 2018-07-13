#!/bin/bash

# Search program for cancer.gov and clinicaltrials.gov
# Writes titles, NCT ids, minimum age, maximum age and gender related to found studies to gen_info.txt
# Writes diseases to mesh_diseases.txt
# Writes unstructured eligibility criteria to ec_criteria.txt (if running on cancer.gov)
# 6.19.18

if [ "$3" == "cancer.gov" ] # Make cancer.gov request
then
    SEARCH_STRING="https://clinicaltrialsapi.cancer.gov/v1/clinical-trials?size=$2&official_title_fulltext=${1/_/%20}&include=official_title&include=nct_id&include=diseases&include=eligibility"

    curl -X GET --header 'Accept: application/json' ${SEARCH_STRING} > .internal/results.json
    echo -e "JSON response output to .internal/results.json\n"

    # Run KNIME workflow
    /Applications/KNIME\ 3.5.3.app/Contents/MacOS/Knime -nosplash -reset --launcher.suppressErrors -application org.knime.product.KNIME_BATCH_APPLICATION -workflowDir="/Applications/Knime/cancer_knime" &> .internal/knime.log
elif [ "$3" == "clinicaltrials.gov" ] # Make clinicaltrials.gov request
then
    SEARCH_STRING="https://clinicaltrials.gov/ct2/results/download_fields?&recr=open&term=${1/_/+}&down_count=$2&down_flds=all&down_chunk=1&down_fmt=xml"

    curl -X GET --header 'Accept: application/xml' ${SEARCH_STRING} > .internal/results.xml
    echo -e "XML response output to .internal/results.xml\n"

    # Run KNIME workflow
    /Applications/KNIME\ 3.5.3.app/Contents/MacOS/Knime -nosplash -reset --launcher.suppressErrors -application org.knime.product.KNIME_BATCH_APPLICATION -workflowDir="/Applications/Knime/clintrials_knime" &> .internal/knime.log
else # Incorrect parameter
    >&2 echo "Usage: third argument must be cancer.gov, or clinicaltrials.gov"
    exit 1
fi
