import sys
import json
import logging
import csv
from urllib import request
from pathlib import Path

log = logging.getLogger(__name__)


def full_prompt_for(seed_prompt, joke: str):
    return seed_prompt.replace("{{JOKE}}", joke).replace(" {{INSTRUCTION}}", "")


def process_tweet(api_address, seed_prompt, tweet: dict):
    assert tweet["_type"] == "snscrape.modules.twitter.Tweet"
    log.debug("processing %r", tweet["url"])

    full_prompt = full_prompt_for(seed_prompt, tweet["renderedContent"])
    log.debug("full prompt: %r", full_prompt)
    request_json = json.dumps(
        {
            # llama-precise.txt
            "top_p": 0.1,
            "top_k": 40,
            "temperature": 0.7,
            "repetition_penalty": 1.18,
            "typical_p": 1.0,
            "prompt": full_prompt,
        }
    ).encode()
    req = request.Request(api_address, data=request_json)
    response = request.urlopen(req)
    log.debug("resp: %r", response)
    data = response.read()
    log.debug("data: %r", data)


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
        for jsonl_data in fd:
            print(jsonl_data)
            tweet = json.loads(jsonl_data)
            process_tweet(api_address, seed_prompt, tweet)
            return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
