from TextParser import TextParser as tp

parser = tp(min_freq = 40, labels = True)

parser.print_characters()
parser.read_file()
parser.print_graph()