from TextParser import TextParser as tp

parser = tp(min_freq = 120, labels = True)

parser.add_location("Hogwarts")
parser.add_location("Deathly Hallows")

parser.add_object("Horcrux")
parser.add_object("Wand")

parser.print_characters()
parser.print_locations()
parser.print_objects()

parser.read_file()
parser.print_graph()