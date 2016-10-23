import networkx as nx
import re
from matplotlib import pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 10, 10

class TextParser:

    def __init__(self, inp=False, lim = 0,labels = False):
        while(True):
            try:
                self.file = input("Input a path to a text file: ")
                break;
            except FileNotFoundError:
                print ("This file does not exist.")
        self.lim = lim
        self.characterList = []
        self.labels=labels

        if (inp):
            self.characterList = self.getCharacters(input("Input character names seperated by commas: "))
        else:
            self.characterList = self.detectCharacters(self.file)

        if(len(self.characterList) >= 35):
            self.labels = False

        self.graph = self.initializeGraph()
        self.dict = self.initializeCharacterDict()

        return

    def getCharacters(self, name_string):
        list = name_string.split(',')
        return list

    def initializeCharacterDict(self):
        dict = {}
        for i in range(0, len(self.characterList)):
            dict[self.characterList[i]] = i
        return dict

    def initializeGraph(self):
        graph = nx.Graph()
        for i in range(0, len(self.characterList)):
            graph.add_node(i, {'name' : self.characterList[i], 'frequency' : 1})
        return graph

    def incrementNameFrequency(self, name, amount = 1):
        newFrequency = self.graph.node[self.dict[name]]['frequency'] + amount
        self.graph.node[self.dict[name]]['frequency'] = newFrequency
        return

    def addEdge(self, name1, name2):
        if self.graph.has_edge(self.dict[name1], self.dict[name2]):
            newFrequency = self.graph.get_edge_data(self.dict[name1], self.dict[name2])['frequency'] + 1;
            newWeight = self.graph.get_edge_data(self.dict[name1], self.dict[name2])['weight'] + 1;
            self.graph.add_edge(self.dict[name1], self.dict[name2], frequency=newFrequency, weight = newWeight)
            pass
        else:
            self.graph.add_edge(self.dict[name1], self.dict[name2], frequency = 1, weight=1)
        return

    def printCharacters(self):
        print(self.characterList)

    def printGraph(self):
        self.clean()
        node_labels = nx.get_node_attributes(self.graph, 'name')
        edge_labels = nx.get_edge_attributes(self.graph, 'frequency')
        d=[]
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

    def addCharacter(self, name):
        self.characterList.append(name)
        return

    def readFile(self):
        with open(self.file) as f:
            content = f.readlines()
            for line in content:
                self.word_is_name(line)
        return

    def word_is_name(self, line):
        active = {}
        delimiters = ['\n', ' ', ',', '.', '?', '!', ':']
        words = line.split()
        for delimiter in delimiters:
            new_words = []
            for word in words:
                new_words += word.split(delimiter)
            words = new_words

        for current_word in words:
            if current_word in self.characterList:
                current_name = current_word
                self.incrementNameFrequency(current_name)
                for activeName in active:
                    if activeName != current_name:
                        self.addEdge(activeName, current_name)
                active[current_name] = 15
            for activeName in active:
                active[activeName] -= 1
            for activeName in active:
                if active[activeName] == 0:
                    del active[activeName]
                    break

    def detectCharacters(self, file):
        with open(file) as f:
            lines = f.read().replace('\n', ' ')
            pattern = '[A-Z][\w]+ said|said [A-Z][\w]+'
            matches = re.findall(pattern, lines)
            matches = list(set(matches))
            matches = [word for word in matches if "He" not in word and "She" not in word and "It" not in word and "They" not in word and "You" not in word and "Mr" not in word]
            for i in range(0, len(matches)):
                matches[i] = matches[i].replace('said', '')
                matches[i] = matches[i].strip()

            name_set = list(set(matches))
            matches = []
            for i in range(0,len(name_set)):
                matches.append(name_set[i])
                if i >= 80:
                    break
        return matches

    def clean(self):
        nodes = self.graph.nodes(data=True)
        toDelete = []
        for i in range(0,len(nodes)):
            if int(self.graph.node[i]['frequency']) < self.lim:
                toDelete.append(i)
        toDelete.reverse()
        self.graph.remove_nodes_from(toDelete)