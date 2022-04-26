import pandas as pd

"""
Questions:
- Which state spends the most per ESRD patient (Inpatient + Outpatient + RX Drug) per year
- Which state spends the least per ESRD patient (Inpatient + Outpatient + RX Drug) per year
- What is the average amount spent by ESRD patient on claims INITIATED 180 days before EOL. 

Needed Variables:
CLM_PMT_AMT - Claim Payment Amount
CLM_FROM_DT - Claim Start Date
BENE_DEATH_DT - Death date 
BENE_ESRD_IND - ESRD Indicator
TOT_RX_CST_AMT - Total RX Cost Amount
SRVC_DT - Service Date
SP_STATE_Code - State Code
"""

# Set max rows displayed in print output to 25
pd.set_option("display.max_rows", 25)


# ------Extract data from CSVs into a dataframe then select only the necessary columns

inpatientData = pd.read_csv("/Users/damiyrleonard/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv");
outpatientData = pd.read_csv("/Users/damiyrleonard/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv");
prescriptionData = pd.read_csv("/Users/damiyrleonard/Downloads/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.csv");
beneficiaryData2008 = pd.read_csv("/Users/damiyrleonard/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv");
beneficiaryData2009 = pd.read_csv("/Users/damiyrleonard/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_1.csv");
beneficiaryData2010 = pd.read_csv("/Users/damiyrleonard/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_1.csv");

bd08 = beneficiaryData2008[['DESYNPUF_ID', 'BENE_ESRD_IND', 'BENE_DEATH_DT', 'SP_STATE_CODE']]
bd09 = beneficiaryData2009[['DESYNPUF_ID', 'BENE_ESRD_IND', 'BENE_DEATH_DT', 'SP_STATE_CODE']]
bd10 = beneficiaryData2010[['DESYNPUF_ID', 'BENE_ESRD_IND', 'BENE_DEATH_DT', 'SP_STATE_CODE']]
opd = outpatientData[['DESYNPUF_ID','CLM_PMT_AMT','CLM_FROM_DT']]
ipd = inpatientData[['DESYNPUF_ID','CLM_PMT_AMT','CLM_FROM_DT']]
rxd = prescriptionData[['DESYNPUF_ID','TOT_RX_CST_AMT','SRVC_DT']]


# The following script function takes in the variable of a beneficiary dataframe
# ---Start Script Function---------------------------------------------------------------------------


def runScript(beneficiary_variable):

        # Reassign variable file to work with script
        bd = beneficiary_variable

        # Assign variable file name to new variable to create ending file name
        vname = [name for name in globals() if globals()[name] is bd]
        vname = "".join(str(x) for x in vname)

        print("Loading beneficiary file: " + vname)


        # Create filter for ESRD patient
        print("Filtering by ESRD Patients")
        bd = bd.loc[bd.BENE_ESRD_IND == 'Y']


        # Join beneficiary data with claims data
        print("Joining in Claims data")
        bd = pd.merge(bd, opd, how="left", on="DESYNPUF_ID") #x - outpatient
        bd = pd.merge(bd, ipd, how="left", on="DESYNPUF_ID") #y - inpatient
        bd = pd.merge(bd, rxd, how="left", on="DESYNPUF_ID") #prescriptions

        # Change date columns to datetime datatype
        print("Converting data types")
        bd['BENE_DEATH_DT'] = pd.to_datetime(bd["BENE_DEATH_DT"], format='%Y%m%d')
        bd['CLM_FROM_DT_x'] = pd.to_datetime(bd["CLM_FROM_DT_x"], format='%Y%m%d')
        bd['CLM_FROM_DT_y'] = pd.to_datetime(bd["CLM_FROM_DT_y"], format='%Y%m%d')
        bd['SRVC_DT'] = pd.to_datetime(bd["SRVC_DT"], format='%Y%m%d')

        # Calculate days between last claim and death and load into new column
        print("Calculating claims before death")
        bd['Death_Period_Outpatient'] = (bd["BENE_DEATH_DT"] - bd["CLM_FROM_DT_x"]).dt.days
        bd['Death_Period_Inpatient'] = (bd["BENE_DEATH_DT"] - bd["CLM_FROM_DT_y"]).dt.days
        bd['Death_Period_RX'] = (bd["BENE_DEATH_DT"] - bd["SRVC_DT"]).dt.days

        # Change format of date to extract the year and add to a new column
        print("Extracting year of claims")
        bd['Outpatient Claim Year'] = bd['CLM_FROM_DT_x'].dt.year
        bd['Inpatient Claim Year'] = bd['CLM_FROM_DT_y'].dt.year
        bd['Rx Claim Year'] = bd['SRVC_DT'].dt.year

        # --- Uncomment this section to run average numbers--------------------------
        """
        #Filter the dataframe into three sets for patients who passed on 180 days or less ago
        print("Filtering patients who have passed on")
        a = bd.loc[bd.Death_Period_Outpatient <= 180]
        b = bd.loc[bd.Death_Period_Inpatient <= 180]
        c = bd.loc[bd.Death_Period_RX <= 180]

        #Verify that the dataframe is not empty and if not drop unneeded columns
        print("Writing average numbers to disk")
        if not a.empty:
            print("Creating Average file for Outpatient")
            a.drop(columns=['CLM_PMT_AMT_y', 'CLM_FROM_DT_y', 'TOT_RX_CST_AMT', 'SRVC_DT', 'Death_Period_Inpatient','Death_Period_RX','Inpatient Claim Year','Rx Claim Year'], axis=1, inplace=True)
            a.to_csv("/Users/damiyrleonard/Downloads/outpatientaverage" + vname + ".csv")

        if not b.empty:
            print("Creating Average file for Inpatient")
            b.drop(columns=['CLM_PMT_AMT_x', 'CLM_FROM_DT_x', 'TOT_RX_CST_AMT', 'SRVC_DT', 'Death_Period_Outpatient','Death_Period_RX','Outpatient Claim Year','Rx Claim Year'], axis=1, inplace=True)
            b.to_csv("/Users/damiyrleonard/Downloads/inpatientaverage" + vname + ".csv")

        if not c.empty:
            print("Creating Average file for RX")
            c.drop(columns=['CLM_PMT_AMT_x', 'CLM_FROM_DT_x','CLM_PMT_AMT_y','CLM_FROM_DT_y','Death_Period_Outpatient','Death_Period_Inpatient','Outpatient Claim Year','Inpatient Claim Year'], axis=1, inplace=True)
            c.to_csv("/Users/damiyrleonard/Downloads/rxaverage" + vname + ".csv")

        else:
            print("Dataframes do not contain data.")

        print("Writing average numbers to disk")
        """



        # ------Uncomment this section for total aggregation costs------------------
        #"""
        # Sum the inpatient, outpatient, and RX costs

        print('Grouping patients by claim year and state')
        ab = bd.groupby(['Outpatient Claim Year','SP_STATE_CODE','Death_Period_Outpatient']).sum().reset_index()
        cd = bd.groupby(['Inpatient Claim Year','SP_STATE_CODE', 'Death_Period_Inpatient']).sum().reset_index()
        ef = bd.groupby(['Rx Claim Year','SP_STATE_CODE', 'Death_Period_RX']).count().reset_index()

        if not ab.empty:
            print("Creating Claims file for Outpatient")
            ab.drop(columns=['CLM_PMT_AMT_y', 'TOT_RX_CST_AMT', 'Death_Period_Inpatient','Death_Period_RX','Inpatient Claim Year','Rx Claim Year'], axis=1, inplace=True)
            ab.to_csv("/Users/damiyrleonard/Downloads/cricketOutpatient" + vname + ".csv")

        if not cd.empty:
            print("Creating Claims file for Inpatient")
            cd.drop(columns=['CLM_PMT_AMT_x', 'TOT_RX_CST_AMT', 'Death_Period_Outpatient','Death_Period_RX','Outpatient Claim Year','Rx Claim Year'], axis=1, inplace=True)
            cd.to_csv("/Users/damiyrleonard/Downloads/cricketInpatient" + vname + ".csv")

        if not ef.empty:
            print("Creating Claims file for RX")
            ef.drop(columns=['CLM_PMT_AMT_x', 'CLM_FROM_DT_x','CLM_PMT_AMT_y','CLM_FROM_DT_y','Death_Period_Outpatient','Death_Period_Inpatient','Outpatient Claim Year','Inpatient Claim Year'], axis=1, inplace=True)
            ef.to_csv("/Users/damiyrleonard/Downloads/cricketRx" + vname + ".csv")
            
        else:
            print("Dataframes do not contain data.")

        #"""
        # ----------------------------------------------------------------------------

        print("Script Finished.\n")


# ---- End script function --------------------------------------------------------

# Execute the script
runScript(bd08)

runScript(bd09)

runScript(bd10)
