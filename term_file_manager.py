"""
Name: term_file_manager.py
Descriptions: a script to generate/update term file in _data/ 
parameters: term (str): the term name (optional)
Contributors: Dan Lu, Jess Vera
"""
# load modules
import argparse
import glob
import os
from functools import partial

import pandas as pd


def get_template_keys(data_model, template):
    """
    Function to get the list of terms for the metadata template

    :param data_model (pd.DataFrame): data model data frame
    :param template (str): the metadata template name in data model file

    :returns: a list of terms for the metadata template
    """
    # extrace dependsOn values for the tempalte
    depends_on = (
        data_model.loc[data_model["Attribute"] == template, "DependsOn"]
        .str.split(",")
        .values[0]
    )
    # extract dependencies for valid values of required attributes
    valid_values = (
        data_model.loc[data_model["Attribute"].isin(depends_on), "Valid Values"]
        .dropna()
        .tolist()
    )
    valid_values = list(
        set([value for values_list in valid_values for value in values_list.split(",")])
    )
    # get the dependsOn values for valid values and concatenate it with original dependsOn list of the template
    depend_on_ext = (
        data_model.loc[data_model["Attribute"].isin(valid_values), "DependsOn"]
        .dropna()
        .tolist()
    )
    depend_on_ext = list(
        set(
            [value for values_list in depend_on_ext for value in values_list.split(",")]
        )
    )
    depends_on.extend(depend_on_ext)
    return depends_on


def generate_term_file(data_model, term):
    """
    Function to generate term file for an annotation term

    :param data_model (pd.DataFrame): data model data frame
    :param term (str): an annotation term
    :returns: a term csv file saved in _data/module folder
    """
    module_folder = data_model.loc[data_model["Attribute"] == term,][
        "Module"
    ].unique()[0]
    if "Template" in term:
        # generate file for template
        depends_on = get_template_keys(data_model, term)
        # filter out attributes from data model table
        df = data_model.loc[
            data_model["Attribute"].isin(depends_on),
        ]
        df = df[
            [
                "Attribute",
                "Description",
                "Type",
                "Valid Values",
                "DependsOn",
                "Required",
                "Source",
                "Module",
            ]
        ].reset_index(drop=True)
        df.rename(
            columns={"Attribute": "Key", "Description": "Key Description"}, inplace=True
        )
    else:
        df = data_model.loc[
            data_model["Attribute"] == term,
        ][["Attribute", "Valid Values", "DependsOn", "Type", "Module"]]
        # generate file for term
        df = (
            df.drop(columns=["Attribute", "DependsOn"])
            .set_index(["Type", "Module"])
            .apply(lambda x: x.str.split(",").explode())
            .reset_index()
        )
        # add columns
        df.rename(columns={"Valid Values": "Key"}, inplace=True)
        df = df.assign(**dict([(_, None) for _ in ["Key Description", "Source"]]))
        df = df[["Key", "Key Description", "Type", "Source", "Module"]]
    
    # if _data/{module_folder} doesn't exits, create the directory first
    if not os.path.exists(f"./_data/{module_folder}"):
      os.makedirs(f"./_data/{module_folder}")
    df.to_csv(f"./_data/{module_folder}/{term}.csv", index=False)
    print("\033[92m {} \033[00m".format(f"Added {term}.csv"))


def update_term_file(data_model, term):
    """
    Function to update existing term file for an annotation term

    :param data_model (pd.DataFrame): data model data frame
    :param term (str): an annotation term
    :returns: an updated term csv file saved in _data/moduel folder
    """
    if "Template" in term:
        module_folder = data_model.loc[data_model["Attribute"] == term,][
            "Module"
        ].unique()[0]
        depends_on = get_template_keys(data_model, term)
        new = data_model.loc[
            data_model["Attribute"].isin(depends_on),
        ]
        new = new[
            [
                "Attribute",
                "Description",
                "Type",
                "Valid Values",
                "DependsOn",
                "Required",
                "Source",
                "Module",
            ]
        ].reset_index(drop=True)
        new.rename(
            columns={"Attribute": "Key", "Description": "Key Description"}, inplace=True
        )
        # update template file
        new.to_csv(f"./_data/{module_folder}/{term}.csv", index=False)
        print("\033[92m {} \033[00m".format(f"Updated {term}.csv"))
    else:
        # convert dataframe to long format
        new = data_model.loc[
            data_model["Attribute"] == term,
        ][["Attribute", "Valid Values", "DependsOn", "Type", "Module"]]
        new = (
            new.drop(columns=["Attribute", "DependsOn"])
            .set_index(["Type", "Module"])
            .apply(lambda x: x.str.split(",").explode())
            .reset_index()
        )
        # add columns
        new.rename(columns={"Valid Values": "Key"}, inplace=True)
        # load existing file
        old = pd.read_csv(f"./_data/{new.Module.dropna().unique()[0]}/{term}.csv")
        # upload existing file if Key, Type or Module column is changed
        if not (
            new["Key"].equals(old["Key"])
            and new["Type"].equals(old["Type"])
            and new["Module"].equals(old["Module"])
        ):
            updated = new.merge(
                old[["Key", "Key Description", "Source"]], how="left", on=["Key"]
            )
            updated = updated[["Key", "Key Description", "Type", "Source", "Module"]]
            updated.to_csv(f"./_data/{new.Module.dropna().unique()[0]}/{term}.csv", index=False)
            print("\033[92m {} \033[00m".format(f"Updated {term}.csv"))


def manage_term_files(term=None):
    """
    Helper function to manage term file by calling generate_term_file() and update_term_file()
    :param term (str, optional): an annotation term
    """
    # load data model
    data_model = pd.read_csv("./veoibd.data.model.csv")
    # get the list of existing term csvs
    files = [file.split("/")[-1].split(".")[0] for file in glob.glob("_data/**/*")]
    if term:
        df = data_model.loc[
            (data_model["Module"].notnull()) & (data_model["Attribute"].isin(term))
        ]
    else:
        df = data_model.loc[
            data_model["Module"].notnull(),
        ]
    # generate files when term files don't exist
    new_terms = df.loc[~df["Attribute"].isin(files), "Attribute"].tolist()
    # generate file by calling reformatter for each row of the df
    generate_term_file_temp = partial(generate_term_file, data_model)
    list(map(generate_term_file_temp, new_terms))
    # update files if the term files exist
    exist_terms = df.loc[df["Attribute"].isin(files), "Attribute"].tolist()
    update_term_file_temp = partial(update_term_file, data_model)
    list(map(update_term_file_temp, exist_terms))
    # delete term file if the attribute is removed from data model
    [
        os.remove(file)
        for file in glob.glob("_data/**/*")
        if file.split("/")[-1].split(".")[0] not in data_model.Attribute.values
    ]


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
