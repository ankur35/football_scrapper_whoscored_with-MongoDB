"""
Created on Fri Apr  4 04:38:22 2019

@author: Ankur mehra
"""

import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotInteractableException
from time import sleep, time
#for time function 
def timeit(data_name):
	def inner_deco(func):
		def wrapper(*args, **kwargs):
			start = time()
			result = func(*args, **kwargs)
			end = time()
			print('Scraped {0} data in {1: .3f}'.format(data_name, end-start))
			return result
		return wrapper
	return inner_deco

class StandingsScraper(object):

	def __init__(self, url, driver):
		self.url = url
		self.driver = driver
#for standing table#
	@timeit('Standings')
	def get_standings(self, season):
		self.driver.get(self.url)

		self.select_season(season)
		self.accept_cookies_banner()

		standings_table = self.driver.find_element_by_class_name('standings')

		data = []

		for table_row in standings_table.find_elements_by_tag_name('tr'):
			items = table_row.find_elements_by_tag_name('td')

			team_name = items[1].find_element_by_class_name('team-link').text
			team_link = items[1].find_element_by_class_name('team-link').get_attribute('href')

			team_standings = {
				'season': season,
				'team_name': team_name,
				'team_url': team_link,
				'p': items[2].text,
				'w': items[3].text,
				'd': items[4].text,
				'l': items[5].text,
				'gf': items[6].text,
				'ga': items[7].text,
				'gd': items[8].text,
				'pts': items[9].text
			}
			data.append(team_standings)

		return data

	def accept_cookies_banner(self):
		try:
			banner_button = self.driver.find_element_by_class_name('banner_save--3Xnwp')
			banner_button.click()
		except ElementNotInteractableException:
			print('Cookies banner already accepted')

	def select_season(self, season):
		season_dropdown = Select(self.driver.find_element_by_id('seasons'))
		season_dropdown.select_by_visible_text(season)
		sleep(3)

class MatchLinksScraper(object):

	def __init__(self, url, driver):
		self.url = url
		self.driver = driver

	@timeit('Match Report Links')
	def get_match_links(self, season):
		self.driver.get(self.url)

		self.select_season(season)
		self.accept_cookies_banner()
		self.remove_ad()

		fixtures_link = self.driver.find_element_by_link_text('Fixtures')
		fixtures_link.click()
		sleep(2)

		date_controller = self.driver.find_elements_by_id('date-controller')
		
		data = []

		prev_link = self.find_prev_link()
		while prev_link.get_attribute('title') == 'View previous month':
			data.extend(self.get_links_from_table())
			self.remove_ad()
			prev_link.click()
			sleep(2)
			prev_link = self.find_prev_link()

		data.extend(self.get_links_from_table())

		return data

	def find_prev_link(self):
		date_controller = self.driver.find_element_by_id('date-controller')
		links = date_controller.find_elements_by_tag_name('a')
		return links[0]

	def get_links_from_table(self):
		table = self.driver.find_element_by_id('tournament-fixture')
		links = table.find_elements_by_class_name('match-link')

		result = []

		for link in links:
			if link.text == 'Preview':
				continue
			match_link = link.get_attribute('href')
			match_id = match_link.split('/')[4]
			result.append({match_id: match_link})

		return result

	def select_season(self, season):
		season_dropdown = Select(self.driver.find_element_by_id('seasons'))
		season_dropdown.select_by_visible_text(season)
		sleep(3)

	def accept_cookies_banner(self):
		try:
			banner_button = self.driver.find_element_by_class_name('banner_save--3Xnwp')
			banner_button.click()
		except ElementNotInteractableException:
			print('Cookies banner already accepted')

	def remove_ad(self):
		try:
			buttons = self.driver.find_elements_by_tag_name('input')

			for button in buttons:
				if button.get_attribute('alt') == 'Close':
					button.click()
		except:
			print('No ad found')


class MatchReportScraper(object):

	def __init__(self, url, driver):
		self.url = url
		self.driver = driver

	def get_match_report(self):
		self.driver.get(self.url)

		header = self.driver.find_element_by_id('match-header')
		team_links = header.find_elements_by_class_name('team-link')

		team1_name = team_links[0].text
		team2_name = team_links[1].text

		report_data = {
			'team1_name': team1_name,
			'team2_name': team2_name,
			'live_goals': self.get_live_goals(),
			'live_passes': self.get_live_passes(),
			'live_aggression': self.get_live_aggression()
		}

		return report_data

	def get_live_goals(self):
		subsection = self.driver.find_element_by_id('live-goals')

		stats = subsection.find_elements_by_class_name('stat')
		stats_data = {
			'total_attemts': {
				'team1': stats[0].find_element_by_class_name('pulsable').text,
				'team2': stats[0].find_element_by_class_name('pulsable').text
			},
			'open_play': {
				'team1': stats[1].find_element_by_class_name('pulsable').text,
				'team2': stats[1].find_element_by_class_name('pulsable').text
			},
			'set_piece': {
				'team1': stats[2].find_element_by_class_name('pulsable').text,
				'team2': stats[2].find_element_by_class_name('pulsable').text
			},
			'counter_attack': {
				'team1': stats[3].find_element_by_class_name('pulsable').text,
				'team2': stats[3].find_element_by_class_name('pulsable').text
			},
			'penalty': {
				'team1': stats[4].find_element_by_class_name('pulsable').text,
				'team2': stats[4].find_element_by_class_name('pulsable').text
			},
			'own_goal': {
				'team1': stats[5].find_element_by_class_name('pulsable').text,
				'team2': stats[5].find_element_by_class_name('pulsable').text
			}
		}

		return stats_data

	def get_live_passes(self):
		self.accept_cookies_banner()
		self.remove_ad()
		self.select_live_chart_tab('Pass Types')

		subsection = self.driver.find_element_by_id('live-passes')

		stats = subsection.find_elements_by_class_name('stat')
		stats_data = {
			'total_passes': {
				'team1': stats[0].find_element_by_class_name('pulsable').text,
				'team2': stats[0].find_element_by_class_name('pulsable').text
			},
			'crosses': {
				'team1': stats[1].find_element_by_class_name('pulsable').text,
				'team2': stats[1].find_element_by_class_name('pulsable').text
			},
			'through_balls': {
				'team1': stats[2].find_element_by_class_name('pulsable').text,
				'team2': stats[2].find_element_by_class_name('pulsable').text
			},
			'long_balls': {
				'team1': stats[3].find_element_by_class_name('pulsable').text,
				'team2': stats[3].find_element_by_class_name('pulsable').text
			},
			'short_passes': {
				'team1': stats[4].find_element_by_class_name('pulsable').text,
				'team2': stats[4].find_element_by_class_name('pulsable').text
			}
		}
		return stats_data

	def get_live_aggression(self):
		self.accept_cookies_banner()
		self.remove_ad()
		self.select_live_chart_tab('Card Situations')

		subsection = self.driver.find_element_by_id('live-aggression')

		stats = subsection.find_elements_by_class_name('stat')
		stats_data = {
			'total_card_reasons': {
				'team1': stats[0].find_element_by_class_name('pulsable').text,
				'team2': stats[0].find_element_by_class_name('pulsable').text
			},
			'fouls': {
				'team1': stats[1].find_element_by_class_name('pulsable').text,
				'team2': stats[1].find_element_by_class_name('pulsable').text
			},
			'unprofessional': {
				'team1': stats[2].find_element_by_class_name('pulsable').text,
				'team2': stats[2].find_element_by_class_name('pulsable').text
			},
			'dive': {
				'team1': stats[3].find_element_by_class_name('pulsable').text,
				'team2': stats[3].find_element_by_class_name('pulsable').text
			},
			'other': {
				'team1': stats[4].find_element_by_class_name('pulsable').text,
				'team2': stats[4].find_element_by_class_name('pulsable').text
			}
		}
		return stats_data

	def get_team_match_stats(self):
		sidebar = self.driver.find_element_by_id('match-report-team-statistics')

		stats = sidebar.find_elements_by_class_name('stat')
		stats_data = {
			'shots': {
				'team1': stats[0].find_element_by_class_name('pulsable').text,
				'team2': stats[0].find_element_by_class_name('pulsable').text
			},
			'shots_on_target': {
				'team1': stats[1].find_element_by_class_name('pulsable').text,
				'team2': stats[1].find_element_by_class_name('pulsable').text
			},
			'pass_success': {
				'team1': stats[2].find_element_by_class_name('pulsable').text,
				'team2': stats[2].find_element_by_class_name('pulsable').text
			},
			'aerial_duel_success': {
				'team1': stats[3].find_element_by_class_name('pulsable').text,
				'team2': stats[3].find_element_by_class_name('pulsable').text
			},
			'dribbles_won': {
				'team1': stats[4].find_element_by_class_name('pulsable').text,
				'team2': stats[4].find_element_by_class_name('pulsable').text
			},
			'tackles': {
				'team1': stats[5].find_element_by_class_name('pulsable').text,
				'team2': stats[5].find_element_by_class_name('pulsable').text
			},
			'possession': {
				'team1': stats[6].find_element_by_class_name('pulsable').text,
				'team2': stats[6].find_element_by_class_name('pulsable').text
			}
		}
		return stats_data

	def accept_cookies_banner(self):
		try:
			banner_button = self.driver.find_element_by_class_name('banner_save--3Xnwp')
			banner_button.click()
		except:
			print('Cookies banner already accepted')
		sleep(2)

	def remove_ad(self):
		try:
			buttons = self.driver.find_elements_by_tag_name('input')

			for button in buttons:
				if button.get_attribute('alt') == 'Close':
					button.click()
		except:
			print('No ad found')

	def select_live_chart_tab(self, name):
		section = self.driver.find_element_by_id('live-chart-stats')
		link = section.find_element_by_link_text(name)
		link.click()
		sleep(3)


class TeamScraper(object):

	def __init__(self, url, driver):
		self.url = url
		self.driver = driver

	def get_team_data(self, season):
		self.driver.get(self.url)
		self.accept_cookies_banner()
		self.remove_ad()

		if not season == '2018/2019':
			try:
				self.select_history_page()
				self.select_season(season)
			except:
				self.remove_ad()
				self.select_history_page()
				self.select_season(season)

		team_data = {
			'summary_data': self.get_summary_data(),
			'defensive_data': self.get_defensive_data(),
			'offensive_data': self.get_offensive_data(),
			'passing_data': self.get_passing_data(),
			'detailed_data': self.get_detailed_data(),
			'profile_data': self.get_profile_data()
		}
		return team_data

	@timeit('Summary')
	def get_summary_data(self):
		try:
			subsection = self.driver.find_element_by_id('team-squad-stats-summary')
		except:
			subsection = self.driver.find_element_by_id('team-squad-archive-stats-summary')

		try:
			table = subsection.find_element_by_id('player-table-statistics-body')
		except:
			sleep(3)
			table = subsection.find_element_by_id('player-table-statistics-body')

		summary_data = []

		for table_row in table.find_elements_by_tag_name('tr'):
			columns = table_row.find_elements_by_tag_name('td')

			player_node = table_row.find_element_by_class_name('player-link')
			player_link = player_node.get_attribute('href')
			player_name = player_node.text

			player_data = {
				'player_name': player_name,
				'player_link': player_link,
				'cm': columns[3].text,
				'kg': columns[4].text,
				'apps': columns[5].text,
				'mins_played': columns[6].text,
				'goals': columns[7].text,
				'assists': columns[8].text,
				'yellow_cards': columns[9].text,
				'red_cards': columns[10].text,
				'shots_per_game': columns[11].text,
				'success_passes': columns[12].text,
				'aerial_won_per_game': columns[13].text,
				'man_of_the_month': columns[14].text,
				'rating_sorted': columns[15].text
			}

			summary_data.append(player_data)

		return summary_data

	@timeit('Defensive')
	def get_defensive_data(self):
		self.remove_ad()
		self.select_squad_tab('Defensive')

		try:
			subsection = self.driver.find_element_by_id('team-squad-stats-defensive')
		except:
			subsection = self.driver.find_element_by_id('team-squad-archive-stats-defensive')
		
		try:
			table = subsection.find_element_by_id('player-table-statistics-body')
		except:
			sleep(3)
			table = subsection.find_element_by_id('player-table-statistics-body')

		defensive_data = []

		for table_row in table.find_elements_by_tag_name('tr'):
			columns = table_row.find_elements_by_tag_name('td')

			player_node = table_row.find_element_by_class_name('player-link')
			player_link = player_node.get_attribute('href')
			player_name = player_node.text

			player_data = {
				'player_name': player_name,
				'player_link': player_link,
				'cm': columns[3].text,
				'kg': columns[4].text,
				'apps': columns[5].text,
				'mins_played': columns[6].text,
				'tackels_per_game': columns[7].text,
				'interceptions_per_game': columns[8].text,
				'fouls_per_game': columns[9].text,
				'offsides_won_per_game': columns[10].text,
				'clearances_per_game': columns[11].text,
				'was_dribbled_per_game': columns[12].text,
				'outfielder_block_per_game': columns[13].text,
				'own_goals': columns[14].text,
				'rating': columns[15].text
			}

			defensive_data.append(player_data)

		return defensive_data

	@timeit('Offensive')
	def get_offensive_data(self):
		self.remove_ad()
		self.select_squad_tab('Offensive')

		try:
			subsection = self.driver.find_element_by_id('team-squad-stats-offensive')
		except:
			subsection = self.driver.find_element_by_id('team-squad-archive-stats-offensive')

		try:
			table = subsection.find_element_by_id('player-table-statistics-body')
		except:
			sleep(3)
			table = subsection.find_element_by_id('player-table-statistics-body')

		offensive_data = []

		for table_row in table.find_elements_by_tag_name('tr'):
			columns = table_row.find_elements_by_tag_name('td')

			player_node = table_row.find_element_by_class_name('player-link')
			player_link = player_node.get_attribute('href')
			player_name = player_node.text

			player_data = {
				'player_name': player_name,
				'player_link': player_link,
				'cm': columns[3].text,
				'kg': columns[4].text,
				'apps': columns[5].text,
				'mins_played': columns[6].text,
				'goals': columns[7].text,
				'assists': columns[8].text,
				'shots_per_game': columns[9].text,
				'key_passes_per_game': columns[10].text,
				'dribbles_won_per_game': columns[11].text,
				'fouls_given_per_game': columns[12].text,
				'offsides_gives_per_game': columns[13].text,
				'dispossessed_per_game': columns[14].text,
				'turnover_per_game': columns[15].text,
				'rating': columns[16].text
			}

			offensive_data.append(player_data)

		return offensive_data

	@timeit('Passing')
	def get_passing_data(self):
		self.remove_ad()
		self.select_squad_tab('Passing')

		try:
			subsection = self.driver.find_element_by_id('team-squad-stats-passing')
		except:
			subsection = self.driver.find_element_by_id('team-squad-archive-stats-passing')

		try:
			table = subsection.find_element_by_id('player-table-statistics-body')
		except:
			sleep(3)
			table = subsection.find_element_by_id('player-table-statistics-body')

		passing_data = []

		for table_row in table.find_elements_by_tag_name('tr'):
			columns = table_row.find_elements_by_tag_name('td')

			player_node = table_row.find_element_by_class_name('player-link')
			player_link = player_node.get_attribute('href')
			player_name = player_node.text

			player_data = {
				'player_name': player_name,
				'player_link': player_link,
				'cm': columns[3].text,
				'kg': columns[4].text,
				'apps': columns[5].text,
				'mins_played': columns[6].text,
				'assists': columns[7].text,
				'key_passes_per_game': columns[8].text,
				'total_passes_per_game': columns[9].text,
				'pass_success': columns[10].text,
				'accurate_crosses_per_game': columns[11].text,
				'accurate_long_passes_per_game': columns[12].text,
				'accurate_through_ball_per_game': columns[13].text,
				'rating': columns[14].text
			}

			passing_data.append(player_data)

		return passing_data

	@timeit('Detailed')
	def get_detailed_data(self):
		self.remove_ad()
		self.select_squad_tab('Detailed')

		try:
			subsection = self.driver.find_element_by_id('team-squad-stats-detailed')
		except:
			subsection = self.driver.find_element_by_id('team-squad-archive-stats-detailed')

		try:
			table = subsection.find_element_by_id('player-table-statistics-body')
		except:
			sleep(3)
			table = subsection.find_element_by_id('player-table-statistics-body')

		detailed_data = []

		for table_row in table.find_elements_by_tag_name('tr'):
			columns = table_row.find_elements_by_tag_name('td')

			player_node = table_row.find_element_by_class_name('player-link')
			player_link = player_node.get_attribute('href')
			player_name = player_node.text

			player_data = {
				'player_name': player_name,
				'player_link': player_link,
				'cm': columns[3].text,
				'kg': columns[4].text,
				'apps': columns[5].text,
				'mins_played': columns[6].text,
				'total_shots': columns[7].text,
				'shot_out_of_box': columns[8].text,
				'shot_six_yard_box': columns[9].text,
				'shot_penalty_area': columns[10].text,
				'rating': columns[11].text
			}

			detailed_data.append(player_data)

	@timeit('Profile')
	def get_profile_data(self):
		sidebox = self.driver.find_element_by_class_name('team-profile-side-box')
		stats_container = sidebox.find_element_by_class_name('stats-container')
		dynamic_list = stats_container.find_element_by_class_name('stats')
		items = dynamic_list.find_elements_by_tag_name('dd')

		profile_data = {
			'season': items[1].text,
			'goals_per_game': items[2].text,
			'average_possession': items[3].text,
			'pass_accuracy': items[4].text,
			'shots_per_game': items[5].text,
			'tackles_per_game': items[6].text,
			'dribbles_per_game': items[7].text,
			'yellow_cards': items[8].find_element_by_class_name('yellow-card-box').text,
			'red_cards': items[8].find_element_by_class_name('red-card-box').text
		}

		return profile_data

	def accept_cookies_banner(self):
		try:
			banner_button = self.driver.find_element_by_class_name('banner_save--3Xnwp')
			banner_button.click()
		except:
			print('Cookies banner already accepted')

	def remove_ad(self):
		try:
			buttons = self.driver.find_elements_by_tag_name('input')

			for button in buttons:
				if button.get_attribute('alt') == 'Close':
					button.click()
		except:
			print('No ad found')

	def select_squad_tab(self, name):
		try:
			section = self.driver.find_element_by_id('team-squad-stats')
		except:
			section = self.driver.find_element_by_id('team-squad-archive-stats')
		link = section.find_element_by_link_text(name)
		link.click()
		sleep(3)

	def select_history_page(self):
		navigation = self.driver.find_element_by_id('sub-navigation')
		link = navigation.find_element_by_link_text('History')
		link.click()
		sleep(3)

	def select_season(self, season):
		season_dropdown = Select(self.driver.find_element_by_id('stageId'))
		season_text = 'Bundesliga - {}'.format(season)
		season_dropdown.select_by_visible_text(season_text)
		sleep(3)



def create_data_dirs():
	dirs = ['./standingsData1', './teamData1', './matchLinksData1', './matchReportData1']

	for d in dirs:
		if not os.path.exists(d):
			os.makedirs(d)


if __name__ == '__main__':

	url = "https://www.whoscored.com/Regions/81/Tournaments/3/Germany-Bundesliga"
	driver = webdriver.Firefox()
	seasons = ['2018/2019']

	create_data_dirs()

	standings_scraper = StandingsScraper(url, driver)
	match_links_scraper = MatchLinksScraper(url, driver)

	for season in seasons:
		season_dashed = season.replace('/', '-')

		standings_filename = './standingsData1/standings_{}.json'.format(season_dashed)
		match_links_filename = './matchLinksData1/match_links_{}.json'.format(season_dashed)

		if not os.path.isfile(standings_filename):
			standings = standings_scraper.get_standings(season)

			with open(standings_filename, 'w') as f:
				print('saving standings to {}'.format(standings_filename))
				json.dump(standings, f)
				f.close()
		else:
			with open(standings_filename, 'r') as f:
				standings = json.load(f)
				f.close()

		if not os.path.isfile(match_links_filename):
			match_links = match_links_scraper.get_match_links(season)

			with open(match_links_filename, 'w') as f:
				print('saving match links to {}'.format(match_links_filename))
				json.dump(match_links, f)
				f.close()
		else:
			with open(match_links_filename, 'r') as f:
				match_links = json.load(f)
				f.close()

		for team in standings:
			team_name = team['team_name']
			filename = './teamData1/{}_{}.json'.format(team_name, season_dashed)

			if os.path.isfile(filename):
				print('| {} | already has data. skipping..'.format(team_name))
				continue

			team_scraper = TeamScraper(team['team_url'], driver)
			team_data = team_scraper.get_team_data(season)

			with open(filename, 'w') as f:
				print('saving data to: {}'.format(filename))
				json.dump(team_data, f)
				f.close()

		for link in match_links:
			match_id = list(link.keys())[0]
			match_link = link[match_id]

			filename = './matchReportData1/{}_{}.json'.format(match_id, season_dashed)

			if os.path.isfile(filename):
				print('| match {} | already has data. skipping..'.format(match_id))
				continue

			match_report_scraper = MatchReportScraper(match_link, driver)
			match_report_data = match_report_scraper.get_match_report()

			with open(filename, 'w') as f:
				print('saving match report to: {}'.format(filename))
				print('----------------------------------------------------------')
				json.dump(match_report_data, f)
				f.close()

	driver.quit()
