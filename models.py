from mongoengine import (StringField, IntField, FloatField, ListField, EmbeddedDocumentField,
	EmbeddedDocument, Document)

class GoalReport(EmbeddedDocument):

	total_attempts = ListField(IntField())
	open_play = ListField(IntField())
	set_piece = ListField(IntField())
	counter_attack = ListField(IntField())
	penalty = ListField(IntField())
	own_goal = ListField(IntField())

class AggressionReport(EmbeddedDocument):

	total_card_reasons = ListField(IntField())
	fouls = ListField(IntField())
	unprofessional = ListField(IntField())
	dive = ListField(IntField())
	other = ListField(IntField())

class PassReport(EmbeddedDocument):

	total_passes = ListField(IntField())
	crosses = ListField(IntField())
	through_balls = ListField(IntField())
	long_balls = ListField(IntField())
	short_passes = ListField(IntField())

class MatchStats(EmbeddedDocument):

	shots = ListField(IntField())
	shots_on_target = ListField(IntField())
	pass_success = ListField(FloatField())
	aerial_duel_success = ListField(FloatField())
	dribbles_won = ListField(IntField())
	tackles = ListField(IntField())
	possession = ListField(FloatField())

class MatchReport(Document):

	team1_name = StringField()
	team2_name = StringField()
	season = StringField()
	#match_url = StringField()
	goal_report = EmbeddedDocumentField(GoalReport)
	pass_report = EmbeddedDocumentField(PassReport)
	aggression_report = EmbeddedDocumentField(AggressionReport)
	stats = EmbeddedDocumentField(MatchStats)



class MatchLink(Document):

	match_name = StringField()
	match_url = StringField()

class StandingTable(Document):

	team_name = StringField()
	team_url = StringField()
	season = StringField()
	plays = IntField()
	wins = IntField()
	draws = IntField()
	losses = IntField()
	goal_for = IntField()
	goal_against = IntField()
	goal_difference = IntField()
	points = IntField()


class PlayerSummary(EmbeddedDocument):

	player_name = StringField()
	player_url = StringField()
	height_in_cm = IntField()
	weight_in_kg = IntField()
	apps = StringField()
	mins_played = IntField()
	goals = IntField()
	assists = IntField()
	yellow_cards = IntField()
	red_cards = IntField()
	shots_per_game = FloatField()
	success_passes = FloatField()
	aerial_won_per_game = FloatField()
	man_of_the_match = IntField()
	rating = FloatField()

class PlayerDefensive(EmbeddedDocument):

	player_name = StringField()
	player_url = StringField()
	height_in_cm = IntField()
	weight_in_kg = IntField()
	apps = StringField()
	mins_played = IntField()
	tackels_per_game = FloatField()
	interceptions_per_game = FloatField()
	fouls_per_game = FloatField()
	offsides_won_per_game = FloatField()
	clearances_per_game = FloatField()
	was_dribbled_per_game = FloatField()
	outfielder_block_per_game = FloatField()
	own_goals = IntField()
	rating = FloatField()

class PlayerOffensive(EmbeddedDocument):

	player_name = StringField()
	player_url = StringField()
	height_in_cm = IntField()
	weight_in_kg = IntField()
	apps = StringField()
	mins_played = IntField()
	goals = IntField()
	assists = IntField()
	shots_per_game = FloatField()
	key_passes_per_game = FloatField()
	dribbles_won_per_game = FloatField()
	fouls_given_per_game = FloatField()
	offsides_given_per_game = FloatField()
	dispossessed_per_game = FloatField()
	turnover_per_game = FloatField()
	rating = FloatField()

class PlayerPassing(EmbeddedDocument):

	player_name = StringField()
	player_url = StringField()
	height_in_cm = IntField()
	weight_in_kg = IntField()
	apps = StringField()
	mins_played = IntField()
	assists = IntField()
	key_passes_per_game = FloatField()
	total_passes_per_game = FloatField()
	pass_success = FloatField()
	accurate_crosses_per_game = FloatField()
	accurate_long_passes_per_game = FloatField()
	accurate_through_ball_per_game = FloatField()
	rating = FloatField()

class PlayerDetailed(EmbeddedDocument):

	player_name = StringField()
	player_url = StringField()
	height_in_cm = IntField()
	weight_in_kg = IntField()
	apps = StringField()
	mins_played = IntField()
	total_shots = FloatField()
	shot_out_of_box = FloatField()
	shot_six_yard_box = FloatField()
	shot_penalty_area = FloatField()
	rating = FloatField()

class TeamProfile(EmbeddedDocument):

	season = StringField()
	goals_per_game = FloatField()
	average_possession = FloatField()
	pass_accuracy = FloatField()
	shots_per_game = FloatField()
	tackels_per_game = FloatField()
	dribbles_won_per_game = FloatField()
	yellow_cards = IntField()
	red_cards = IntField()

class TeamReport(Document):

	team_name = StringField()
	#team_url = StringField()
	season = StringField()
	summary_report = ListField(EmbeddedDocumentField(PlayerSummary))
	defensive_report = ListField(EmbeddedDocumentField(PlayerDefensive))
	offensive_report = ListField(EmbeddedDocumentField(PlayerOffensive))
	passing_report = ListField(EmbeddedDocumentField(PlayerPassing))
	detailed_report = ListField(EmbeddedDocumentField(PlayerDetailed))
	profile = EmbeddedDocumentField(TeamProfile)
