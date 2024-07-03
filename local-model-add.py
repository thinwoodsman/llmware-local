#!/usr/bin/env python
# the purpose of this script is to add models which are not included in the
# llmware model catalog. This script maintains a local model registry
# that operates in parallel with the one in the package.
# TODO: OpenAI API on arbitrary host/port

import os 
import sys
import argparse
import json

from llmware.models import ModelCatalog
from llmware.configs import LLMWareConfig

_local_model_catalog = "local_llmware_model_catalog.json"

def ensure_model_directory(model_card, dry_run=False):
    print("Model card added.")
    print(model_card) 

    model_dir_name = model_card["model_name"].split("/")[-1]
    model_dir = os.path.join(LLMWareConfig.get_model_repo_path(), 
                             model_card["model_name"].split("/")[-1])
    print("Ensure model is located in the following directory:")
    print(model_dir)

    if not dry_run:
        # create model card json
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        card_json_file = os.path.join(model_dir, "model_card.json")
        with open(card_json_file, "w") as f:
            json.dump(model_card, f)

def delete_existing_model(mc, card_names):
    models = mc.global_model_list
    for model in models:
        if model["model_name"] in card_names or \
           model["display_name"] in card_names :
            mc.delete_model_card(model["model_name"])

def load_local_model_catalog(cat_dir=LLMWareConfig.get_model_repo_path(), cat_file=_local_model_catalog):
    mc = ModelCatalog()
    cat_path = os.path.join(cat_dir, cat_file)
    if os.path.exists(cat_path):
        mc.load_model_registry(fp=cat_dir, fn=cat_file)
    else:
        print("Catalog does not exist: " + cat_path)
    return mc

def save_local_model_catalog(mc, cat_dir=LLMWareConfig.get_model_repo_path(), cat_file=_local_model_catalog,create_backup=True):
    if not os.path.exists(cat_dir):
        os.makedirs(cat_dir)

    cat_path = os.path.join(cat_dir, cat_file)
    if os.path.exists(cat_path) and create_backup:
        os.rename(cat_path, cat_path + '.prev'

    mc.save_model_registry(fp=cat_dir, fn=cat_file)

def read_model_config(args_path, args):
    path = args.model_config
    if not path:
        if args_path.endswith("json"):
            # this *is* the config - file/model name must be inferred
            path = args_path
        elif os.path.isdir(args_path):
            json_path = os.path.join(args_path, 'config.json')
            if os.path.exists(json_path):
                path = json_path
        else:
            json_path = os.path.join(os.path.dirname(args_path), 'config.json')
            if os.path.exists(json_path):
                path = json_path

    if not path:
        return { }

    with open(path) as f:                                                 
        config_h = json.load(f)
    return config_h

def fill_model_card_by_model_type(model_card, model_dirname, model_filename, args):
    model_config = read_model_config(args_path, args)
    if args.model_file:
        model_dirname, model_filename = os.path.split(args.model_file)

    model_card["prompt_wrapper"] = args.prompt_wrapper
    if not model_card["prompt_wrapper"]:
         model_card["prompt_wrapper"] = model_config.get('prompt_wrapper', "<INST>")

    model_card["context_window"] = args.context_window
    if not model_card["context_window"]:
         model_card["context_window"] = model_config.get('context_window', 2048)

    model_card["embedding_dims"] = args.embedding_dims
    if not model_card["embedding_dims"]:
         model_card["embedding_dims"] = model_config.get('embedding_dims', 1500)

    model_card["instruction_following"] = args.instruction_following
    model_card["temperature"] = model_config.get('temperature', 0.6)
    model_card["trailing_space"] = model_config.get('trailing_space', "")
    model_card["eos_token_id"] = model_config.get('eos_token_id', 0)

    model_card["model_family"] = args.model_family
    model_card["model_category"] = args.model_category
    model_card["custom_model_files"] = []
    model_card["custom_model_repo"] = ""
    model_card["link"] = ""

    if args.model_source == SRC_HUGGINGFACE:
        # FIXME: ~/.cache/hugging_face/hub/
        model_card["hf_repo"] = args.path[0]
        model_card["model_family"] = "HFGenerativeModel"
        model_card["model_location"] = "hf_repo"
        model_card["model_category"] = "generative_local"
    elif args.model_source == SRC_SENTENCE_XFORM:
        model_card["model_family"] = "LLMWareSemanticModel"
        model_card["model_location"] = "st_repo"
        model_card["model_category"] = "embedding"
    elif args.model_source == SRC_GGUF:
        model_card["model_family"] = "GGUFGenerativeModel"
        model_card["model_location"] = "llmware_repo"
        model_card["model_category"] = "generative_local"
        model_card["gguf_file"] = model_file_name
        model_card["gguf_repo"] = ""
        model_card["custom_model_files"] = [model_file_name]
        model_card["custom_model_repo"] = model_dir_name
        #model_card["fetch"] = {"module":"llmware.models","method":"pull_model_from_hf"}
        #model_card["validation_files"] = [model_file_name]
    elif args.model_source == SRC_ONNX:
        model_card["custom_model_files"] = [model_file_name]
        model_card["custom_model_repo"] = model_dir_name,
        pass
    else: # custom
        print("Using family %s and category %s for custom LLM" % ( model_card["model_family"], model_card["model_category"])) 
        model_card["custom_model_files"] = [model_file_name]
        model_card["custom_model_repo"] = model_dir_name,
        # def register_new_model_card(self, model_card_dict):
        # """ Registers a new model card directly in the model catalog """ 
        #register_new_model_card(self, model_card_dict)
        # general
        # {"model_name": llmware_lookup_name,
        # "context_window": context_window,
        # "prompt_wrapper": prompt_wrapper,
        # hf_model_name should correspond to the hf repo/model standard
        # "hf_repo": hf_model_name,
        # "display_name": display_name, "temperature": temperature, "trailing_space": trailing_space,
        # "model_family": "HFGenerativeModel", "model_category": "generative_local",
        # "model_location": "hf_repo", "instruction_following": False,
        # "link": link,
        # "custom_model_files": [], "custom_model_repo": ""}

        # add_local_model(model_card)

def model_card_from_config(args_path, args):
    # FIXME: check edge cases where --model-file is required:
    #        ARG is JSON and type is ONNX CUSTOM GGUF
    #        ARG is DIR and type is ONNX CUSTOM GGUF
    # FIXME: check that JSON or DIR arg is handled correctly for HF, ST
    model_dir_name = os.path.dirname(args_path)
    model_file_name = os.path.basename(args_path)
    lookup_name = args.lookup_name
    display_name = args.display_name
    model_name = args.model_name
    if not model_name:
         model_name = model_config.get('model_name', model_file_name)

    model_card = None
    if args.model_clone:
        model_card = mc.lookup_model_card(args.model_clone)
        model_card['model_name'] = model_name
        model_card['lookup_name'] = lookup_name
        model_card['display_name'] = display_name
    else:
        model_card = { 'model_name': model_name,
                       'lookup_name': lookup_name,
                       'display_name': display_name
                     }
        fill_model_card_by_model_type(model_card, model_dirname, model_filename, args)
    return model_card

# ----------------------------------------------------------------------
SRC_HUGGINGFACE='hf'
SRC_SENTENCE_XFORM='st'
SRC_GGUF='gguf'
SRC_ONNX='onnx'
SRC_CUSTOM='custom'

def get_args():
    parser = argparse.ArgumentParser(
            description='',
            epilog="""Examples:

""")

    cat_path = os.path.join(LLMWareConfig.get_model_repo_path(), _local_model_catalog)
    parser.add_argument('--catalog-file', dest='cat_path', type=str, 
                        default=cat_path, help="Path to catalog file")
    # ----------------------------------------------------------------
    # model source
    parser.add_argument('-H', '--hugging-face', dest='model_source', 
                        action='store_const', const=SRC_HUGGINGFACE,
                        help='Model argument is a HuggingFace repo name')
    parser.add_argument('-S', '--sentence-transformers', dest='model_source', 
                        action='store_const', const=SRC_SENTENCE_XFORM,
                        help='Model argument is a sentence transformers name')
    parser.add_argument('-G', '--gguf', dest='model_source', 
                        action='store_const', const=SRC_GGUF,
                        help='Model argument is a GGUF file')
    parser.add_argument('-O', '--onnx', dest='model_source', 
                        action='store_const', const=SRC_ONNX,
                        help='Model argument is an ONNX file')
    # jan
    # local-ai
    # lm-studio
    # gpt4all
    # custom
    parser.add_argument('-F', '--binary-file', dest='model_source', 
                        action='store_const', const=SRC_CUSTOM,
                        help='Binary file (custom)')

    # ----------------------------------------------------------------
    # model card

    parser.add_argument('--config-json', dest='model_config', 
                        help='config.json for model')

    parser.add_argument('--clone', dest='model_clone', 
                        help='Clone an existing model card')

    # read model card from file
    parser.add_argument('--model-card', dest='model_card', action="store_true",
                    help='Model argument is a JSON model card')

    # read array of cards from file
    parser.add_argument('--import', dest='import_manifest', action='store_true',
                    help='Model argument is a manifest file of model cards')

    # ----------------------------------------------------------------
    # manual model card specification
    parser.add_argument('--model-file', dest='model_file', 
                        help='Model file, required when main argument is dir or json')
    parser.add_argument('--model-uri', dest='model_uri', 
                        help='Model URI including host, port, URL [UNUSED]')
    parser.add_argument('--model-type', dest='model_type', 
                        help='Model type, e.g. llama, chat [UNUSED]')
    parser.add_argument('--model-name', dest='model_name', 
                        help='Model name')
    parser.add_argument('--model-family', dest='model_family', 
                        default="GGUFGenerativeModel",
                        help='llmware model class, e.g. HFGenerativeModel')
    parser.add_argument('--model-category', dest='model_category', 
                        default="generative_local",
                        help='Category of model, e.g. generative, embedding')
    parser.add_argument('--lookup-name', dest='lookup_name', 
                        help='llmware lookup name for model')
    parser.add_argument('--display-name', dest='display_name', 
                        help='llmware display name for model')
    parser.add_argument('--prompt-wrapper', dest='prompt_wrapper', 
                        help='Prompt wrapper, e.g. "<INST>" or "human_bot"')
    parser.add_argument('--context-window', dest='context_window', type=int,
                        help='Context window length')
    parser.add_argument('--embedding-dims', dest='embedding_dims', type=int,
                        help='Number of embedding dimensions')
    parser.add_argument('--instruction-following', dest='instruction_following',
                        action="store_true",
                        help='This is an instruction-following model')
    # --------
    parser.add_argument('--verify', dest='verify', action='store_true',
                    help='Perform verification load of model')
    parser.add_argument('--no-backup', dest='backup', action='store_false',
                    help='Disable backup of catalog file')
    parser.add_argument('--debug', dest='debug', action='store_true',
                    help='Enable debug output')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true',
                    help='Do not write new model catalog file')

    # the actual model!
    parser.add_argument('path', nargs=1,
                        help='Model directory, GGUF file, ONNX file, HF repo name, ST repo name, or config.json path')
    
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    if args.debug:
        print("Loading catalog from " + args.cat_path)
    cat_dir, cat_file = os.path.split(args.cat_path)

    mc = load_local_model_catalog(cat_dir, cat_file, args.backup)
    args_path = os.path.abspath(args.path[0])

    # handle simple imports
    if args.import_manifest:
        # a JSON array of model cards
        json_dir, json_file = os.path.split(args_path)
        # NOTE: This will error out if model exists
        mc.add_model_cards_from_file(fp=json_dir, fn=json_file)
        sys.exit()
    if args.model_card:
        with open(args.model_card) as f:
            model_card = json.load(f)
            mc.register_new_model_card(model_card)
        ensure_model_directory(model_card, args.dry_run)
        sys.exit()


    model_card = model_card_from_config(args_path, args)
    # ------------------------------------------------------------------------
    delete_existing_model(mc, [model_card['model_name'], model_card['display_name']])
    mc.register_new_model_card(model_card)

    if not model_card:
        print("Error! Could not create model card!")
        sys.exit(2)

    # TODO: add
    if args.verify:
        print("Loading model card")


    if args.debug:
        for i, m in enumerate(mc.list_all_models()):
            print("[%04d] %s (%s)" % (i, m['model_name'], m['model_family'])) 

    ensure_model_directory(model_card, args.dry_run)

    if not args.dry_run:
        save_local_model_catalog(mc, cat_dir, cat_file, args.backup)
