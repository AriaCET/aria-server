#!/usr/bin/python2
from flask import request,make_response,Flask,render_template,redirect,url_for,send_from_directory
from server.asterisk import asterisk as asterisk
import server.accs_control as key


DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

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
        if key.auth (request.form['username'],request.form['password']):
            return resp
        else :
            return render_template('layout.html',logedin = auth(),loginFailed = True)
    else:
        return render_template('layout.html',logedin = auth())

@app.route('/logout/')
def logoutPage():
    server = asterisk()
    try:
        server.reloadDialplan()
    except Exception, e:
        pass
    resp = make_response(redirect(url_for('loginPage')))
    resp.set_cookie('username'," ")
    resp.set_cookie('password'," ")

    return resp

@app.route('/addspeaker',methods=["POST"])
def speakerAddHandle():
    if auth():
        server = asterisk();
        try:
            result = server.addClient(request.form['number'],request.form['name'],request.form['ip'])
            return "Done."
        except Exception ,e:
            return "Speakers Not Added"
    else:
        return authfail

@app.route('/removespeaker/<speaker>')
def speakerRemoveHandle(speaker):
    if auth():
        server = asterisk();
        server.deleteClient(speaker);
        return redirect(root)
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
        try:
            server.addGroup(request.form['channelid'],request.form['channelname']);
            return "Done."
        except Exception:
            return "Error:Channel not added"
    else:
        return authfail

@app.route('/removechannel/',methods=["POST"])
def channelRemoveHandle():
    if auth():
        server = asterisk();
        try:
            server.deleteGroup(request.form['channel'])
            return "Done."
        except Exception, e:
            return "Error"
    else:
        return authfail

@app.route('/addtochannel/',methods=["POST"])
def channelAddToHandle():
    if auth():
        server = asterisk()
        try:
            server.addClientToGroup(request.form['clientid'],request.form['groupid'])
            return "Done."
        except Exception, e:
            return "Error"
    else:
        return authfail

@app.route('/removefromchannel/',methods=["POST"])
def channelRemoveFromHandle():
    if auth():
        server = asterisk()
        try:
            server.deleteClientFromGroup(request.form['clientid'],request.form['groupid'])
            return "Done."
        except Exception, e:
            return "Error"
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
        try:
            server.reloadDialplan();
            return "Server Reloaded ."
        except Exception, e:
            return "Error!:"
    else:
        return authfail


@app.route('/speakerpassword/')
@app.route('/speakerpassword',methods=['GET','POST'])
def speakerpasswordmanager():
    if auth():
        if request.method == 'POST':
            password = request.form['password']
            rpassword = request.form['rpassword']
            if password == rpassword :
                server = asterisk()
                server.setpassword(password)
                return "Done."
            else:
                return "Error"
        else:
            return render_template("speakerpassword.html")
    else:
        return authfail

@app.route('/changepassword/')
@app.route('/changepassword',methods=['GET','POST'])
def passwordmanager():
    if auth():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            rpassword = request.form['rpassword']
            if password == rpassword :
                key.updateKey(username,password)
                resp = make_response(redirect(root))
                resp.set_cookie('username',username)
                resp.set_cookie('password',password)
                return resp
            else:
                return "Error"
        else:
            return render_template("passwordmanager.html")
    else:
        return authfail

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path+'/static','favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
