"""
Name: term_file_manager.py
Descriptions: a script to generate/update term csv 
parameters: term (str): the term name (optional)
Contributors: Dan Lu
"""
# load modules
import argparse
import glob
import os
from functools import partial

import pandas as pd


def get_template_keys(data_model,template):
    """
    Function to get the list of terms for metadata template

    :param data_model (pd.DataFrame): data model data frame
    :param template (str): metadata template name in data model file
    """
    # extrace dependsOn values for the tempalte
    depends_on = data_model.loc[data_model['Attribute'] == template, 'DependsOn'].str.split(',').values[0]
    # extract dependencies for valid values of required attributes
    valid_values = data_model.loc[data_model['Attribute'].isin(depends_on), 'Valid Values'].dropna().tolist()
    valid_values = list(set([value for values_list in valid_values for value in values_list.split(',')]))
    # get the dependsOn values for valid values and concatenate it with original dependsOn list of the template
    depend_on_ext = data_model.loc[data_model['Attribute'].isin(valid_values), 'DependsOn'].dropna().tolist()
    depend_on_ext = list(set([value for values_list in depend_on_ext for value in values_list.split(',')]))
    depends_on.extend(depend_on_ext)    
    return depends_on

def generate_csv(data_model,term):
    """
    Function to generate term csv file for an annotation term

    :param data_model (pd.DataFrame): data model data frame
    :param term (str): an annotation term
    """
    parent_folder = data_model.loc[data_model['Attribute'] == term, ]["Module"].unique()[0]
    if 'Template' in term:
        # generate csv for template
        depends_on = get_template_keys(data_model, term)
        # filter out attributes from data model table
        df = data_model.loc[data_model['Attribute'].isin(depends_on), ]
        df = df[['Attribute','Description', 'Type', 'Valid Values', 'DependsOn', 'Required','Source','Module']].reset_index(drop= True)
        df.rename(columns = {'Attribute': 'Key', 'Description':'Key Description'}, inplace = True)
    else: 
        df = data_model.loc[data_model['Attribute'] == term, ][["Attribute", "Valid Values", "DependsOn","Type", "Module"]]
        # generate csv for term
        df = df.drop(columns = ['Attribute','DependsOn']).set_index(["Type", "Module"]).apply(lambda x: x.str.split(",").explode()).reset_index()
        # add columns
        df.rename(columns={"Valid Values": "Key"}, inplace=True)
        df = df.assign(**dict([(_, None) for _ in ["Key Description", "Source"]]))
        df = df[["Key", "Key Description", "Type", "Source", "Module"]]
    df.to_csv(f"./_data/{parent_folder}/{term}.csv", index=False)
    print("\033[92m {} \033[00m" .format(f'Added {term}.csv'))

def update_csv(data_model, term):
    if 'Template' in term:
        depends_on = get_template_keys(data_model, term)
        new = data_model.loc[data_model['Attribute'].isin(depends_on), ]
        new = new[['Attribute','Description', 'Type', 'Valid Values', 'DependsOn', 'Required','Source','Module']].reset_index(drop= True)
        new.rename(columns = {'Attribute': 'Key', 'Description':'Key Description'}, inplace = True)
        # update template file
        new.to_csv(f"./_data/{new.Module.unique()[0]}/{term}.csv", index=False)
        print("\033[92m {} \033[00m" .format(f'Updated {term}.csv'))
    else: 
        # convert dataframe to long format
        new = data_model.loc[data_model['Attribute'] == term, ][["Attribute", "Valid Values", "DependsOn","Type", "Module"]]
        new = new.drop(columns = ['Attribute','DependsOn']).set_index(["Type", "Module"]).apply(lambda x: x.str.split(",").explode()).reset_index()
        # add columns
        new.rename(columns={"Valid Values": "Key"}, inplace=True)
        #load existing csv
        old = pd.read_csv(f"./_data/{new.Module.unique()[0]}/{term}.csv")
        # upload existing csv if Key, Type or Module column is changed
        if not (new['Key'].equals(old['Key']) and new['Type'].equals(old['Type']) and new['Module'].equals(old['Module'])):
            updated = new.merge(old[["Key", "Key Description","Source"]], how='left', on=["Key"])
            updated = updated[["Key", "Key Description", "Type", "Source", "Module"]]
            updated.to_csv(f"./_data/{new.Module.unique()[0]}/{term}.csv", index=False)
            print("\033[92m {} \033[00m" .format(f'Updated {term}.csv'))     
    
def manage_term_files(term=None):
    # load data model
    data_model = pd.read_csv('./veoibd.data.model.csv')
    # get the list of existing term csvs
    files = [
        file.split("/")[-1].split(".")[0] for file in glob.glob('_data/**/*') if file.endswith(('csv','json'))
    ]
    if term:
        df = data_model.loc[
            (data_model["Module"].notnull()) & (data_model["Attribute"].isin(term))
        ]
    else:
        df = data_model.loc[data_model["Module"].notnull(),]
    # generate files when term files don't exist
    new_terms = df.loc[~df["Attribute"].isin(files),'Attribute'].tolist()
    # generate csv by calling reformatter for each row of the df
    generate_csv_temp = partial(generate_csv, data_model)
    list(map(generate_csv_temp, new_terms))
    # update files if the term files exist
    exist_terms = df.loc[df["Attribute"].isin(files),'Attribute'].tolist()
    update_csv_temp = partial(update_csv, data_model)
    list(map(update_csv_temp, exist_terms))
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
