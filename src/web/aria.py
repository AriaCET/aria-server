#!/usr/bin/python2
from flask import request,make_response,Flask,render_template,redirect,url_for
from dbconnect import *

app = Flask(__name__)
authfail = "Please Login and try again."
root = '/'

def auth():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if username == "admin" and password == "login":
        return True
    else:
        return False

@app.route('/')
@app.route('/login',methods=["POST"])
def loginPage():
    if request.method == 'POST':
        resp = make_response(redirect(root))
        resp.set_cookie('username',request.form['username'])
        resp.set_cookie('password',request.form['password'])
	return resp
    else:
	return render_template('layout.html',logedin = auth())
@app.route('/logout/')
def logoutPage():
    resp = make_response(redirect(url_for('loginPage')))
    resp.set_cookie('username'," ")
    resp.set_cookie('password'," ")
    return resp

@app.route('/addspeaker',methods=["POST"])
def speakerAddHandle():    
    if auth():
        f = functions();
        result = f.addClient(request.form['number'],request.form['name'],request.form['ip'])
        return redirect(root);
    else:
        return authfail

@app.route('/removespeaker/<speaker>')
def speakerRemoveHandle(speaker):    
    if auth():
        f = functions();
        f.deleteClient(speaker);
        return redirect(root);
    else:
        return authfail

@app.route('/listspeakers/')
def speakerListHandle():    
    if auth():
        f = functions();
        return render_template("speakermanagelist.html",clients=f.getClientsList());
    else:
        return authfail

@app.route('/channelmanager/')
def channelManagerHandle():
    if auth(): 
        f = functions();
        return render_template("channelmanager.html",channels=f.getGroupsList());
    else:
        return authfail

@app.route('/addchannel/',methods=["POST"])
def channelAddHandle():    
    if auth():
        f = functions();
        f.addGroup(request.form['channelid'],request.form['channelname']);
        return redirect(root)
    else:
        return authfail

@app.route('/removechannel/',methods=["POST"])
def channelRemoveHandle():    
    if auth():
        f = functions();
        f.deleteGroup(request.form['channel'])
        return "Done."
    else:
        return authfail

@app.route('/addtochannel/',methods=["POST"])
def channelAddToHandle():    
    if auth():
        f = functions();
        f.addClientToGroup(request.form['clientid'],request.form['groupid'])
        return "Done."
    else:
        return authfail

@app.route('/removefromchannel/',methods=["POST"])
def channelRemoveFromHandle():    
    if auth():
        f = functions();
        f.deleteClientFromGroup(request.form['clientid'],request.form['groupid'])
        return "Done."
    else:
        return authfail

@app.route('/listchannel/<channel>')
def channelListHandle(channel):    
    if auth():
        f = functions()
        return render_template("editchannel.html",speakers = f.getClientsInGroup(channel),channel = channel,channelname = f.getchname(channel))
    else:
        return authfail

@app.route('/reloaddialplan/')
def reloadHandle():
    if auth():
        f = functions();
        f.reloadDialplan();
        return "Done."
    else:
        return authfail

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
