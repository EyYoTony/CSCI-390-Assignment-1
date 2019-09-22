import nltk
import re
import csv
from nltk.stem import PorterStemmer

# generic functions used within the project
# takes a sentence and returns a tokenized array
def tokenize(sentence):
    return nltk.word_tokenize(sentence)


# takes a word and makes it lowercase
def lowerCase(word):
    return word.lower()


# takes a tokenized word arr and tags the words and retains only nouns, verbs, adjectives, and adverbs - returns tokenized arr
def tag(wordArr):
    newArr = []
    taggedTokens = nltk.pos_tag(wordArr)
    for i in taggedTokens:
        if(re.search("^(NN|VB|JJ|RB)", i[1])):
            newArr.append(i[0])
    return newArr


# takes a string and removes punctuation, this is necessary because punctuation was messing up tokenization
def rmPunctuation(sentence):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    outStr = ""
    for char in sentence:
        if char not in punctuations:
            outStr = outStr + char
    return outStr


def rmStopWords(wordArr):
    # Default English stop words from https://www.ranks.nl/stopwords
    swStardardArr = ['a','about','above','after','again','against','all','am','an','and','any','are','arent','as','at','be','because','been','before','being','below','between','both','but','by','cant','cannot','could','couldnt','did','didnt','do','does','doesnt','doing','dont','down','during','each','few','for','from','further','had','hadnt','has','hasnt','have','havent','having','he','hed','hell','hes','her','here','heres','hers','herself','him','himself','his','how','hows','i','id','ill','im','ive','if','in','into','is','isnt','it','its','its','itself','lets','me','more','most','mustnt','my','myself','no','nor','not','of','off','on','once','only','or','other','ought','our','ours','ourselves','out','over','own','same','shant','she','shed','shell','shes','should','shouldnt','so','some','such','than','that','thats','the','their','theirs','them','themselves','then','there','theres','these','they','theyd','theyll','theyre','theyve','this','those','through','to','too','under','until','up','very','was','wasnt','we','wed','well','were','weve','were','werent','what','whats','when','whens','where','wheres','which','while','who','whos','whom','why','whys','with','wont','would','wouldnt','you','youd','youll','youre','youve','your','yours','yourself','yourselves']
    swCustomArr = ['smart','home','smart-home']
    outArr = []
    for i in wordArr:
        if i not in swStardardArr:
            if i not in swCustomArr:
                outArr.append(i)
    return outArr


def lemmatizeWords(wordArr):
    porter = PorterStemmer()
    newArr = []
    for word in wordArr:
        newArr.append(porter.stem(word))
    return newArr


# This is the main function to format one incoming csv object
# csv object should be in the form [id, role, feature, benefit]
def formatObj(objArr):
    # uses range(1,4) because there isn't a need to tokenize the ID
    for i in range(1, 4):
        objArr[i] = lemmatizeWords(tag(rmStopWords(tokenize(rmPunctuation(lowerCase(objArr[i]))))))
    return objArr


# main running code
stories = []
with open('smarthome-userstories-3k.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        stories.append(formatObj(row))

# removes the title row
del stories[0]

# show output in console
print(*stories, sep="\n")
