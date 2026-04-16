from datetime import datetime
from flask import Flask,request,redirect,render_template,session,url_for
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL=os.getenv(
    "DATABASE_URL",
    "postgresql://postgres.wegsxzwhrdhqsvkuqweg:codexhusseinmartinnkya@aws-1-eu-central-1.pooler.supabase.com:5432/postgres",
)

app=Flask(__name__)
app.secret_key='mysecrete12'


@app.route('/')
def home():
        return redirect(url_for('login'))
    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username').strip().upper()
        password=request.form.get('password')
        value=[password,username]
        values,error=login_users(value)

        catch_password(password)

        error="wrong credentials!"
        if not values:
            return render_template('login.html',error=error)


        if username == values['roles'] and password == values['passwords']:
            session['username']=username
            session['password']=password
            if username == 'HOMEROOM':
                   print(password)

                   return redirect(url_for('homeroom_sheet'))
            
            elif username == 'ADMIN' :
              print(password)
              return redirect(('dashboard_admin'))
    
    return render_template('login.html')



def login_users(value):
    sql="""
    SELECT roles,passwords FROM manage_user
    WHERE passwords=%s AND roles=%s
"""

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,value)
                row=cur.fetchone()
            conn.commit()
        return row,None
    except Exception as e:
        print('ERROR',e)
        return False,None

def hoomroom_summary(value):
    sql="""
   SELECT classes,streams,round_circle,names,year
   FROM manage_user
   WHERE passwords=%s
"""
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
           with conn.cursor(cursor_factory=RealDictCursor) as cur:
               cur.execute(sql,(value,))
               row=cur.fetchone()
           conn.commit()
        return row,None
    except Exception as e:
        print('ERROR',e)
        return False,None
           

            
@app.route('/uptime')
def uptime():
    return 'Uptime: 24 hours'

@app.route('/homeroom_res',methods=['GET','POST'])
def homeroom_dashboard():
    st_name=request.form['name']
    topic=request.form['topic']
    date=request.form['date']
    time=request.form['time_spent']
    grade=request.form['grade']
    speech_grade=request.form['speech_grade']
    comment=request.form['comment']

    dt = datetime.strptime(date,"%Y-%m-%dT%H:%M")
    nice_date = dt.strftime("%d %B %Y,%H:%M")

    return render_template('homeroom_res.html',name=st_name,topic=topic,date=nice_date,time=time,grade=grade,speech_grade=speech_grade,comment=comment)

@app.route('/homeroom_sheetb')
def homeroom_sheetb():
    return render_template('homeroom_sheetb.html')

@app.route('/homeroom_resb', methods=['GET','POST'])
def homeroom_resb():
    name=request.form['name']
    topic=request.form['topic']
    date=request.form['date']
    time_spent=request.form['time_spent']
    grade=request.form['grade']
    speech_grade=request.form['speech_grade']
    section2_marks=request.form['section2_marks']
    comment=request.form['comment']
    
    dt = datetime.strptime(date,"%Y-%m-%dT%H:%M")
    nice_date = dt.strftime("%d %B %Y,%H:%M")

    return render_template('homeroom_resb.html',name=name,topic=topic,date=nice_date,time_spent=time_spent,grade=grade,speech_grade=speech_grade,section2_marks=section2_marks,comment=comment)

@app.route('/dashboard_admin' , methods=['POST','GET'])
def dashboard_admin():

    getting,losing=admin_summary(session['password'])

    if not getting:
        print('ERROR',losing)

    name=getting['names']
    role=getting['roles']
    year=getting['year']

    cool=None
    success=None

    if request.method=='POST':
        if 'speech_round' in request.form:
            dates=request.form.get('date')
            
            cool,burn=speech_circle(dates)
            if not cool:
                print('ERROR',burn)

       

 


    

    return render_template('dashboard_admin.html',names=name,roles=role,years=year,cool=cool,success=success)

def admin_summary(values):
    sql='''
    SELECT names,roles,year
    FROM manage_user
    WHERE passwords=%s
'''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchone()
            conn.commit()
        return row,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)

def speech_circle(values):
    #filter admin speech circles
    sql='''
     SELECT name,topic,date_speech,time_grade,speech_quality,round_circle,classes,stream,total_score
     FROM speech_table 
     WHERE date_speech=%s
'''
    
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)

@app.route('/admin_report_sc',methods=['POST','GET'])
def admin_report_lb():


  success=None
  suv=None

  if request.method=='POST':
     if 'report' in request.form:
            from_date=request.form.get('from')
            to_date=request.form.get('to')

            set_coty=[from_date,to_date]
            success,ery=admin_report(set_coty)

            if not success:
                print('ERROR',ery)

     if 'report_optional' in request.form:
           from_date=request.form.get('from')
           to_date=request.form.get('to')
            
           sez=[from_date,to_date]
           suv,ery=admin_optional(sez)

           if not suv:
               print('ERROR',ery)

  return render_template('admin_report.html',success=success,suv=suv)

    
def admin_report(values):
    sql='''
     SELECT name,classes,stream,round_circle,total_score,date_report
     FROM report_table
     WHERE date_report BETWEEN %s AND %s

'''
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,values)
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)

def admin_optional(values):
    sql='''
    SELECT names,reason,classes,stream,round_circle,date_report
    FROM optional_winner
    WHERE date_report BETWEEN %s AND %s
'''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,values)
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)

@app.route('/manage_user')
def manage_user():
    success,error=hm_users()
    

    if not success :
        print('DATABASE_ERROR',error)
    return render_template('manage_user.html',users=success)



@app.route('/new',methods=['POST','GET'])
def allocate():

    if request.method=='POST':
        homeroom=request.form['hm']
        role=request.form['role']
        classe=request.form['class']
        stream=request.form['stream']
        password=request.form['password']
        rounds=request.form['round']

        homeroom=homeroom.strip().upper()
        role=role.strip().upper()
        classe=classe.strip().upper()
        stream=stream.upper()
        password=password
        rounds=rounds


        values=[homeroom,role,classe,stream,password,rounds]
        success,error=insert_homeroom(values)
        if not success:
            print ("DATABASE ERROR",error)

    return render_template('new_hm.html')
def insert_homeroom(values):
    sql="""
     INSERT INTO manage_user(names,roles,classes,streams,passwords,round_circle,year)
     VALUES(%s,%s,%s,%s,%s,%s,%s)

"""

    try:
        with psycopg2.connect(DATABASE_URL, sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql, values)
            conn.commit()

        return True, None

    except Exception as e:
        print("DB ERROR:", e)
        return False, None



def hm_users():
    sql="""
     SELECT names,roles,classes,streams,passwords,round_circle,year
     FROM manage_user
"""  
     
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql)
                rows=cur.fetchall()
            conn.commit()
        return rows,None
    except Exception as e:
        print('DATABASE_ERROR',e)
        return False,str(e)


@app.route('/new_student',methods=['GET','POST'])
def new_student():
    if request.method=='POST':
        sjnumber=request.form.get('sjnumber').strip()
        name=request.form.get('name').strip().upper()
        classes=request.form.get('classes')
        stream=request.form.get('stream')
        circle=request.form.get('circle')
        year_speech=request.form.get('year_speech')
        confirm=request.form.get('confirm')


        
        values=(sjnumber,name,classes,stream,circle,year_speech,confirm)
        data,error=students(values)

        if not data:
            print('ERROR',error)

    return render_template('new_st.html')
    
# a function that holds password from the login for summary puropose
def catch_password(value):
    print('password:',value)

#this is the function which enter data in the students database
def students(data):
    sql="""
     INSERT INTO manage_student(sjnumber,name,classes,stream,round_circle,year_speech,status)
     VALUES(%s,%s,%s,%s,%s,%s,%s)
     ON CONFLICT(sjnumber)
     DO UPDATE SET name = EXCLUDED.name;
"""
     
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,data)
            conn.commit()
        return True,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)


@app.route('/homeroom_setting',methods=['POST','GET'])
def hm_setting():
    
    catch_password(session['password'])

    passey=session['password']

    summary,opps=hoomroom_summary(session['password'])

    if not summary: 
        return render_template('hm_setting.html',classes=[],streams=[],rounds=[],names=[],year=[])


    classes=summary['classes']
    streams=summary['streams']
    rounds=summary['round_circle']
    names=summary['names']
    year=summary['year']

    get_fork=[classes,streams]
    success,chaos=select_all_student(get_fork)

    if not success:
        print(chaos)

    if request.method=='POST':
        if 'change_homeroom' in request.form:
           round_get=request.form.get('round')
           year_get=request.form.get('year')
           password_get=request.form.get('password')
          
          
           sets = [round_get, password_get, year_get, names]

           homeroom_change(sets)

        elif 'change_student' in request.form:        
          
          sjnumber=request.form.get('sjnumber')
          name=request.form.get('name')
          classes=request.form.get('classes')
          stream=request.form.get('stream')
          rounds=request.form.get('rounds')
          year=request.form.get('year')
          status=request.form.get('status')

          sets_student=[name,classes,stream,rounds,year,status,sjnumber]
          student_change(sets_student)   


          

    return render_template('hm_setting.html',passey=passey,classes=classes,streams=streams,rounds=rounds,names=names,year=year,success=success)


def homeroom_change(value):
    sql='''
    UPDATE manage_user
    SET 
    round_circle = %s,
    passwords = %s,
    year = %s
    WHERE  names = %s;
    
'''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,value)
            conn.commit()
        return True,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)

def student_change(value):
    sql='''
      UPDATE manage_student
      SET
      name=%s,
      classes=%s,
      stream=%s,
      round_circle=%s,
      year_speech=%s,
      status=%s
      WHERE sjnumber=%s;
'''
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,value)
            conn.commit()
        return True,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)


def select_all_student(value):
    sql='''
     SELECT sjnumber,name,classes,stream,round_circle,year_speech
     FROM manage_student
     WHERE classes=%s AND stream=%s
   '''
    
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,value)
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)
    

@app.route('/homeroom_sheet',methods=['GET','POST'])

def homeroom_sheet():
  
  if "password" not in session:
        return redirect(url_for('login'))

  if 'password' in session:

    print(session['password'])
    summary,opps=hoomroom_summary(session['password'])

    if not summary: 
        return redirect(url_for('login'))
       #print(opps) 

    classes=summary['classes']
    streams=summary['streams']
    rounds=summary['round_circle']
    names=summary['names']
    year=summary['year']
    
    

    lists=[classes,streams,rounds,year]
    
    names_for_student,error=all_student_name(lists)

    
    if not names_for_student:
        print('ERROR',error)


    get_names=names_for_student

     
    if request.method=='POST':

        name=request.form.get('name')
        classey=request.form.get('classey').strip()
        streamey=request.form.get('streamey').strip()
        topic=request.form.get('topic').strip().upper()
        date_speech=request.form.get('date_speech')
        time_spent=request.form.get('time_spent').strip()
        time_grade=request.form.get('time_grade')
        speech_grade=request.form.get('speech_grade')
        comment=request.form.get('comment').strip().upper()
        year_speech=request.form.get('year_speech').strip()
        rounds=request.form.get('rounds').strip()
        total_score=int(time_grade)+int(speech_grade)
        
        value=[name,topic,date_speech,time_spent,time_grade,speech_grade,comment,year_speech,rounds,classey,streamey,total_score]

        sent,error=save_speech_info(value)
        if not sent:
            print('ERROR',error)
        if sent:
            datas=[name,rounds,year_speech]
            success,mist=get_confirm(datas)

            if not success:
                print('error')
        
            
    
    
    return render_template('homeroom_sheet.html',classes=classes,streams=streams,rounds=rounds,names=names,year=year,get_names=get_names,opps=opps)   
  

def get_confirm(value):
    sql='''
        UPDATE manage_student
        SET status = TRUE
        WHERE name = %s AND round_circle = %s AND year_speech = %s;
'''
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,value)
            conn.commit()
        return True,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)

#this is the function that will be responsible to handle the information and take it to the database of speech
def save_speech_info(value):

    sql="""
      INSERT INTO speech_table(name,topic,date_speech,time_spent,time_grade,speech_quality,comment,year_speech,round_circle,classes,stream,total_score)
      VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,value)
            conn.commit()
        return True,None
    except Exception as e:
        print(e)
        return False,str(e)

    #this fuction select all the name of that particular class
def all_student_name(value):
    sql="""
    SELECT name FROM manage_student
    WHERE classes=%s AND stream=%s AND round_circle=%s AND year_speech=%s AND status=FALSE
"""
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,value)
                name=cur.fetchall()
            conn.commit()
        return name,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)



@app.route('/manage_student',methods=['POST','GET'])
def manage_student():
    return render_template('manage_student.html')


@app.route('/view_student',methods=['POST','GET'])
def view_student():
    
    first_catch=[]
    
    if request.method=='POST':
        classes_get=request.form.get('classes')
        stream_get=request.form.get('stream')
        circle_round=request.form.get('circle')
        year_speech=request.form.get('year_speech')

        sets=[classes_get,stream_get,circle_round,year_speech]

        

        first_catch,first_catch_error=view_data_round(sets)

        if not first_catch:
          print(first_catch_error)    

    return render_template('view_student.html',first_catch=first_catch)

def view_data_round(value):
    sql='''
  SELECT name,topic,date_speech,time_spent,round_circle,classes,stream
  FROM speech_table
  WHERE classes=%s AND stream=%s AND round_circle=%s AND year_speech=%s

'''
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,value)
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)
    

@app.route('/homeroom_report',methods=['POST','GET'])
def homeroom_report():

    summary,opps=hoomroom_summary(session['password'])

    if not summary: 
        return redirect(url_for('login'))
       #print(opps) 

    classes=summary['classes']
    streams=summary['streams']
    rounds=int(summary['round_circle'])
    names=summary['names']
    year=summary['year']

    

    year_fil = year
    class_fil = classes
    current_round = rounds
   

    set_value=[year_fil,class_fil,current_round]
    
    hoorey,opps=preview_db_report(set_value)
    if not hoorey:
        print(opps)

    if request.method=='POST':
      if 'current_winner' in request.form:
        name = request.form.get('name')
        classey = request.form.get('class')
        stream = request.form.get('stream')
        round_circle = request.form.get('rounds')
        score = request.form.get('score')
        year_sent = request.form.get('year_sent')


        set_catched=[name,classey,stream,round_circle,score,year_sent]
        first_winner(set_catched)
      elif 'optional_winner' in request.form:
        namez=request.form.get('name')
        reason=request.form.get('reason')
        classez=request.form.get('class')
        streamz=request.form.get('stream')
        roundz=request.form.get('rounds')
      
        set_op=[namez,reason,classez,streamz,roundz]
        option_db(set_op)

    return render_template('hm_report.html',classes=classes,streams=streams,rounds=rounds,names=names,year=year,hoorey=hoorey)
    

def first_winner(values):
    sql='''

    INSERT INTO report_table(names,classes,stream,total_score,round_circle,year_sent)
    VALUES(%s,%s,%s,%s,%s,%s)

'''
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)
    

def option_db(values):
    sql='''
   INSERT INTO optional_winner(names,reason,classes,stream,round_circle)
   VALUES(%s,%s,%s,%s,%s)
'''

    try:
       with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
           with conn.cursor() as cur:
               cur.execute(sql,values)
               conn.commit()
           return True,None
    except Exception as e:
        print('ERROR',e)
        return False,str(e)

     


def preview_db_report(value):
    sql='''
    SELECT 
        name,
        classes,
        stream,
        round_circle,
        total_score
    FROM speech_table
    WHERE 
        year_speech = %s
        AND classes = %s
        AND round_circle = %s
    ORDER BY total_score DESC
    LIMIT 3;
'''
   
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,value)
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        print('ERROR',e)
        return [],str(e)


     


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(host="0.0.0.0", port=port)
