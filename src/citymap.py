import json
import os
from queue import PriorityQueue

from math import sqrt
from math import inf

HUGE_NUMBER = inf

def dist(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def time_to_string(time):
    result = ""
    if time >= 60:
        result += str(int(time // 60)) + 'h'
    result += str(time % 60) + 'm'

    return result


def load_data(source_file):
    """Reading JSON from a file and deserializing it
    :param source_file: JSON object (str)
    :return: obj (array)
    """
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, '..', source_file)) as file:
            return json.load(file)
    except:
        print('Could not read %s file' % source_file)
        exit()


class State:
    """ State class lets you trace back the route from the last stop
    :attr stop: Stop (obj)
    :attr previous: Previous state of the route (State)
    :attr current_time: The time in minutes from the beginning of the trip (int)

    :static attr goal: The goal stop (obj)
    """

    goal = None

    def __init__(self, stop, time=0, previous=None):
        self.stop = stop
        self.current_time = time
        self.previous = previous

    def __str__(self):
        """ Returns route as a string from the last stop to the beginning.
            Format: [12m]1140439(Töölön halli) -> [10m]1140440(Kansaneläkelaitos) -> [8m]1150431(Töölön tulli)
        """
        result = '[' + time_to_string(self.current_time) + ']' + self.stop['code'] + '(' + self.stop[
            'name'] + ')'
        state = self.previous
        while state is not None:
            result += " -> " + '[' + time_to_string(state.current_time) + ']' + state.stop['code'] + '(' + \
                      state.stop['name'] + ')'
            state = state.previous

        return result

    def get_stop_code(self):
        return self.stop['code']

    def get_stop(self):
        return self.stop

    def get_previous(self):
        return self.previous

    def get_time(self):
        return self.current_time

    def __lt__(self, state):
        return self.heuristic() <= state.heuristic() 

    def heuristic(self):
        return dist((self.stop["x"], self.stop["y"]), (dict(State.goal)["x"], dict(State.goal)["y"])) / 260.0
        
class CityMap:
    """Storage of the tram network
    :attr graph_data: (obj)
    :attr routes_data: (obj)
    :attr stops: dictionary {stop_code: stop}
    :attr routes: dictionary {route_code: route}
    """

    def __init__(self, stops_source_file, routes_source_file):
        self.graph_data = load_data(stops_source_file)
        self.routes_data = load_data(routes_source_file)
        self.stops = {}
        self.routes = {}
        for stop in self.graph_data:
            self.stops[stop["code"]] = stop
        for route in self.routes_data:
            self.routes[route["code"]] = route

    def get_stop(self, code):
        return self.stops[code]

    def get_adjacent(self, stop_code):
        """Returns dictionary containing all neighbor stops """
        return self.stops.get(stop_code)["neighbors"]

    def get_adjacent_codes(self, stop_code):
        """Returns codes of all neighbor stops """
        return list(self.stops.get(stop_code)["neighbors"].keys())

    def cost(self, from_code, dest_code, current_time):
        """Returns the fastest transition time between two stops in a direction from_code -> dest_code
           Also counts the waiting time.
        """
        neighbors = self.get_adjacent(from_code)
        transition_time = HUGE_NUMBER

        if dest_code not in neighbors:
            print('There is no railway to this stop! ')
            exit()
        else:
            routes_codes = neighbors[dest_code]
            for rc in routes_codes:
                route = self.routes.get(rc)
                i = route['stopCodes'].index(from_code)
                wait_time = (route['stopTimes'][i] % 10) - (current_time % 10)
                wait_time = (wait_time + 10) if (wait_time < 0) else wait_time
                travel_time = route['stopTimes'][i + 1] - route['stopTimes'][i]
                if transition_time > (wait_time + travel_time):
                    transition_time = wait_time + travel_time

        return transition_time

    def search(self, start, stop, time):
        q = PriorityQueue()
        searched = []

        State.goal = stop
        q.put((0, State(start, time)))
    
        while q.not_empty:
            current = q.get()[1]
            if current.stop == stop:
                return str(current)
            searched.append(current.get_stop_code())
            for adjacent in self.get_adjacent_codes(current.get_stop_code()):
                if adjacent not in searched:
                    cost = self.cost(current.get_stop_code(), adjacent, current.current_time)
                    adjacent_state = State(self.get_stop(adjacent), cost + current.current_time, current)
                    heuristic = adjacent_state.heuristic()
                    total_cost = cost+ heuristic
                    q.put((total_cost, adjacent_state))
        return None
