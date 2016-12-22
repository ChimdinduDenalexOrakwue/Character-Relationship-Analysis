import re
import networkx as nx
from matplotlib import pyplot as plt
from pylab import rcParams
import requests
rcParams['figure.figsize'] = 10, 10


class TextParser:

    def __init__(self, inp = False, min_freq = 40, char_lim = float("inf"),
                 labels = False, char_label_lim = 35, file=""):
        self.char_lim = char_lim
        self.min_freq = min_freq
        self.character_list = []
        self.labels = labels
        self.file = file
        self.char_label_lim = char_label_lim

        if len(file) > 0:
            try:
                if (inp):
                    self.character_list = self.get_characters(input("INPUT CHARACTER NAMES SEPARATED BY COMMAS: "))
                else:
                    self.character_list = self.detect_characters(self.file)
            except FileNotFoundError:
                print("\nERROR: the file " + self.file + " could not be found.\n")
        else:
            while True:
                try:
                    self.file = input("INPUT A PATH TO A TEXT FILE: ")
                    if (inp):
                        self.character_list = self.get_characters(input("INPUT CHARACTER NAMES SEPARATED BY COMMAS: "))
                    else:
                        self.character_list = self.detect_characters(self.file)
                    break
                except FileNotFoundError:
                    print ("\nERROR: the file " + self.file + " could not be found.\n")

        self.graph = self.initialize_graph()
        self.dict = self.initialize_character_dict()
        return


    def get_characters(self, name_string):
        characters = name_string.split(',')
        characters = [name.strip() for name in characters]
        return characters

    def initialize_character_dict(self):
        dict = {}
        for i in range(0, len(self.character_list)):
            dict[self.character_list[i]] = i
        return dict


    def initialize_graph(self):
        graph = nx.Graph()
        for i in range(0, len(self.character_list)):
            graph.add_node(i, {'name' : self.character_list[i], 'frequency' : 1})
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
        print("POTENTIAL CHARACTERS DETECTED: " + str(self.character_list))


    def print_graph(self):
        self.clean()
        node_labels = nx.get_node_attributes(self.graph, 'name')
        edge_labels = nx.get_edge_attributes(self.graph, 'frequency')
        d = []

        for i in range(0, len(self.graph.nodes())):
            if self.graph.has_node(i):
                d.append(int(self.graph.node[i]['frequency']))
        dlen = len(d)
        nx.draw(self.graph,pos=nx.circular_layout(self.graph), labels = node_labels, node_color='r' ,with_labels=True, node_size=[(v * 180)/(dlen + 5) for v in d])

        edges = self.graph.edges()
        weights = [self.graph[u][v]['weight'] for u, v in edges]
        nx.draw_networkx_edges(self.graph, pos = nx.circular_layout(self.graph), edgelist= edges, width=[(50 * self.graph[u][v]['weight'])/sum(weights) for u, v in edges],edge_cmap=plt.cm.winter,edge_color=weights)
        if self.labels:
            nx.draw_networkx_edge_labels(self.graph,pos=nx.circular_layout(self.graph),edge_labels=edge_labels)
        plt.show(block=True)


    def add_character(self, name):
        self.character_list.append(name)
        return


    def read_file(self):
        with open(self.file) as f:
            content = f.readlines()
            for line in content:
                self.word_is_name(line)
        return


    def word_is_name(self, line):
        active = {}
        delimiters = ",", " ", ".", "\n", ";", "; ", ": ", "\""
        regex_pattern = '|'.join(map(re.escape, delimiters))
        words = re.split(regex_pattern, line)
        name_list = [name.lower() for name in self.character_list]

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
                          'yelled', 'announced','muttered','asked','inquired','cried']
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
                ,"Having","Everyone","One","No","Someone","All","Both"}

            matches = [word for word in matches if word not in omitted]

            name_set = list(set(matches))
            matches = []
            for i in range(0,len(name_set)):
                matches.append(name_set[i])
                if i >= self.char_lim:
                    break
        return matches


    def clean(self):
        nodes = self.graph.nodes(data=True)
        to_delete = []
        for i in range(0,len(nodes)):
            if int(self.graph.node[i]['frequency']) < self.min_freq:
                to_delete.append(i)
        to_delete.reverse()
        self.graph.remove_nodes_from(to_delete)

        if self.graph.size() >= self.char_label_lim:
            self.labels = False