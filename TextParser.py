import re
import networkx as nx
from matplotlib import pyplot as plt
from pylab import rcParams

rcParams['figure.figsize'] = 10, 10

class TextParser:

    def __init__(self, inp = False, min_freq = 40, char_lim = float("inf"), labels = False, char_label_limit = 35):
        self.char_lim = char_lim
        self.min_freq = min_freq
        self.character_list = []
        self.labels = labels

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

        if len(self.character_list) >= char_label_limit:
            self.labels = False

        self.graph = self.initialize_graph()
        self.dict = self.initialize_character_dict()
        return

    def get_characters(self, name_string):
        list = name_string.split(',')
        return list

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
        print(self.character_list)

    def print_graph(self):
        self.clean()
        node_labels = nx.get_node_attributes(self.graph, 'name')
        edge_labels = nx.get_edge_attributes(self.graph, 'frequency')
        d = []
        nodes = self.graph.nodes(data=True)
        for i in range(0, len(self.graph.nodes())):
            if self.graph.has_node(i):
                d.append(int(self.graph.node[i]['frequency']))
        dlen = len(d)
        nx.draw(self.graph,pos=nx.circular_layout(self.graph), labels = node_labels, node_color='r' ,with_labels=True, node_size=[(v * 200)/(dlen + 5) for v in d])

        edges = self.graph.edges()
        weights = [0.5 * self.graph[u][v]['weight'] for u, v in edges]
        wlen = len(weights)
        colors = range(wlen)
        nx.draw_networkx_edges(self.graph, pos = nx.circular_layout(self.graph), edgelist= edges, width=[(6 * self.graph[u][v]['weight'])/wlen for u, v in edges],edge_cmap=plt.cm.Greens,edge_color=colors)
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
        delimiters = ",", " ", ".", "\n", ";", "; ", ": "
        regex_pattern = '|'.join(map(re.escape, delimiters))
        words = re.split(regex_pattern, line)

        for current_word in words:
            if current_word in self.character_list:
                current_name = current_word
                self.increment_name_frequency(current_name)
                for activeName in active:
                    if activeName != current_name:
                        self.add_edge(activeName, current_name)
                active[current_name] = 15
            for activeName in active:
                active[activeName] -= 1
            for activeName in active:
                if active[activeName] == 0:
                    del active[activeName]
                    break

    def detect_characters(self, file):
        with open(file) as f:
            lines = f.read().replace('\n', ' ')
            past_verbs = ['said', 'shouted', 'exclaimed', 'remarked', 'quipped', 'whispered', 'yelled', 'announced']
            matches = []

            for i in range(0, len(past_verbs)):
                pattern = '[A-Z][\w]+ ' + past_verbs[i] + '|' + past_verbs[i] + ' [A-Z][\w]+'
                match = re.findall(pattern, lines)
                for j in range(0, len(match)):
                    match[j] = match[j].replace(' ' + past_verbs[i], '')
                    match[j] = match[j].replace(past_verbs[i] + ' ', '')
                matches.extend(match)

            omitted = set(["He","She","It","They","You","Mr","Mrs","Miss","Lord","Professor","Uncle","Aunt"])
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