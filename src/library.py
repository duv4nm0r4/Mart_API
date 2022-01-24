import re
from flask import jsonify
import validators
import pymongo
from pymongo import MongoClient

class ListWords:
    def __init__(self, listW):
        #Pasar todos los terminos de la lista a texto y eliminar los repetidos.
        listW=list(set(map(str,listW)))
        #Ordenar la lista
        listW.sort()
        #Atributo list -> datos de ingreso filtrados.
        self.list=listW                               

        #Atributo longer -> Longitud de la palabra más larga de la lista. 
        longer=list(map(lambda x:len(x),self.list))
        longer.sort(reverse = True)
        self.longer=longer[0]

        #Atributo longWords -> Palabras de longitud máxima.
        self.longWords=list(filter(lambda x:len(x)==self.longer, self.list))

    def long_words_analysis(self):
        longWords_analysis={}
        for w in self.longWords: #Analizo cada palabra del arreglo longWord (Palabras más largas) y agrego rtas a longWords_analysis
            longWords_analysis.update({w:word_analysis(w)}) 
        return longWords_analysis
    
    def domain_URL (self): #Ingresa arreglo de palabras y determina si es una URL. Si es así selecciona el dominio y lo analiza.
        url_analysis={}
        for w in self.longWords:
            if validators.url(w):
                w=w.split(".")[1] #Filtre solo el dominio
                url_analysis.update({w:word_analysis(w)})
        return url_analysis
    
    def martSearch (self):
        #If the “MART” String appears in one of the words of the input list, show it in the response.
        #Retorna arreglo con el filtrado de todas las palabras de la lista dejando solo las que contienen "mart", no tiene en cuenta mayúsculas.
        return list(filter(lambda word:re.search("mart", word.lower()), self.list))



def  letters_used (word):
    lettersUsed={}
    #Selecciono las letras y cuento una a una
    for letter in set(word):  
        countLetter=word.count(letter)
        lettersUsed.update({letter: countLetter})
    #Retorna un diccionario con la información de cada letra de la palabra analizada
    return lettersUsed

def uppercase_lowercase_count(word):
    lowercase=list(filter(lambda x:x==x.lower(), word))
    lowercase=len(lowercase)
    uppercase=len(word)-lowercase
    #Retorna el número de mayúsculas y minúsculas de la palabra.
    return uppercase,lowercase

def caesarEncryption (word,key):
    #ROT13 es un caso especial de cifrado César, con un cambio de 13. 
    # Solo se cambian las letras, los espacios en blanco y los carácteres especiales se dejan como están. 
    # Aplicando dos veces ROT13 se descifra la palabra.
    encrypted_message = ''
    for letter in word:
        abc='abcdefghijklmnopqrstuvwxyz'
        if letter!=letter.lower(): abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if abc.find(letter)!=-1:
            jumps = abc.find(letter) + key
            modulo = int(jumps) % len(abc)
            encrypted_message = encrypted_message + abc[modulo]
        else:
            encrypted_message = encrypted_message + letter
    return encrypted_message

def word_analysis (word):
    rta={}
    rta={"longest_word":word} #Palabra  
    rta.update({"length_word":len(word)}) #Longitud de la palabra
    rta.update({"letters_used_word_count":letters_used(word)}) #Conteo de cada letra de la palabra
    rta.update({"uppercase_count":uppercase_lowercase_count(word)[0]}) #Conteo mayusculas
    rta.update({"lowercase_count":uppercase_lowercase_count(word)[1]}) #Conteo minusculas
    rta.update({"CaesarEncryption_word":caesarEncryption(word,13)}) #Encriptar ROT13
    return rta

def full_word_analysis(listW): #Debe ingresar un objeto de ListWords
    return    {
                        "long_words":listW.long_words_analysis(),
                        "URL_search":listW.domain_URL(),
                        "mart_search":listW.martSearch(),
                        "list_words":listW.list
                    }

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["mart_db"]
    return db

def add_list_db(document):
    try:
        db = get_db()
        collection_db = db["word_lists"]
        collection_db.insert_one(document)
    except:
        pass
    finally:
        if type(db)==MongoClient:
            db.close()     
