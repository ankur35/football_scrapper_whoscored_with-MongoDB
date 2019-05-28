import os
import json
from mongoengine import connect
from models import *
from cleaners import TeamDataCleaner, MatchReportCleaner

class MongoDataStore(object):


    def __init__(self, host, port, database_name):
        connect(database_name, host=host, port=port)


    def import_data_from_files(self):
        self.reset_collections()
        self.import_standing_tables()
        self.import_team_data()
        self.import_match_reports()

    def reset_collections(self):
        StandingTable.drop_collection()
        TeamReport.drop_collection()
        MatchReport.drop_collection()

    def import_standing_tables(self):
        base_path = './standingsData/'
        filenames = os.listdir(base_path)

        for filename in filenames:
            with open(base_path+filename) as f:
                data = json.load(f)

                for table in data:
                    standing_table = StandingTable(
                        team_name=table['team_name'],
                        team_url=table['team_url'],
                        season=table['season'],
                        plays=table['p'],
                        wins=table['w'],
                        draws=table['d'],
                        losses=table['l'],
                        goal_for=table['gf'],
                        goal_against=table['ga'],
                        goal_difference=table['gd'],
                        points=table['pts'])
                    standing_table.save()
                f.close()


    def import_team_data(self):
        base_path = './teamData/'
        filenames = os.listdir(base_path)
        cleaner = TeamDataCleaner()

        for filename in filenames:
            with open(base_path+filename) as f:
                data = json.load(f)
                season = filename.split('_')[-1].split('.')[0].replace('-', '/')
                team_name = filename.split('_')[-2]
                summary_report = []
                defensive_report = []
                offensive_report = []
                passing_report = []
                detailed_report = []
                
                data = cleaner.clean(data)

                for section in data['summary_data']:
                    summary_report.append(PlayerSummary(
                        player_name=section['player_link'],
                        player_url=section['player_name'],
                        height_in_cm=section['cm'],
                        weight_in_kg=section['kg'],
                        apps=section['apps'],
                        mins_played=section['mins_played'],
                        goals=section['goals'],
                        assists=section['assists'],
                        yellow_cards=section['yellow_cards'],
                        red_cards=section['red_cards'],
                        shots_per_game=section['shots_per_game'],
                        success_passes=section['success_passes'],
                        aerial_won_per_game=section['aerial_won_per_game'],
                        man_of_the_match=section['man_of_the_match'],
                        rating=section['rating_sorted']))

                for section in data['defensive_data']:
                    defensive_report.append(PlayerDefensive(
                        player_name=section['player_link'],
                        player_url=section['player_name'],
                        height_in_cm=section['cm'],
                        weight_in_kg=section['kg'],
                        apps=section['apps'],
                        mins_played=section['mins_played'],
                        tackels_per_game=section['tackels_per_game'],
                        interceptions_per_game=section['interceptions_per_game'],
                        fouls_per_game=section['fouls_per_game'],
                        offsides_won_per_game=section['offsides_won_per_game'],
                        clearances_per_game=section['clearances_per_game'],
                        was_dribbled_per_game=section['was_dribbled_per_game'],
                        outfielder_block_per_game=section['outfielder_block_per_game'],
                        own_goals=section['own_goals'],
                        rating=section['rating']))

                for section in data['offensive_data']:
                    offensive_report.append(PlayerOffensive(
                        player_name=section['player_link'],
                        player_url=section['player_name'],
                        height_in_cm=section['cm'],
                        weight_in_kg=section['kg'],
                        apps=section['apps'],
                        mins_played=section['mins_played'],
                        goals=section['goals'],
                        assists=section['assists'],
                        shots_per_game=section['shots_per_game'],
                        key_passes_per_game=section['key_passes_per_game'],
                        dribbles_won_per_game=section['dribbles_won_per_game'],
                        fouls_given_per_game=section['fouls_given_per_game'],
                        offsides_given_per_game=section['offsides_gives_per_game'],
                        dispossessed_per_game=section['dispossessed_per_game'],
                        turnover_per_game=section['turnover_per_game'],
                        rating=section['rating']))

                for section in data['passing_data']:
                    passing_report.append(PlayerPassing(
                        player_name=section['player_link'],
                        player_url=section['player_name'],
                        height_in_cm=section['cm'],
                        weight_in_kg=section['kg'],
                        apps=section['apps'],
                        mins_played=section['mins_played'],
                        assists=section['assists'],
                        key_passes_per_game=section['key_passes_per_game'],
                        total_passes_per_game=section['total_passes_per_game'],
                        pass_success=section['pass_success'],
                        accurate_crosses_per_game=section['accurate_crosses_per_game'],
                        accurate_long_passes_per_game=section['accurate_long_passes_per_game'],
                        accurate_through_ball_per_game=section['accurate_through_ball_per_game'],
                        rating=section['rating']))

                for section in data['detailed_data']:
                    detailed_report.append(PlayerDetailed(
                        player_name=section['player_link'],
                        player_url=section['player_name'],
                        height_in_cm=section['cm'],
                        weight_in_kg=section['kg'],
                        apps=section['apps'],
                        mins_played=section['mins_played'],
                        total_shots=section['total_shots'],
                        shot_out_of_box=section['shot_out_of_box'],
                        shot_six_yard_box=section['shot_six_yard_box'],
                        shot_penalty_area=section['shot_penalty_area'],
                        rating=section['rating']))

                team_profile = TeamProfile(
                    season=data['profile_data']['season'],
                    goals_per_game=data['profile_data']['goals_per_game'],
                    average_possession=data['profile_data']['average_possession'],
                    pass_accuracy=data['profile_data']['pass_accuracy'],
                    shots_per_game=data['profile_data']['shots_per_game'],
                    tackels_per_game=data['profile_data']['tackles_per_game'],
                    dribbles_won_per_game=data['profile_data']['dribbles_per_game'],
                    yellow_cards=data['profile_data']['yellow_cards'],
                    red_cards=data['profile_data']['red_cards'])


                team_report = TeamReport(
                    team_name=team_name,
                    #team_url=team_url,
                    season=season,
                    summary_report=summary_report,
                    defensive_report=defensive_report,
                    offensive_report=offensive_report,
                    passing_report=passing_report,
                    detailed_report=detailed_report,
                    profile=team_profile)
                team_report.save()
                f.close()


    def create_params(self, sectionname, fieldnames, data):
        result = {}

        for fieldname in fieldnames:
            if fieldname not in data[sectionname]:
                return {}

            result[fieldname] = [
                data[sectionname][fieldname]['team1'],
                data[sectionname][fieldname]['team2']
            ]

        return result


    def import_match_reports(self):
        base_path = './matchReportData/'
        filenames = os.listdir(base_path)

        for filename in filenames:
            with open(base_path+filename) as f:
                data = json.load(f)
                season = filename.split('_')[-1].split('.')[0].replace('-', '/')

                if data['live_goals'] == {}:
                    continue

                fieldnames = [
                    'total_attempts',
                    'open_play',
                    'set_price',
                    'counter_attack',
                    'penalty',
                    'own_goal'
                ]
                params = self.create_params('live_goals', fieldnames, data)
                params['set_piece'] = params['set_price']
                params.pop('set_price')
                params = MatchReportCleaner().clean(params)

                goal_report = GoalReport(**params)

                if data['live_aggression'] == {}:
                    continue

                fieldnames = [
                    'total_card_reasons',
                    'fouls',
                    'unprofessional',
                    'dive',
                    'other'
                ]
                params = self.create_params('live_aggression', fieldnames, data)
                params = MatchReportCleaner().clean(params)
                aggression_report = AggressionReport(**params)

                if data['live_passes'] == {}:
                    continue

                fieldnames = [
                    'total_passes',
                    'crosses',
                    'through_balls',
                    'long_balls',
                    'short_passes'
                ]
                params = self.create_params('live_passes', fieldnames, data)
                params = MatchReportCleaner().clean(params)
                pass_report = PassReport(**params)

                if data['match_stats'] == {}:
                    continue

                fieldnames = [
                    'shots',
                    'shots_on_target',
                    'pass_success',
                    'aerial_duel_success',
                    'dribbles_won',
                    'tackles',
                    'possession'
                ]
                params = self.create_params('match_stats', fieldnames, data)
                params = MatchReportCleaner().clean(params)
                stats = MatchStats(**params)

                match_report = MatchReport(
                    team1_name=data['team1_name'],
                    team2_name=data['team2_name'],
                    season=season,
                    goal_report=goal_report,
                    pass_report=pass_report,
                    aggression_report=aggression_report,
                    stats=stats)
                match_report.save()
                f.close()



if __name__ == '__main__':
    host = '127.0.0.1'
    port = 27017
    database_name = 'football_data'

    store = MongoDataStore(host, port, database_name)

    print('importing data from files to mongodb.. just a sec..\n')
    store.import_data_from_files()

    standing_tables = StandingTable.objects(team_name='Bayern Munich', season='2016/2017')

    print('example query 1:')
    print('team name: ', standing_tables[0].team_name)
    print('season: ', standing_tables[0].season)
    print('plays: ', standing_tables[0].plays)
    print('wins: ', standing_tables[0].wins)
    print('draws: ', standing_tables[0].draws)
    print('losses: ', standing_tables[0].losses)
    print('wins-losses: ', standing_tables[0].wins - standing_tables[0].losses, '\n')

    match_reports_2018_2019 = MatchReport.objects(season='2018/2019')

    print('example query 2:')
    print('total reports found: ', len(match_reports_2018_2019))
    if len(match_reports_2018_2019) > 0:
        print('printing a part of the first report: \n')
        print('  team1: ', match_reports_2018_2019[0].team1_name)
        print('    pass success: ', match_reports_2018_2019[0].stats.pass_success[0], '%')
        print('  team2: ', match_reports_2018_2019[0].team2_name)
        print('    pass success:', match_reports_2018_2019[0].stats.pass_success[1], '%\n')

    team_report_bayern_munich_2018_2019 = TeamReport.objects(
        season='2018/2019',
        team_name='Bayern Munich')
    
    print('example query 3:')
    print(team_report_bayern_munich_2018_2019[0].team_name)
    print(team_report_bayern_munich_2018_2019[0].season)
    print('{} played {} mins'.format(
        team_report_bayern_munich_2018_2019[0].summary_report[0].player_name,
        team_report_bayern_munich_2018_2019[0].summary_report[0].mins_played
    ), '\n')
    
    ##########################################################################
    # All Teamreports for all seasons
    ##########################################################################
    all_team_reports = TeamReport.objects()

    for team_report in all_team_reports:
        print('Team name: {}, season: {}\n'.format(team_report.team_name, team_report.season))
        print('Summary:')
        
        for data in team_report.summary_report:
            for field in data._fields:
                print(field, getattr(data, field))
            print()
        
        print('\nDefensive:')
        
        for data in team_report.defensive_report:
            for field in data._fields:
                print(field, getattr(data, field))
        
        print('\nOffensive:')
        
        for data in team_report.offensive_report:
            for field in data._fields:
                print(field, getattr(data, field))
            print()
        
        print('\Passing:')
        
        for data in team_report.passing_report:
            for field in data._fields:
                print(field, getattr(data, field))
            print()
        
        print('\nDetailed:')
        
        for data in team_report.detailed_report:
            for field in data._fields:
                print(field, getattr(data, field))
            print()
        
        print('\nTeam Profile')
        
        for field in team_report.profile._fields:
            print(field, getattr(team_report.profile, field))