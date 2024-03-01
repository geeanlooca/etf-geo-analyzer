import argparse
from requests_html import HTMLSession

URL = "https://www.ishares.com/it/investitore-privato/it/prodotti/etf-investments?switchLocale=y&siteEntryPassthrough=true#/?pageNumber=1&sortColumn=totalFundSizeInMillions&sortDirection=desc&productView=etf&dataView=keyFacts"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape iShares ETF list")
    parser.add_argument(
        "output", help="Output file", type=str, default="ishares_etf_list.html"
    )
    args = parser.parse_args()

    try:
        session = HTMLSession()
        r = session.get(URL)
        r.html.render()

        with open(args.output, "w") as f:
            f.write(r.html.html)
    except Exception as e:
        print(f"Failed to scrape iShares ETF list: {e}")
