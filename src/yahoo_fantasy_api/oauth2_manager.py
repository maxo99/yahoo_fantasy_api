import os
from pathlib import Path

from yahoo_oauth import OAuth2

from yahoo_fantasy_api import oauth2_logger


def get_oauth2():
    oauth2_logger.cleanup()
    return OAuth2(None, None, from_file=_default_oauth_path())


def _default_oauth_path(app_name: str | None = None) -> Path:
    env = os.getenv("YAHOO_OAUTH_FILE")
    if env:
        return Path(env).expanduser()

    # 2) user-scoped location
    if app_name is None:
        home_path = Path.home() / ".yahoo" / "oauth2.json"
    else:
        home_path = Path.home() / ".yahoo" / app_name / "oauth2.json"
    if home_path.exists():
        return home_path

    # 3) repo-root fallback: current working dir oauth2.json
    cwd_candidate = Path.cwd() / "oauth2.json"
    if cwd_candidate.exists():
        return cwd_candidate

    # attempt to find a git repo root as another fallback
    try:
        p = Path.cwd().resolve()
        for parent in [p] + list(p.parents):
            if (parent / ".git").exists():
                git_candidate = parent / "oauth2.json"
                if git_candidate.exists():
                    return git_candidate
                break
    except Exception:
        # ignore resolution errors and continue to fallback
        pass

    return Path(__file__).parent.parent.parent / "oauth2.json"
