"""
Name: term_page_manager.py
Descriptions: A script to generate and delete annotation term page and folder structure mirroring data folder (i.e._data/). 
              Can take csv term files or json files in https://github.com/Sage-Bionetworks/synapseAnnotations
Contributors: Dan Lu, Jess Vera
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
    term = term_path.split("/")[-1]
    module = term_path.split("/")[0]
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

    if "Template" in term_path:
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
    print("\033[92m {} \033[00m".format(f"added or modified docs/{term_path}.md"))

def delete_page(page):
    """
    Function to delete term/template markdown page

    :param page(str): the md file name (without file extension)

    :returns: delete the term Markdown page in the docs/<page>
    """
    print("\033[91m {} \033[00m".format(f"deleting docs/{page}.md"))
    os.remove(f"docs/{page}.md")


def main():
  # Main func
  # load data model csv file
  data_model = pd.read_csv("veoibd.data.model.csv")
  
  # get existing docs/ dirs
  module_folders = [path.split("/")[-1] for path in glob.glob("docs/*")]
  
  # get model modules
  # first remove nan Module
  data_model_nonans = data_model[~data_model['Module'].isna()]
  model_modules = data_model_nonans.Module.unique()
  
  # delete modules no longer defined in the model
  # modules to delete
  mod_to_delete = np.setdiff1d(module_folders, model_modules).tolist()
  for dir in mod_to_delete:
    for file in glob.glob(f"docs/{dir}/*"):
      print("\033[91m {} \033[00m".format(f"deleting {file}"))
      os.remove(f"{file}")
    print("\033[91m {} \033[00m".format(f"deleting docs/{dir}/"))
    os.rmdir(f"docs/{dir}/")
   
  term_files = []
  for file in glob.glob("_data/**/*"):
    file_split = file.split('/')
    file_split[2] = file_split[2].split(".")[0]
    term_files.append(f"{file_split[1]}/{file_split[2]}")
  
  term_pages = []
  for file in glob.glob("docs/**/*"):
    file_split = file.split('/')
    file_split[2] = file_split[2].split(".")[0]
    # ignore md files that define the module, want to keep those
    if not file_split[1] == file_split[2]:
      term_pages.append(f"{file_split[1]}/{file_split[2]}")
  
  to_delete = np.setdiff1d(term_pages, term_files).tolist()
  list(map(delete_page, to_delete))
  
  # generate pages for new terms and rewrite existing pages so that any descriptions 
  # in the model will be pushed to the dictionary site
  generate_page_temp = partial(generate_page, data_model)
  list(map(generate_page_temp, term_files))


if __name__ == "__main__":
    main()
