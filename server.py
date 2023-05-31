# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
import hashlib
import flask
import flask_login
from flask_bootstrap import Bootstrap
import sqlite3

app = flask.Flask(__name__)
app.secret_key = 'ashdlailio:]fhzkxc,zcnkzcnz,cmlzsncl.zmcz'

bootstrap = Bootstrap(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


# upload file size : 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

#SQLite3へ接続
DBNAME = 'komushoDB'

class User(flask_login.UserMixin):
    pass

def blankInt(data):
    if data:
        return data
    else:
        return "null"
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


@login_manager.user_loader
def user_loader(email):
    user = User()
    user.id = email
    return user

# @login_manager.request_loader
# def request_loader(request):
#     # email = request.form.get('email')
#     conn = sqlite3.connect(DBNAME)
#     cur = conn.cursor()

#     #SQLでEMAIL検索
#     sql = "SELECT 'Ois21.com' password"
#     cur.execute(sql)

#     # 取得したデータを出力
#     for row in cur:
#         print(row)

#     cur.close()
#     conn.close()
#     return

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')

    # user = User()
    # user.id = email
    # user.is_authenticated = request.form['password'] == str(targetUser[1])
    # return user
    return

@app.route('/')
def login_shift():
    return flask.redirect(flask.url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    
        if flask.request.method == 'GET':
            return flask.render_template('login.html')
        
        if flask.request.method == 'POST':
            try:
                conn = sqlite3.connect(DBNAME)
                cur = conn.cursor()
                email = flask.request.form['email']
                #SQLでEMAIL検索
                sql = "SELECT password FROM m_login WHERE email = '" + str(email) + "'"
                print(sql)
                cur.execute(sql)
                result = cur.fetchone()
            except:
                flask.flash('DBでエラーが発生しました')
                return flask.redirect(flask.url_for('login'))
            finally:
                cur.close()
                conn.close()
                if not result:
                    flask.flash('ログインに失敗しました。ユーザー名またはパスワードが間違っています。', 'error')
                    return flask.redirect(flask.url_for('login'))

            password = flask.request.form['password']
            hsPassword = hashlib.sha512(password.encode()).hexdigest()

            if hsPassword == result[0]:
                user = User()
                user.id = email
                flask_login.login_user(user)
                return flask.redirect(flask.url_for('menu'))
            else:
              flask.flash('ログインに失敗しました。ユーザー名またはパスワードが間違っています。', 'error')
              return flask.redirect(flask.url_for('login'))
    

@app.route('/menu', methods=['GET'])
@flask_login.login_required
def menu():
    if flask.request.method == 'GET':
        return flask.render_template('menu.html')

@app.route('/session', methods=['GET'])
@flask_login.login_required
def session():
    if flask.request.method == 'GET':
        
        sql = """SELECT B.kokyaku_name, A.session_at
FROM t_session A 
INNER JOIN t_kokyaku B ON A.kokyaku_id = B.id
"""
        kokyakuData = []
        kokyakuList = []
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            result = cur.fetchall()

            sql = "SELECT id, kokyaku_name FROM t_kokyaku ORDER BY ID"
            cur.execute(sql)
            result2 = cur.fetchall()
            
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()

        for elem in result:
            kokyakuData.append([str(elem[0]),str(elem[1])])

        for elem in result2:
            kokyakuList.append([str(elem[0]),str(elem[1])])

        return flask.render_template('session.html', kokyakuList = kokyakuList, kokyakuData = kokyakuData)

@app.route('/session/<sessionId>', methods=['GET'])
@flask_login.login_required
def sessionDetail(sessionId):
    # if not isinstance(sessionId, (int)):
    #     return
    if flask.request.method == 'GET':
        sql = """SELECT A.session_id
, substr(A.session_at, 1, 16) AS session_at
, A.course_id
, ifnull(A.biko, '') AS biko
FROM t_session A
WHERE A.session_id = {}
"""
        sql = sql.format(sessionId)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            result = cur.fetchall()

            sql = """SELECT B.remban
, B.shumoku_id
, B.juryo
, B.kaisu
, B.setsu
, ifnull(B.biko, '') AS shumoku_biko
FROM t_session A
INNER JOIN t_session_sub B ON A.session_id = B.session_id
WHERE A.session_id = {}
ORDER BY B.remban
"""
            sql = sql.format(sessionId)
            print(sql)
            cur.execute(sql)
            result1 = cur.fetchall()


            sql = """SELECT C.code
, C.sval1 AS course_name
FROM m_codevalue C
WHERE C.class = '001'
ORDER BY C.code
"""
            print(sql)
            cur.execute(sql)
            result2 = cur.fetchall()

            sql = """SELECT C.code
, C.sval1
FROM m_codevalue C
WHERE C.class = '100'
ORDER BY C.code
"""
            print(sql)
            cur.execute(sql)
            result3 = cur.fetchall()

        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()


        sessionData = []
        for elem in result[0]:
            sessionData.append(elem)

        sessionDataSub = []
        for elem in result1:
            sessionDataSub.append([str(elem[0]),str(elem[1]),str(elem[2]),str(elem[3]),str(elem[4]),str(elem[5])])
        
        couseList = []
        for elem in result2:
            couseList.append([str(elem[0]),str(elem[1])])
        
        shumokuList = []
        for elem in result3:
            shumokuList.append([str(elem[0]),str(elem[1])])

        print(couseList[0])
        print(sessionData)

        return flask.render_template('sessionDetail.html', sessionData = sessionData, sessionDataSub = sessionDataSub, couseList = couseList, shumokuList = shumokuList)



@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.Response('''
ログアウト<br />
<a href="/login">もう一度ログイン</a>
''')

@app.route('/data/kokyaku', methods=['GET', 'POST', 'PATCH'])
def kokyakuData():
    if flask.request.method == 'GET':
        id = flask.request.args.get('id')
        sql = """SELECT B.kokyaku_name
    , substr(A.session_at, 1, 16) AS session_at
    , C.sval1 AS course_name
    , A.session_id
    FROM t_session A 
    INNER JOIN t_kokyaku B ON A.kokyaku_id = B.id
    LEFT JOIN m_codevalue C ON C.class = '001' AND A.course_id = C.code
    WHERE B.id = '{}'
    ORDER BY session_at DESC
    """
        sql = sql.format(id)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            result = cur.fetchall()   
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        # JSON形式で返す
        return flask.jsonify(result)

    if flask.request.method == 'POST':
        id = flask.request.args.get('id')
        sql = """SELECT B.kokyaku_name
    , substr(A.session_at, 1, 16) AS session_at
    , C.sval1 AS course_name
    , A.session_id
    FROM t_session A 
    INNER JOIN t_kokyaku B ON A.kokyaku_id = B.id
    LEFT JOIN m_codevalue C ON C.class = '001' AND A.course_id = C.code
    WHERE B.id = '{}'
    ORDER BY session_at DESC
    """
        sql = sql.format(id)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            result = cur.fetchall()   
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        # JSON形式で返す
        return flask.jsonify(result)

    if flask.request.method == 'PATCH':
        id = flask.request.args.get('id')
        sql = """SELECT B.kokyaku_name
    , substr(A.session_at, 1, 16) AS session_at
    , C.sval1 AS course_name
    , A.session_id
    FROM t_session A 
    INNER JOIN t_kokyaku B ON A.kokyaku_id = B.id
    LEFT JOIN m_codevalue C ON C.class = '001' AND A.course_id = C.code
    WHERE B.id = '{}'
    ORDER BY session_at DESC
    """
        sql = sql.format(id)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            result = cur.fetchall()   
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        # JSON形式で返す
        return flask.jsonify(result)

@app.route('/data/session/<sessionId>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@flask_login.login_required
def sessionData(sessionId):
    if flask.request.method == 'GET':
        sql = """SELECT B.remban
    , B.shumoku_id
    , B.juryo
    , B.kaisu
    , B.setsu
    , ifnull(B.biko, '') AS shumoku_biko
    FROM t_session A
    INNER JOIN t_session_sub B ON A.session_id = B.session_id
    WHERE A.session_id = {}
    ORDER BY B.remban
    """
        sql = sql.format(sessionId)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            result = cur.fetchall()   
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        # JSON形式で返す
        return flask.jsonify(result)

    if flask.request.method == 'PATCH':
        data = flask.request.get_json()
        sql = """UPDATE t_session SET
session_at = '{}'
, course_id = '{}'
, biko = '{}'
, sys_updated_at = datetime('now', 'localtime')
WHERE session_id = {}
"""
        sql = sql.format(data['sessionAt'], data['courseId'], data['biko'], sessionId)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            conn.commit()
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        return {"result": "OK"}
    
    if flask.request.method == 'DELETE':
        sql = """DELETE FROM t_session
WHERE session_id = {}
"""
        sql = sql.format(sessionId)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)

            sql = """DELETE FROM t_session_sub
WHERE session_id = {}
"""
            sql = sql.format(sessionId)
            print(sql)
            cur.execute(sql)

            conn.commit()
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        return {"result": "OK"}

    if flask.request.method == 'POST':
        sql = """INSERT INTO t_session_sub
SELECT '{}' AS session_id
, ifnull(MAX(remban), 0) + 1 AS remban
, null AS shumoku_id
, null AS juryo
, null AS kaisu
, null AS setsu
, null AS biko
, datetime('now', 'localtime') AS sys_created_at
, datetime('now', 'localtime') AS sys_updated_at
FROM t_session_sub
"""
        sql = sql.format(sessionId)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            conn.commit()
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        return {"result": "OK"}

@app.route('/data/session/<sessionId>/<remban>', methods=['PATCH', 'DELETE'])
@flask_login.login_required
def sessionDataNaiyo(sessionId, remban):
    if flask.request.method == 'PATCH':
        data = flask.request.get_json()
        sql = """UPDATE t_session_sub SET
shumoku_id = '{}'
, juryo = {}
, kaisu = {}
, setsu = {}
, biko = '{}'
, sys_updated_at = datetime('now', 'localtime')
WHERE session_id = {} AND remban = {}
"""
        sql = sql.format(data['shumoku_id'], blankInt(data['juryo']), blankInt(data['kaisu']), blankInt(data['setsu']), data['biko'], sessionId, remban)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            conn.commit()
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        return {"result": "OK"}
    
    if flask.request.method == 'DELETE':
        sql = """DELETE FROM t_session_sub
WHERE session_id = {} AND remban = {}
"""
        sql = sql.format(sessionId, remban)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            conn.commit()
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        return {"result": "OK"}

@app.route('/data/session', methods=['GET', 'POST'])
@flask_login.login_required
def sessionCreate():
    if flask.request.method == 'GET':
        id = flask.request.args.get('id')
        sessionAt1 = flask.request.args.get('sessionAt1') 
        sessionAt2 = flask.request.args.get('sessionAt2')
        if (sessionAt1 is None) :
            sessionAt1 = '1990-01-01'
        if (sessionAt2 is None) :
            sessionAt2 = '2190-01-01'


        sql = """SELECT B.kokyaku_name
, substr(A.session_at, 1, 16) AS session_at
, C.sval1 AS course_name
, A.session_id
FROM t_session A 
INNER JOIN t_kokyaku B ON A.kokyaku_id = B.id
LEFT JOIN m_codevalue C ON C.class = '001' AND A.course_id = C.code
WHERE B.id = '{}'
AND A.session_at >= '{}' AND A.session_at < DATE('{}', '+1 day')
ORDER BY session_at DESC
"""
        sql = sql.format(id, sessionAt1, sessionAt2)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            result = cur.fetchall()   
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        # JSON形式で返す
        return flask.jsonify(result)

    if flask.request.method == 'POST':
        data = flask.request.get_json()
        sql = """INSERT INTO t_session
SELECT ifnull(MAX(session_id), 0) + 1 AS session_id
, datetime('now', 'localtime') AS session_at
, '{}' AS kokyaku_id
, B.course_id1 AS course_id
, null AS biko
, datetime('now', 'localtime') AS sys_created_at
, datetime('now', 'localtime') AS sys_updated_at
FROM t_session A 
INNER JOIN t_kokyaku B ON A.kokyaku_id = B.id  
"""
        sql = sql.format(data['kokyakuId'])
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            conn.commit()
        
            sql = """SELECT MAX(session_id) AS session_id
FROM t_session
"""     
            print(sql)
            cur.execute(sql)
            result = cur.fetchone()
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        return flask.jsonify(result)
    
@app.route('/addkokyaku', methods=['GET', 'POST'])
def addKokyaku():
    if flask.request.method == 'GET':
        kokyakuList = []
        courseList = []
        sql = """
SELECT id, kokyaku_name FROM t_kokyaku ORDER BY ID
"""
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            result = cur.fetchall()

            sql = """SELECT C.code
, C.sval1 AS course_name
FROM m_codevalue C
WHERE C.class = '001'
ORDER BY C.code
"""
            cur.execute(sql)
            result2 = cur.fetchall()
            
            for elem in result:
              kokyakuList.append([str(elem[0]),str(elem[1])])
            for elem in result2:
              courseList.append([str(elem[0]),str(elem[1])])
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
            return flask.render_template('addkokyaku.html', kokyakuList = kokyakuList, courseList = courseList)

    if flask.request.method == 'POST':
        data = flask.request.get_json()
        sql = """
INSERT INTO t_kokyaku (
id
, kokyaku_name
, kokyaku_name_kana
, gender
, email
, tel
, jusho
, birthday
, course_id1
, course_id2
, course_id3
, biko
, sys_created_at
, sys_updated_at
) VALUES (
(SELECT MAX(id) + 1 FROM t_kokyaku)
, '{}'
, '{}'
, '{}'
, '{}'
, '{}'
, '{}'
, '{}'
, '{}'
, '{}'
, '{}'
, '{}'
, datetime('now', 'localtime')
, datetime('now', 'localtime')
)
"""
        sql = sql.format(data['kokyakuName'], data['kokyakuNameKana'], data['gender'], data['email'], data['tel'], data['jusho'], data['birthday'], data['courseId1'], data['courseId2'], data['courseId3'], data['biko'])
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            conn.commit()
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        # JSON形式で返す
        return {"result": "OK"}



@app.route('/addkokyaku/<kokyakuId>', methods=['GET', 'PATCH'])
@flask_login.login_required
def addKokyakuData(kokyakuId):
    if flask.request.method == 'GET':
        sql = """SELECT gender
, kokyaku_name
, kokyaku_name_kana
, email
, tel
, jusho
, birthday
, course_id1
, course_id2
, course_id3
, biko
FROM t_kokyaku
WHERE id = {}
"""
        sql = sql.format(kokyakuId)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            result = cur.fetchone()
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        # JSON形式で返す
        return flask.jsonify(result)
    if flask.request.method == 'PATCH':
        data = flask.request.get_json()
        sql = """
UPDATE t_kokyaku SET
kokyaku_name = '{}'
, kokyaku_name_kana = '{}'
, gender = '{}'
, email = '{}'
, tel = '{}'
, jusho = '{}'
, birthday = '{}'
, course_id1 = '{}'
, course_id2 = '{}'
, course_id3 = '{}'
, biko = '{}'
, sys_updated_at = datetime('now', 'localtime')
WHERE id = {}
"""
        sql = sql.format(data['kokyakuName'], data['kokyakuNameKana'], data['gender'], data['email'], data['tel'], data['jusho'], data['birthday'], data['courseId1'], data['courseId2'], data['courseId3'], data['biko'], kokyakuId)
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
            print(sql)
            cur.execute(sql)
            conn.commit()
        except:
            print('DBでエラーが発生しました')
            return
        finally:
            cur.close()
            conn.close()
        # JSON形式で返す
        return {"result": "OK"}

# 支払いのSQLメモ
# SELECT
# B.kokyaku_name
# , C.sval1 AS course_name
# FROM t_session A 
# INNER JOIN t_kokyaku B ON A.kokyaku_id = B.id
# INNER JOIN m_codevalue C ON C.class = '001' AND A.course_id = C.code
# GROUP BY B.kokyaku_name, C.sval1
    
@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for('login'))

port = os.getenv('VCAP_APP_PORT', '8000')

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=int(port), debug=True)
