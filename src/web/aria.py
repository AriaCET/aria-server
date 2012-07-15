from flask import render_template
from flask import Flask
class Client:
    def __init__(self):
        self.name = ""
        self.status = ""
app = Flask(__name__)
@app.route('/')
def root():
    return "Working"
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/manage_clients')
def manage_clients():
    theClients = []
    myClient1 = Client()
    myClient1.name = "Dhananjay"
    myClient1.status = "Active"
    theClients.append(myClient1)
    myClient2 = Client()
    myClient2.name = "Joji"
    myClient2.status = "inActive"
    theClients.append(myClient2)
    return render_template('client_manager.html',clients=theClients)
if __name__ == '__main__':
    app.debug = True
    app.run()
