#!/usr/bin/env python
# list models in local model registry
# Usage:
#    mc = load_local_model_catalog()
#    print("Models:")
#    for i, m in enumerate(ModelCatalog().list_all_models()):
#        print("[%04d] %s (%s)" % (i, m['model_name'], m['model_family']))


import os 

from llmware.models import ModelCatalog
from llmware.configs import LLMWareConfig

_local_model_catalog = "local_llmware_model_catalog.json"
_last_used_model_dir = LLMWareConfig.get_model_repo_path()
_last_used_model_file = _local_model_catalog

# Note: this will create the catalog if it does not exist
def load_local_model_catalog(cat_dir=LLMWareConfig.get_model_repo_path(), cat_file=_local_model_catalog):
    mc = ModelCatalog()
    if not os.path.exists(cat_dir):
        os.makedirs(cat_dir)
    cat_path = os.path.join(cat_dir, cat_file)
    if not os.path.exists(cat_path):
        # Create local catalog from built-in if it doesn't exist
        mc.save_model_registry(fp=cat_dir, fn=cat_file)
    mc.load_model_registry(fp=cat_dir, fn=cat_file)
    # pretty unsafe if the same process opens multiple catalogs: be warned
    _last_used_model_dir = cat_dir
    _last_used_model_file = cat_file
    return mc

def save_local_model_catalog(mc, cat_dir=_last_used_model_dir, cat_file=_last_used_model_file, create_backup=True):
    if not os.path.exists(cat_dir):
        os.makedirs(cat_dir)

    cat_path = os.path.join(cat_dir, cat_file)
    if os.path.exists(cat_path) and create_backup:
        os.rename(cat_path, cat_path + '.prev')

    mc.save_model_registry(fp=cat_dir, fn=cat_file)

def local_model_catalog():
    return (_last_used_model_dir,_last_used_model_file)
