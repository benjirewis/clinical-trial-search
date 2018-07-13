#!/bin/env python

# Pulls eligibility for a given trial from linkedCT.org (semantic web source for clinical trials)
# Usage: python linkedCT_eligibility_request.py #######
# 7.11.18

import sys
import requests
import re

def main():
    # Check arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python linkedCT_eligibility_request.py trialID")

    # Make request from linkedCT
    headers = {"content-type": "application/rdf"}
    r = requests.get("http://linkedct.org/resource/trial/nct" + sys.argv[1], headers=headers)

    # Write html to 'results/html' and open for reading
    fp = open("results/html", "w+")
    fp.write(r.content)
    fp.close()
    fp = open("results/html", 'r')

    # Retrieve eligibility object from trial html
    eligibility_request = ""
    for line in fp:
        if line.strip().lstrip().startswith("<a href=\"/resource/eligibility/"):
	    cleanr = re.compile('<.*?>')
	    cleantext = re.sub(cleanr, '', line)
            eligibility_request = cleantext.strip().lstrip()

    # Close results/html and make new request for eligibility object
    fp.close()
    r = requests.get("http://linkedct.org/resource/eligibility/" + eligibility_request, headers=headers)

    # Write eligibility html to 'results/html' and open for reading
    fp = open("results/html", 'w')
    fp.write(r.content)
    fp.close()
    fp = open("results/html", 'r')

    # Open new file 'results/hits' for found criteria
    new_fp = open("results/hits", "w+")

    # Find only useful information in Criteria field
    copy = False
    for line in fp:
        if line.strip().lstrip() == "<th>Criteria</th>":
            copy = True
        elif line.strip().lstrip() == "</td>":
            copy = False
        elif copy:
            # Regex to clean html tags
	    cleanr = re.compile('<.*?>')
	    cleantext = re.sub(cleanr, '', line)
            new_fp.write(cleantext.strip().lstrip())

    # Close 'results/html' and 'results/hits'
    new_fp.close(); fp.close()


if __name__ == "__main__":
    main()
