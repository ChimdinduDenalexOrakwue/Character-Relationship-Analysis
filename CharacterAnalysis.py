from TextParser import TextParser as tp

parser = tp(min_freq = 80, labels = True)

parser.add_characters([])
parser.add_locations([])
parser.add_objects([])

parser.print_characters()
parser.print_locations()
parser.print_objects()

parser.read_file()
parser.print_graph()