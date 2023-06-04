import argparse
import sys
import logging
from pathlib import Path
from fastchat import conversation, register_conv_remplate

from transformers import LlamaForCausalLM, LlamaTokenizer
from peft import get_peft_config, get_peft_model, LoraConfig, TaskType


BASE_MODEL = "reeducator/vicuna-13b-cocktail"
log = logging.getLogger(__name__)


def fetch_args():
    parser = argparse.ArgumentParser(
        prog="dril-instruct-finetune", description="finetune on shit"
    )
    parser.add_argument("path_to_fastchat_json", type=Path)
    return parser.parse_args()


def main():
    args = fetch_args()
    log.info("fastchat path: %r", args.path_to_fastchat_json)
    dataset = load_dataset("json", data_files=args.path_to_fastchat_json)

    # tokenize it
    tokenizer = LlamaTokenizer.from_pretrained(BASE_MODEL)

    processed_datasets = dataset.map(
        preprocess_function,
        batched=True,
        num_proc=1,
        remove_columns=dataset["train"].column_names,
        load_from_cache_file=True,
        desc="Running tokenizer on dataset",
    )

    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=8,
        lora_alpha=32,
        lora_dropout=0.1,
    )
    model = LlamaForCausalLM.from_pretrained(BASE_MODEL)
    model = get_peft_model(model, peft_config)
    log.info("trainable params: %r", model.print_trainable_parameters())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
