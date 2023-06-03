import sys
import json
import logging
import csv
from urllib import request
from pathlib import Path

log = logging.getLogger(__name__)


def full_prompt_for(seed_prompt, joke: str):
    return seed_prompt.replace("{{JOKE}}", joke).replace(" {{INSTRUCTION}}", "")


def main():
    try:
        seed_prompt_path = Path(sys.argv[1])
        dril_tweets_path = Path(sys.argv[2])
        text_generation_webui_address = sys.argv[3]
    except IndexError:
        log.error(
            "usage: %s <seed_prompt_path> <dril_tweets_path> <text_generation_webui_address>",
            sys.argv[0],
        )
        return 1

    text_generation_webui_address = text_generation_webui_address.rstrip("/")

    with seed_prompt_path.open() as fd:
        seed_prompt = fd.read()

    api_address = f"{text_generation_webui_address}/api/v1/generate"
    with dril_tweets_path.open() as fd:
        for tweet in fd:
            full_prompt = full_prompt_for(seed_prompt, tweet)
            log.debug("full prompt: %r", full_prompt)
            request_json = json.dumps({"prompt": full_prompt}).encode()
            req = request.Request(api_address, data=request_json)
            response = request.urlopen(req)
            log.debug("resp: %r", response)
            data = response.read()
            log.debug("data: %r", data)
            return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
