import sys
import json
import logging
import csv
from urllib import request
from pathlib import Path

log = logging.getLogger(__name__)


def main():
    try:
        extrapolated_path = Path(sys.argv[1])
    except IndexError:
        log.error("usage: %s <extrapolated_path>", sys.argv[0])
        return 1

    fastchat_data = []

    with extrapolated_path.open() as fd:
        lines = fd.readlines()
        for index, jsonl_data in enumerate(lines):
            instruction = json.loads(jsonl_data)
            assert (
                instruction["_type"] == "pm.l4.dril_instruct.extrapolated_instruction"
            )
            fastchat_data.append(
                {
                    "id": f"dril_{index}",
                    "conversations": [
                        {"from": "human", "value": instruction["instruction"]},
                        {"from": "gpt", "value": instruction["input"]},
                    ],
                }
            )

        print(json.dumps(fastchat_data))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
