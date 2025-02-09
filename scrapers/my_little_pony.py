"""
Web-scrapes the MLP wikia for transcript data of all the main episodes.
- get_episodeindex: Compiles an ordered list of episodes to scrape.
- get_episodetranscript: Compiles the transcript for a given episode.
"""

import logging

import requests
from bs4 import BeautifulSoup

def get_index() -> dict:
    """
    Compiles a list of MLP episodes by season.
    Returns: {season_num: [(episode_name, episode_url)]}
    """
    # Returns {season_num: [episodes]}
    episodeindex_path = "https://mlp.fandom.com/wiki/List_of_episodes"
    response = requests.get(episodeindex_path)
    episode_table = BeautifulSoup(response.text, 'html.parser').find('table').find_next('table')
    episode_index = {}
    for rowno, row in enumerate(episode_table.find('tbody').find_all('tr')):
        if not rowno:
            continue
        cell_list = list(row.find_all('td'))
        episode_name = cell_list[-1].find('a').attrs['title']
        episode_url = cell_list[-1].find('a').attrs['href']
        try:
            season_num = int(cell_list[0].text)
        except ValueError:
            logging.info("MLP: Best Gift Ever is being added to Season 8.")
            season_num = 8
        if season_num not in episode_index:
            episode_index[season_num] = []
        episode_index[season_num].append((episode_name, episode_url))
    logging.info("%d rows have been scraped from %r", rowno, episodeindex_path)
    return episode_index

def get_transcript(episodeurl: str) -> str:
    """
    Compiles the transcript, line-by-line, from the URL corresponding to `episodeurl`.
    Returns: newline.join(transcript_lines)
    """
    root = "https://mlp.fandom.com/wiki/Transcripts/"
    tail = episodeurl.split('/')[-1]
    transcript_url = root + tail
    response = requests.get(transcript_url)
    line_list = []
    transcript = BeautifulSoup(response.text, 'html.parser')
    for lineno, line in enumerate(transcript.find_all('dd'), start=1):
        logging.debug("line: %r, type(line): %r", line, type(line))
        line_list.append(line.text.strip())
    logging.info("%d lines have been scraped from %r", lineno, transcript_url)
    return '\n'.join(line_list)
