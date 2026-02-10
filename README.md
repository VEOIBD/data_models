# VEOIBD Data Model

This is the repository hosting [VEOIBD data model](https://github.com/VEOIBD/data_models/blob/main/veoibd.data.model.csv) 
and a set of [standardized metadata terms](https://github.com/VEOIBD/data_models/tree/main/_data) 
that can be used to describe attributes in the data model. The data model defines attributes
that are associated with a dataset type (e.g. clinical metadata) and their interdependencies. 

> This branch should not be merged with `gh-pages` and vice versa

## Updata Data Model and Metadata Dictionary
<img src="https://github.com/VEOIBD/data_models/assets/90745557/e061e265-77ff-4bca-a6bb-a525e79d3352" width="300" />

**Step 1.** Pull most recent changes from the `main` branch and create a **new branch**

**Step 2.** On the new branch, edit the veoibd.data.model.csv. 

**Step 3.** Push the new branch to the remote repo create a pull request (PR) to the `main` branch. 
Creating a PR will trigger the `ci-schema-convert.yml` workflow 

**Step 4.** Review PR and merge to main branch. Merging the PR will trigger several 
GitHub Actions in the `gh-pages` branch to update and deploy the data dictionary site. 
See the `gh-pages` branch for more details.

## `main` branch

This repository contains 2 major files:

1. `veoibd.data.model.csv`: The CSV representation of the VEOIBD data model and is used 
to create the JSON-LD representation of the data model.

2. `veoibd.data.model.jsonld`: The JSON-LD representation of the data model, which is 
automatically created from the CSV data model using the schematic CLI. More details 
on how to convert the CSV data model to the JSON-LD data model can be 
found [here](https://sage-schematic.readthedocs.io/en/develop/cli_reference.html#schematic-schema-convert). 
This is the central schema (data model) which will be used to power the 
generation of metadata manifest templates for various data types (e.g., `scRNA-seq Level 1`) 
from the schema.

