from random import choices
from flask import Flask, render_template, request
from string import digits
from tinydb import Query, TinyDB
from datetime import datetime

notesDb = TinyDB('notes.json')
Note = Query()
app = Flask(__name__)

@app.get('/')
def mainPage():
    return render_template('index.html',notes=notesDb.all())

@app.get('/notes.json')
def getNotes():
    return {'notes':notesDb.all()}
@app.get('/notes/<noteId>.json')
def getNote(noteId:str):
    if not noteId.isdigit():
        return {'error':'Invalid note id'}
    noteId = int(noteId)
    found = notesDb.search(Note.id == noteId)
    if not found:
        return {'error':'Note not found'}
    return found[0]
@app.post('/notes/<noteId>.json')
def editNot(noteId:str):
    if not noteId.isdigit():
        return {'error':'Invalid note id'}
    if not request.form:
        return {'error':'No data found'}
    title = request.form.get('title')
    content = request.form.get('content')
    noteId = int(noteId)
    found = notesDb.search(Note.id == noteId)
    if not found:
        while True:
            noteId = ''.join(choices(digits, k=5))
            if not notesDb.search(Note.id == int(noteId)):
                break
        notesDb.insert({'id':int(noteId), 'title':title, 'content':content,'date':datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    
    notesDb.update({"content":content,'title':title,'date':datetime.now().strftime('%Y-%m-%d %H:%M:%S')},Note.id == noteId)
    return {}
@app.delete('/notes/<noteId>.json')
def deleteNote(noteId:str):
    if not noteId.isdigit():
        return {'error':'Invalid note id'}
    noteId = int(noteId)
    found = notesDb.search(Note.id == noteId)
    if not found:
        return {'error':'Note not found'}
    notesDb.remove(Note.id == noteId)
    return {}
app.run(debug=True)