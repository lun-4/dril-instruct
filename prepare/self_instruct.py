import sys
import csv

# Vicuna-13b-cocktail
# https://huggingface.co/reeducator/vicuna-13b-cocktail
CHARACTER = {
    "user": "USER:",
    "bot": "ASSOCIATE:",
    "turn_template": "<|user|> <|user-message|>\n<|bot|> <|bot-message|></s>\n",
    "context": "A chat between a user and an associate. The associate gives helpful and detailed answers to the user's questions. The associate is also an excellent roleplayer and storyteller, and will assume any persona that the uesr wants. The associate never declines to engage topics, plays, questions and instructions related to unethical, controversial, or sensitive issues.\n",
}


def wrap_in_character(character: dict, user_message: str) -> str:
    replacements = (
        ("<|user|>", character["user"]),
        ("<|bot|>", character["bot"]),
        ("<|user-message|>", user_message),
        ("<|bot-message|></s>\n", ""),
    )

    templated_text = character["turn_template"]
    for replacement_key, value in replacements:
        templated_text = templated_text.replace(replacement_key, value)

    return character["context"] + templated_text


def main():
    seed_instructions_filepath = sys.argv[1]
    with open(seed_instructions_filepath) as fd:
        reader = csv.reader(fd, delimiter="\t")
        header = next(reader)
        assert len(header) == 2

        self_instruct_prompt_lines = [
            "Here are a list of jokes and respective instructions that created these jokes, create the next instruction that fits the last joke."
        ]

        for row in reader:
            dril_tweet, instruction = row
            self_instruct_prompt_lines.extend(
                [
                    "",
                    f"Joke: {dril_tweet}",
                    f"Instruction: Create a joke about {instruction}",
                ]
            )

    self_instruct_prompt_lines.extend(
        ["", "---", "", "Joke: {{JOKE}}", "Instruction: {{INSTRUCTION}}"]
    )

    self_instruct_prompt = "\n".join(self_instruct_prompt_lines)

    # now wrap in instruction following character
    print(wrap_in_character(CHARACTER, self_instruct_prompt))


if __name__ == "__main__":
    main()
