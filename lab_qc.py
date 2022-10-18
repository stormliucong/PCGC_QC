import pandas as pd
import argparse


def filterHighQualityCodes(x, count_limit = 0.01):
    '''
    input a row
    '''
    if x['count_y'] < int(x['count_x'] * count_limit): # ignore those low quality ones.
        return 0
    
    # remove if exceed the iqr
    if x['50%_x'] < x['25%_y']: 
        return 0
    if x['50%_x'] > x['75%_y']:
        return 0  
    if x['50%_y'] < x['25%_x']:
        return 0 
    if x['50%_y'] > x['75%_x']:
        return 0 
    return 1

def qcLab(pcgc_raw_file_path, output_qc_file_path=None, count_limit = 0.01):
    '''
    load pcgc v2 submission format
    return qc'd submission format
    '''
    lab_extracted_df =pd.read_csv(pcgc_raw_file_path)
    unit_count_df = lab_extracted_df.groupby(["LAB_LOINC_CODE","LAB_VALUE_UNIT"])['LAB_VALUE_NUMERIC'].describe().reset_index()
    idx =  unit_count_df.groupby(['LAB_LOINC_CODE'])['count'].idxmax()
    majority_df = unit_count_df.loc[idx]
    comp_df = majority_df.merge(unit_count_df,on='LAB_LOINC_CODE')

    comp_df['HIGH_QUALITY'] = comp_df.apply(lambda x: filterHighQualityCodes(x, count_limit = count_limit), axis = 1)
    filtered_code_df = comp_df[comp_df['HIGH_QUALITY'] == 1][['LAB_LOINC_CODE','LAB_VALUE_UNIT_y']].rename(columns={"LAB_VALUE_UNIT_y" : "LAB_VALUE_UNIT"})
    lab_extracted_highqc_df = filtered_code_df.merge(lab_extracted_df)
    if output_qc_file_path is not None:
        lab_extracted_highqc_df.to_csv("/phi_home/cl3720/phi/PCGC-EMR-extraction/2nd_request/PCGC-EMRv2-CUMC-Lab-High-QC.csv",index=None)
    return lab_extracted_highqc_df


if __name__ == "__main__":
    # pcgc_raw_file_path = "/phi_home/cl3720/phi/PCGC-EMR-extraction/2nd_request/PCGC-EMRv2-CUMC-Lab.csv"
    # output_qc_file_path = "/phi_home/cl3720/phi/PCGC-EMR-extraction/2nd_request/PCGC-EMRv2-CUMC-Lab-QC.csv"
    parser = argparse.ArgumentParser()
    parser.add_argument("-input", help="file path of the raw pcgc lab submission file",required=True)
    parser.add_argument("-output", help="file path of the qc'd pcgc lab submission file",required=True)
    parser.add_argument("-count_limit", default=0.01, help="the lowest ratio of the counts a unit should be considered for a loinc-code. e.g. if the majority of the unit have 100 observation, 10 observations are required for any unit for that loinc-code if 0.1 is provided (default: %(default)s)")
    args = parser.parse_args()
    pcgc_raw_file_path = args.input
    output_qc_file_path = args.output
    count_limit = args.count_limit
    qcLab(pcgc_raw_file_path,output_qc_file_path, count_limit)