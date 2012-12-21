#!/usr/bin/python2
from flask import request,make_response,Flask,render_template,redirect,url_for
from asterisk import *
import accs_control as key

app = Flask(__name__)
authfail = "Please Login and try again."
root = '/'

def auth():
    username = request.cookies.get('username')
    password = request.cookies.get('password')

    return key.auth(username,password)

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
        server = asterisk();
        result = server.addClient(request.form['number'],request.form['name'],request.form['ip'])
        return redirect(root);
    else:
        return authfail

@app.route('/removespeaker/<speaker>')
def speakerRemoveHandle(speaker):
    if auth():
        server = asterisk();
        server.deleteClient(speaker);
        return redirect(root);
    else:
        return authfail

@app.route('/listspeakers/')
def speakerListHandle():
    if auth():
        server = asterisk();
        return render_template("speakermanagelist.html",clients=server.getClientsList());
    else:
        return authfail

@app.route('/channelmanager/')
def channelManagerHandle():
    if auth():
        server = asterisk();
        return render_template("channelmanager.html",channels=server.getGroupsList());
    else:
        return authfail

@app.route('/addchannel/',methods=["POST"])
def channelAddHandle():
    if auth():
        server = asterisk();
        server.addGroup(request.form['channelid'],request.form['channelname']);
        return redirect(root)
    else:
        return authfail

@app.route('/removechannel/',methods=["POST"])
def channelRemoveHandle():
    if auth():
        server = asterisk();
        server.deleteGroup(request.form['channel'])
        return "Done."
    else:
        return authfail

@app.route('/addtochannel/',methods=["POST"])
def channelAddToHandle():
    if auth():
        server = asterisk()
        server.addClientToGroup(request.form['clientid'],request.form['groupid'])
        return "Done."
    else:
        return authfail

@app.route('/removefromchannel/',methods=["POST"])
def channelRemoveFromHandle():
    if auth():
        server = asterisk()
        server.deleteClientFromGroup(request.form['clientid'],request.form['groupid'])
        return "Done."
    else:
        return authfail

@app.route('/listchannel/<channel>')
def channelListHandle(channel):
    if auth():
        server = asterisk()
        return render_template("editchannel.html",speakers = server.getClientsInGroup(channel),channel = channel,channelname = server.getchname(channel))
    else:
        return authfail

@app.route('/reloaddialplan/')
def reloadHandle():
    if auth():
        server = asterisk();
        server.reloadDialplan();
        return "Done."
    else:
        return authfail
@app.route('/passwordmanager/')
def passwordmanager():
    if auth():
        return render_template("passwordmanager.html")
    else:
        return authfail
@app.route('/changepassword',methods=["POST"])
def function():
    if auth():
        password = request.form['password']
        rpassword = request.form['rpassword']
        if password == rpassword :
            server = asterisk()
            server.setpassword(password)
            print "test"
            return "Done."
        else:
            pass
    else:
        return authfail
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
