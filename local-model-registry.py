#!/usr/bin/env python
# list models in local model registry

import os 
import sys

from llmware.models import ModelCatalog
from llmware.configs import LLMWareConfig

_local_model_catalog = "local_llmware_model_catalog.json"

def load_local_model_catalog(cat_dir=LLMWareConfig.get_model_repo_path(), cat_file=_local_model_catalog):
    mc = ModelCatalog()
    cat_path = os.path.join(cat_dir, cat_file)
    if not os.path.exists(cat_path):
        mc.save_model_registry(fp=cat_dir, fn=cat_file)
    print("Using Model Catalog " + cat_path)
    mc.load_model_registry(fp=cat_dir, fn=cat_file)
    return mc

if __name__ == "__main__":
    mc = load_local_model_catalog()
    print("Model Families:")
    for name in mc.model_classes():
        print("\t" + name)
    #print("Prompt Wrappers:")
    #PromptCatalog.list_all_prompts
    #print("Model Tools:")
    #mc.list_llm_tools()
    #mc.get_llm_fx_mapping()
    print("Models:")
    for i, m in enumerate(ModelCatalog().list_all_models()):
        print("[%04d] %s (%s)" % (i, m['model_name'], m['model_family']))





# tools:
# - list
# - add
# - remove
# - update?
# - edit model card : using $EDITOR
# - sync: update from code base

# Plan:
# - load model_registry from JSON
# - use ModelRegistry.new_model_registry
#def new_model_registry(cls, model_registry):
#        #   remove current models
#        cls.registered_models = []
#        #   add new model registry
#        for i, model in enumerate(model_registry):
#            if cls.validate(model):
#                cls.registered_models.append(model)
# backup plan:
# for model in local models:
#   if model in registry:
#       def update_model(cls, model_name_lookup, new_model_card_dict):
#   else
#        add_model(cls, model_card_dict)
# ModelCatalog 
#  def save_model_registry(self, fp=None, fn="llmware_model_catalog.json"):
#  def load_model_registry(self, fp=None, fn="llmware_model_catalog.json"):
#  def add_model_cards_from_file(self, fp=None, fn="custom_models_manifest.json"):
#        """ Utility method that loads model cards from a single json file and incrementally adds to the model global model list.  """
# def register_new_model_card(self, model_card_dict):
#        """ Registers a new model card directly in the model catalog """ 
# def register_new_hf_generative_model(self, hf_model_name, llmware_lookup_name=None, display_name=None, context_window=2048, prompt_wrapper="<INST>", temperature=0.3, trailing_space="", link=""):
# Registers any Huggingface Generative Model in the ModelCatalog for easy future lookup and integration into LLMWare RAG workflows.  The most important input parameter is hf_model_name, which should correspond to the Huggingface Repo/Model format, e.g., microsoft/phi-2 Any names can be assigned as 'aliases' for the LLMWare Model catalog with both a main lookup name and an optional secondary lookup to be used as a short-name for screen display.  For example, the 'llmware_lookup_name' for 'microsoft/phi-2' could be 'phi-2' or 'my-favorite-model-with-2-in-the-name'.  If no llmware_lookup_name is provided, then it will automatically save as the hf_model_name.
# def register_sentence_transformer_model(self, model_name, embedding_dims, context_window, display_name=None, link=""):
#        """ Registers a model from the SentenceTransformers library into an LLMWare Model Catalog.
#        NOTE: for SentenceTransformers, the model_name should match the SentenceTransformer library lookup
#        name.  """
#
# def register_gguf_model(self, model_name, gguf_model_repo, gguf_model_file_name, prompt_wrapper=None, eos_token_id=0, display_name=None,trailing_space="", temperature=0.3, context_window=2048, instruction_following=True):
#        """ Registers a new GGUF model in model catalog - by default, assumes that the GGUF file is in a Huggingface
#        repository, and will be pulled directly from that repository into a local model_repo cache.
#        Any arbitrary name can be selected as the model_name and/or display_name for the llmware catalog, as the
#        core lookup is in the "gguf_repo" and "gguf_file" parameters.
#        If the GGUF file is in another local file path, then you can access it directly by setting:
#            "custom_model_repo": "/path/to/local/gguf_model/"
#            "custom_model_files": "my_model.gguf"
