from flask import Flask, render_template, request, redirect, url_for,flash,session
import mysql.connector


conn=mysql.connector.connect(host="localhost",user="root",password="root",autocommit=True)
mycursor=conn.cursor(dictionary=True,buffered=True)
mycursor.execute("create database if not exists egram")
mycursor.execute("use egram")
mycursor.execute("create table if not exists userreg(id int primary key auto_increment,uname varchar(255),email varchar(30) unique,upassword text)")
mycursor.execute("create table if not exists pdoreg(id int primary key auto_increment,pname varchar(255),email varchar(30) unique,ppassword text)")
mycursor.execute("CREATE TABLE if not exists complaints (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255)  NOT NULL, email VARCHAR(255) NOT NULL, phone VARCHAR(20) NOT NULL, address VARCHAR(255) NOT NULL, category VARCHAR(50) NOT NULL, description TEXT NOT NULL, priority VARCHAR(10) NOT NULL,status varchar(200), attachment_path VARCHAR(255))")
mycursor.execute("create table if not exists paytax(id int primary key auto_increment,category  varchar(255),amount varchar(200),email varchar(200))")
mycursor.execute("CREATE TABLE if not exists schemes (id INT AUTO_INCREMENT PRIMARY KEY,scheme_name VARCHAR(255) NOT NULL,scheme_link VARCHAR(255) NOT NULL)")
mycursor.execute("CREATE TABLE if not exists notifications (id INT AUTO_INCREMENT PRIMARY KEY,notification_title VARCHAR(255) NOT NULL,notification_content VARCHAR(255) NOT NULL)")


app = Flask(__name__)
app.secret_key = 'egarm'


"-------------------------------------------------------------------------------"

@app.route('/')
def home():
    return render_template('home.html')

"---------------------------------------------------------------------------------"

@app.route('/login')
def login():
    return render_template('login.html')


"----------------------------------------------------------------------------"

# @app.route('/register')
# def register():
#     return render_template('register.html')


"------------------------------------------------------------------------------"


@app.route('/pregistration',methods =['GET', 'POST'])
def pregistration():
  if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form.get('name')
        password=request.form.get('password')
        email = request.form.get('email')
        mycursor.execute("SELECT * FROM pdoreg WHERE email = '"+ email +"' ")
        account = mycursor.fetchone()
        if account:
            flash('You are already registered, please log in')
        else:
            
            mycursor.execute("insert into pdoreg values(NULL,'"+ name +"','"+ email +"','"+ password +"')")
            # msg=flash('You have successfully registered !')
            return render_template("pdologin.html")
  return render_template("pregistration.html")


"---------------------------------------------------------------------"

@app.route('/uregistration',methods =['GET', 'POST'])
def uregistration():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form.get('name')
        password=request.form.get('password')
        email = request.form.get('email')
        mycursor.execute("SELECT * FROM userreg WHERE email = '"+ email +"' ")
        account = mycursor.fetchone()
        if account:
            flash('You are already registered, please log in')
        else:
            
            mycursor.execute("insert into  userreg values(NULL,'"+ name +"','"+ email +"','"+ password +"')")
            # msg=flash('You have successfully registered !')
            return render_template("userlogin.html")
    return render_template("uregistration.html")
        

"------------------------------------------------------------"

@app.route('/userlogin',methods =['GET', 'POST'])
def userlogin():
    if request.method == 'POST' and 'first' in request.form and 'password' in request.form:
        email = request.form['first']
        password = request.form['password']
        
        mycursor.execute("SELECT * FROM userreg WHERE email = '"+ email +"' AND upassword = '"+ password +"'")
        account = mycursor.fetchone()
        print(account)
        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            msg = flash('Logged in successfully !')
                
            return render_template('useraction.html')
        else:
            msg = flash('Incorrect username / password !')
            return render_template('userlogin.html',msg=msg)
    return render_template('userlogin.html')

"------------------------------------------------------------------"

@app.route('/pdologin',methods =['GET', 'POST'])
def pdologin():
    if request.method == 'POST' and 'first' in request.form and 'password' in request.form:
        email = request.form['first']
        password = request.form['password']
        
        mycursor.execute("SELECT * FROM pdoreg WHERE email = '"+ email +"' AND ppassword = '"+ password +"'")
        account = mycursor.fetchone()
        print(account)
        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            msg = flash('Logged in successfully !')
                
            return render_template('pdoaction.html')
        else:
            msg = flash('Incorrect username / password !')
            return render_template('pdologin.html',msg=msg)
    return render_template('pdologin.html')



"----------------------------------------------------------------"

@app.route('/adminlogin',methods =['GET', 'POST'])
def adminlogin():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
    
        email = request.form['email']
        password = request.form['password']

        if email=='admin@gmail.com' and password=='admin':
            return render_template('adminaction.html')
        else:
            return render_template('login.html')
        
    return render_template('adminlogin.html')

"-----------------------------------------------------------------"



@app.route('/Complaint',methods=['GET','POST'])
def Complaint():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        category = request.form['category']
        description = request.form['description']
        priority = request.form['priority']
        status = "Pending"  # Initial status for new complaints
        mycursor.execute("INSERT INTO complaints (name, email, phone, address, category, description, priority, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                         (name, email, phone, address, category, description, priority, status))
        msg='Your Complaint Submitted Sucessfully'

        return render_template('complaint.html',msg=msg)


    return render_template('complaint.html')
"--------------------------------------------------------------------"


@app.route('/submit_payment', methods=['GET','POST'])
def submit_payment():
    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['amount']
        if 'loggedin' in session and session['loggedin']:
            # Get the user's email from the session
            email = session['email']

        
        mycursor.execute("INSERT INTO paytax (category, amount,email) VALUES (%s, %s,%s)", (category, amount,email))
      

        msg= 'Payment submitted successfully!'
        return render_template('paytax.html',msg=msg)


    return render_template('paytax.html')




"-----------------------------------------------------"

@app.route('/viewuser')
def viewuser():
    mycursor.execute("select * from userreg")
    value=mycursor.fetchall()
    return render_template('viewuser.html',value=value)
"--------------------------------------------------------------"


@app.route('/add_scheme', methods=['GET', 'POST'])
def add_scheme():
    if request.method == 'POST':
        scheme_name = request.form['scheme_name']
        scheme_link = request.form['scheme_link']

        mycursor.execute("INSERT INTO schemes (scheme_name, scheme_link) VALUES (%s, %s)", (scheme_name, scheme_link))

        msg='Scheme added successfully!'

        return render_template('addscheme.html',msg=msg)


    return render_template('addscheme.html')

"----------------------------------------------------------------------"


@app.route('/add_notification', methods=['GET', 'POST'])
def add_notification():
    if request.method == 'POST':
        notification_title = request.form['notification_title']
        notification_content = request.form['notification_content']

      
        mycursor.execute("INSERT INTO notifications (notification_title, notification_content) VALUES (%s, %s)", (notification_title, notification_content))
        

        msg='Notification added successfully!'
        return render_template('addnotification.html',msg=msg)

    return render_template('addnotification.html')


"--------------------------------------------------------------------------"


@app.route('/view_complaints')
def view_complaints():

    mycursor.execute("SELECT * FROM complaints")
    complaints = mycursor.fetchall()
    print(complaints)
    return render_template('complaints.html', complaints=complaints)

"-------------------------------------------------------------------"

@app.route('/complaint/<int:complaint_id>/take_action', methods=['GET', 'POST'])
def take_action(complaint_id):
    if request.method == 'POST':
        action = request.form['action']
        # comment = request.form['comment']
        mycursor.execute("UPDATE complaints SET status = %s WHERE id = %s",
                     (action, complaint_id))
       
        return redirect(url_for('view_complaints'))

    mycursor.execute("SELECT * FROM complaints WHERE id = %s", (complaint_id,))
    complaint = mycursor.fetchone()
    return render_template('take_action.html', complaint=complaint)



"---------------------------------------------------------------------"

@app.route('/viewaction')
def viewaction():

    mycursor.execute("SELECT * FROM complaints")
    complaints = mycursor.fetchall()
   
    return render_template('action.html', complaints=complaints)




"--------------------------------------------------------------------"

@app.route('/viewscheme')
def viewscheme():

    mycursor.execute("SELECT * FROM schemes")
    schemes = mycursor.fetchall()
    
    return render_template('viewscheme.html', schemes=schemes)

@app.route('/viewnotification')
def viewnotification():

    mycursor.execute("SELECT * FROM notifications")
    notifications = mycursor.fetchall()
    
    return render_template('notifications.html', notifications=notifications)

if __name__ == "__main__":
    app.run(debug=True)
