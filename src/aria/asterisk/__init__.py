import sqlite3
import os
from config import *

class connection:
        def __init__(self):
                print "Connection object created"

        def connectDB(self,DBpath=DB_path):

                if not(os.path.exists(os.path.dirname(DBpath))):
                        raise IOError('Invalid database path_1')

                if(os.path.exists(DBpath)):
                        try:
                                conn=sqlite3.connect(DBpath)
                                return conn
                        except sqlite3.OperationalError:
                                raise IOError('Unable to connect to database')
                else:
                        conn = sqlite3.connect(DBpath)
                        c = conn.cursor()
                        c.execute('create table clients(ClientID integer primary key,ClientName text,IP text not null)')
                        c.execute('create table groups(GroupID integer primary key,GroupName text)')
                        c.execute('create table assoc(cID integer,gID integer,primary key(cID,gID))')
                        conn.commit()
                        return conn
#raise IOError('Invalid database path');


class asterisk:

        connect = connection()

        def getClientsList(self):

                conn = self.connect.connectDB()
                c = conn.cursor()
                c.execute("select * from clients")
                clientlist=[]
                for name in c :
                        clientlist.append(name)

                return clientlist

        def getClientsInGroup(self, group):
                conn = self.connect.connectDB()
                c = conn.cursor()
                c.execute("select ClientID, ClientName, gID from clients left join (select * from assoc where gID = {0}) on clients.ClientID = cID".format(group))
                clientlist=[]
                for name in c :
                        clientlist.append(name)
                return clientlist

        def deleteClient(self,cID):

                conn = self.connect.connectDB()
                c = conn.cursor()
                c.execute("delete from clients where ClientID = {0}".format(cID))
                c.execute("delete from assoc where cID = {0}".format(cID))
                conn.commit()
                c.close()

        def addClient(self,c_id,name,ip):

                conn = self.connect.connectDB()
                c = conn.cursor()
                c.execute("insert into clients values ( {0}, '{1}', '{2}')".format(c_id,name,ip))
                conn.commit()
                c.close()

        def getGroupsList(self):

                conn = self.connect.connectDB()
                c = conn.cursor()
                c.execute("select * from groups")
                grouplist = []
                for name in c :
                        grouplist.append(name)

                return grouplist

        def addGroup(self,g_id,gname):

                conn = self.connect.connectDB()
                c = conn.cursor()
                c.execute("insert into groups values ( {0}, '{1}' )".format(g_id,gname))
                conn.commit();
                c.close();

        def deleteGroup(self,groupID):

                conn = self.connect.connectDB()
                c = conn.cursor()
                c.execute("delete from groups where GroupID = '{0}'".format(groupID))
                c.execute("delete from assoc where cID = '{0}'".format(groupID));
                conn.commit();
                c.close();

        def addClientToGroup(self,c_id,g_id):
                conn = self.connect.connectDB()
                c = conn.cursor()
                c.execute("insert into assoc values ( {0}, {1} )".format(c_id,g_id))
                conn.commit();
                c.close();

        def deleteClientFromGroup(self,c_id,g_id):

                conn = self.connect.connectDB()
                c = conn.cursor()
                c.execute("delete from assoc where cID = {0} and gID = {1}".format(c_id,g_id))
                conn.commit();
                c.close();

        def getchname(self,group):
                conn = self.connect.connectDB()
                c = conn.cursor()
                c.execute("select GroupName from groups where GroupID = {0} ".format(group))
                for name in c:
                        return name[0];
        def reloadDialplan(self):
                manifest='''[general]\ncontext=unauthenticated\nallowguest=no\nsrvlookup=yes\nudpbindaddr=0.0.0.0\ntcpenable=no\n\n'''
                context='''[overhead](!)\ntype=friend
context=LocalSets\n
host=dynamic\n
nat=yes\nsecret=welcome\ndtmfmode=auto\ndisallow=all\nallow=ulaw\n\n'''
                sipfile = open("/tmp/sip.conf","w")
                sipfile.write(manifest)
                sipfile.write(context)

                # Write the clients
                clients = self.getClientsList()

                for client in clients:
                        tmpstr = "\n["+str(client[0])+"](overhead)\t; Name:"+ client[1]+"\n"
                        sipfile.write(tmpstr)
                        if len(client[2]) != 0:
                                tmpstr="host="+client[2]+"\n"
                                sipfile.write(tmpstr)
                sipfile.close()
