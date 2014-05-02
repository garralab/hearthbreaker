import random
import unittest
from hsgame.agents.basic_agents import PredictableBot, DoNothingBot
from tests.testing_agents import *
from tests.testing_utils import generate_game_for
from hsgame.replay import SavedGame

from hsgame.cards import *

__author__ = 'Daniel'

class TestPaladin(unittest.TestCase):

    def setUp(self):
        random.seed(1857)


    def testPaladinPower(self):
        game = generate_game_for(AvengingWrath, MogushanWarden, PredictableBot, DoNothingBot)

        for turn in range(0, 3):
            game.play_single_turn()

        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual(1, game.current_player.minions[0].attack_power)
        self.assertEqual(1, game.current_player.minions[0].defense)
        self.assertEqual("Silver Hand Recruit", game.current_player.minions[0].card.name)


    def testAvengingWrath(self):
        game = generate_game_for(MogushanWarden, AvengingWrath, MinionPlayingAgent, SpellTestingAgent)

        for turn in range(0, 12):
            game.play_single_turn()

        #The random numbers work so that Avenging Wrath hits the player once, first minion once, second minion four times and third minion two times (total of eight hits)
        self.assertEqual(29, game.other_player.health)
        self.assertEqual(3, len(game.other_player.minions))
        self.assertEqual("Mogu'shan Warden", game.other_player.minions[0].card.name)
        self.assertEqual("Mogu'shan Warden", game.other_player.minions[1].card.name)
        self.assertEqual("Mogu'shan Warden", game.other_player.minions[2].card.name)
        self.assertEqual(6, game.other_player.minions[0].defense)
        self.assertEqual(3, game.other_player.minions[1].defense)
        self.assertEqual(5, game.other_player.minions[2].defense)

    def testBlessedChampion(self):
        game = generate_game_for(BlessedChampion, StonetuskBoar, EnemyMinionSpellTestingAgent, MinionPlayingAgent)
        
        for turn in range(0, 9):
            game.play_single_turn()

        self.assertEqual(2, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)

        #Test that this spell is being silenced properly as well
        game.other_player.minions[0].silence()
        self.assertEqual(1, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)
        
    def testBlessingOfKings(self):
        game = generate_game_for(BlessingOfKings, StonetuskBoar, EnemyMinionSpellTestingAgent, MinionPlayingAgent)
        
        for turn in range(0, 7):
            game.play_single_turn()

        self.assertEqual(5, game.other_player.minions[0].attack_power)
        self.assertEqual(5, game.other_player.minions[0].defense)
        self.assertEqual(5, game.other_player.minions[0].max_defense)

        #Test that this spell is being silenced properly as well
        game.other_player.minions[0].silence()
        self.assertEqual(1, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)

    def testBlessingOfMight(self):
        game = generate_game_for(StonetuskBoar, BlessingOfMight, MinionPlayingAgent, EnemyMinionSpellTestingAgent)
        
        for turn in range(0, 2):
            game.play_single_turn()

        self.assertEqual(4, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)

        #Test that this spell is being silenced properly as well
        game.other_player.minions[0].silence()
        self.assertEqual(1, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)

    def testBlessingOfWisdom(self):
        game = SavedGame("tests/replays/card_tests/BlessingOfWisdom.rep")
        game.start()
        self.assertEqual(3, len(game.current_player.minions))
        # 7 cards have been drawn.
        # 3 for starting first, 3 for new turn and 1 for minion attack with Blessing of Wisdom (the second minion who had it got silenced)
        self.assertEqual(23, game.other_player.deck.left)