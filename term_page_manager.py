"""
Name: term_page_manager.py
Descriptions: A script to generate and delete annotation term page and folder structure mirroring data folder (i.e._data/). 
              Can take csv term files or json files in https://github.com/Sage-Bionetworks/synapseAnnotations
Contributors: Dan Lu
"""
# load modules
import glob
import json
import os
import re
from functools import partial

import frontmatter
import numpy as np
import pandas as pd
from mdutils import fileutils


def get_term_info(data_model, term):
    """
    Function to get a dictionary for term definition, definition source, module
    :param data_model (pd.DataFrame): data model data frame
    :param term(str): the term name

    :returns: a dictionary with keys: Description and Module
    """
    # get the definition and module of the term from data model
    results = data_model.loc[
        data_model["Attribute"] == term, ["Description", "Source", "Module"]
    ].to_dict("records")
    return results


def generate_page(data_model, term_path):
    """
    Function to generate term/template markdown page

    :param data_model: data model dataframe
    :param term_path: the file path to the term file

    :returns: a term Markdown page generated under the docs/<module_name> folder
    """
    # get term information
    term = term_path.split("/")[-1].split(".")[0]
    module = term_path.split("/")[1]
    if "json" in term_path:
        # term with JSON files
        with open(term_path) as f:
            results = json.load(f)
            description = results["description"]
            source = results["$id"]
    else:
        # term with csv files
        results = get_term_info(data_model, term)
        description = results[0]["Description"]
        source = results[0]["Source"]

    # add source url for Sage Bionetworks
    if source == "Sage Bionetworks":
        source = "https://sagebionetworks.org/"

    if "Template" in term:
        # load template
        post = frontmatter.load("template_page_template.md")
        # convert camel case to title
        post.metadata["title"] = re.sub("([A-Z]+)", r" \1", term).title()
        post.metadata["permalink"] = f'docs/{post.metadata["title"]}.html'
    elif "json" in term_path:
        # load template
        post = frontmatter.load("json_term_page_template.md")
        post.metadata["title"] = term
    else:
        post = frontmatter.load("csv_term_page_template.md")
        post.metadata["title"] = term
    # post.metadata["parent"] = re.sub("([A-Z]+)", r" \1", module).title() # used when working with json file in synapseAnnotation repo
    post.metadata["parent"] = module
    # load input data and term/template description
    if "Template" in term_path:
        post.content = (
            "{% assign mydata=site.data."
            + f"{module}."
            + f"{term}"
            + " %} \n{: .note-title } \n"
            + f">{post.metadata['title']}\n"
            + ">\n"
            + f">{description} [[Source]]({source})\n"
            + post.content
        )
    elif "json" in term_path:
        post.content = (
            "{% assign mydata=site.data."
            + f"{module}."
            + f"{term}.anyOf"
            + " %} \n"
            + "{% assign module=site.data."
            + f"{module}."
            + f"{term}"
            + " %} "
            + "\n{: .note-title } \n"
            + f">{post.metadata['title']}\n"
            + ">\n"
            + f">{description} [[Source]]({source})\n"
            + post.content
        )
    else:
        post.content = (
            "{% assign mydata=site.data."
            + f"{module}."
            + f"{term}"
            + " %} \n"
            + "\n{: .note-title } \n"
            + f">{post.metadata['title']}\n"
            + ">\n"
            + f">{description} [[Source]]({source})\n"
            + post.content
        )

    # create directory for the moduel if not exist
    if not os.path.exists(f"docs/{post.metadata['parent']}/"):
        os.mkdir(f"docs/{post.metadata['parent']}/")
        # create a module page
        module_page = fileutils.MarkDownFile(
            f"docs/{post.metadata['parent']}/{post.metadata['parent']}"
        )
        if "Template" in term:
            # add permalink for template page
            module_page.append_end(
                f"--- \nlayout: page \ntitle: {post.metadata['parent']} \nhas_children: true \nnav_order: 5 \npermalink: docs/{' '.join(post.metadata['parent'].split('_'))}.html \n---"
            )
        else:
            module_page.append_end(
                f"--- \nlayout: page \ntitle: {post.metadata['parent']} \nhas_children: true \nnav_order: 2 \npermalink: docs/{' '.join(post.metadata['parent'].split('_'))}.html \n---"
            )

    # create file
    file = fileutils.MarkDownFile(f"docs/{post.metadata['parent']}/{term}")
    # add content to the file
    file.append_end(frontmatter.dumps(post))


def delete_page(term):
    """
    Function to delete term/template markdown page

    :param term(str): the term name

    :returns: delete the term Markdown page in the docs/<module_name> folder
    """
    for file in glob.glob("docs/**/*.md"):
        if file.split("/")[-1].split(".")[0] == term:
            os.remove(file)


def main():
    # load data model csv file
    data_model = pd.read_csv("veoibd.data.model.csv")
    # pull terms
    term_files = [file.split("/")[-1].split(".")[0] for file in glob.glob("_data/**/*")]
    term_pages = [
        file.split("/")[-1].split(".")[0] for file in glob.glob("docs/**/*.md")
    ]
    to_add = np.setdiff1d(term_files, term_pages).tolist()
    to_delete = np.setdiff1d(term_pages, term_files).tolist()
    to_add_path = [
        file
        for term in to_add
        for file in glob.glob("_data/**/*")
        if file.split("/")[-1].split(".")[0] == term
    ]
    # generate pages for terms with the term files
    generate_page_temp = partial(generate_page, data_model)
    list(map(generate_page_temp, to_add_path))
    # delete pages for terms without the term files and exclude module page
    to_delete = [
        x for x in to_delete if x not in data_model["Module"].dropna().unique().tolist()
    ]
    list(map(delete_page, to_delete))


if __name__ == "__main__":
    main()
