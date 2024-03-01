from argparse import ArgumentParser
from bs4 import BeautifulSoup
import polars as pl
from typing import Tuple, List


BASE_URL = "https://www.ishares.com"


def create_dataframe(entries: List[Tuple[str, str, str]]) -> pl.DataFrame:
    """Create a polars DataFrame from a list of ETF information."""
    schema = {"ticker": pl.String, "name": pl.String, "url": pl.String}
    return pl.DataFrame(data=entries, schema=schema)


def extract_entries_from_html(soup: BeautifulSoup) -> List[Tuple[str, str, str]]:
    rows = soup.body.table.find_all("tr")

    entries = []

    for row in rows:
        try:
            cells = row.find_all("td")
            first, second = cells[0], cells[1]
        except IndexError:
            continue

        ticker = first.text
        url = BASE_URL + first.a["href"]
        name = second.text
        entries.append((ticker, name, url))

    return entries


if __name__ == "__main__":
    parser = ArgumentParser(description="Parse scraped list of iShares ETFs")
    parser.add_argument("html_file", help="HTML file to parse", type=str)
    parser.add_argument("-o", "--output", help="Output file", type=str, default=None)

    args = parser.parse_args()

    with open(args.html_file, "r") as f:
        soup = BeautifulSoup(f, "html.parser")
        try:
            entries = extract_entries_from_html(soup)
            df = create_dataframe(entries)
            print(df)
            print(f"Total entries: {len(entries)}")

            if args.output:
                df.write_csv(args.output)
        except Exception as e:
            print(f"Failed to parse HTML: {e}")
