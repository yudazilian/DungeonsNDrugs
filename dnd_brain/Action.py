# -*- coding: UTF-8 -*-
import sqlite3
from random import randint
from Events import GodDecides, JudgeEvent, PoliceEvent, GangsterEvent, DiseaseStrokeEvent

def standarlise_output(clsmeth):
	# Return Value Format:
	# (char_state <dict>, story_message <str>)
	def _wrap(cls, user_id):
		rtn = clsmeth(cls, user_id)
		return {
			'character': rtn[0], 
			'message'  : rtn[1]
		}
	return _wrap

# def update_status_vector(, money_var, health_var, evil_var):

def query_user_items(cursor, user_id):

	items = []
	query_result = cursor.execute('''
		SELECT * FROM items WHERE user_id == %s''' % (user_id))
	query_result = query_result.fetchall()
	
	## query_result: (<drug_name>, <drug_weight>)
	for result in query_result:
		items.append((result[1], result[2]))
	return items

# def query_user_symptoms(cursor, user_id):

# 	symptoms = []
# 	query_result = cursor.execute('''
# 		SELECT * FROM ''')

class Action():

	conn = sqlite3.connect('./dnd.db', check_same_thread=False)
	cursor = conn.cursor()
	record = None

	@classmethod
	@standarlise_output
	def check_saved_game(cls, user_id):
		
		result = cls.cursor.execute(
			'''SELECT * FROM user WHERE user_id == %s''' % user_id)

		cls.record = result.fetchone()
		if cls.record:
			cls.record = {
				'user_id': cls.record[0],
				'age'    : cls.record[1],
				'health': cls.record[2],
				'money' : cls.record[3],
				'evil'  : cls.record[4],
				'identity': cls.record[5],
				'city': cls.record[6],
				'items': [],
				'symptoms': []
			}

			cls.record['items'] = query_user_items(cls.cursor, user_id)
			# cls.record['symptoms'] = query_user_symptoms(cls.scursor, user_id)

			return (cls.record, '歡迎你回到這個遊戲，想要繼續嗎？')
		else:
			return ({}, '你第一次參與這項遊戲，想要開始毒與地下城嗎？')

	@classmethod
	@standarlise_output
	def start_game(cls, user_id):

		if cls.record:
			
			return (cls.record,
				'玩家%s現年%s歲，健康為%s，目前擁有%s元，惡名為%s，身份是名%s' % (
				str(cls.record['user_id']), str(cls.record['age']), str(cls.record['health']),
				str(cls.record['money']), str(cls.record['evil']), cls.record['identity'].encode('utf8')))
		
		# Create a new identity for the new user.	
		else:
			cls.record = {
				'user_id': str(user_id),
				'age':  16,
				'health': 100,
				'money' : 10000,
				'evil'  : 50,
				'city': '台北市',
				'identity': '少年',
				'items': [],
				'symptoms': []
			}

			result = cls.cursor.execute(
				'''INSERT INTO user VALUES (%s, 16, 100, 10000, 0, '少年', '台北市')'''
				% str(user_id))

			cls.conn.commit()

			return (cls.record, '你是一個十六歲少年，出生於台北市.... 你目前有10000元，健康值為100，身世清白')

	@classmethod
	def save_game(cls, user_status):

		cls.cursor.execute(
			"UPDATE user SET age = %s, health = %s, money = %s, evil = %s, city = '%s' WHERE user_id=%s" 
			% (str(user_status['age']), str(user_status['health']), str(user_status['money']),
			   str(user_status['evil']), user_status['city'], user_status['user_id']))

		## TODO: Save Symptoms
		## TODO: Save Drug Items

		cls.conn.commit()

		pass

	@classmethod
	def check_status(cls, user_status):
		return '玩家%s現年%s歲，健康為%s，目前擁有%s元，惡名為%s，身份是名%s' % (
			str(user_status['user_id']), str(user_status['age']), str(user_status['health']),
			str(user_status['money']), str(user_status['evil']), user_status['identity'].encode('utf8'))

	@classmethod
	def delete_record(cls, user_id):
		cls.cursor.execute(
			"DELETE FROM user WHERE user_id=%s" % user_id)
		cls.cursor.execute(
			"DELETE FROM items WHERE user_id=%s" % user_id)
		cls.cursor.execute(
			"DELETE FROM symptoms WHERE user_id=%s" % user_id)
		cls.cursor.execute(
			"DELETE FROM crime_record WHERE user_id=%s" % user_id)

	@classmethod
	def throw_dice(cls):
		return randint(1, 12)

	@classmethod
	def travel(cls, user_status):
		pass

	@classmethod
	def buy_drugs(cls, user_status):

		pass

	@classmethod
	def sell_drugs(cls, user_status):
		god_decision = GodDecides(user_status)
		return god_decision

	@classmethod
	def gain_money(cls, user_status, transaction):
		
		income = 0
		for drug, item, price in transaction:
			income = item * price

		user_status['money'] += income
		user_status['evil']  += 20 

		return (user_status, '共獲得%s元，惡名值上升%s' % (str(income), str(20)))

	@classmethod
	def get_event_result(cls, user_status, event, dice_value):
		evil_var, money_var, health_var, age_var, event_message, judge_flag = event.make_result(dice_value)
		user_status['age']    += age_var
		user_status['evil']   += evil_var
		user_status['money']  += money_var
		user_status['health'] += health_var
		return (event_message, judge_flag)

	@classmethod
	def start_investigation(cls, user_status):

		# 販賣事件直接進入審判程序
		if user_status['crime_state'] in set(['販賣第一級毒品', '販賣第二級毒品', '販賣第三級毒品', '販賣第四級毒品']):
			pass

	@classmethod
	def go_to_rehab(cls, user_status):
		pass

	@classmethod
	def go_to_big_rehab(cls, user_status):
		pass

	@classmethod
	def go_to_court(cls, user_status):
		return JudgeEvent(user_status)

	@classmethod
	def conduct_darksocial(cls, user_status):
		pass


	@classmethod
	def be_sentenced(cls, user_status):
		pass





