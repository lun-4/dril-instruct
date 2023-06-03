# dril-instruct
[WIP] can large language models create good shitposts?

> the idea: take dril tweets, ask Vicuna-13b to generate a prompt that would spit out a dril tweet,
> do this for all dril tweets. you now have a dataset of instruction2dril.
> finetune a Vicuna model on top of that data, and you can now have a shitpost generator

![drilinstruct](./files/drilinstruct.png)

