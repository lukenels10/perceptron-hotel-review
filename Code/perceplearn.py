import os
import sys
import re
import json
import re
import random

path=sys.argv[1]

directory=os.listdir(path)   #Ex. ['.DS_Store', 'LICENSE', 'positive_polarity', 'README.md', 'README.txt', 'negative_polarity']

#Class types
positive='positive'
negative='negative'

deceptive='deceptive'
truthful='truthful'


################################
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

##################################


#Positive and Negative Folders    ex. 'positive_path'
    #variabl for positive is positive_folder
    #variable for negative is negative_folder
for i in directory:
    if positive in i:
        positive_folder=i
    if negative in i:
        negative_folder=i

#Positive and Negative Paths    ex. '/Users/lukenelson/Desktop/CSCI_544/Homework/Assignment_3/My_Codes/Testing/op_spam_training_data/positive_polarity'
positive_path=os.path.join(path, positive_folder)
negative_path=os.path.join(path, negative_folder)

positive_directory=os.listdir(positive_path)
negative_directory=os.listdir(negative_path)

#Deceptive and Truthful folders
for i in positive_directory:
    if deceptive in i:
        deceptive_folder_1=i
    if truthful in i:
        truthful_folder_1=i

for i in negative_directory:
    if deceptive in i:
        deceptive_folder_2=i
    if truthful in i:
        truthful_folder_2=i
        
#Deceptive and Truthful Paths and Directories
positive_deceptive_path=os.path.join(positive_path, deceptive_folder_1)
negative_deceptive_path=os.path.join(negative_path, deceptive_folder_2)

positive_truthful_path=os.path.join(positive_path, truthful_folder_1)
negative_truthful_path=os.path.join(negative_path, truthful_folder_2)

#Final 4 Directories    ex. ['fold2', 'fold4', 'fold3']
positive_deceptive_directory=os.listdir(positive_deceptive_path)    
positive_truthful_directory=os.listdir(positive_truthful_path)

negative_deceptive_directory=os.listdir(negative_deceptive_path)
negative_truthful_directory=os.listdir(negative_truthful_path)

#Remove '.DS_Store' from directories
try:
    positive_deceptive_directory.remove('.DS_Store')
    positive_truthful_directory.remove('.DS_Store')
    negative_deceptive_directory.remove('.DS_Store')
    negative_truthful_directory.remove('.DS_Store')
except:
    pass











#DESIGNATIONS#
#Positive (+1) / Negative (-1)
#Truthful (+1) / Deceptive (-1)


#Store all documents
#Create lists and dictionaries of all documents
all_paths_list=list()    #List of all the pathways to all documents
all_paths_dict=dict()    #Dictionary of all file paths as key and class designations. See designations above

def store_files(path, classes):
    temp_files=list()    #This is all files but we only want the text files
    for (dirpath, dirnames, filenames) in os.walk(path):
        temp_files += [os.path.join(dirpath, file) for file in filenames]

    for i in temp_files:    #Take only the text files from the path and add them to the all_paths_list
        if i[-4:] == '.txt':
            all_paths_list.append(i)
            
            #Now create the dictionary of classes for each path
            if classes == 'positive_truthful_path':
                all_paths_dict[i]=[1,1]
                
            if classes == 'positive_deceptive_path':
                all_paths_dict[i]=[1,-1]
                
            if classes == 'negative_truthful_path':
                all_paths_dict[i]=[-1,1]
                
            if classes == 'negative_deceptive_path':
                all_paths_dict[i]=[-1,-1]
            

#Run the function on all 4 classes
store_files(positive_truthful_path,'positive_truthful_path')
store_files(positive_deceptive_path,'positive_deceptive_path')
store_files(negative_truthful_path,'negative_truthful_path')
store_files(negative_deceptive_path,'negative_deceptive_path')
        








#Function for removing values
def remover(list): 
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list] 
    return list







#Step 1: Create a list of the vocabularity
#Step 2: Create a dictionary of the weights which is the vocabularity, each starting with 0

all_instances=dict()    #nested dictionary of the form: {path1:{'dog':2,'cat':3,'mouse':1},path2:{}.....}
vocabulary=''

for document in all_paths_list:
    file = open(document, 'r')
    lines=file.readlines()
    doc_words=''    #Saving all the words from a given document so we can create the instances dictionary
    for line in lines:
        line=line.rstrip()    #Get rid of newline characters
        line = re.sub(r'[^\w\s]','',line)    #Remove punctuation
        line=line.lower()    #Make all words lowercase
        doc_words=doc_words+' '+line
        vocabulary=vocabulary+' '+line
        #print(line, 'END!!!!')
    doc_words=doc_words.split(' ')
    doc_words = remover(doc_words)    #Remove all numbers from the list
    doc_words = [i for i in doc_words if i]     #Remove empty strings '' from list

    ###############################
    for i in stop_words:
        try:
            doc_words.remove(i)
        except:
            continue
    ##############################



    instance=dict()    #create the nested dictionary of the word counts from doc_words
    for i in doc_words:    #Create wordcount of each word in doc_words
        instance[i]=instance.get(i,0)+1
    all_instances[document]=instance    #Add the dictionary of word counts with the pathname as the key to all_instances
    
    

#print(vocabulary)     
vocabulary=vocabulary.split(' ')    #Turn the vocabulary into a list of words
vocabulary=remover(vocabulary)    #Remove all number values
vocabulary = [i for i in vocabulary if i]    #Remove all empty strings from the list



#####################
for i in stop_words:
    try:
        vocabulary.remove(i)
    except:
        continue
##################################

vocabulary=list(set(vocabulary))
try:
    vocabulary.remove('')
except:
    pass

#Now create the vocabulary dictionary of weights
vocabulary_weights=dict()
for word in vocabulary:
    vocabulary_weights[word]=0
    

Class_A_Weights=vocabulary_weights.copy()    #Truthful / Deceptive
Class_B_Weights=vocabulary_weights.copy()    #Positive / Negative
cached_Weights_A=vocabulary_weights.copy()
cached_Weights_B=vocabulary_weights.copy()








#####VANILLA ICE####
#Variable Contents

    #vocabulary_weights -> your weight vector
    
    #Class_A_Weights ->    #Truthful / Deceptive
    
    #Class_B_Weights ->    #Positive / Negative
    
    #all_paths_list -> the list of all document filepaths
    
    #all_instances ->    nested dictionary of the form: {path1:{'dog':2,'cat':3,'mouse':1},path2:{}.....}
    
    #all_paths_dict ->    #Dictionary of all file paths as key and class designations.


#Lets make this perceptron baby!
bias_A = 0
bias_B = 0
cached_bias_A = 0
cached_bias_B = 0
c=1

iterations=20

#Do the Vanilla for Class A and B
for i in range(iterations):
    paths=all_paths_list.copy()
    random.shuffle(paths)    #Shuffle the order of the documents with every iteration
    for path in paths:
        #positive/negative
        #multiply the document instance vector by the weight vector and add the bias term
        activation_A = 0
        activation_B = 0
        features=all_instances[path]    #Get just the dictionary of feature words for this path
        classes=all_paths_dict[path]    #This is a list of the two classes [1,-1]
        for word, count in features.items():
            #print('word:',word,'count:',count)
            product_A = count * Class_A_Weights[word]
            activation_A = activation_A + product_A
            
            product_B = count * Class_B_Weights.get(word)
            activation_B = activation_B + product_B
            
            
        activation_A = activation_A + bias_A    #Add the bias to get the total activation
        activation_B = activation_B + bias_B
        
        #Determine whether or not to update the weights and bias
        if activation_A > 0 and classes[1]==1:
            pass
        if activation_A < 0 and classes[1]==-1:
            pass
        if activation_A <= 0 and classes[1]==1:
            for word, count in features.items():
                Class_A_Weights[word]=Class_A_Weights[word]+count
                cached_Weights_A[word]=cached_Weights_A[word] + (c * count)
            bias_A = bias_A + 1
            cached_bias_A = cached_bias_A + c
        if activation_A >= 0 and classes[1] == -1:
            for word, count in features.items():
                Class_A_Weights[word]=Class_A_Weights[word]-count
                cached_Weights_A[word]=cached_Weights_A[word] - (c * count)
            bias_A = bias_A - 1
            cached_bias_A = cached_bias_A - c
                
                
        if activation_B > 0 and classes[0]==1:
            pass
        if activation_B < 0 and classes[0]==-1:
            pass
        if activation_B <= 0 and classes[0]==1:
            for word, count in features.items():
                Class_B_Weights[word]=Class_B_Weights[word]+count
                cached_Weights_B[word]=cached_Weights_B[word] + (c * count)
            bias_B = bias_B + 1
            cached_bias_B = cached_bias_B + c
        if activation_B >= 0 and classes[0] == -1:
            for word, count in features.items():
                Class_B_Weights[word]=Class_B_Weights[word]-count
                cached_Weights_B[word]=cached_Weights_B[word] - (c * count)
            bias_B=bias_B - 1
            cached_bias_B = cached_bias_B - c
        
        c = c + 1
        









#The final dictionary of averaged weights that we will use to predict
Average_Weights_A=dict()
Average_Weights_B=dict()

for word, count in cached_Weights_A.items():
    Average_Weights_A[word] = Class_A_Weights[word] - (count/c)
    
for word, count in cached_Weights_B.items():
    Average_Weights_B[word] = Class_B_Weights[word] - (count/c)

Average_bias_A = bias_A - (cached_bias_A/c)
Average_bias_B = bias_B - (cached_bias_B/c)











#Save your files into 1 dictionary and then put that dictionary into a text file


###For the AVERAGE####
#vocabulary
#Average_Weights_A
#Average_Weights_B
#Average_bias_A
#Average_bias_B

average_params=dict()

average_params['vocabulary']=vocabulary
average_params['Weights_A']=Average_Weights_A
average_params['Weights_B']=Average_Weights_B
average_params['bias_A']=Average_bias_A
average_params['bias_B']=Average_bias_B









###For the Vanilla###
#vocabulary
#Class_A_weights
#Class_B_weights
#bias_A
#bias_B

vanilla_params=dict()

vanilla_params['vocabulary']=vocabulary
vanilla_params['Weights_A']=Class_A_Weights
vanilla_params['Weights_B']=Class_B_Weights
vanilla_params['bias_A']=bias_A
vanilla_params['bias_B']=bias_B





#Vanilla
#Write the params dictionary to a text file
with open('vanillamodel.txt', 'w') as file:
     file.write(json.dumps(vanilla_params)) # use `json.loads` to do the reverse
file.close()

#Average
#Write the params dictionary to a text file
with open('averagedmodel.txt', 'w') as file:
     file.write(json.dumps(average_params)) # use `json.loads` to do the reverse
file.close()










