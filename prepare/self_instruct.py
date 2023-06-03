import sys
import csv


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

    self_instruct_prompt_lines.extend(["", "---", "", "Joke:", "Instruction:"])

    self_instruct_prompt = "\n".join(self_instruct_prompt_lines)
    print(self_instruct_prompt)


if __name__ == "__main__":
    main()
