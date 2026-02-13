from synapseclient import Synapse
from synapseclient.extensions.curator import generate_jsonschema
import pandas as pd

'''
use synapseclient extension to create Curator json schema from context models
'''

# create synapse client obj, this will be unnecessary in future client releases
syn = Synapse()

# compile list of templates defined in the model
model_csv_fid = "veoibd.data.model.csv"
model = pd.read_csv(model_csv_fid, dtype=object)
templates = model[model.DependsOn.str.contains("Component") == True]
templates = templates[templates.Attribute.str.contains("Template") == True]
templates.loc[:,'Attribute'] = templates['Attribute'].apply(lambda x: x.replace(' ',''))

def first_cap(x):
  return x[0].upper() + x[1:]

templates.loc[:,'Attribute'] = templates['Attribute'].apply(lambda x: first_cap(x))
templates = list(templates.Attribute)

for t in templates:
  print(f"Generating JSON schemas for {t}...")
  schemas, file_paths = generate_jsonschema(
    data_model_source = model_csv_fid,
    output=f"model_json_schemas/veoibd.{t}.schema.json",
    data_types= [t],
    synapse_client=syn
  )

print("JSON schema generation complete!")

# END
