from flask import Flask,jsonify
import datetime,secrets,memcache,json
app=Flask(__name__)
MEMCACHETTL=1000
TOKENLEN=12
beats_set={}
"""
cach=memcache.Client(["127.0.0.1:11211"])

def insert_in_cache(content:list,key:str):
    content=json.dumps(content)
    cach.set(key,content,MEMCACHETTL)

def get_from_cache(key:str):
    data=cach.get(key)
    if data is not None:
        data=list(data)
    return data"""
@app.route('/keygen')
def newkey():
    token =secrets.token_hex(TOKENLEN)
    while token in beats_set.keys():
        token=secrets.token_hex(TOKENLEN)
    beats_set[token]=[]
    return jsonify({"HeartKey":token})

@app.route('/newheartbeat/<key>')
def newhb(key:str):
    if str(key) not in beats_set:
        return jsonify({"message":"Please generate a valid key."}),500
    now=datetime.datetime.now()
    beats_set[key].append(now)
    return jsonify ({"message":"successfully inserted"})
@app.route('/checkbeat/<key>')
def checkBeat(key):
    if key not in beats_set.keys():
        return jsonify({"messge":"Key does not exists."}),404
    if len(beats_set[key])<1:
        return jsonify({"message":"No beats"}),200
    return jsonify({"key":key,"lastbeat":beats_set[key][-1]})
@app.route('/checkbeat/all/<key>')
def CheckAll(key):
    return beats_set[key]

#app.run()
