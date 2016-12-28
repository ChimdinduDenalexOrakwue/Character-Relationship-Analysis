import re
import networkx as nx
from matplotlib import pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12, 12


class TextParser:

    def __init__(self, inp = False, min_freq = 40, char_lim = float("inf"),
                 labels = False, char_label_lim = 40):
        self.char_lim = char_lim
        self.min_freq = min_freq
        self.character_list = []
        self.location_list = []
        self.object_list = []
        self.labels = labels
        self.file = None
        self.inp = inp
        self.char_label_lim = char_label_lim
        return


    def get_characters(self, name_string):
        if name_string == None:
            return []
        if len(name_string) == 0:
            return []
        characters = name_string.split(',')
        characters = [name.strip() for name in characters]
        return characters

    def initialize_dict(self):
        dict = {}
        dict_counter = 0

        for i in range(0, len(self.character_list)):
            dict[self.character_list[i]] = dict_counter
            dict_counter += 1

        for i in range(0, len(self.location_list)):
            dict[self.location_list[i]] = dict_counter
            dict_counter += 1

        for i in range(0, len(self.object_list)):
            dict[self.object_list[i]] = dict_counter
            dict_counter += 1

        return dict


    def initialize_graph(self):
        graph = nx.Graph()
        node_counter = 0

        for i in range(0, len(self.character_list)):
            graph.add_node(node_counter, {'name' : self.character_list[i], 'frequency' : 1, 'category' : 'character'})
            node_counter += 1

        for i in range(0, len(self.location_list)):
            graph.add_node(node_counter, {'name' : self.location_list[i], 'frequency' : 1, 'category' : 'location'})
            node_counter += 1

        for i in range(0, len(self.object_list)):
            graph.add_node(node_counter, {'name' : self.object_list[i], 'frequency' : 1, 'category' : 'object'})
            node_counter += 1

        return graph


    def increment_name_frequency(self, name, amount = 1):
        newFrequency = self.graph.node[self.dict[name]]['frequency'] + amount
        self.graph.node[self.dict[name]]['frequency'] = newFrequency
        return


    def add_edge(self, name1, name2):
        if self.graph.has_edge(self.dict[name1], self.dict[name2]):
            newFrequency = self.graph.get_edge_data(self.dict[name1], self.dict[name2])['frequency'] + 1;
            newWeight = self.graph.get_edge_data(self.dict[name1], self.dict[name2])['weight'] + 1;
            self.graph.add_edge(self.dict[name1], self.dict[name2], frequency=newFrequency, weight = newWeight)
            pass
        else:
            self.graph.add_edge(self.dict[name1], self.dict[name2], frequency = 1, weight=1)
        return


    def print_characters(self):
        print("CHARACTER LIST: " + str(self.character_list))


    def print_locations(self):
        print("LOCATION LIST: " + str(self.location_list))


    def print_objects(self):
        print("OBJECT LIST: " + str(self.object_list))


    def print_graph(self):
        self.clean_graph()
        node_labels = nx.get_node_attributes(self.graph, 'name')
        edge_labels = nx.get_edge_attributes(self.graph, 'frequency')
        color_map = {'character': 'r', 'location': '#FF0099', 'object': '#00a1ff'}
        d = []

        for i in range(0, len(self.graph.nodes())):
            if self.graph.has_node(i):
                d.append(int(self.graph.node[i]['frequency']))
        dlen = len(d)
        nx.draw(self.graph, pos=nx.circular_layout(self.graph), labels = node_labels,
                node_color = [color_map[self.graph.node[node]['category']] for node in self.graph], with_labels=True,
                node_size=[(v * 180)/(dlen + 5) for v in d])

        edges = self.graph.edges()
        weights = [self.graph[u][v]['weight'] for u, v in edges]
        nx.draw_networkx_edges(self.graph, pos = nx.circular_layout(self.graph), edgelist = edges,
                               width=[(50 * self.graph[u][v]['weight'])/sum(weights) for u, v in edges],
                               edge_cmap=plt.cm.winter,edge_color=weights)

        if self.labels:
            nx.draw_networkx_edge_labels(self.graph,pos=nx.circular_layout(self.graph),edge_labels=edge_labels)

        plt.show(block=True)


    def add_character(self, name):
        self.character_list.append(name)
        return


    def add_characters(self, names):
        if names != None:
            self.character_list.extend(names)
            return self.character_list
        else:
            return self.character_list


    def add_location(self, location):
        self.location_list.append(location)
        return self.location_list


    def add_locations(self, locations):
        self.location_list.extend(locations)
        return self.location_list


    def add_object(self, obj):
        self.object_list.append(obj)
        return self.object_list


    def add_objects(self, objs):
        self.object_list.extend(objs)
        return self.object_list


    def read_file(self, file=None):
        if file != None:
            self.file = file
            try:
                if (self.inp):
                    self.character_list = self.add_characters(self.get_characters(input("INPUT CHARACTER NAMES SEPARATED BY COMMAS: ")))
                else:
                    self.character_list = self.detect_characters(self.file)
            except FileNotFoundError:
                print("\nERROR: the file " + self.file + " could not be found.\n")
        else:
            while True:
                try:
                    self.file = input("INPUT A PATH TO A TEXT FILE: ")
                    if (self.inp):
                        self.character_list = self.add_characters(self.get_characters(input("INPUT CHARACTER NAMES SEPARATED BY COMMAS: ")))
                    else:
                        self.character_list = self.detect_characters(self.file)
                    break
                except FileNotFoundError:
                    print ("\nERROR: the file " + self.file + " could not be found.\n")

        self.graph = self.initialize_graph()
        self.dict = self.initialize_dict()

        with open(self.file) as f:
            content = f.readlines()
            for line in content:
                self.parse_line(line)
        return


    def parse_line(self, line):
        active = {}
        delimiters = ",", " ", ".", "\n", ";", "; ", ": ", "\""
        regex_pattern = '|'.join(map(re.escape, delimiters))
        words = re.split(regex_pattern, line)
        name_list = set([name.lower() for name in self.character_list])
        location_list = set([location.lower() for location in self.location_list])
        object_list = set([obj.lower() for obj in self.object_list])

        for current_word in words:
            current_name = ""
            if current_word.lower() in name_list:
                for i in range(0, len(self.character_list)):
                    if current_word.lower() == self.character_list[i].lower():
                        current_name = self.character_list[i]
                self.increment_name_frequency(current_name)
                for active_name in active:
                    if active_name != current_name:
                        self.add_edge(active_name, current_name)
                active[current_name] = 15

            if current_word.lower() in location_list:
                for i in range(0, len(self.location_list)):
                    if current_word.lower() == self.location_list[i].lower():
                        current_name = self.location_list[i]
                self.increment_name_frequency(current_name)
                for active_name in active:
                    if active_name != current_name:
                        self.add_edge(active_name, current_name)
                active[current_name] = 40

            if current_word.lower() in object_list:
                for i in range(0, len(self.object_list)):
                    if current_word.lower() == self.object_list[i].lower():
                        current_name = self.object_list[i]
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


    def detect_characters(self, file):
        with open(file) as f:
            lines = f.read().replace('\n', ' ')
            past_verbs = ['said', 'shouted', 'exclaimed', 'remarked', 'quipped', 'whispered',
                          'yelled','yelped', 'announced','muttered','asked','inquired','cried','answered',
                          'interposed','interrupted','suggested','thought','called','added','began','observed',
                          'echoed','repeated','shrugged','pointed','argued','promised','noted',
                          'mentioned','replied','screamed','grumbled','stammered','screeched',
                          'questioned','pleaded','proclaimed','professed','moaned','spouted',
                          'surmised','murmured','voiced','urged','wept','rambled','ranted',
                          'decided','demanded','wailed','chuckled','chanted','boasted','coaxed',
                          'blurted','lectured','hinted','barked','rebuffed','kissed','ran','walked',
                          'swung','lifted','charged','sped','crept','restrained','droned','uttered',
                          'took','yanked','collapsed','tumbled','crumpled','screeched','glided',
                          'trudged','limped','hesitated','erupted','stampeded','created','started',
                          'created','initiated','ended','chided','reached','glanced']
            matches = []

            for i in range(0, len(past_verbs)):
                pattern = '[A-Z][\w]+ ' + past_verbs[i] + '|' + past_verbs[i] + ' [A-Z][\w]+'
                match = re.findall(pattern, lines)
                for j in range(0, len(match)):
                    match[j] = match[j].replace(' ' + past_verbs[i], '')
                    match[j] = match[j].replace(past_verbs[i] + ' ', '')
                matches.extend(match)

            omitted = {"He","She","It","They","You","Mr","Mrs","Miss","Lord"
                ,"Professor","Uncle","Aunt","Then",'I','We','When','If','Others','Some'
                ,"In","And","On","An","What","His","Her","Have","That","But","Not"
                ,"This","The","You","Your","Or","My","So","Nearly","Who","YOU","Another"
                ,"Having","Everyone","One","No","Someone","All","Both","Never","Nobody"
                ,"Did","Such","At","Other","Their","Our","By","Nothing","Which","Where"
                ,"Were","Here","Well","Do","Either","There","Now"}

            matches = [word for word in matches if word not in omitted]

            name_set = list(set(matches))
            matches = []
            for i in range(0,len(name_set)):
                matches.append(name_set[i])
                if i >= self.char_lim:
                    break

        return matches


    def clean_graph(self):
        nodes = self.graph.nodes(data=True)
        to_delete = []
        for i in range(0,len(nodes)):
            if int(self.graph.node[i]['frequency']) < self.min_freq and self.graph.node[i]['category'] == 'character':
                to_delete.append(i)
        to_delete.reverse()
        self.graph.remove_nodes_from(to_delete)

        if self.graph.size() >= self.char_label_lim:
            self.labels = False

    def get_frequency(self, name):
        if self.graph == None:
            return 0
        if name not in self.dict:
            return 0
        return int(self.graph.node[self.dict[name]]['frequency'])

    def get_num_connections(self, name_one, name_two):
        if self.graph == None:
            return 0
        if name_one not in self.dict or name_two not in self.dict:
            return 0
        return int(self.graph.get_edge_data(self.dict[name_one], self.dict[name_two])['frequency'])

    def get_num_characters(self):
        return len(self.character_list)

    def get_shortest_path(self, name_one, name_two):
        if self.graph == None:
            return []
        elif name_one not in self.dict or name_two not in self.dict:
            return []
        else:
            num_path = nx.shortest_path(self.graph, source=self.dict[name_one], target=self.dict[name_two], weight=None)
            path = [self.graph.node[i]['name'] for i in num_path]
            return path