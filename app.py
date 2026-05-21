from flask import Flask ,redirect , request , render_template , url_for
import sqlite3
import datetime as dt





app = Flask(__name__)

delta = dt.timedelta(hours=23)
@app.route('/')
def helo():
    return 'hello world'

@app.route('/login' , methods = ['GET' , 'POST'])
def login():
    if request.method == 'POST':
        # username = request.form['firstname']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db' ,isolation_level=None) #The isolation_level=None keyword argument causes the database touse autocommit mode.
        query = f"""
        SELECT * FROM USERS WHERE email = '{email}' AND password = '{password}' 
        """
        print(query)
        result = conn.execute(query).fetchall()
        
        conn.close()
        # if checking[0][1] == password:
        if result:
            return redirect(url_for('profile' , fav=email))
    return render_template('login.html')


@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirm_password']
        datetime = dt.timezone(delta)
        if password == confirmPassword:
            pass
        else:
            return 'the password dont match'
        conn = sqlite3.connect('database.db' ,isolation_level=None) #The isolation_level=None keyword argument causes the database touse autocommit mode.
        conn.execute("CREATE TABLE IF NOT EXISTS USERS(firstname TEXT NOT NULL,lastname TEXT NOT NULL,email TEXT NOT NULL,password TEXT NOT NULL ,  DATETIME TEXT NOT NULL) STRICT")
        conn.execute(f'INSERT INTO USERS VALUES ("{first_name}" , "{last_name}" , "{email}" , "{password}" , "{datetime}")')
        return redirect(url_for('profile' , fav=first_name))
    return render_template('register.html')

@app.route('/admin' , methods= ['GET'])
def admin():
    return render_template('admin.html')


@app.route('/profile/<fav>' , methods=['GET'])
def  profile(fav):
    return render_template('profile.html' , firstname=fav) 

@app.route('/comments_page', methods=['GET'])
def comment_page():

    conn = sqlite3.connect('database.db')
    conn.execute("""
    CREATE TABLE IF NOT EXISTS COMMENTS(
        comment TEXT NOT NULL
    )
    """)

    comments = conn.execute("""
    SELECT comment FROM COMMENTS
    """).fetchall()

    conn.close()

    return render_template(
        'comments_page.html',
        comments=comments
    )
@app.route('/add_comment', methods=['POST'])
def add_comment():

    data = request.get_json()

    comment = data['comment']

    conn = sqlite3.connect('database.db', isolation_level=None)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS COMMENTS(
        comment TEXT NOT NULL
    )
    """)

    conn.execute(f"""
    INSERT INTO COMMENTS VALUES ("{comment}")
    """)

    conn.close()

    return {
        'message': 'comment added successfully'
    }

if __name__ == '__main__':
    app.run(debug=True)