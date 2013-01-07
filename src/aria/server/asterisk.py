import sqlite3
import config
import subprocess
import connection

class asterisk(object):

        def __init__( self,DBpath=config.DB_path):
                self.DBpath = DBpath

        def getPassword(self):
                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("select password from clientconfig")
                password = c.fetchone()[0]
                return password

        def getClientsList(self):

                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("select * from clients")
                clientlist=[]
                for name in c :
                        clientlist.append(name)

                return clientlist

        def getClientsInGroup(self, group):
                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("select ClientID, ClientName, gID from clients left join (select * from assoc where gID = {0}) on clients.ClientID = cID".format(group))
                clientlist=[]
                for name in c :
                        clientlist.append(name)
                return clientlist

        def deleteClient(self,cID):

                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("delete from clients where ClientID = {0}".format(cID))
                c.execute("delete from assoc where cID = {0}".format(cID))
                conn.commit()
                c.close()

        def addClient(self,c_id,name,ip):

                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                if len(ip) == 0:
                        #set default IP
                        pass 
                c.execute("insert into clients values ( {0}, '{1}', '{2}')".format(c_id,name,ip))
                conn.commit()
                c.close()

        def getGroupsList(self):

                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("select * from groups")
                grouplist = []
                for name in c :
                        grouplist.append(name)

                return grouplist

        def addGroup(self,g_id,gname):

                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("insert into groups values ( {0}, '{1}' )".format(g_id,gname))
                conn.commit();
                c.close();

        def deleteGroup(self,groupID):

                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("delete from groups where GroupID = '{0}'".format(groupID))
                c.execute("delete from assoc where cID = '{0}'".format(groupID));
                conn.commit();
                c.close();

        def addClientToGroup(self,c_id,g_id):
                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("insert into assoc values ( {0}, {1} )".format(c_id,g_id))
                conn.commit();
                c.close();

        def deleteClientFromGroup(self,c_id,g_id):

                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("delete from assoc where cID = {0} and gID = {1}".format(c_id,g_id))
                conn.commit();
                c.close();

        def getchname(self,group):
                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("select GroupName from groups where GroupID = {0} ".format(group))
                for name in c:
                        return name[0];
        def reloadClientConf(self):
                password = self.getPassword()
                manifest="""
                        [general]
                        context=unauthenticated
                        allowguest=no
                        srvlookup=yes
                        udpbindaddr=0.0.0.0
                        tcpenable=no
                        """
                context="""
                        [overhead](!)
                        ntype=friend
                        context=LocalSets
                        host=dynamic
                        nat=yes
                        secret="{password}"
                        dtmfmode=auto
                        disallow=all
                        allow=ulaw
                        """
                context=context.format(password=password)
                sipfile = open(config.clientConf,"w")
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

        def reloadChannelConf(self):
                manifest = '''[general]\n\n[LocalSets]\n'''
                extfile = open(config.channelConf,"w")
                extfile.write(manifest)

                for member in self.getGroupsList():
                        clients = self.getClientsInGroup(member[0])
                        pagestr = "exten => " +str(member[0])+",1,Page("
                        for ct in clients:
                                if ct[2] == member[0]:
                                        pagestr = pagestr + "sip/"+str(ct[0])+"&"
                        pagestr = pagestr[:-1] + ",i,120)\t;"+str(member[1])+"\n"
                        pagestr = pagestr + "exten => "+str(member[0])+",2,Hangup()\n\n"
                        extfile.write(pagestr)

                extfile.close()
        def setpassword(self,password):
                conn = connection.connectDB(self.DBpath)
                c = conn.cursor()
                c.execute("delete from clientconfig")
                c.execute("insert into clientconfig(password) values ('{0}')".format(password))
                conn.commit();
                c.close();

        def reloadAsterisk(self):
                sipReload = subprocess.Popen(["asterisk","-rx","sip reload"],stdout=subprocess.PIPE)
                sipReload.wait()
                dialplanReload = subprocess.Popen(["asterisk","-rx","dialplan reload"],stdout=subprocess.PIPE)
                dialplanReload.wait()
                return (sipReload.poll() and dialplanReload.poll())

        def reloadDialplan(self):
                self.reloadClientConf()
                self.reloadChannelConf()
                self.reloadAsterisk()
