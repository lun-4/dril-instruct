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
    dril_tweet = tweet["renderedContent"]
    full_prompt = full_prompt_for(seed_prompt, dril_tweet)
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
    data_bytes = response.read()
    log.debug("data: %r", data_bytes)
    data = json.loads(data_bytes.decode())
    output = data["results"][0]["text"]
    log.debug("output: %r", output)
    return dril_tweet, output


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
    processed_count = 0
    with dril_tweets_path.open() as fd:
        lines = fd.readlines()

        for jsonl_data in lines:
            tweet = json.loads(jsonl_data)
            dril_tweet, extrapolated_instruction = process_tweet(
                api_address, seed_prompt, tweet
            )
            processed_count += 1

            log.info("processed %d/%d", processed_count, len(lines))

            instruction_data = {
                "_type": "pm.l4.dril_instruct.extrapolated_instruction",
                "input": dril_tweet,
                "instruction": extrapolated_instruction,
            }

            print(json.dumps(instruction_data))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
