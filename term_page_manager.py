"""
Name: term_page_manager.py
definition: a script to generate and delete annotation term page
Contributors: Dan Lu
"""
# load modules
import argparse
import glob
import os
import pdb
from functools import partial

import frontmatter
import numpy as np
import pandas as pd
from mdutils import fileutils


def get_term_info(data_model,term):
    """
    Function to get a dictionary for term definition, definition source, module

    :param term: the term name

    :returns: a dictionary with keys: Description and Module
    """
    # get the definition and module of the term from data model
    results = data_model.loc[
        data_model["Attribute"] == term, ["Description", "Source", "Module"]
    ].to_dict("records")
    return results


def generate_page(data_model, term):
    """
    Function to generate term page

    :param term: the term name

    :returns: a term Markdown page generated under the docs/<module_name> folder
    """
    # load template
    post = frontmatter.load("dataTable_template.md")
    # get term information
    results = get_term_info(data_model, term)
    # add paragraph for term definition and source
    if results[0]["Source"] == "Sage Bionetworks":
        results[0]["Source"] = "https://sagebionetworks.org/"
    post.content = (
        "{% assign mydata=site.data."
        + f"{term}"
        + " %} \n{: .highlight } \n"
        + f"**{term}:**\n"
        + f"{results[0]['Description']} [[Source]]({results[0]['Source']})\n"
        + post.content
    )
    post.metadata["title"] = term
    post.metadata["parent"] = results[0]["Module"]
    # create directory for the moduel if not exist
    if not os.path.exists(f"docs/{results[0]['Module']}/"):
        os.mkdir(f"docs/{results[0]['Module']}/")
        # create a module page
        module = fileutils.MarkDownFile(f"docs/{results[0]['Module']}/{results[0]['Module']}")
        module.append_end(f"--- \nlayout: page \ntitle: {results[0]['Module']} \nhas_children: true \nnav_order: 2 \n---")
    # create file
    file = fileutils.MarkDownFile(f"docs/{results[0]['Module']}/{term}")
    # add content to the file
    file.append_end(frontmatter.dumps(post))

def delete_page(term):
    for file in glob.glob("docs/*/*.md"):
        if file.split('/')[-1].split('.')[0] == term:
            os.remove(file)
def main():
    # load data model csv file
    data_model = pd.read_csv("veoibd.data.model.csv")
    # pull terms 
    term_files = [file.split('/')[-1].split('.')[0] for file in glob.glob("_data/*.csv")]
    term_pages = [file.split('/')[-1].split('.')[0] for file in glob.glob("docs/*/*.md")]
    to_add = map(str,np.setdiff1d(term_files,term_pages))
    to_delete = np.setdiff1d(term_pages,term_files).tolist()
    # generate pages for terms with the term files
    generate_page_temp = partial(generate_page, data_model)
    list(map(generate_page_temp, to_add))
    # delete pages for terms without the term files and exclude module and template pages
    to_delete = [x for x in to_delete if x not in data_model['Module'].dropna().unique().tolist() and 'Template' not in x ]
    list(map(delete_page, to_delete))

if __name__ == "__main__":
    main()
