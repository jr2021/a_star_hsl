import unittest
import io
import contextlib
from unittest.mock import patch
from src.citymap import CityMap
from src.citymap import State

from tmc import points

FIRST_VAL = 11.9873
SECOND_VAL = 9.9933

citymap = CityMap('graph.json', 'routes.json')
metsolantie = citymap.get_stop('1250429')
urheilutalo = citymap.get_stop('1121480')
meilahdentie = citymap.get_stop("1150435");
caloniuksenkatu = citymap.get_stop("1130446");


@points('AStar')
class MainTest(unittest.TestCase):
    def test_01_heuristic(self):
        self.longMessage = False
        State.goal = urheilutalo
        state = State(metsolantie)
        self.assertAlmostEqual(FIRST_VAL, state.heuristic(), delta=0.1)

    def test_02_heuristic(self):
        self.longMessage = False
        State.goal = caloniuksenkatu
        state = State(meilahdentie)
        self.assertAlmostEqual(SECOND_VAL, state.heuristic(), delta=0.1)

    def test_03_comparator1(self):
        self.longMessage = False
        State.goal = urheilutalo
        state1 = State(metsolantie, 20)
        state2 = State(metsolantie, 10)
        self.assertGreater(state1, state2)

    def test_04_comparator2(self):
        self.longMessage = False
        State.goal = urheilutalo
        state1 = State(metsolantie, 20)
        state2 = State(metsolantie, 10)
        self.assertLess(state2, state1)

    def test_05_comparator3(self):
        self.longMessage = False
        State.goal = urheilutalo
        state1 = State(metsolantie, 20)
        state2 = State(metsolantie, 10)
        self.assertNotEqual(state1, state2)

    def test_06_comparator4(self):
        self.longMessage = False
        State.goal = urheilutalo
        state1 = State(caloniuksenkatu, 10)
        state2 = State(metsolantie, 10)
        self.assertGreater(state2, state1)

    def test_07_comparator5(self):
        self.longMessage = False
        State.goal = urheilutalo
        state1 = State(caloniuksenkatu, 10)
        state2 = State(metsolantie, 10)
        self.assertLess(state1, state2)
