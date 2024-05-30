import time
from flask import Flask, render_template, url_for, redirect, request, jsonify, session, flash
from db import setup_db, User, add_user, Admin, db, Text, add_text
import main2
import main1
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath
from main2 import *
from main1 import *
from pathlib import Path
import sqlite3
import random
from main3 import *
import main3
import main2
import main1

app = Flask(__name__)
setup_db(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plagiarism_checker.db'
app.config['SECRET_KEY'] = '12345'  # change it later
app.config['JSON_AS_ASCII'] = False
ALLOWED_EXTENSIONS = set(['docx', 'pdf'])
filenames = []
DATABASE_PATH = Path(__file__).parent / "plagiarism_checker.db"


def connect_db():
    return sqlite3.connect(str(DATABASE_PATH))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:

            session['logged_in'] = True
            session['username'] = user.username
            session['password'] = password
            session["permission"] = 0
            session['percentage'] = '95'
            session['min'] = '2'
            session['max'] = '4'
            return redirect(url_for('dashboard'))
        else:
            flash('البيانات غير صحيحة!', 'danger')
    return render_template('login.html')


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = join(dirname(realpath(__file__)), 'files/' + filename)
            file.save(os.path.join(filename))
            filenames.append(file.filename)

            main1.run(filename, session['percentage'], session['min'], session['max'])
            return redirect(url_for('results'))

    return render_template('dashboard.html')


@app.route('/dashboard2', methods=['POST', 'GET'])
def dashboard2():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file1']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = join(dirname(realpath(__file__)), 'files/' + filename)
            file.save(os.path.join(filename))
            filenames.append(file.filename)

            file2 = request.files['file2']
            if file2 and allowed_file(file2.filename):
                filename2 = secure_filename(file2.filename)
                filename2 = join(dirname(realpath(__file__)), 'files/' + filename2)
                file2.save(os.path.join(filename2))
                filenames.append(file2.filename)

            main2.run2(filename, filename2, session['percentage'], session['min'], session['max'])

            return redirect(url_for('resultFile'))
        return redirect(url_for('dashboard2'))

    return render_template('dashboard.html')


@app.route('/dashboard3', methods=['POST', 'GET'])
def dashboard3():
    if request.method == 'POST':
        file = request.files['file3']
        if file and allowed_file(file.filename):
            filename3 = secure_filename(file.filename)
            filename3 = join(dirname(realpath(__file__)), 'files/' + filename3)
            file.save(os.path.join(filename3))
            filenames.append(file.filename)

        text = request.form.get('urls')
        main3.run(filename3, text, session['percentage'], session['min'], session['max'])

        return redirect(url_for('resultFile3'))
    return render_template('dashboard.html')


@app.route('/results', methods=['POST', 'GET'])
def results():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    y = 0
    counter = 0
    temp = []
    temp2 = []
    t1 = []
    t2 = []
    for i in BigList:
        x = i.split(',')
        temp.append(tuple(x))
    # temp = tuple(temp)

    for i in outlierList:
        x = i.split(',')
        temp2.append(tuple(x))

    for i in temp:
        y += 1
        t1.append([y, i[0], i[1], i[2]])

    for i in temp2:
        counter += 1
        t2.append([counter, i[0], i[1], i[2]])

    tot = len(total)
    try:
        percentage = (Length[0] / tot) * 100
        if percentage > 100:
            percentage = 100
        percentage = '%.2f' % percentage

    except:
        percentage = 0
        percentage = '%.2f' % percentage

    return render_template('results.html', temp=t1, temp2=t2, per=percentage)


@app.route('/resultFile', methods=['POST', 'GET'])
def resultFile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    y = 0
    temp = []
    t1 = []
    for i in BigList1:
        x = i.split(',')
        temp.append(tuple(x))
    # temp = tuple(temp)

    for i in temp:
        y += 1
        t1.append([y, i[0], i[1], i[2]])

    
    print(len(total1))
    print(Length1[0])
    try:
        percentage = (Length1[0] / len(total1)) * 100
        print(percentage)
        if percentage > 100:
            percentage = 100
        percentage = '%.2f' % percentage
    except:
        percentage = 0
        percentage = '%.2f' % percentage

    return render_template('resultFile.html', temp=t1, per=percentage)


@app.route('/resultFile3', methods=['POST', 'GET'])
def resultFile3():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    y = 0
    temp = []
    t1 = []
    for i in BigList3:
        x = i.split(',')
        temp.append(tuple(x))
    # temp = tuple(temp)

    for i in temp:
        y += 1
        t1.append([y, i[0], i[1], i[2], i[3]])

    tot = len(total3)
    try:
        percentage = (Length3[0] / tot) * 100
        if percentage > 100:
            percentage = 100
        percentage = '%.2f' % percentage
    except:
        percentage = 0
        percentage = '%.2f' % percentage

    return render_template('resultFile3.html', temp=t1, per=percentage, len = len(temp))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        hashed_password = request.form.get('password')
        username = request.form.get('username')
        add_user(username, hashed_password)
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    # flash('تم تسجيل الدخول بنجاح', 'success')
    return redirect(url_for('login'))


@app.route('/adminlogin', methods=['POST', 'GET'])
def adminlogin():
    global name, passw
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            name = username
            passw = password
            session['logged_in'] = True
            session["permission"] = 1
            session['username'] = admin.username
            session['password'] = password
            session['percentage'] = '95'
            session['min'] = '2'
            session['max'] = '4'
            return redirect(url_for('dashboard'))
        else:
            flash('البيانات غير صحيحة!', 'danger')

    return render_template('login.html')


@app.route('/account', methods=['POST', 'GET'])
def account():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    return render_template('account.html',
                           username=session['username'],
                           password=session['password'])


@app.route('/setting', methods=['POST', 'GET'])
def setting():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    return render_template('setting.html')


@app.route('/addDB', methods=['POST', 'GET'])
def addDB():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    THIS_FOLDER = Path(__file__).parent.resolve()
    my_file = THIS_FOLDER / "plagiarism_checker.db"
    con = connect('plagiarism_checker.db')
    c = con.cursor()
    x = c.execute("SELECT * FROM text").fetchall()
    return render_template('addDB.html', dbNames=x, lenNames=len(x))


@app.route('/removeDB', methods=['POST'])
def remove_db():
    if request.method == 'POST':
        row_ids = request.form.getlist(
            'row_ids[]')  # Assuming 'row_ids' is an array sent from the frontend
        if row_ids:
            conn = connect_db()
            cursor = conn.cursor()

            for row_id in row_ids:
                cursor.execute("DELETE FROM text WHERE id = ?", (row_id,))
            conn.commit()
            cursor.close()
            return redirect(url_for('addDB'))
    return redirect(url_for('addDB'))


@app.route('/addText', methods=['POST', 'GET'])
def addText():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    THIS_FOLDER = Path(__file__).parent.resolve()
    my_file = THIS_FOLDER / "plagiarism_checker.db"
    con = connect('plagiarism_checker.db')
    c = con.cursor()
    x = c.execute("SELECT * FROM text").fetchall()

    if request.method == "POST":
        text = request.form.get("text")
        exist = Text.query.filter_by(content=text).first()
        if len(text) > 200:
            return render_template('addDB.html',
                                   msg='النص يتجاوز 200 حرف',
                                   dbNames=x,
                                   lenNames=len(x))
        elif exist:
            return render_template('addDB.html',
                                   msg='هذا النص موجود مسبقًا في قاعدة البيانات',
                                   dbNames=x,
                                   lenNames=len(x))
        else:
            add_text(text)
            x = c.execute("SELECT * FROM text").fetchall()
            return render_template('addDB.html',
                                   msg1='تمت إضافة النص بنجاح',
                                   dbNames=x,
                                   lenNames=len(x))

    return render_template('addDB.html')


@app.route('/saveSettings', methods=['POST', 'GET'])
def saveSettings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    session['percentage'] = request.form.get('slider')
    session['percentageStatus'] = 1

    session['min'] = request.form.get('percentageInput1')
    session['minStatus'] = 1
    session['max'] = request.form.get('percentageInput2')
    session['maxStatus'] = 1

    return render_template('setting.html')


if __name__ == '__main__':
    app.run(debug=False)
