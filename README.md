# dril-instruct
[WIP] can large language models create good shitposts?

> the idea: take dril tweets, ask Vicuna-13b to generate a prompt that would spit out a dril tweet,
> do this for all dril tweets. you now have a dataset of instruction2dril.
> finetune a Vicuna model on top of that data, and you can now have a shitpost generator

![drilinstruct](./files/drilinstruct.png)


# how

project state: proof of concept for data preparation, no finetunes made yet

```
git clone ...
cd ...
python3 ./prepare/self_instruct.py "./files/Dril Instruct many-shot samples - data.tsv" > tmp/prompt.txt

# get dril tweets
# TODO: create process for that

# you need text-generation-webui with an instruct model in it
python3 ./prepare/extrapolate_instructions.py "tmp/prompt.txt" "dril.jsonl" "http://127.0.0.1:5000"
```
