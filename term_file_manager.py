"""
Name: term_file_manager.py
definition: a script to generate/update term csv 
parameters: term (str): the term name (optional)
Contributors: Dan Lu
"""
# load modules
import argparse
import os
import pdb
from optparse import Values

import pandas as pd


def generate_csv(row):
    # convert dataframe to long format
    df = row.to_frame().T.reset_index(drop=True)
    df = df.drop(columns = ['Attribute']).set_index(["Type", "Module"]).apply(lambda x: x.str.split(",").explode()).reset_index()
    # add columns
    df.rename(columns={"Valid Values": "Key"}, inplace=True)
    df = df.assign(**dict([(_, None) for _ in ["Key Description", "Source"]]))
    df = df[["Key", "Key Description", "Type", "Source", "Module"]]
    df.to_csv(f"./_data/{row.Attribute}.csv", index=False)
    return df

def update_csv(row):
    # convert dataframe to long format
    new = row.to_frame().T.reset_index(drop=True)
    new = new.drop(columns = ['Attribute']).set_index(["Type", "Module"]).apply(lambda x: x.str.split(",").explode()).reset_index()
    # add columns
    new.rename(columns={"Valid Values": "Key"}, inplace=True)
    #load existing csv
    old = pd.read_csv(f"./_data/{row.Attribute}.csv")
    # upload existing csv if Key, Type or Module column is changed
    if not (new['Key'].equals(old['Key']) and new['Type'].equals(old['Type']) and new['Module'].equals(old['Module'])):
        updated = new.merge(old, how='left', on=["Key","Type", "Module"])
        updated["Type"] = new["Type"]
        updated["Module"] = new["Module"]
        updated = updated[["Key", "Key Description", "Type", "Source", "Module"]]
        updated.to_csv(f"./_data/{row.Attribute}.csv", index=False)
        print(f"updated {row.Attribute}.csv")      
    
def manage_term_files(term=None):
    # load data model
    data_model = pd.read_csv('veoibd.data.model.csv')
    # get the list of existing term csvs
    files = [
        file.split(".csv")[0] for file in os.listdir("_data/") if file.endswith(".csv")
    ]
    if term:
        df = data_model.loc[
            (data_model["Module"].notnull()) & (data_model["Attribute"].isin(term))
        ][["Attribute", "Valid Values", "Type", "Module"]]
    else:
        df = data_model.loc[data_model["Module"].notnull(),][
            ["Attribute", "Valid Values", "Type", "Module"]
        ]
    # generate files when term files don't exist
    new_terms = df.loc[~df["Attribute"].isin(files),].reset_index(drop=True)
    # generate csv by calling reformatter for each row of the df
    new_terms.apply(lambda row: generate_csv(row), axis=1)
    # update files if the term files exist
    exist_terms = df.loc[df["Attribute"].isin(files),].reset_index(drop=True)
    exist_terms.apply(lambda row: update_csv(row), axis=1)
    # delete term csv if the attribute is removed from data model
    [os.remove(f"_data/{file}.csv") for file in files if file not in data_model.Attribute.values]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "term",
        type=str,
        help="The term name(s) (Optional). Provide when you want to generate file(s) for specific term(s). Leave it blank if you want to edit files for all terms",
        nargs="*",
    )
    args = parser.parse_args()
    if args.term:
        manage_term_files(args.term)
    else:
        manage_term_files()


if __name__ == "__main__":
    main()
