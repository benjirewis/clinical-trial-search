#!/bin/env python

# Scrape eligibility criteria for a given NCT id
# Usage: python web_scrape.py NCT########
# 7.11.18

import sys
import re

from urllib import urlopen as uReq

def main():
    # Argument check
    if len(sys.argv) != 2:
        sys.exit("Usage: python web_scrape.py trialID")

    # Define URL
    url = "https://clinicaltrials.gov/ct2/show/" + sys.argv[1]

    # Open connection and grab html
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    # Write html to file 'html'
    fp = open("results/html", "w+")
    fp.write(page_html)
    fp.close()

    # Open 'html' for reading and new file 'hits' for writing
    fp = open("results/html", 'r')
    new_fp = open("results/hits", "w+")
    copy = False

    # Remove all text between "Criteria" and "Locations & Contacts"
    for line in fp:
        if line.strip().lstrip() == "<div class=\"header3\" style=\"margin-top:2ex\">Criteria</div>":
            copy = True
        elif line.strip().lstrip() == "<!-- location_section -->":
            copy = False
        elif copy:
            # Regex to strip all html tags (everything between triangle brackets)
	    cleanr = re.compile('<.*?>')
	    cleantext = re.sub(cleanr, '', line)
            new_fp.write(cleantext.strip().lstrip())

    # Close 'hits' and 'html'
    new_fp.close(); fp.close()

if __name__ == "__main__":
    main()
