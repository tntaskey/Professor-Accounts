#!/bin/python
import bottle as bottle
from bottle import *
import os
import urlparse # if we're pre-2.6, this will not include parse_qs
global User_list
global renewList
global unknownList
global closeList
global deleteList
global gid
global uid
global queryvars
queryvars=[]
User_list=[]
renewList=[]
unknownList=[]
closeList=[]
deleteList=[]
uid=[]
gid=""

try:
            from urlparse import parse_qs
except ImportError: # old version, grab it from cgi
            from cgi import parse_qs
            urlparse.parse_qs = parse_qs
#Static
@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/')

#Template
@route('/',method=["GET","POST"])
def post_home():
    accounts = "none";
    error = "none";
    finish = "none";
    USER_IN=request.query.get("USER_IN")
    return template('index.tpl', renewList=renewList, unknownList=unknownList, deleteList=deleteList, closeList=closeList, User_list=User_list, accounts=accounts, error=error, finish=finish)

@get("/GID")
def get_gid():
    global gid
    global uid
    User_list[:] = []
    renewList[:] = []
    unknownList[:] = []
    closeList[:] = []
    deleteList[:] = []
    queryvars[:] = []
    uid[:] = []
    gid=""
    USER_IN=request.query.get("USER_IN")
    finish = "none";

    print USER_IN

    for i in open('Files/Groups'):
        if USER_IN == i.split(":",3)[0]:
            gid=i.split(":",3)[2];
        elif USER_IN not in open('Files/Groups').read():
            error = "block";
            accounts = "none";
            return template('index.tpl', renewList=renewList, unknownList=unknownList, deleteList=deleteList, closeList=closeList, User_list=User_list, accounts=accounts, error=error, finish=finish)

    print gid

    #check Passwd for user name, if GID matchs pgroup GID then add user to userList
    for i in open('Files/Passwd'):
            if gid == i.split(":",5)[3]:
                uid.append(i.split(":",5)[2])
                User_list.append(i.split(":",5)[0])
    if gid == "":
            error = "block";
            accounts = "none";
            return template('index.tpl', renewList=renewList, unknownList=unknownList, deleteList=deleteList, closeList=closeList, USER_IN=USER_IN, User_list=User_list, error=error, accounts=accounts, finish=finish)
    else:
            accounts = "block";
            error = "none";
            return template('index.tpl', renewList=renewList, unknownList=unknownList, deleteList=deleteList, closeList=closeList, User_list=User_list, accounts=accounts, error=error, finish=finish)

@get("/end")
def post_gid():
        finish = "block";
        accounts = "none";
        error = "none";
        queryvars = parse_qs(request.query_string)
        print queryvars
        for htmlvar in queryvars:
            htmlvalue=queryvars.get(htmlvar)[0]
            if htmlvar.endswith("radio"):
                if htmlvalue == "known":
                    if htmlvar.split("radio",1)[0] in renewList:
                        pass;
                    else:
                        print(htmlvar.split("radio",1)[0] + " is renew")
                        renewList.append(htmlvar.split("radio",1)[0])
                        #print("This is where you do things with confirmed accounts")
                elif htmlvalue == "unknown":
                    if htmlvar.split("radio",1)[0] in unknownList:
                        pass;
                    else:
                        print(htmlvar.split("radio",1)[0] + "is unknown")
                        unknownList.append(htmlvar.split("radio",1)[0])
                        # print("This is where you do things with unknown accounts")
                elif htmlvalue == "close":
                    if htmlvar.split("radio",1)[0] in closeList:
                        pass;
                    else:
                        print(htmlvar.split("radio",1)[0] + "is closed")
                        closeList.append(htmlvar.split("radio",1)[0])
                        # print("This is where you do things with unknown accounts")
            elif htmlvar.endswith("check"):
                    if htmlvar.split("check",1)[0] in deleteList:
                        pass;
                    else:
                        print("Deletion of " + htmlvar.split("check",1)[0] + " is confirmed")
                        deleteList.append(htmlvar.split("check",1)[0])
                        #print("This is where you do things with deleted accounts")
            else: #ignore the 'submit'
                pass

        target = open("decisions.csv", 'a+')

        x=0
        for i in User_list:
            if uid[x] + ":" + gid in open('decisions.csv').read():
                pass
            elif i in renewList:
                target.write(uid[x] + ":" + gid + ":" + i + ":renew:false" + '\n')
            elif i in unknownList:
                target.write(uid[x] + ":" + gid + ":" + i + ":unknown:false" + '\n')
            elif i in closeList and i not in deleteList:
                target.write(uid[x] + ":" + gid + ":" + i + ":close:false" + '\n')
            elif i in closeList and i in deleteList:
                target.write(uid[x] + ":" + gid + ":" + i + ":close:true" + '\n')
            else:
                pass
            x+=1

        target.close

        for i in deleteList:
            if i in closeList:
                closeList.remove(i)

        print unknownList

        #Do things with your csvs using these lists, confirmedList unknownList deleteList
        print "RENEW LIST " + str(renewList)
        print "UNKNOWN LIST " + str(unknownList)
        print "DELETE LIST " + str(deleteList)
     	print "CLOSE LIST" + str(closeList)
        return template('index.tpl', renewList=renewList, unknownList=unknownList, deleteList=deleteList, closeList=closeList, User_list=User_list, error=error, accounts=accounts, finish=finish)
run(host='localhost', port=8081, debug=True)
