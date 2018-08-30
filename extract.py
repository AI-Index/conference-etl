from scrapers import source_to_scraper, validate_sources
import argparse
import pickle
from parsers.yamlparser import YamlParser


def main(sourcelist):
    print("Running extraction")

    if '.yaml' in sourcelist:
        parser = YamlParser()
        sources = parser.parse(sourcelist)
    else:
        raise Exception("Source list is of unrecognized type.")

    # Initial sanity check
    validate_sources(sources)

    # Extraction loop
    for source in sources:
        scraper = source_to_scraper(source)
        if scraper is not None:
            data = scraper.scrape(source)
            print(data)
            pickle_name = source["name"] + ".p"
            with open(pickle_name, 'wb') as fh:
                pickle.dump(data, fh)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract data from sources')
    parser.add_argument(
        '--sourcelist',
        default="sources/sources.yaml",
        help='The filename of sources from which to extract data'
    )
    args = parser.parse_args()
    main(args.sourcelist)
