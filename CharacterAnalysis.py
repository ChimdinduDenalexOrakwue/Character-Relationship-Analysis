from TextParser import TextParser as tp
import matplotlib


#parser = tp(lim=1,labels=True)
parser = tp(min_freq = 250, labels = True)
#parser = tp(lim=100,labels=True)
parser.print_characters()
parser.read_file()
parser.print_graph()