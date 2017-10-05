"""
Created on Thursday July 7th, 2016

Author:  Sean Benner
"""

from random import shuffle
import itertools
from collections import defaultdict
import basicstrategy
import hilo

class Player(object):

	def __init__(self, name="Player", money=0, strategy = basicstrategy, counting_strategy = hilo, count = 0):
		self.hand = []
		self.name = name
		self.money = money
		self.strategy = strategy
		self.counting_strategy = counting_strategy
		self.count = count

	def bet(self, amount):
		self.money -= amount
		return self

	def strategy(self):
		return self

	def hit(self):
		self.hand.append(shoe.pop())
		return self

	def discard_hand(self):
		self.hand = []
		return self

default_player = Player("Default Player")

num_decks = 6
shuffle_point = 1


def create_shoe():
	"""Creates a new shoe to deal cards from"""
	shoe = []
	SUITS = 'cdhs'
	RANKS = '23456789TJQKA'
	DECK = [''.join(card) for card in itertools.product(RANKS, SUITS)]
	for x in range(num_decks):
		shoe += DECK
	shuffle(shoe)
	return shoe

shoe = create_shoe()

def is_splittable(hand):
	"""Check if hand is splittable"""
	if hand[0][0] == hand[1][0] or ((hand[0][0] == 'T' or hand[0][0] == 'J' or hand[0][0] == 'Q' or hand[0][0] == 'K') and \
					(hand[1][0] == 'T' or hand[1][0] == 'J' or hand[1][0] == 'Q' or hand[1][0] =='K')):
		return True
	else:
		return False


def get_score(hand, soft_status = False):
	"""Get score of hand"""
	x = 0
	# Count aces last
	soft = False
	for i in range(len(hand)):
		if hand[i][0] == 'J' or hand[i][0] == 'Q' or hand[i][0] == 'K' or hand[i][0] == 'T':
			x += 10
		elif hand[i][0] == 'A':
			continue
		else:
			x += int(hand[i][0])
	for i in range(len(hand)):
		if hand[i][0] == 'A':
			if x + 11 <= 21:
				x += 11
				soft = True
			else:
				x += 1
	if soft and x > 21:
		x-=10
		soft = False
	if soft_status:
		return x, soft
	else:
		return x


def play_game(players = [default_player], betsize = 'default',games = 1, rules={}, auto = False, splits_allowed = 1):
	"""Play a set amount of games.  This function will take user input on hitting, splitting, and standing."""

	again = 'y'
	while again == 'y':
		dealer_hand = []
		bets = {}
		hands = defaultdict(list)
		p_split = defaultdict(bool)
		p_bust = defaultdict(bool)
		p_double = defaultdict(bool)
		# take bets
		for p in players:
			if betsize == 'default':
				bets[p] = int(raw_input("How much would you like to bet?  "))
			else:
				bets[p] = betsize


		# deal cards
		for p in players:
			hands[p].append(shoe.pop())
			hands[p].append(shoe.pop())
		dealer_hand.append(shoe.pop())
		dealer_hand.append(shoe.pop())


		#  take action from player
		for p in players:
			decision = 'hit'

			if is_splittable(hands[p]):
				print hands[p]
				if raw_input("Split? ") == 'split':
					p_split[p] = True
					hands[p] = [[hands[p][0], shoe.pop()], [hands[p][1], shoe.pop()]]
					for hand in hands[p]:
						decision = 'hit'
						can_double = True
						while get_score(hand) <= 21 and decision == 'hit':
							print "\tDealer card: {} \n\tPlayer hand:  {}\n\tPlayer score:  {}".format(dealer_hand[0], hand, get_score(hand))
							decision = raw_input("What would you like to do?  ")
							if decision == 'hit':
								hand.append(shoe.pop())
								can_double = False
							if decision == 'double':
								hand.append(shoe.pop())
								p_double[hand] = True
							if get_score(hand) > 21:
								print "Player hand:  {}\n{} busts with {}!".format(hand, p.name, get_score(hand))

					if get_score(hands[0]) > 21 and get_score(hands[1]) > 21:
						p_bust[p] = True
			if p_split[p] == False:
				can_double = True
				while get_score(hands[p]) <= 21 and decision == 'hit':
					print "\tDealer card: {} \n\tPlayer hand:  {}\n\tPlayer score:  {}".format(dealer_hand[0], hands[p], get_score(hands[p]))
					decision = raw_input("What would you like to do?  ")
					if decision == 'hit':
						hands[p].append(shoe.pop())
						can_double = False
					if decision == 'double':
						p_double[hands[p]] = True
						hands[p].append(shoe.pop())
					if get_score(hands[p]) > 21:
						p_bust[p] = True
						print "Player hand:  {}\n{} busts with {}!".format(hands[p], p.name, get_score(hands[p]))

		if any(p_bust.values()) != True:
			while get_score(dealer_hand) <= 17:
				dealer_hand.append(shoe.pop())

		dealer_score = get_score(dealer_hand)
		print "\nResults:\nDealer cards: {} \nDealer score: {}".format(dealer_hand, dealer_score)

		#  PAYOUT
		for p in players:
			if p_split[p] == False:
				if 	get_score(hands[p]) > dealer_score and get_score(hands[p]) <= 21:
						if len(hands[p]) == 2:
							p.money += bets[p] * 1.5
							print "{} wins ${} with a Blackjack!".format(p.name, bets[p] * 1.5)
						else:
							if p_double[hands[p]]:
								p.money += bets[p] * 2
								print "{} wins ${}".format(p.name, bets[p] *2)
							else:
								p.money += bets[p]
								print "{} wins ${}".format(p.name, bets[p])
				elif get_score(hands[p]) < dealer_score and dealer_score > 21:
					if p_double[hands[p]]:
						p.money += bets[p] * 2
						print "Dealer busts!  {} wins {}".format(p.name, bets[p]*2)
					else:
						p.money += bets[p]
						print "Dealer busts!  {} wins {}".format(p.name, bets[p])
				elif (get_score(hands[p]) < dealer_score and dealer_score <= 21) or get_score(hands[p]) > 21:
					if p_double[hands[p]]:
						p.money -= bets[p] * 2
						print "{} loses ${}".format(p.name, bets[p]*2)
					else:
						p.money -= bets[p]
						print "{} loses ${}".format(p.name, bets[p])
				elif get_score(hands[p]) == dealer_score:
					print "{} ties".format(p.name)
			else:
				for num, hand in enumerate(hands[p]):
					print 'Hand number {}'.format(num+1)
					if get_score(hand) > dealer_score and get_score(hand) <= 21:
						if len(hand) == 2:
							p.money += bets[p] * 1.5
							print "{} wins ${} with a Blackjack!".format(p.name, bets[p] * 1.5)
						else:
							if p_double[hand]:
								p.money += bets[p] * 2
								print "{} wins ${}".format(p.name, bets[p]*2)
							else:
								p.money += bets[p]
								print "{} wins ${}".format(p.name, bets[p])
					elif get_score(hand) < dealer_score and dealer_score > 21:
						if p_double[hand]:
							p.money += bets[p] * 2
							print "Dealer busts!  {} wins {}".format(p.name, bets[p]*2)
						else:
							p.money += bets[p]
							print "Dealer busts!  {} wins {}".format(p.name, bets[p])
					elif (get_score(hand) < dealer_score and dealer_score <= 21) or get_score(hand) > 21:
						if p_double[hand]:
							p.money -= bets[p]*2
							print "{} loses ${}".format(p.name, bets[p]*2)
						else:
							p.money -= bets[p]
							print "{} loses ${}".format(p.name, bets[p])
					elif get_score(hands[p]) == dealer_score:
						print "{} ties".format(p.name)
		again = raw_input("Play again? y/n  ")

def automate_games(players, num_games = 10, betsize = 1):
	"""Automatically play games using basic strategy and/or card counting"""
	global shoe
	players_totals = defaultdict(list)
	players_hands = defaultdict(list)
	dealers_hands = []
	# for p in players:
	# 	players_totals[p].append(p.money)
	count = 0

	# print "Player's starting money:  {}".format(p.money)
	for x in xrange(num_games):
		if len(shoe) < 52 * shuffle_point:
			shoe = create_shoe()
			for p in players:
				p.count = 0

		dealer_hand = []
		bets = {}
		hands = defaultdict(list)
		p_split = defaultdict(bool)
		p_split_double = defaultdict(list)
		p_busts = defaultdict(bool)
		p_double = defaultdict(bool)
		p_soft = defaultdict(bool)

		# take bets
		for p in players:
			if betsize == 'dynamic':
				bets[p] = p.counting_strategy.bet_amount(p.count, shoe, 1)
			else:
				bets[p] = betsize

		# deal cards
		for p in players:
			hands[p].append(shoe.pop())
			hands[p].append(shoe.pop())
		dealer_hand.append(shoe.pop())
		dealer_hand.append(shoe.pop())

		# Test specific hands
		# print dealer_hand[0]

		# Check hole card, if dealer has 21, do not play.
		if (dealer_hand[0][0] == 'A' and get_score(dealer_hand) == 21):
			for p in players:
				p.money -= bets[p]
				players_totals[p].append(p.money)
				players_hands[p].append(hands[p])
				dealers_hands.append(dealer_hand)
		else:
			#Implement strategy
			for p in players:
				# print hands[p]
				if is_splittable(hands[p]):
					decision = p.strategy.split(hands[p], dealer_hand[0])
					# print "***********Is splittable"
					# print "***********Choice: {}".format(decision)
					if decision == 'split':
						# print "******Split hands"
						p_split[p] = True
						hands[p] = [[hands[p][0], shoe.pop()], [hands[p][1], shoe.pop()]]
						for hand_num, hand in enumerate(hands[p]):
							decision = 'hit'
							can_double = True
							p_split_double[p].append(False)
							while get_score(hand) < 21 and decision == 'hit':
								decision = p.strategy.decision(hand, dealer_hand[0], can_double)
								if decision == 'hit':
									hand.append(shoe.pop())
									can_double = False
								if decision == 'double':
									hand.append(shoe.pop())
									p_split_double[p][hand_num] = True
							if (get_score(hands[p][0]) > 21) and (get_score(hands[p][1]) > 21):
								p_busts[p] = True
							# print "Player score: {}".format(get_score(hand))
							# print hand
				if p_split[p] == False:
					can_double = True
					decision = 'hit'
					while get_score(hands[p]) <= 21 and decision == 'hit':
						decision = p.strategy.decision(hands[p], dealer_hand[0], can_double)
						if decision == 'hit':
							hands[p].append(shoe.pop())
							can_double = False
						if decision == 'double':
							hands[p].append(shoe.pop())
							p_double[p] = True
					if get_score(hands[p]) > 21:
						p_busts[p] = True
					# print "Player score:  {}".format(get_score(hands[p]))
					# print hands[p]

			if any(p_busts.values()) != True:
				while get_score(dealer_hand) < 17:
					dealer_hand.append(shoe.pop())

			dealer_score = get_score(dealer_hand)
			# print "Dealer score:  {}".format(dealer_score)
			# print "Dealer hand:  {}".format(dealer_hand)
			H = hands.values()
			H.append(dealer_hand)


			# payout
			for p in players:
				if p_split[p] == False:
					if get_score(hands[p]) > 21:
						p.money -= bets[p]
					elif dealer_score < get_score(hands[p]) and get_score(hands[p]) <= 21:
						if len(hands[p]) == 2 and get_score(hands[p]) == 21:
							p.money += bets[p] * 1.5
						else:
							if p_double[p]:
								p.money += bets[p] * 2
							else:
								p.money += bets[p]
					elif get_score(hands[p]) <= 21 and 21 < dealer_score:
						if p_double[p]:
							p.money += bets[p] * 2
						else:
							p.money += bets[p]
					elif (get_score(hands[p]) < dealer_score and dealer_score <= 21):
						if p_double[p]:
							p.money -= bets[p] *2
						else:
							p.money -= bets[p]
					players_totals[p].append(p.money)
					players_hands[p].append(hands[p])
					dealers_hands.append(dealer_hand)
				else:
					for hand_num, hand in enumerate(hands[p]):
						if 21 < get_score(hand):
							p.money -= bets[p]
						elif get_score(hand) > dealer_score and get_score(hand) <= 21:
							if len(hand) == 2 and get_score(hand) == 21:
								p.money += bets[p] * 1.5
							else:
								if p_split_double[p][hand_num]:
									p.money += bets[p] * 2
								else:
									p.money += bets[p]
						elif get_score(hand) <= 21 and 21 < dealer_score:
							if p_split_double[p][hand_num]:
								p.money += bets[p] * 2
							else:
								p.money += bets[p]
						elif get_score(hand) < dealer_score and dealer_score <= 21:
							if p_split_double[p][hand_num]:
								p.money -= bets[p] * 2
							else:
								p.money -= bets[p]
						players_hands[p].append(hand)
						players_totals[p].append(p.money)
						dealers_hands.append(dealer_hand)

				# print "player's money:  {}".format(p.money)

				p.count = p.counting_strategy.running_count(H, p.count)


				# print "{} percent complete".format(float(x)/num_games * 100)

	# for p in players:
		# print "{} played {} games and now has {}".format(p.name, num_games, p.money)

	return players_totals, players_hands, dealers_hands
