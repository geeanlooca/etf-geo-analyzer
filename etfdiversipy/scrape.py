import argparse
import requests
import os
import asyncio
import tqdm.asyncio

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DATA_DICT = {
    "SWDA": "https://www.ishares.com/it/investitore-privato/it/prodotti/251882/ishares-msci-world-ucits-etf-acc-fund/1506575546154.ajax?fileType=csv&fileName=SWDA_holdings&dataType=fund",
    "EIMI": "https://www.ishares.com/it/investitore-privato/it/prodotti/264659/ishares-msci-emerging-markets-imi-ucits-etf/1506575546154.ajax?fileType=csv&fileName=EIMI_holdings&dataType=fund",
    "SP500": "https://www.ishares.com/it/investitore-privato/it/prodotti/253743/ishares-sp-500-b-ucits-etf-acc-fund/1506575546154.ajax?fileType=csv&fileName=CSSPX_holdings&dataType=fund",
    "STOXXEU600": "https://www.ishares.com/it/investitore-privato/it/prodotti/251931/ishares-stoxx-europe-600-ucits-etf-de-fund/1506575546154.ajax?fileType=csv&fileName=EXSA&dataType=fund",
}


def send_request(url: str, filename: str) -> None:
    """Send a request to the given url and save the response to the given filename."""

    logger.debug(f"Downloading {url} to {filename}")
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Failed to download {url}")

    with open(filename, "wb") as f:
        f.write(response.content)


async def send_async_request(url: str, filename: str) -> None:
    """Asynchronously send a request to the given url and save the response to the given filename."""
    return await asyncio.to_thread(send_request, url, filename)


async def batch_download_etfs(urls: list[str], filenames: list[str], data_dir: str):
    """Download a batch of ETFs in an async way."""
    # for each element in the dictionary, send a request in async way
    tasks = [
        send_async_request(url, os.path.join(data_dir, f"{filename}.csv"))
        for (filename, url) in zip(filenames, urls)
    ]

    _ = await tqdm.asyncio.tqdm.gather(*tasks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape ETF data")
    parser.add_argument("data_dir", help="Directory to save ETF data", type=str)

    args = parser.parse_args()
    data_path = args.data_dir

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    urls, filenames = DATA_DICT.values(), DATA_DICT.keys()
    asyncio.run(batch_download_etfs(urls, filenames, data_path))
