from TextParser import TextParser as tp

parser = tp(min_freq = 120, labels = True)

parser.add_locations(["Hogwarts","Deathly Hallows"])
parser.add_objects(["Horcrux","Wand"])

parser.print_characters()
parser.print_locations()
parser.print_objects()

parser.read_file()
parser.print_graph()