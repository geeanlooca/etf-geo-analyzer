import polars as pl
import asyncio
import argparse
import os
from more_itertools import chunked
from etfdiversipy.scrape import batch_download_etfs
from tqdm import tqdm
import time
from pprint import pprint


def read_csv(path: str) -> pl.DataFrame:
    """Read a CSV file into a polars DataFrame."""
    print(f"Reading {path}")
    return pl.read_csv(
        path,
        schema={"ticker": pl.String, "name": pl.String, "url": pl.String},
        truncate_ragged_lines=True,
        has_header=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download all iShares ETFs")
    parser.add_argument("input", help="Input file", type=str)
    parser.add_argument("data_dir", help="Directory containing ETF data", type=str)
    args = parser.parse_args()
    data_path = args.data_dir

    if os.path.exists(data_path) and not os.path.isdir(data_path):
        print(f"{data_path} is not a directory")

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    df = read_csv(args.input)

    print(df)

    # extract the urls and filenames from the dataframe
    urls = df["url"].to_list()
    etf_names = df["ticker"].to_list()
    urls = [
        url + f"/1506575546154.ajax?fileType=csv&dataType=fund&fileName={etf_name}"
        for (url, etf_name) in zip(urls, etf_names)
    ]

    for url, filename in zip(urls, etf_names):
        print(f"Downloading {url} to {filename}.csv")

    for batch in tqdm(chunked(zip(urls, etf_names), 3)):
        url_batch, etf_name_batch = zip(*batch)
        pprint(etf_name_batch)
        asyncio.run(batch_download_etfs(url_batch, etf_name_batch, data_path))
        time.sleep(3)

    # urls, filenames = DATA_DICT.values(), DATA_DICT.keys()

    # print(data_path)
