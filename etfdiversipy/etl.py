import polars as pl


def get_unique_country_names(ishares_df: pl.DataFrame) -> list[str]:
    countries = ishares_df["Area Geografica"].unique().to_list()
    return countries


europa = [
    "Austria",
    "Grecia",
    "Polonia",
    "Svizzera",
    "Ungheria",
    "Repubblica Ceca",
    "Francia",
    "Norvegia",
    "Danimarca",
    "Svezia",
    "Svizzera",
    "Finlandia",
    "Belgio",
    "Italia",
    "Unione Europea",
    "Paesi Bassi",
    "Portogallo",
    "Germania",
    "Spagna",
    "Irlanda",
    "Regno Unito",
    "Regno unito",
]

NA = ["Canada", "Stati Uniti"]
SA = ["Cile", "Colombia", "Brasile", "Messico", "Peru"]
other = [
    "Australia",
    "Nuova Zelanda",
    "-",
    "Turchia",
    "Sud Africa",
    "Russia",
    "None",
    "Egitto",
]
asia = [
    "Cina",
    "Singapore",
    "Hong Kong",
    "Giappone",
    "Irlanda",
    "Taiwan",
    "Indonesia",
    "Tailandia",
    "India",
    "Malesia",
    "Filippine",
    "Pakistan",
    "Corea",
]
medio_oriente = ["Israele", "Arabia Saudita", "Emirati Arabi Uniti", "Kuwait", "Qatar"]

areas_list = {
    "Europe": europa,
    "North America": NA,
    "Asia": asia,
    "Other": other,
    "South America": SA,
    "Middle East": medio_oriente,
}
country_to_area = {}

for area_name, countries in areas_list.items():
    country_to_area.update({country.lower(): area_name for country in countries})


def get_area(country: str) -> str:
    return country_to_area.get(country.lower(), "Other")


def ishares_geo_distribution(filename: str) -> pl.DataFrame:
    df = pl.read_csv(filename, skip_rows=2, has_header=True)

    numeric_cols = ["Ponderazione (%)", "Valore nozionale", "Prezzo", "Nominale"]

    def fix_decimals(x: str) -> str:
        x = x.replace(".", "")
        x = x.replace(",", ".")
        return x

    df = df.filter(~pl.all_horizontal(pl.col("Ponderazione (%)").is_null()))

    df = df.with_columns(
        *[
            pl.col(col_name).map_elements(fix_decimals).cast(pl.Float32)
            for col_name in numeric_cols
        ]
    )

    df = df.with_columns(pl.col("Area Geografica").map_elements(get_area))
    df.head()

    geo_dist = df.group_by(pl.col("Area Geografica")).agg(
        pl.col("Ponderazione (%)").sum()
    )
    geo_dist = geo_dist.rename(
        {"Area Geografica": "Area", "Ponderazione (%)": "Percentage"}
    )
    return geo_dist.sort(by="Area")


def lyxor_stoxx_600_distribution() -> pl.DataFrame:
    """From pdf"""
    df = pl.DataFrame(
        {
            "Area": [
                "Regno unito",
                "Francia",
                "Svizzera",
                "Germania",
                "Paesi bassi",
                "Danimarca",
                "Svezia",
                "Italia",
                "Spagna",
                "Finlandia",
                "Belgio",
                "Norvegia",
                "None",
            ],
            "Percentage": [
                23.14,
                18.12,
                14.55,
                12.51,
                7.11,
                5.14,
                4.85,
                4.39,
                3.93,
                1.78,
                1.46,
                1.08,
                1.94,
            ],
        }
    )
    df = df.with_columns(
        pl.col("Area").map_elements(get_area), pl.col("Percentage").cast(pl.Float32)
    )
    geo_dist = df.group_by(pl.col("Area")).agg(pl.col("Percentage").sum())
    return geo_dist.sort(by="Area")


def normalize(*weights):
    s = 0
    for w in weights:
        s += w
    return [w / s for w in weights]


def scale_etf(etf: pl.DataFrame, weight: float) -> pl.DataFrame:
    etf = etf.with_columns(pl.col("Percentage") * weight)
    return etf


def combined_geo(*etf_weights_tuples) -> tuple[pl.DataFrame, list[float]]:
    etfs = [etf for etf, _ in etf_weights_tuples]
    weights = [w for _, w in etf_weights_tuples]
    weights = normalize(*weights)

    print(weights)
    normalized_etfs = []
    for etf, weight in zip(etfs, weights):
        normalized_etfs.append(scale_etf(etf, weight))

    return pl.concat(normalized_etfs, how="diagonal").group_by(
        "Area", maintain_order=True
    ).sum().sort(by="Percentage", descending=True), weights
