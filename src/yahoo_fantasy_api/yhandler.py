#!/bin/python

import datetime

YAHOO_ENDPOINT = "https://fantasysports.yahooapis.com/fantasy/v2"


class YHandler:
    """Class that constructs the APIs to send to Yahoo"""

    def __init__(self, sc):
        self.sc = sc

    def get(self, uri):
        """Send an API request to the URI and return the response as JSON

        :param uri: URI of the API to call
        :type uri: str
        :return: JSON document of the response
        :raises: RuntimeError if any response comes back with an error
        """
        response = self.sc.session.get(
            f"{YAHOO_ENDPOINT}/{uri}", params={"format": "json"}
        )
        if response.status_code != 200:
            raise RuntimeError(response.content)
        jresp = response.json()
        return jresp

    def put(self, uri, data):
        """Calls the PUT method to the uri with a payload

        :param uri: URI of the API to call
        :type uri: str
        :param data: What to pass as the payload
        :type data: str
        :return: XML document of the response
        :raises: RuntimeError if any response comes back with an error
        """
        headers = {"Content-Type": "application/xml"}
        response = self.sc.session.put(
            f"{YAHOO_ENDPOINT}/{uri}", data=data, headers=headers
        )
        if response.status_code != 200:
            raise RuntimeError(response.content)
        return response

    def post(self, uri, data):
        """Calls the POST method to the URI with a payload

        :param uri: URI of the API to call
        :type uri: str
        :param data: What to pass as the payload
        :type data: str
        :return: XML document of the response
        :raises: RuntimeError if any response comes back with an error
        """
        headers = {"Content-Type": "application/xml"}
        response = self.sc.session.post(
            f"{YAHOO_ENDPOINT}/{uri}", data=data, headers=headers
        )
        if response.status_code != 201:
            raise RuntimeError(response.content)
        return response

    def get_teams_raw(self):
        """Return the raw JSON when requesting the logged in players teams.

        :return: JSON document of the request.
        """
        return self.get("users;use_login=1/games/teams")

    def get_leagues_raw(
        self, is_available=False, game_types=None, game_codes=None, seasons=None
    ):
        """Return the raw JSON when requesting the logged in players leagues.

        :param is_available: Filter the leagues to only those that are Available
        :type is_available: bool
        :param game_types: Filter the leagues to only those that are of the given types
        :type game_types: list[str]
        :param game_codes: Filter the leagues to only those that are of the given game codes
        :type game_codes: list[str]
        :param season: Filter the leagues to only those that are of the given season
        :type seasons: list[str]
        :return: JSON document of the request.
        """
        is_available = 1 if is_available else 0
        game_types = ",".join(game_types) if game_types is not None else ""
        game_codes = ",".join(game_codes) if game_codes is not None else ""
        seasons = ",".join(seasons) if seasons is not None else ""
        return self.get(
            f"users/games/leagues?use_login=1&is_available={is_available}&game_types={game_types}&game_codes={game_codes}&seasons={seasons}"
        )

    def get_teams_by_keys_raw(self, team_keys):
        """Return the raw JSON when requesting details of a team.

        :param team_keys: List of team keys to fetch the details For
        :type team_keys: list[str]
        :return: JSON document of the request.
        """
        return self.get("teams;team_keys={}".format(",".join(team_keys)))

    def get_standings_raw(self, league_id):
        """Return the raw JSON when requesting standings for a league.

        :param league_id: League ID to get the standings for
        :type league_id: str
        :return: JSON document of the request.
        """
        return self.get(f"league/{league_id}/standings")

    def get_settings_raw(self, league_id):
        """Return the raw JSON when requesting settings for a league.

        :param league_id: League ID to get the standings for
        :type league_id: str
        :return: JSON document of the request.
        """
        return self.get(f"league/{league_id}/settings")

    def get_matchup_raw(self, team_key, week):
        """Return the raw JSON when requesting match-ups for a team

        :param team_key: Team key identifier to find the matchups for
        :type team_key: str
        :param week: What week number to request the matchup for?
        :type week: int
        :return: JSON of the request
        """
        return self.get(f"team/{team_key}/matchups;weeks={week}")

    def get_roster_raw(self, team_key, week=None, day=None):
        """Return the raw JSON when requesting a team's roster

        Can request a roster for a given week or a given day.  If neither is
        given the current day's roster is returned.

        :param team_key: Team key identifier to find the matchups for
        :type team_key: str
        :param week: What week number to request the roster for?
        :type week: int
        :param day: What day number to request the roster
        :type day: datetime.date
        :return: JSON of the request
        """
        if week is not None:
            param = f";week={week}"
        elif day is not None:
            param = ";date={}".format(day.strftime("%Y-%m-%d"))
        else:
            param = ""
        return self.get(f"team/{team_key}/roster{param}")

    def get_scoreboard_raw(self, league_id, week=None):
        """Return the raw JSON when requesting the scoreboard for a week

        :param league_id: League ID to get the standings for
        :type league_id: str
        :param week: The week number to request the scoreboard for
        :type week: int
        :return: JSON document of the request.
        """
        week_uri = ""
        if week is not None:
            week_uri = f";week={week}"
        return self.get(f"league/{league_id}/scoreboard{week_uri}")

    def get_players_raw(self, league_id, start, status, position=None):
        """Return the raw JSON when requesting players in the league

        The result is limited to 25 players.

        :param league_id: League ID to get the players for
        :type league_id: str
        :param start: The output is paged at 25 players each time.  Use this
        parameter for subsequent calls to get the players at the next page.
        For example, you specify 0 for the first call, 25 for the second call,
        etc.
        :type start: int
        :param status: A filter to limit the player status.  Available values
        are: 'A' - all available; 'FA' - free agents; 'W' - waivers, 'T' -
        taken players, 'K' - keepers
        :type status: str
        :param position: A filter to return players only for a specific
        position.  If None is passed, then no position filtering occurs.
        :type position: str
        :return: JSON document of the request.
        """
        if position is None:
            pos_parm = ""
        else:
            pos_parm = f";position={position}"
        return self.get(
            f"league/{league_id}/players;start={start};count=25;status={status}{pos_parm}/percent_owned"
        )

    def get_player_raw(self, league_id, search=None, ids=None):
        """Return the raw JSON when requesting player details

        :param league_id: League ID to get the player for
        :type league_id: str
        :param search: Search string to apply.  This can be a full or partial
            name of a player.  Cannot be used with ids.
        :type search: str
        :param ids: Set of player IDs to lookup.  Cannot be used with search.
        :type ids: list
        :return: JSON document of the request.
        """
        if search is not None:
            assert ids is None
            players_uri = f"search={search}"
        elif ids is not None and len(ids) > 0:
            assert search is None
            # Construct a player key by prefixing the start of the league ID
            lg_pref = league_id[0 : league_id.find(".")]
            players_uri = "player_keys=" + ",".join(
                f"{lg_pref}.p.{i}" for i in ids
            )
        else:
            raise RuntimeError("Must use search or ids options to filter players.")
        return self.get(f"league/{league_id}/players;{players_uri}/stats")

    def get_percent_owned_raw(self, league_id, player_ids):
        """Return the raw JSON when requesting the percentage owned of players

        :param league_id: League ID we are requesting data from
        :type league_id: str
        :param player_ids: Yahoo! Player IDs to retrieve % owned for
        :type player_ids: list(str)
        :return: JSON document of the request
        """
        lg_pref = league_id[0 : league_id.find(".")]
        joined_ids = ",".join([lg_pref + ".p." + str(i) for i in player_ids])
        return self.get(
            f"league/{league_id}/players;player_keys={joined_ids}/percent_owned"
        )

    def get_player_ownership_raw(self, league_id, player_ids):
        """Return the raw JSON when requesting the ownership of players

        :param league_id: League ID we are requesting data from
        :type league_id: str
        :param player_ids: Yahoo! Player IDs to retrieve % owned for
        :type player_ids: list(int)
        :return: JSON document of the request
        """
        lg_pref = league_id[0 : league_id.find(".")]
        joined_ids = ",".join([lg_pref + ".p." + str(i) for i in player_ids])
        return self.get(
            f"league/{league_id}/players;player_keys={joined_ids}/ownership"
        )

    def put_roster(self, team_key, xml):
        """Calls PUT against the roster API passing it an xml document

        :param team_key: The key of the team the roster move applies too
        :type team_key: str
        :param xml: The XML document to send
        :type xml: str
        :return: Response from the PUT
        """
        return self.put(f"team/{team_key}/roster", xml)

    def post_transactions(self, league_id, xml):
        """Calls POST against the transaction API passing it an xml document

        :param league_id: The league ID that the API request applies to
        :type league_id: str
        :param xml: The XML document to send as the payload
        :type xml: str
        :return: Response from the POST
        """
        return self.post(f"league/{league_id}/transactions", xml)

    def get_team_transactions(self, league_id, team_key, tran_type):
        """
        Calls GET to retrieve transactions for a team of a given type.

        :param league_id: The league ID that the API request applies to
        :type league_id: str
        :param team_key: The key of the team the roster move applies too
        :type team_key: str
        :param tran_type: The type of transaction retrieve.  Valid values
        are: waiver or pending_trade
        :return: Response from the GET
        """
        return self.get(
            f"league/{league_id}/transactions;team_key={team_key};type={tran_type}"
        )

    def get_transactions_raw(self, league_id, tran_types, count):
        """
        Calls GET to retrieve transactions of a given type.

        :param league_id: The league ID that the API request applies to
        :type league_id: str
        :param tran_types: The comman seperated types of transactions retrieve.  Valid values
        are: add,drop,commish,trade
        :type tran_types str
        :param count: The number of transactions to retrieve. Leave blank to return all
        transactions
        :type count str
        :return: Response from the GET
        """
        return self.get(
            f"league/{league_id}/transactions;types={tran_types};count={count}"
        )

    def put_transaction(self, transaction_key, xml):
        """
        PUT to the transaction API

        This can be used to accept/reject trades, voting for/against a trade,
        and editing a waiver claim.

        :param xml: The XML document to send
        :type xml: str
        :return: Response from the PUT
        """
        return self.put("transaction/" + str(transaction_key), xml)

    def get_player_stats_raw(self, league_id, player_ids, req_type, date, week, season):
        """
        GET stats for a list of player IDs

        :param league_id: The league id the players belong too.
        :type game_code: str
        :param player_ids: Yahoo! player IDs we are requesting stats for
        :type player_ids: list(int)
        :param req_type: The request type.  This defines the range of dates to
            return the stats for.
        :param date: When req_type == 'date', this is the date we want the
            stats for.  If None, we'll get the stats for the current date.
        :type date: datetime.date
        :param week: NFL ONLY: When req_type == 'week', this is the week we want
            the stats for.  If None, we'll get the stats for the current week
        :type season: int
        :param season: When req_type == 'season', this is the season we want
            the stats for.  If None, we'll get the stats for the current season
        :type season: int
        :return: Response from the GET call
        """
        uri = self._build_player_stats_uri(
            league_id, player_ids, req_type, date, week, season
        )
        return self.get(uri)

    def get_draftresults_raw(self, league_id):
        """
        GET draft results for the league

        :param league_id: The league ID that the API request applies to
        :type league_id: str
        :return: Response from the GET call
        """
        return self.get(f"league/{league_id}/draftresults")

    def _build_player_stats_uri(
        self, league_id, player_ids, req_type, date, week, season
    ):
        uri = f"league/{league_id}/players;player_keys="
        game_code = league_id[:3]
        if isinstance(player_ids, list):
            for i, p in enumerate(player_ids):
                if i != 0:
                    uri += ","
                uri += f"{game_code}.p.{p}"
        uri += f"/stats;{self._get_stats_type(req_type, date, week, season)}"
        return uri

    def _get_stats_type(self, req_type, date, week, season):
        if req_type == "season":
            if season is None:
                return "type=season"
            else:
                return f"type=season;season={season}"
        elif req_type == "week":
            if week is None:
                return "type=week"
            else:
                return f"type=week;week={week}"
        elif req_type == "average_season":
            if season is None:
                return "type=average_season"
            else:
                return f"type=average_season;season={season}"
        elif req_type == "date":
            if date is None:
                date = datetime.date.today()
            if isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
                return "type=date;date={}".format(date.strftime("%Y-%m-%d"))
            else:
                return f"type=date;date={date}"
        elif req_type in ["lastweek", "lastmonth"]:
            return f"type={req_type}"
        else:
            assert False, f"Unknown req_type type: {req_type}"

    def get_game_raw(self, game_code):
        """Return the raw JSON when requesting details of a game.

        :param game_code: Game code to get the standings for. (nfl,mlb,nba, nhl)
        :type game_code: str
        :return: JSON document of the request.
        """
        return self.get(f"game/{game_code}")

    def get_league_teams_raw(self, league_id):
        """Return the raw JSON when requesting the teams in a league

        :param league_id: League ID to get the teams for
        :type league_id: str
        :return: JSON document of the request.
        """
        return self.get(f"league/{league_id}/teams")
