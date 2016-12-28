from TextParser import TextParser as tp

parser = tp(min_freq = 0, labels = True)
parser.add_characters([])
parser.add_locations([])
parser.add_objects([])

parser.read_file()

print("\nTOTAL CHARACTERS: " + str(parser.get_num_characters()))
parser.print_characters()
parser.print_locations()
parser.print_objects()
#print("SHORTEST PATH: " + str(parser.get_shortest_path("", "")))
parser.print_graph()
