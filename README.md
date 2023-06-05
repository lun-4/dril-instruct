# dril-instruct
[WIP] can large language models create good shitposts?

> the idea: take dril tweets, ask Vicuna-13b to generate a prompt that would spit out a dril tweet,
> do this for all dril tweets. you now have a dataset of instruction2dril.
> finetune a Vicuna model on top of that data, and you can now have a shitpost generator

![drilinstruct](./files/drilinstruct.png)


# how

project state: LoRA was made. results incoming

- create a "seed prompt", take some dril tweets and create their respective instructions manually
  - a TSV file is left in `files/` to create the main seed prompt
- from the seed prompt, "extrapolate" instructions to all dril tweets using an existing instruction model
- we now have a dataset of instruction-to-dril-tweet
- finetune on that, and you get a shitposter (that's the idea)

```
git clone ...
cd ...
python3 ./prepare/self_instruct.py "./files/Dril Instruct many-shot samples - data.tsv" > tmp/prompt.txt

# dril data!
snscrape -vv --progress --jsonl twitter-user dril > tmp/dril.jsonl

# you need text-generation-webui with an instruct model loaded in it
python3 ./prepare/extrapolate_instructions.py "tmp/prompt.txt" "tmp/dril.jsonl" "http://127.0.0.1:5000" > tmp/instructiosn.jsonl

# tmp/instructions.jsonl now has a bunch of data that you can finetune with!

# in this example, we'll export to the FastChat format, to finetune a Vicuna model
python3 ./prepare/convert_to_fastchat.py ./tmp/instructions.jsonl > tmp/fastchat.json

cd ..
git clone https://github.com/git-cloner/llama-lora-fine-tuning
cd ..
# then follow their instructions to get a lora file in its output/
# my finetune of Vicuna-13b-cocktail was done in INT8 mode, deepspeed zero, and an A100 80GB VRAM
# (total spent was less than 10USD on RunPod)
```
