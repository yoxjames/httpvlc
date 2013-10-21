from app import app
from flask import render_template, request, g, session, redirect

import json, os, subprocess


''' AJAX LISTENERS '''

''' list '''
@app.route('/ajax/ls', methods=['POST','GET'])
def list_dir():
    if "CURRENT_DIR" not in session:
        session["CURRENT_DIR"] = app.config["HOME_DIRECTORY"]

    r_list = []
    ls_output = os.listdir(session["CURRENT_DIR"])
    for f in ls_output:
        if f[0] != '.': #Exclude hidden files like "ls"
            t = (f,os.path.isdir(session["CURRENT_DIR"]+"/"+f))
            r_list.append(t)

    return json.dumps(r_list)

    

'''
OPEN
NOTE THIS IS NOT SECURE AT ALL
'''
@app.route('/ajax/cd/<dir_d>', methods=['POST','GET'])
def change_dir(dir_d):
    if dir_d == "~":
        session["CURRENT_DIR"] = app.config["HOME_DIRECTORY"]
    elif dir_d == "__BACK__":
        session["CURRENT_DIR"] = session["CURRENT_DIR"]+"/.."
    else:
        new_dir = dir_d.replace("_space_"," ")
        session["CURRENT_DIR"] = session["CURRENT_DIR"] + "/"+new_dir
    return session["CURRENT_DIR"]

'''
PWD
'''
@app.route('/ajax/pwd', methods=['POST','GET'])
def print_dir():
    return session['CURRENT_DIR']

'''
PLAY
'''
@app.route('/ajax/play/<f>', methods=['POST','GET'])
def play(f):
    
    if "VLC_INSTANCE" in session:
        return "RUNNING" # We need to handle the already playing case
    new_f = f.replace("_space_"," ")
    session['VLC_INSTANCE'] = 1 # Playing
    subprocess.Popen(['vlc', session['CURRENT_DIR']+"/" + new_f],
                shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return "VLC ENGAGED"




''' HTTP LISTENERS '''
@app.route('/')
def index():
    return redirect('/media')

@app.route('/remote')
def remote():
    if "CURRENT_DIR" not in session:
        session["CURRENT_DIR"] = app.config["HOME_DIRECTORY"]

    return render_template("remote.html", VLC_PORT = app.config["VLC_PORT"])

@app.route('/index')
@app.route('/media')
def media():
    if "CURRENT_DIR" not in session:
        session["CURRENT_DIR"] = app.config["HOME_DIRECTORY"]

    return render_template("media.html", CURRENT_DIR = session["CURRENT_DIR"])


