from etfdiversipy.etl import (
    ishares_geo_distribution,
    lyxor_stoxx_600_distribution,
    combined_geo,
)
from cli_utils import dir_path
import argparse
import os


def main() -> None:
    """Main function for the CLI."""
    parser = argparse.ArgumentParser(description="Diversify your ETF portfolio")
    parser.add_argument("data_dir", help="Directory containing ETF data", type=dir_path)

    args = parser.parse_args()
    data_path = args.data_dir

    swda = ishares_geo_distribution(os.path.join(data_path, "SWDA_holdings.csv"))
    eimi = ishares_geo_distribution(os.path.join(data_path, "EIMI_holdings.csv"))
    lyx = lyxor_stoxx_600_distribution()

    combined, weights = combined_geo((swda, 1), (lyx, 0), (eimi, 0.0))
    combined_opt, weights_opt = combined_geo((swda, 4), (lyx, 1.5), (eimi, 1.5))

    print(combined)
    print(weights)
    print(combined_opt)
    print(weights_opt)


if __name__ == "__main__":
    main()
