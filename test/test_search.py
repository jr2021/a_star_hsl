import unittest
import io
import contextlib
from unittest.mock import patch
from src.citymap import CityMap

from tmc import points

from tmc.utils import load, get_stdout

FIRST_OUTPUT = '[23m]1130446(Caloniuksenkatu) -> [19m]1130442(Apollonkatu) -> [17m]1140447(Töölöntori) -> [13m]1140436(Ooppera) -> [12m]1140439(Töölön halli) -> [10m]1140440(Kansaneläkelaitos) -> [8m]1150431(Töölön tulli) -> [7m]1150433(Meilahden sairaala) -> [4m]1150435(Meilahdentie)'
SECOND_OUTPUT = '[33m]1130446(Caloniuksenkatu) -> [29m]1130442(Apollonkatu) -> [27m]1140447(Töölöntori) -> [23m]1140436(Ooppera) -> [22m]1140439(Töölön halli) -> [20m]1140440(Kansaneläkelaitos) -> [18m]1150431(Töölön tulli) -> [17m]1150433(Meilahden sairaala) -> [9m]1150435(Meilahdentie)'
THIRD_OUTPUT = '[25m]1121480(Urheilutalo) -> [24m]1121438(Brahenkatu) -> [22m]1220414(Roineentie) -> [21m]1220416(Hattulantie) -> [20m]1220418(Rautalammintie) -> [19m]1220420(Mäkelänrinne) -> [18m]1220426(Uintikeskus) -> [17m]1173416(Pyöräilystadion) -> [15m]1173423(Koskelantie) -> [14m]1250425(Kimmontie) -> [13m]1250427(Käpylänaukio) -> [3m]1250429(Metsolantie)'
#FOURTH_OUTPUT = '[57m]1250431(Pohjolanaukio) -> [56m]1250429(Metsolantie) -> [55m]1250427(Käpylänaukio) -> [54m]1250425(Kimmontie) -> [53m]1173423(Koskelantie) -> [51m]1173416(Pyöräilystadion) -> [47m]1220426(Uintikeskus) -> [46m]1220420(Mäkelänrinne) -> [45m]1220418(Rautalammintie) -> [44m]1220416(Hattulantie) -> [42m]1220425(Vallilan kirjasto) -> [41m]1220406(Lautatarhankatu) -> [40m]1121436(Sörnäinen(M)) -> [38m]1113434(Käenkuja) -> [37m]1113432(Haapaniemi) -> [30m]1111428(Hakaniemi) -> [27m]1020459(Varsapuistikko) -> [26m]1020457(Kaisaniemi) -> [24m]1020453(Rautatieasema) -> [20m]1020463(Ylioppilastalo) -> [18m]1020449(Aleksanterinkatu) -> [17m]1010451(Senaatintori) -> [16m]1010424(Ritarihuone) -> [14m]1080404(Katajanokan puisto) -> [9m]1080406(Kauppiaankatu) -> [0m]1080403(Katajanokan puisto)'


@points('AStar')
class MainTest(unittest.TestCase):
    def test_01_simple_route(self):
        self.longMessage = False
        citymap = CityMap('graph.json', 'routes.json')
        start = citymap.get_stop('1150435')
        goal = citymap.get_stop('1130446')
        time = 4
        results = str(citymap.search(start, goal, time))
        self.assertEqual(FIRST_OUTPUT, results, msg="Output doesn't match for the route (4min) 1150435 -> 1130446")

    def test_02_simple_route_different_time(self):
        self.longMessage = False
        citymap = CityMap('graph.json', 'routes.json')
        start = citymap.get_stop('1150435')
        goal = citymap.get_stop('1130446')
        time = 9
        results = str(citymap.search(start, goal, time))
        self.assertEqual(SECOND_OUTPUT, results, msg="Output doesn't match for the route (9min) 1150435 -> 1130446: " + results)

    def test_03_simple_route2(self):
        self.longMessage = False
        citymap = CityMap('graph.json', 'routes.json')
        start = citymap.get_stop('1250429')
        goal = citymap.get_stop('1121480')
        time = 3
        results = str(citymap.search(start, goal, time))
        self.assertEqual(THIRD_OUTPUT, results, msg="Output doesn't match for the route (3min) 1250429 -> 1121480")

    '''def test_04_longest_route(self):
        self.longMessage = False
        citymap = CityMap('graph.json', 'routes.json')
        start = citymap.get_stop('1080403')
        goal = citymap.get_stop('1250431')
        time = 0
        results = str(citymap.search(start, goal, time))
        self.assertEqual(FOURTH_OUTPUT, results, msg="Output doesn't match for the route (0min) 1080403 -> 1250431")
    '''
