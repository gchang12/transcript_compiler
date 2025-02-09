# should accept from scraper module:
# - function to get episode index {season: [(episode_no, episode_name, episode_url)]
# - function to get episode transcript, given a URL
# - function to get name of folder to store transcripts in [optional]

import logging
from pathlib import Path

# NOTE: These should not be touched.
LOGPATH = Path("logs/")
OUTPATH = Path("transcripts/")

# TODO: Edit these as necessary; write scraper in 'scrapers/'
SEASONDIR_FMT = "S%d"
EPISODEFILE_FMT = "E%02d_%s.txt"
SCRAPER_NAME = "my_little_pony"
NUM_SEASONS = 9

# TODO: Replace with name of scraper module in 'scrapers/'.
from scrapers import my_little_pony
import scrapers
SCRAPER_MODULE = getattr(scrapers, SCRAPER_NAME)

def main():
    """
    Creates a filetree to store transcripts in, scrapes those transcripts, and saves them.
    """
    get_index = getattr(SCRAPER_MODULE, "get_index")
    get_transcript = getattr(SCRAPER_MODULE, "get_transcript")
    transcript_outdir = Path(OUTPATH, SCRAPER_NAME)
    transcript_outdir.mkdir(exist_ok=True)
    for season_num, episodeurl_list in get_index().items():
        season_path = transcript_outdir.joinpath(SEASONDIR_FMT % season_num)
        season_path.mkdir(exist_ok=True)
        logging.info("%s now exists. Loading episode transcript text files into here.", season_path)
        logging.info("Now scraping from Season %d.", season_num)
        for episode_num, (episodename, episodeurl) in enumerate(episodeurl_list, start=1):
            episodetranscript = get_transcript(episodeurl)
            episode_path = season_path.joinpath(EPISODEFILE_FMT % (episode_num, episodename))
            episode_path.write_text(episodetranscript)
            logging.debug("Transcript written to %s", episode_path)
        logging.info("Scraped a total of %d episodes from Season %d", episode_num, season_num)

logging.basicConfig(
    filename="%s/%s.log" % (LOGPATH, SCRAPER_NAME),
    format="%(levelname)s:%(module)s.%(funcName)s: %(message)s",
    level=logging.INFO,
)

if __name__ == '__main__':
    main()
