from flask import Flask, url_for, render_template, request, redirect, session, send_file, make_response, jsonify
from mysql.connector import connect
from flask_mail import Mail,Message
import random
import string
app= Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='jainsaloni317@gmail.com',
    MAIL_PASSWORD='newsaloni@317'
)
app.secret_key='ghjhjhq/213763fbf'


mail=Mail(app)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/<url>')
def dynamicUrl(url):
    print(url)
    connection = connect(host="localhost", database="student", user="root", password="saloni@598")
    cur = connection.cursor()
    query1 = "select * from urlinfo where encryptedUrl='{}'".format(url)
    cur.execute(query1)
    originalurl = cur.fetchone()
    if originalurl==None:
        return render_template('index.html')
    else:
        print(originalurl[1])
        return redirect(originalurl[1])

@app.route('/urlshortner')
def urlshortner():
    url = request.args.get('link')
    custom = request.args.get('customurl')
    print(custom)
    print("planettech")
    connection = connect(host="localhost", database="student", user="root", password="saloni@598")
    cur = connection.cursor()

    encryptedurl=''
    if custom=='':
        while True:
            encryptedurl = createEncryptedUrl()
            query1 = "select * from urlinfo where encryptedUrl='{}'".format(url)
            cur.execute(query1)
            xyz = cur.fetchone()
            if xyz == None:
                break
        print(encryptedurl)
        if 'userid' in session:
            id=session['userid']
            query = "insert into urlinfo(originalUrl,encryptedurl,is_Active,created_by) values('{}','{}',1,'{}')".format(url,encryptedurl,id)
        else:
            query = "insert into urlinfo(originalUrl,encryptedUrl,is_Active) values('{}','{}',1)".format(url,encryptedurl)

        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        finalencryptedurl = 'sd.in/' + encryptedurl


    else:
        query1 = "select * from urlinfo where encryptedUrl='{}'".format(custom)
        cur.execute(query1)
        xyz = cur.fetchone()
        if xyz == None:
            if 'userid' in session:
                id = session['userid']
                query = "insert into urlinfo(originalUrl,encryptedurl,is_Active,created_by) values('{}','{}',1,'{}')".format(url, encryptedurl,id)
            else:
                query = "insert into urlinfo(originalUrl,encryptedUrl,is_Active) values('{}','{}',1)".format(url, encryptedurl)

            query = "insert into urlinfo(originalUrl,encryptedurl,is_Active) values('{}','{}',1)".format(url,custom,1)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            finalencryptedurl = 'sd.in/' + custom

        else:
            return "url already exist"

    if 'userid' in session:
        return redirect('/home')
    else:
        return render_template('index.html',finalencryptedurl=finalencryptedurl,url=url)



def createEncryptedUrl():
    letter = string.ascii_letters + string.digits
    encryptedurl = ''
    for i in range(6):
        encryptedurl = encryptedurl + ''.join(random.choice(letter))
    print(encryptedurl)
    return encryptedurl


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/checklogin')
def checklogin():
    email=request.args.get('email')
    password=request.args.get('pwd')
    connection = connect(host="localhost", database="student", user="root", password="saloni@598")
    cur = connection.cursor()
    query1 = "select * from userDetails where emailId='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if xyz == None:
        return render_template('login.html',xyz='you are not successfully registered')

    else:
        if password==xyz[3]:
            session['email']=email
            session['userid']=xyz[0]
            #return render_template('UserHome.html')
            return redirect('/home')

        else:
            return render_template('login.html',xyz='your password is not correct')

    return render_template('login.html')




@app.route('/signup')
def signup():
    return render_template('Signup.html')
@app.route('/register',methods=['post'])
def register():
    email = request.form.get('email')
    username = request.form.get('uname')
    password = request.form.get('pwd')
    connection = connect(host="localhost", database="student", user="root", password="saloni@598")
    cur = connection.cursor()
    query1 = "select * from userDetails where emailId='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    if xyz==None:
        file=request.files['file']
        print(type(file))
        file.save('E:/'+file.filename)
        query = "insert into userDetails(emailId,userName,password,is_Active,created_Date) values('{}','{}','{}',1,now())".format(email,username,password,1)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        return 'you are successfully registered'

    else:
        return 'already registered'


@app.route('/google')
def google():
    path='E:/as.jpg'
    return send_file(path,mimetype='image/jpg',as_attachment=True)

@app.route('/home')
def home():
    if 'userid' in session:
        email=session['email']
        id = session['userid']
        print(id)
        connection = connect(host="localhost", database="student", user="root", password="saloni@598")
        cur = connection.cursor()
        query1 = "select * from  urlinfo where created_by={}".format(id)
        cur.execute(query1)
        data = cur.fetchall()
        print(data)
        return render_template('updateUrl.html', data=data)
    return render_template('login.html')


@app.route('/editUrl',methods=['post'])
def editUrl():
    if 'userid' in session:
        email = session['email']
        print(email)
        id = request.form.get('id')
        url = request.form.get('orignalurl')
        encrypted = request.form.get('encrypted')
        return render_template("editUrl.html",url=url,encrypted=encrypted,id=id)
    return render_template('login.html')

@app.route('/updateUrl',methods=['post'])
def updateUrl():
    if 'userid' in session:
        id = request.form.get('id')
        url = request.form.get('orignalurl')
        encrypted = request.form.get('encrypted')
        connection = connect(host="localhost", database="student", user="root", password="saloni@598")
        cur = connection.cursor()
        query = "select * from  urlinfo where encryptedUrl='{}'and pk_urlId!={}".format(encrypted, id)
        cur.execute(query)
        data = cur.fetchone()
        if data == None:
            query1 = "update urlinfo set originalUrl='{}',encryptedUrl='{}' where pk_urlId={}".format(url, encrypted,
                                                                                                      id)
            cur.execute(query1)
            connection.commit()
            return redirect('/home')
        else:
            return render_template("editUrl.html", url=url, encrypted=encrypted, id=id, error='short url already exist')

    return render_template('login.html')


@app.route('/deleteUrl',methods=['post'])
def deleteUrl():
    if 'userid' in session:
        id = request.form.get('id')
        connection = connect(host="localhost", database="student", user="root", password="saloni@598")
        cur = connection.cursor()
        query1 = "delete from urlinfo where pk_urlId=" + id
        cur.execute(query1)
        connection.commit()
        return redirect('/home')
    return render_template('login.html')


@app.route('/mailbhezo')
def mailbhezo():
    msg = Message(subject='mail sender', sender='jainsaloni317@gmail.com',
                  recipients=['gangwalsaloni629@gmail.com'], body=
                  "This is my first email through python")
    msg.cc = ['salonigangwal.ece22@jecrc.ac.in']
    msg.html = render_template('index.html')
    with app.open_resource("E:/1.docx")as f:
        msg.attach("1.docx","text/docx",f.read())
    mail.send(msg)
    return "mail sent!!"


@app.route('/logout')
def logout():
    session.pop('userid',None)
    return render_template('login.html')

@app.route('/xyzlogin',methods=['post'])
def testapi():
    abc = request.get_json()
    print(abc)
    list = []
    da = {}
    connection = connect(host="localhost", database="student", user="root", password="saloni@598")
    cur = connection.cursor()
    query = "select * from urlinfo"
    cur.execute(query)
    data = cur.fetchall()
    for i in data:
        da["name"] = i[0]
        da["email"] = i[1]
        list.append(da)
    return jsonify(list)


if __name__ == '__main__':
    app.run()

app.add_url_rule('/abc','hello_world')
