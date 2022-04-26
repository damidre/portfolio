import json
from operator import index
import pandas as pd
import glob

### Set Debug Configuration ###
pd.set_option("display.max_rows", None, "display.max_columns", None)
test_patientID = "d13874ec-22ea-46ed-a55c-1fd75ef56a58"
test_givenName = 'Cleo27'
test_familyName = 'Bode78'
test_fullName = test_givenName + ' ' + test_familyName


### Parse Input Data ###
patient_info = test_fullName
if len(patient_info) < 34:
    pt_jsonFile= r"data-eng-coding-challenge-hvaoyr\CodingChallengeData\Patient.ndjson"
    pt_table = pd.read_json(pt_jsonFile, lines=True)
    pt_table = pt_table[['id','name']]
    pt_truth_table_givenName = pt_table.apply(lambda row: row.astype(str).str.contains(test_givenName).any(), axis=1)

### Verify Patient Name and Match to Patient ID ###

    if pt_truth_table_givenName.any() == True:
        index_list = pt_truth_table_givenName[pt_truth_table_givenName].index.to_list()
        index_list_length = len(index_list)
        pt_truth_table_familyName = pt_table.apply(lambda row: row.astype(str).str.contains(test_familyName).any(), axis=1)
        if pt_truth_table_familyName.any() == True:
            for elem in range(index_list_length):
                if pt_truth_table_familyName[index_list[elem]] == True:
                    val = pt_table['id'].values[index_list[elem]]
                    test_patientID = val
                else:
                    print("No last name found for this patient")
                
    else: 
        print("Patient Not Found")
        quit()

#### Load and Transform Resource Files into Searchable List ####

resource_files = glob.glob(r"data-eng-coding-challenge-hvaoyr\CodingChallengeData\*.ndjson")
resource_files_len = len(resource_files)

### Search each resource file for the selected patient and count the occurrences ###

for elem in range(resource_files_len):
    json_filename = resource_files[elem]
    json_df = pd.read_json(json_filename, lines=True)
    truth_table = json_df.apply(lambda row: row.astype(str).str.contains(test_patientID).any(), axis=1)
    if truth_table.any() == True:
        count = 0
        for row in truth_table:
            if row == True:
                count += 1
        print(json_filename + "| " + "  Resource Count: " + str(count))