# Boolean Query Model

A simple tradional boolean query model which handles the `AND` `OR` `NOT` operations. 

# How to run?
* Different build options - 
  1. normal 
  2. index
  3. stop_words
  4. stemming
  5. lemmatize
  6. wildcard 
   
* NOTE: Default build option is normal

## Build option: Normal

In normal build option - 
1. All the docs will be preprocessed by considering the important preprocessing steps 
2. Zone-Index will be constructed from the preprocessed documents 
3. User can put a query to get the results 

You can use the following command to run - 

`python main.py -q "<query>"` 

`python main.py --query "<query>"`

`python main.py -q "<query>" --norm <norm_type>` : norm_type = "stemming" or "lemmatization"

Query Format - 

1. Enclose each operation in paranthesis to get better results 
2. Query should begin with `(` 
3. Query should end with `)`

Complex Query examples -  
1. (tok1 AND (tok2 OR tok3))
2. ((tok1 AND tok2) OR NOT tok3)
3. (tok1 OR NOT (tok2 OR tok3))


Example - 

`python main.py -q (midsummer AND dream)` 

result- 
```
title               [1]       
meta                [1]       
characters          []        
body                [4, 8, 40]

 FILES - 
docIDs         File Paths     
1              ./dataset/a-midsummer-nights-dream_TXT_FolgerShakespeare.txt
4              ./dataset/as-you-like-it_TXT_FolgerShakespeare.txt
8              ./dataset/henry-iv-part-1_TXT_FolgerShakespeare.txt
40             ./dataset/twelfth-night_TXT_FolgerShakespeare.txt
```

## Build option: stop_words 

Simply gives the output with tokenized docs after removing stop words 

`python main.py -b stop_words` 

will print all docs 

`python main.py -b stop_words -f <path to file>` 

will print a preprocessed specific doc

Example - 
`python main.py -b stop_words -f "./datasset/  a-midsummer-nights-dream_TXT_FolgerShakespeare.txt"`

This will output tokenized document after removing stop_words 

## Build option: index

`python main.py -b index`  

will output the zone index. By default will print first 8 tokens only 

`python main.py -b index --upto n`  

will print first n tokens

## Build option: stemming 

`python main.py -b stemming -f <path to a doc>` 

will output a tokenized preprocessed document after using stemming 

## Build option: lemmatize
`python main.py -b lemmatize -f <path to a doc>` 

will ouput a tokenized preprofcessed doc afer using lemmatization

## Build option: wildcard 
`python main.py -b wildcard -t "<token>"`

Eg - `python main.py -b wildcard -t "he*"`