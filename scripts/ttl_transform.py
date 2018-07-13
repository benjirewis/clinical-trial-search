#!/bin/env python

# Transfrom script for turning search data into Turtle format
# Writes ttl-RDF encoding of search data to results.ttl
# 6.26.18

import sys

# Class for clinical trials
class ClinicalTrial:
    def __init__(self):
        self.title = None
        self.id_num = None
        self.gender = None
        self.min_age = None
        self.max_age = "999"
        self.inclusion = []
        self.cond_list = []

    def setTitle(self, new_title):
        self.title = new_title

    def setID(self, new_id):
        self.id_num = new_id

    def setMinAge(self, new_age):
        self.min_age = new_age

    def setMaxAge(self, new_age):
        self.max_age = new_age

    def setGender(self, new_gender):
        self.gender = new_gender

    def appendInclusion(self, new_inclusion):
        self.inclusion.append(new_inclusion)

    def appendCond(self, new_cond_item):
        self.cond_list.append(new_cond_item)

# Create and return new trial object with information from info_list
def createTrial(info_list):
    new_trial = ClinicalTrial()

    # Set basic information
    new_trial.setTitle(info_list[0]);
    new_trial.setID(info_list[1]);

    # Set age range (or min-age) and gender
    if len(info_list) == 5: # a cancer.gov set
        new_trial.setMinAge(info_list[3])
        new_trial.setMaxAge(info_list[2])
        new_trial.setGender(info_list[4])
    elif len(info_list) == 4: # a clintrials.gov set
        new_trial.setMinAge(info_list[2])
        new_trial.setGender(info_list[3])
    else:
        sys.exit("gen_info.txt has some formatting error")

    # Return newly created trial
    return new_trial

# Writes all relations for a given trial to a file
def createAllTurtles(trial, fp):
    # Write general info
    fp.write("<" + trial.id_num + ">\n")
    fp.write("\trel:title " + "\"" + trial.title + "\" ;\n")
    fp.write("\trel:min_age " + "\"" + trial.min_age + "\" ;\n")
    fp.write("\trel:max_age " + "\"" + trial.max_age + "\" ;\n")
    fp.write("\trel:gender " + "\"" + trial.gender + "\" ;\n")

    # Write conditions
    fp.write("\trel:condition ")
    object_list = ""
    for item in trial.cond_list:
        object_list += "\"" + item + "\", "
    object_list = object_list.rstrip(', ')
    fp.write(object_list)

    # Write inclusion criteria (if exists)
    if trial.inclusion:
        fp.write(";\n")
        object_list = ""
        fp.write("\trel:criteria ")
        for item in trial.inclusion:
             object_list += "\"" + item + "\", "
        object_list = object_list.rstrip(', ')
        fp.write(object_list)

    # Write final period
    fp.write(" .\n")

def main():
    # Check usage
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        sys.exit("Usage: ttl_transfer.py input_gen_info.txt input_mesh_diseases.txt (input_ec_criteria.txt)")

    # Define new filepointers
    f = input_gen_info = input_mesh_diseases = input_ec_criteria = None

    # Open filepointers
    try:
        f = open("results/results.ttl", "w+")
        input_gen_info = open(sys.argv[1], "r")
        input_mesh_diseases = open(sys.argv[2], "r")
        input_ec_criteria = open(sys.argv[3], "r")
    except IOError:
        sys.exit("Input file(s) do not exist")
    except IndexError:
        pass

    # Define list to hold trial objects
    ClinicalTrialList = []

    # Create trials with data from gen_info.txt
    for line in input_gen_info.readlines():
        line = line.rstrip('\n')
        info_list = line.split('~')
        ClinicalTrialList.append(createTrial(info_list))

    # Add conditions to trials in ClinicalTrialList with data from mesh_diseases.txt
    for line in input_mesh_diseases.readlines():
        line = line.rstrip('\n')
        info_list = line.split('~')
        if len(info_list) != 2:
            sys.exit("mesh_diseases.txt has some formatting error")
        ClinicalTrialList[int(info_list[1])].appendCond(info_list[0])

    # Add inclusion criteria to trials if it exists
    if input_ec_criteria:
        for line in input_ec_criteria.readlines():
            line = line.rstrip('\n')
            info_list = line.split('~')
            if len(info_list) != 2:
                sys.exit("ec_criteria.txt has some formatting error")
            ClinicalTrialList[int(info_list[1])].appendInclusion(info_list[0])

    # Write ttl PREFIX information
    f.write("@base <http://clinicaltrials.gov/ct2/show/>\n")
    f.write("@prefix rel: <http://www.dbpedia.org/property/>\n\n")

    # Write all gathered data to results.ttl in ttl format
    for clin_trial in ClinicalTrialList:
        createAllTurtles(clin_trial, f)

    # Close all file-pointers
    f.close(); input_gen_info.close(); input_mesh_diseases.close()
    if input_ec_criteria: input_ec_criteria.close()

if __name__ == "__main__":
    main()
