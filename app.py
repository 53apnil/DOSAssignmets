from flask import Flask
import pymysql
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
app=Flask(__name__)
os.system("/etc/init.d/mysql start")
db=pymysql.Connect(host="localhost",user="root",port=3306)
cursor = db.cursor()
cursor.execute("drop database if exists test;")
cursor.execute ("create database if not exists test;")
db.close()
db=pymysql.Connect(host="localhost",user="root",database="test",port=3306)
cursor=db.cursor()
cursor.execute("drop table if exists Student;")
cursor.execute("create table Student(ID INT NOT NULL Primary Key,Name varchar(20),Age INT,Department varchar(20),Subject varchar(100));")
cursor.execute("Insert into Student(ID,Name,Age,Department,Subject) values(1,'Tom',20,'computer','Computer,Math,Electronix');")
@app.route('/user',methods=['GET','POST','PUT','DELETE'])
def user():
    cursor=db.cursor()
    if request.method=='GET':
        sql="""select ID,Name,Age,Department,Subject from Student"""
        cursor.execute(sql)
        row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv= cursor.fetchall()
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        resp=jsonify(json_data)
        return resp
    elif request.method=='POST':
        _json=request.json
        _id =_json['ID']
        _name = _json['Name']
        _age =_json['Age']
        _dept = _json['Department']
        _sub = _json['Subject']
        cursor.execute("Insert into Student(ID,Name,Age,Department,Subject) values(%s,%s,%s,%s,%s)",(_id,_name,_age,_dept,_sub))
        message = {'status':200,'message':'OK '+request.url}
        resp=jsonify(message)
        resp.status_code=200
        return resp
    elif request.method=='PUT':
        _json=request.json
        _id =_json['ID']
        _name = _json['Name']
        _age =_json['Age']
        _dept = _json['Department']
        _sub = _json['Subject']
        if _id:
            if _name:
                cursor.execute("update Student set Name=%s where ID=%s",(_name,_id))
            else:
                pass
            if _age:
                cursor.execute("update Student set Age=%s where ID=%s",(_age,_id))
            else:
                pass
            if _dept:
                cursor.execute("update Student set Department=%s where ID=%s",(_dept,_id))
            else:
                pass
            if _sub:
                cursor.execute("update Student set Subject=%s where ID=%s",(_sub,_id))
            else:
                pass
            if _name or _age or _dept or _sub:
                message = {'status':200,'message':'OK '+request.url}
                resp=jsonify(message)
                resp.status_code=200
                return resp
            else:
                message = {'status':204,'message':'No Content to Update '+request.url}
                resp=jsonify(message)
                resp.status_code=204
                return resp
        else:
            message = {'status':204,'message':'No Content to update '+request.url}
            resp=jsonify(message)
            resp.status_code=204
            return resp
    elif request.method=='DELETE':
        _json=request.json
        _id=_json["ID"]
        if _id:
            cursor.execute("delete from Student where ID=%s",(_id))
            message = {'status':200,'message':'OK '+request.url}
            resp=jsonify(message)
            resp.status_code=200
            return resp
        else:
            message = {'status':204,'message':'No Content to update '+request.url}
            resp=jsonify(message)
            resp.status_code=204
            return resp

@app.errorhandler(404)
def not_found(error=None):
	message = {'status':404,'message':'Not Found '+request.url}
	resp=jsonify(message)
	resp.status_code=404
	return resp
if __name__=="__main__":
	app.run(host="0.0.0.0",port=8080)
