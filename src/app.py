#https://www.youtube.com/watch?v=Esdj9wlBOaI
#https://www.youtube.com/watch?v=YENw-bNHZwg docker
#https://www.youtube.com/watch?v=RuaKvPq0Fzo Building & Deploying Dockerized Flask + MongoDB Application
#https://www.youtube.com/watch?v=IgCfZkR8wME Vistas flask
#"pip freeze > requirements.txt" usado para generar requirements

import collections
from json import JSONDecodeError
from flask import Flask, jsonify, request, render_template,url_for, redirect
from library import ListWords, add_list_db, full_word_analysis, get_db, word_analysis
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

#app es mi servidor
app=Flask(__name__)


@app.route("/")
def Index():
    db = get_db()
    _collection_db = db.word_lists.find()
    return render_template("index.html", lists_db=_collection_db )

@app.route('/gui/insert_one', methods=["POST"])
def insert_one_gui():
        words=request.form["list"].split(",") #Crea arreglo 
        list1=ListWords(words)
        add_list_db(full_word_analysis(list1))
        print (full_word_analysis(list1))
        return redirect(url_for("Index"))

"""::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::       API_REST JSON         ::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"""

@app.route('/api/test', methods=["POST"])#Agregar y analizar nueva lista
def insert_one_test():
    words=request.json['list']
    list1=ListWords(words)
    #return jsonify(full_word_analysis(list1))
    return jsonify(word_analysis("https://www.apple.com"))

@app.route('/api/insert_one', methods=["POST"])#Agregar y analizar nueva lista
def insert_one():
    words=request.json['list']
    list1=ListWords(words)
    add_list_db(full_word_analysis(list1))
    return jsonify(full_word_analysis(list1))

@app.route('/api/db')#Lectura general de la DB
def get_mart_db():
    try:
        db = get_db()
        _collection_db = db.word_lists.find()
        dbDocuments = [{"_id": str(dbList["_id"]),"list_words":dbList["list_words"]} for dbList in _collection_db]
        return jsonify(dbDocuments)
    except:
        pass
    finally:
        if type(db)==MongoClient:
            db.close()
            
@app.route('/api/db/<string:search_id>')#Lectura específica (_id) de la DB
def get_document_db(search_id):
    try:
        db = get_db()
        _collection_db = db.word_lists.find()
        for dbDocument in _collection_db:
            if str(dbDocument["_id"]) == str(search_id):
                return jsonify(
                    {
                        "_id": str(dbDocument["_id"]),
                        "list_words":dbDocument["list_words"],
                        "long_words":dbDocument["long_words"],
                        "URL_search":dbDocument["URL_search"],
                        "mart_search":dbDocument["mart_search"]
                    }
                )
        return  jsonify({"message":"data_not_found"})
    except:
        pass
    finally:
        if type(db)==MongoClient:
            db.close()

@app.route('/api/db/delete/<string:delete_id>')#Eliminar dato(_id)
def delete_document_db(delete_id):
    try:
        db = get_db()
        myquery = {'_id': ObjectId(delete_id) }
        db.word_lists.remove(myquery)
        _collection_db = db.word_lists.find()
        dbDocuments = [{"_id": str(dbList["_id"]),"list_words":dbList["list_words"]} for dbList in _collection_db]
        return jsonify(dbDocuments)
    except:
        pass
    finally:
        if type(db)==MongoClient:
            db.close()

#Inicialización
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000) #, debug=True