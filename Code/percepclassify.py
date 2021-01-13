import os
import sys
import re
import json
import re
import random



#Bring in the params from vanillamodel.txt or averagemodel.txt

model=sys.argv[1]


with open(model) as file:
    params = json.load(file)

vocabulary=params['vocabulary']

Weights_A=params['Weights_A']
Weights_B=params['Weights_B']
bias_A=params['bias_A']
bias_B=params['bias_B']



########################################
stop_words=[
            'other', 'really',
            'been', 'their', 'some', 'more', 'what', 'got', 
            'also', 'here', 'only', 'or', 'which', 'by', 'could', 'even',
            'did', 'after', 'about', 'will', 'just', 'again', 'get',
            'if', 'up', 'us', 'out', 'an', 
            'one', 'are', 'me', 'so', 'all',
            'when', 'would', 'be', 'from', 'as', 'you', 'there', 'have',
            'stay', 'very', 'but', 'our', 'they', 'on', 'had', 'with', 
            'this', 'were', 'is', 'that', 'at', 'my', 'it', 'for',
             'we', 'of', 'in', 'was', 'i', 'a', 'to', 'and', 'the',
             'hotel','hotels', 'do','can','could','them','too']
########################################



#Function for removing values
def remover(list): 
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list] 
    return list







test_path=sys.argv[2]

# Get the list of all files in directory tree at given path
list_of_files = list()
for (dirpath, dirnames, filenames) in os.walk(test_path):
    list_of_files += [os.path.join(dirpath, file) for file in filenames]
    
#Create list of all the pathnames of text files in the Test directory
all_text_files=list()
for i in list_of_files:
    if i[-4:] == '.txt':
        all_text_files.append(i)

#Remove the README file if it is present
all_text_files = [ x for x in all_text_files if "README.txt" not in x ]

#Create new txt file
text_file = open("percepoutput.txt", "w")

for file in all_text_files:   #This is where we starg going through the test txt files
    file_path=file    #NOTE: This is the filepath you will add to the txt file
    test_list=''
    file = open(file, 'r')
    lines=file.readlines()
    for line in lines:
        line=line.rstrip()    #Get rid of newline characters
        line = re.sub(r'[^\w\s]','',line)    #Remove punctuation
        line=line.lower()    #Make all words lowercase
        test_list=test_list+' '+line

    ######Let's Make some Prediction!!!####
    test_list=test_list.split(' ')   #Turn the file into a list of words in it
    test_list = remover(test_list)    #Remove all numbers from the list
    test_list = [i for i in test_list if i]     #Remove empty strings '' from list


    ###################################################
    for i in stop_words:
        try:
            test_list.remove(i)
        except:
            continue

    ###################################################

    
    #Remove words not in the vocabulary
    features=dict()    #Creating the dictionary of the features for the document so we can calculate the activation
    for word in test_list:
        features[word]=features.get(word,0)+1
    
    #Calculate the activation for both classes to determine the class 
    activation_A=0
    activation_B=0
    for word, count in features.items():
        if word not in vocabulary:
            continue
        
        product_A = count * Weights_A[word]
        activation_A = activation_A + product_A
        
        product_B = count * Weights_B[word]
        activation_B = activation_B + product_B
    
    
    activation_A = activation_A + bias_A
    activation_B = activation_B + bias_B
    
    
    #Set the labels
    if activation_A >= 0:
        label_a = 'truthful'
    else:
        label_a = 'deceptive'
        
    if activation_B >= 0:
        label_b = 'positive'
    else:
        label_b = 'negative'
        
    text_file.write(label_a+' '+label_b+' '+file_path+'\n')
    