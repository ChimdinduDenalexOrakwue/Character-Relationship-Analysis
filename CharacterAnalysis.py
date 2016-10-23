from TextParser import TextParser as tp
import matplotlib


#parser = tp(lim=1,labels=True)
parser = tp(lim=40,labels=True)
#parser = tp(lim=100,labels=True)
parser.printCharacters()
parser.readFile()
parser.printGraph()