from pathlib import Path

from yahoo_oauth import OAuth2

from yahoo_fantasy_api import oauth2_logger

oauth_file = Path(__file__).parent.parent.parent / "oauth2.json"


def get_oauth2():
    oauth2_logger.cleanup()
    return OAuth2(None, None, from_file=oauth_file)
