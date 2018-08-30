from . import scrapers

SCRAPER_MAP = {
    "foo": scrapers.Scraper,
    "source1": scrapers.ICRA2018,
    "ICML2018": scrapers.ICML2018,
    "ICRA2018": scrapers.ICRA2018
}


def validate_sources(sources: list) -> None:
    """
    Throws a warning if no scraper is specified for a source in the provided
    list.
    """
    for source in sources:
        name = source["name"]
        if SCRAPER_MAP.get(name) is None:
            warn_string = "No scraper specified for {}. This source will be skipped.".format(name)
            print("WARNING:", warn_string)


def source_to_scraper(source: dict) -> scrapers.Scraper:
    """
    Return the scraper for the provided source (a dictionary)
    """
    scraperClass = SCRAPER_MAP.get(source["name"])
    if scraperClass is not None:
        return scraperClass()