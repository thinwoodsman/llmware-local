#!/usr/bin/env python
# list models in local model registry
# Usage:
#    mc = load_local_model_catalog()
#    print("Models:")
#    for i, m in enumerate(ModelCatalog().list_all_models()):
#        print("[%04d] %s (%s)" % (i, m['model_name'], m['model_family']))


import os 
import sys

from llmware.models import ModelCatalog
from llmware.configs import LLMWareConfig

_local_model_catalog = "local_llmware_model_catalog.json"

# Note: this will create the catalog if it does not exist
def load_local_model_catalog(cat_dir=LLMWareConfig.get_model_repo_path(), cat_file=_local_model_catalog):
    mc = ModelCatalog()
    cat_path = os.path.join(cat_dir, cat_file)
    if not os.path.exists(cat_path):
        mc.save_model_registry(fp=cat_dir, fn=cat_file)
    print("Using Model Catalog " + cat_path)
    mc.load_model_registry(fp=cat_dir, fn=cat_file)
    return mc

