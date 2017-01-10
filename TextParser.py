import re
import networkx as nx
from matplotlib import pyplot as plt


class TextParser:
    def __init__(self, inp=False, min_freq=40, labels=False, char_label_lim=40):
        """
        Initialize the text parser
        :param inp: set to True to manually input characters
        :param min_freq: minimum frequency a node must have in order to remain in the graph at print time
        :param labels: set to True to show edge labels
        :param char_label_lim: maximum amount of characters before labels are not shown automatically
        """
        self.__min_freq = min_freq
        self.__character_list = []
        self.__location_list = []
        self.__object_list = []
        self.__labels = labels
        self.__file = None
        self.__inp = inp
        self.__graph = None
        self.__dict = None
        self.__char_label_lim = char_label_lim
        self.__plot = plt.figure(figsize=(12, 12))
        self.__subplot = self.__plot.add_subplot(1, 1, 1)
        return

    @staticmethod
    def parse_characters(name_string):
        """
        :param name_string: string
        :return: list
        """
        if name_string is None:
            return []
        if len(name_string) == 0:
            return []

        # split the string by the ',' delimiter and remove spaces from the front and back of each word
        characters = name_string.split(',')
        characters = [name.strip() for name in characters]

        return characters

    def __initialize_dict(self):
        """
        Initializes the characters, locations, and objects to a new dictionary object
        :return: dict
        """
        dictionary = {}
        dict_counter = 0

        char_len = len(self.__character_list)
        for i in range(0, char_len):
            dictionary[self.__character_list[i].lower()] = dict_counter
            dict_counter += 1

        for i in range(0, len(self.__location_list)):
            dictionary[self.__location_list[i]] = dict_counter
            dict_counter += 1

        for i in range(0, len(self.__object_list)):
            dictionary[self.__object_list[i]] = dict_counter
            dict_counter += 1

        return dictionary

    def __initialize_graph(self):
        """
        Initializes the characters, locations, and objects as nodes to a new graph object
        :return: networkx graph object
        """
        graph = nx.Graph()
        node_counter = 0

        char_len = len(self.__character_list)
        for i in range(0, char_len):
            graph.add_node(node_counter, {'name': self.__character_list[i], 'frequency': 1, 'category': 'character'})
            node_counter += 1

        for i in range(0, len(self.__location_list)):
            graph.add_node(node_counter, {'name': self.__location_list[i], 'frequency': 1, 'category': 'location'})
            node_counter += 1

        for i in range(0, len(self.__object_list)):
            graph.add_node(node_counter, {'name': self.__object_list[i], 'frequency': 1, 'category': 'object'})
            node_counter += 1

        return graph

    def load_graph(self, file, label="label"):
        """
        Load graph from a gml file
        :param file: path where gml file is located
        :param label: label to name loaded nodes by
        :return: graph
        """
        self.__graph = nx.read_gml(file, label=label)
        return self.__graph

    def increment_name_frequency(self, name, amount=1):
        """
        Increments the frequency of a node in the graph.
        :param name: name of node
        :param amount: amount to increment by
        """
        if self.__graph is None:
            raise Exception("graph has not been initialized")
        elif self.__dict is None:
            raise Exception("dict has not been initialized")

        dict_name = self.__dict[name.lower()]
        new_frequency = self.__graph.node[dict_name]['frequency'] + amount
        self.__graph.node[dict_name]['frequency'] = new_frequency

    def add_edge(self, name1, name2):
        """
        Adds an edge between two nodes in a graph and increments the weight and frequency of the edge.
        :param name1: name of first node
        :param name2: name of second node
        :return: None
        """
        name1 = name1.lower()
        name2 = name2.lower()
        if self.__graph.has_edge(self.__dict[name1], self.__dict[name2]):
            new_frequency = self.__graph.get_edge_data(self.__dict[name1], self.__dict[name2])['frequency'] + 1
            self.__graph.add_edge(self.__dict[name1], self.__dict[name2], frequency=new_frequency)
            pass
        else:
            self.__graph.add_edge(self.__dict[name1], self.__dict[name2], frequency=1)

    def print_characters(self):
        """Prints the character list to the console."""
        print("CHARACTER LIST: " + str(self.__character_list))

    def print_locations(self):
        """Prints the location list to the console."""
        print("LOCATION LIST: " + str(self.__location_list))

    def print_objects(self):
        """Prints the object list to the console."""
        print("OBJECT LIST: " + str(self.__object_list))

    def print_graph(self, show=True):
        """
        Prints the graph to matplotlib plot.
        :param show: boolean value, graph will appear in GUI when set to True.
        :return: None
        """

        if self.__graph is None:
            raise Exception("graph has not been initialized")

        self.__clean_graph()
        node_labels = nx.get_node_attributes(self.__graph, 'name')
        edge_labels = nx.get_edge_attributes(self.__graph, 'frequency')

        # color map for different node types
        color_map = {'character': 'r', 'location': '#FF0099', 'object': '#00a1ff'}

        # list of node frequencies
        d = []
        nodes_len = len(self.__graph.nodes())
        for i in range(0, nodes_len):
            if self.__graph.has_node(i):
                d.append(int(self.__graph.node[i]['frequency']))

        # draw the graph nodes
        nx.draw(self.__graph, pos=nx.circular_layout(self.__graph), labels=node_labels,
                node_color=[color_map[self.__graph.node[node]['category']] for node in self.__graph], with_labels=True,
                node_size=[(v * 10000 / sum(d)) for v in d], ax=self.__subplot)

        edges = self.__graph.edges()
        weights = [self.__graph[u][v]['frequency'] for u, v in edges]

        # draw the edges of the network
        nx.draw_networkx_edges(self.__graph, pos=nx.circular_layout(self.__graph), edgelist=edges,
                               width=[(50 * self.__graph[u][v]['frequency']) / sum(weights) for u, v in edges],
                               edge_cmap=plt.cm.winter, edge_color=weights, ax=self.__subplot)

        # print the edge labels if .__labels is True
        if self.__labels:
            nx.draw_networkx_edge_labels(self.__graph, pos=nx.circular_layout(self.__graph),
                                         edge_labels=edge_labels, ax=self.__subplot)

        # only show the graph if show is True
        if show:
            plt.show()

    def add_character(self, name):
        """
        Adds the given name to the character list.
        :param name: name to add to the character list
        :return: list
        """
        if name is not None and isinstance(name, str):
            self.__character_list.append(name)
            return self.__character_list
        else:
            raise Exception("input must be a string")

    def add_characters(self, names):
        """
        Adds the given names to the character list
        :param names: list of names
        :return: list
        """
        if names is not None and isinstance(names, list):
            self.__character_list.extend(names)
            return self.__character_list
        else:
            raise Exception("input must be a list")

    def add_location(self, location):
        """
        Adds the given location to the location list.
        :param location: location to add to the location list
        :return: list
        """
        if location is not None and isinstance(location, str):
            self.__location_list.append(location)
            return self.__location_list
        else:
            raise Exception("input must be a string")

    def add_locations(self, locations):
        """
        Adds the given locations to the location list
        :param locations: list of locations
        :return: list
        """
        if locations is not None and isinstance(locations, list):
            self.__location_list.extend(locations)
            return self.__location_list
        else:
            raise Exception("input must be a list")

    def add_object(self, obj):
        """
        Adds the given object to the object list.
        :param obj: object to add to the object list
        :return: list
        """
        if obj is not None and isinstance(obj, str):
            self.__object_list.append(obj)
            return self.__object_list
        else:
            raise Exception("input must be a string")

    def add_objects(self, objs):
        """
        Adds the given objects to the objects list
        :param objs: list of objects
        :return: list
        """
        if objs is not None and isinstance(objs, list):
            self.__object_list.extend(objs)
            return self.__object_list
        else:
            raise Exception("input must be a list")

    def read_file(self, file=None):
        """
        parses the given file to initialize the dict and graph
        :param file: path to a txt file
        :return: None
        """
        if file is not None:
            self.__file = file
            try:
                if self.__inp:
                    self.__character_list = self.add_characters(
                        self.parse_characters(input("INPUT CHARACTER NAMES SEPARATED BY COMMAS: ")))
                else:
                    self.__character_list = self.detect_characters(self.__file)
            except FileNotFoundError:
                print("\nERROR: the file " + self.__file + " could not be found.\n")
        else:
            while True:
                try:
                    self.__file = input("INPUT A PATH TO A TEXT FILE: ")
                    if self.__inp:
                        self.__character_list = self.add_characters(
                            self.parse_characters(input("INPUT CHARACTER NAMES SEPARATED BY COMMAS: ")))
                    else:
                        self.__character_list = self.detect_characters(self.__file)
                    break
                except FileNotFoundError:
                    print("\nERROR: the file " + self.__file + " could not be found.\n")

        # initialize the graph and dict once the character list has been created
        self.__graph = self.__initialize_graph()
        self.__dict = self.__initialize_dict()

        # open the file and parse each line
        name_list = frozenset([name.lower() for name in self.__character_list])
        location_list = frozenset([location.lower() for location in self.__location_list])
        object_list = frozenset([obj.lower() for obj in self.__object_list])
        with open(self.__file, encoding="utf-8") as f:
            for line in f:
                self.__parse_line(line, name_list, location_list, object_list)

    def __parse_line(self, line, name_list, location_list, object_list):
        """
        Parses the given line and creates connections between graph nodes
        :param line: line from file
        :return: None
        """
        active = {}
        delimiters = ",", " ", ".", "\n", ";", ":", "\"", "!", "?", "\\", "]", "[", "(", ")"
        regex_pattern = '|'.join(map(re.escape, delimiters))
        words = re.split(regex_pattern, line)

        for current_word in words:
            current_name = ""
            name = current_word.lower()
            if name in name_list:
                current_name = name
                self.increment_name_frequency(current_name)
                for active_name in active:
                    if active_name != current_name:
                        self.add_edge(active_name, current_name)
                active[current_name] = 20

            elif current_word.lower() in location_list:
                for i in range(0, len(self.__location_list)):
                    if current_word.lower() == self.__location_list[i].lower():
                        current_name = self.__location_list[i]
                self.increment_name_frequency(current_name)
                for active_name in active:
                    if active_name != current_name:
                        self.add_edge(active_name, current_name)
                active[current_name] = 45

            elif current_word.lower() in object_list:
                for i in range(0, len(self.__object_list)):
                    if current_word.lower() == self.__object_list[i].lower():
                        current_name = self.__object_list[i]
                self.increment_name_frequency(current_name)
                for active_name in active:
                    if active_name.lower() != current_name.lower():
                        self.add_edge(active_name, current_name)
                active[current_name] = 30

            for active_name in active:
                active[active_name] -= 1

            for active_name in active:
                if active[active_name] == 0:
                    del active[active_name]
                    break

    @staticmethod
    def detect_characters(file):
        """
        Detects characters in a given file.
        :param file: path to file
        :return: list of detected characters
        """

        # list of past tense verbs used to detect characters
        past_verbs = ("said", "shouted", "exclaimed", "remarked", "quipped", "whispered", "watched",
                      'yelled', 'yelped', 'announced', 'muttered', 'asked', 'inquired', 'desired',
                      'cried', "answered", 'interposed', 'interrupted', 'suggested', 'thought', 'might',
                      'called', 'added', 'began', 'observed', 'echoed', 'repeated', 'shrugged', 'subtracted',
                      'pointed', 'argued', 'promised', 'noted', 'mentioned', 'replied', 'wanted', 'put',
                      'screamed', 'grumbled', 'stammered', 'screeched', 'questioned', 'pleaded', 'fell',
                      'proclaimed', 'professed', 'moaned', 'spouted', 'surmised', 'murmured', 'appeared',
                      'ranted', 'decided', 'demanded', 'stopped', 'voiced', 'urged', 'wept', 'rambled',
                      'wailed', 'chuckled', 'chanted', 'boasted', 'coaxed', 'blurted', 'lectured', 'spent',
                      'hinted', 'barked', 'rebuffed', 'kissed', 'ran', 'walked', 'swung', 'lifted', 'stood',
                      'charged', 'sped', 'crept', 'restrained', 'droned', 'uttered', 'glided', 'loved',
                      'took', 'yanked', 'collapsed', 'tumbled', 'crumpled', 'screeched', 'understood',
                      'trudged', 'limped', 'hesitated', 'erupted', 'stampeded', 'created', 'started', 'gave',
                      'created', 'initiated', 'ended', 'chided', 'reached', 'glanced', 'felt', 'believed',
                      'turned', 'grew', 'became', 'fought', 'killed', 'went', 'will', 'shot', 'nodded',
                      'fumed', 'tried', 'crouched', 'ordered', 'shuddered', 'ignored', 'grabbed',
                      'countered', 'hoping', 'looked', 'made', 'closed', 'caught', 'gave')

        # words that are omitted from the list of detected characters
        omitted = frozenset(["He", "She", "It", "They", "You", "Mr", "Mrs", "Miss", "Lord", "Just", "Everything",
                             "Professor", "Uncle", "Aunt", "Then", 'We', 'When', 'If', 'Others', 'Some', "Only", "I",
                             "Soon", "In", "And", "On", "An", "What", "His", "Her", "Have", "That", "But", "Not", "How", "More",
                             "Me",
                             "This", "The", "You", "Your", "Or", "My", "So", "Nearly", "Who", "YOU", "Another", "Very",
                             "Having", "Everyone", "One", "No", "Someone", "All", "Both", "Never", "Nobody", "Of",
                             "End",
                             "Did", "Such", "At", "Other", "Their", "Our", "By", "Nothing", "Which", "Where", "Into",
                             "IT",
                             "Were", "Well", "Here", "Do", "Either", "There", "Now", "To", "As", "Anything", "These",
                             "Something", "Thou", "Why", "New", "Maybe", "Yes", "OFF", "ON", "Almost", "Nor", "Many",
                             "Those",
                             "Most", "Instantly", "Thing", "Things", "Nearby", "Stay", "Out", "Always", "Somebody",
                             "Yet",
                             "Sure", "Everybody", "Done", "With", "Get", "Ever", "Already", "Often", "HE", "WOULD",
                             "Way", "Whatever", "Ending", "Tonight", "Thank", "Go", "THE", "Beyond", "ALL", "WHAT", "Anyone",
                             "Yeah", "Stop", "Words", "Old", "Men", "Getting", "Dr", "People", "THEY", "Whoever"])

        with open(file, encoding="utf-8") as f:

            matches = set()

            # replace new line characters with spaces
            lines = f.read().replace('\n', ' ')

            # loop through past_verbs and use regex expressions to create a list of matches
            past_verbs_len = len(past_verbs)

            for i in range(0, past_verbs_len):
                pattern = "[A-Z][\w]+ {}|{} [A-Z][\w]+".format(past_verbs[i], past_verbs[i])
                match = re.findall(pattern, lines)
                length = len(match)
                for j in range(0, length):
                    match[j] = match[j].replace(' ' + past_verbs[i], '')
                    match[j] = match[j].replace(past_verbs[i] + ' ', '')
                matches |= frozenset(match)

            # remove the words in the omitted set from the list of matches
            matches = [word for word in matches if word not in omitted]

        return matches

    def __clean_graph(self):
        """
        Removes nodes from graph which do not meet the frequency requirement.
        :return: None
        """
        if self.__graph is None:
            raise Exception("graph has not been initialized")

        # create list of nodes  who have a frequency less than min_freq to delete
        nodes = self.__graph.nodes(data=True)
        to_delete = []
        nodes_len = len(nodes)
        for i in range(0, nodes_len):
            if int(self.__graph.node[i]['frequency']) \
                    < self.__min_freq and 'character' == self.__graph.node[i]['category']:
                to_delete.append(i)

        # reverse the list of nodes to reverse in order to format it for remove_nodes_from()
        to_delete.reverse()
        self.__graph.remove_nodes_from(to_delete)

        # do not show labels if there are too many nodes in the graoh
        if self.__graph.size() >= self.__char_label_lim:
            self.__labels = False

    def get_frequency_in_graph(self, name):
        """
        Returns the number of times the input has been detected
        :rtype: int
        """
        if self.__graph is None:
            raise Exception("graph has not been initialized")
        if name.lower() not in self.__dict:
            return 0
        return int(self.__graph.node[self.__dict[name.lower()]]['frequency'])

    def get_num_connections(self, name_one, name_two):
        """
        Returns the number of connections between two nodes in the graph.
        :param name_one: name of first node
        :param name_two: name of second node
        :return:
        """
        if self.__graph is None:
            raise Exception("graph has not been initialized")
        if name_one.lower() not in self.__dict or name_two.lower() not in self.__dict:
            # return 0 as either one or both names are not in the dict, making a connection impossible
            return 0
        return int(self.__graph.get_edge_data(self.__dict[name_one.lower()],
                                              self.__dict[name_two.lower()])['frequency'])

    @property
    def get_num_characters(self):
        """
        Returns the number of characters in the character list.
        :return: length of the character list
        """
        return len(self.__character_list)

    @property
    def get_num_objects(self):
        """
        Returns the number of objects in the object list.
        :return: length of the object list
        """
        return len(self.__object_list)

    @property
    def get_num_locations(self):
        """
        Returns the number of locations in the location list.
        :return: length of the location list
        """
        return len(self.__location_list)

    def get_shortest_path(self, name_one, name_two):
        """
        Returns the shortest path between two nodes in list form
        :param name_one: source node
        :param name_two: destination node
        :return: list
        """
        if self.__graph is None:
            raise Exception("graph has not been initialized")
        elif name_one.lower() not in self.__dict or name_two.lower() not in self.__dict:
            return []
        else:
            # num_path is a list of ints corresponding to node id's
            num_path = nx.shortest_path(self.__graph, source=self.__dict[name_one.lower()],
                                        target=self.__dict[name_two.lower()],
                                        weight=None)
            # path is the names corresponding to the node id's in num_path
            path = [self.__graph.node[i]['name'] for i in num_path]
            return path

    def get_degree_of_connection(self, name_one, name_two):
        """
        Returns the degree of the connection between two nodes
        :param name_one: source node
        :param name_two: destination node
        :return: int
        """
        if self.__graph is None:
            raise Exception("graph has not been initialized")
        elif name_one.lower() not in self.__dict or name_two.lower() not in self.__dict:
            return -1
        else:
            # num_path is a list of ints corresponding to node id's
            num_path = nx.shortest_path(self.__graph, source=self.__dict[name_one.lower()],
                                        target=self.__dict[name_two.lower()],
                                        weight=None)
            degree = len(num_path) - 2
            if degree <= 0:
                return -1
            elif degree == -1:
                return 1
            else:
                return degree

    def get_degree_of_node(self, name):
        """
        Returns the degree of a node (how many adjacent edges it has).
        :param name: name of the node
        :return: int
        """
        if self.__graph is None:
            raise Exception("graph has not been initialized")
        elif name.lower() not in self.__dict:
            return 0
        else:
            return int(self.__graph.degree(self.__dict[name.lower()]))

    @property
    def get_graph(self):
        """
        Returns the graph.
        :return: list
        """
        return self.__graph

    @property
    def get_characters(self):
        """
        Returns the character list.
        :return: list
        """
        return self.__character_list

    @property
    def get_locations(self):
        """
        Returns the location list.
        :return: list
        """
        return self.__location_list

    @property
    def get_objects(self):
        """
        Returns the object list.
        :return: list
        """
        return self.__object_list

    def save_graph(self, directory='', form='png', name='character_graph',
                   compressed=False, compression_format='gz'):
        """
        Saves the graph externally.
        :param directory: directory in which the file will be saved
        :param form: type of file, supported types = png, pdf, gml, eps, svg.
        :param name: name of the graph file to be saved
        :param compressed: boolean, set to True when file will be compressed.
        :param compression_format: the format the file will be compressed to.
        :return: None
        """

        if self.__graph is None:
            raise Exception("graph has not been initialized")

        # assemble the path string
        name = "{}//{}.{}".format(directory, name, form)

        # append a compression format if necessary
        if compressed:
            name = "{}.{}".format(name, compression_format)

        if form == 'gml':
            nx.write_gml(self.__graph, name)
        elif form == 'png':
            self.__plot.savefig(name)
        elif form == 'pdf':
            self.__plot.savefig(name, format='pdf')
        elif form == 'eps':
            self.__plot.savefig(name, format='eps')
        elif form == 'svg':
            self.__plot.savefig(name, format='svg')
