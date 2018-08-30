# conference-etl
Tools to extract data from Conference websites. Initially author affiliation 
from accepted papers.

## Extract - Transform - Load (ETL)

For a given list of supplied conferences, and sublists of the sources that
list accepted papers (e.g. by year), these tools should:

 - Extract the submission meta data
    - Submission title
    - Author name(s)
    - Author email(s)
    - Submission type
        - Paper (Primary Goal)
        - Poster
        - Talk
        - Keynote
    - Date
 - Transform this data by:
    - putting it into a usable tabular intermediate representation
        - primary keys being conference name and date
    - mapping email addresses to:
        - Affiliated institution
        - Primary country associated with that institution
            - Or 'ambiguous'
            - Or 'unknown'
 - Load this data into a simple to access format
    - ideally something like a Google sheet

## Sources, scripts, and sinks - ETL Pipeline

The following should be mapped either directly to pipeline component files
or to methods within a library.

  - Sources
    - (Initial) - YAML file containing
        - conference names
        - conference years
            - starting URL for extracting accepted papers
    - (Later) - Google sheet containing the above
  - Scripts
    - parse_sources.py (lib) -> python dict
    - extract.py (script) -> local db representation
        - should warn if no scraper is implemented for a source
        - scrapers.py ->
            - (Library of per-conference-year scraping logic)
        - email_to_institution.py -> institution
        - institution_to_country.py -> country
    - load.py (script) -> human readable CSV
        - (Later) -> upload to Google sheets
    - conference-etl.py (script) -> human readable output
        - main wrapper
        - options
            - start from scratch
            - add only
            - (later) specify source by name-year
    - (Later) visualize.py -> charts from data
  


## Edge Cases

 - What about non-paper accepted submissions?
 - What if we want to add types of meta data to re-extract later?
 - What if the source url points to a pdf or other, non-website?
