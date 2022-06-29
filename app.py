
from ast import Not
import webbrowser
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy import true
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import sqlalchemy.sql.default_comparator


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function





# Configure application
app = Flask(__name__)


    
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")

webbrowser.open('http://192.168.1.125:5000/', new = 2)


id_copy = 0
global checks
checks = 0

@app.route("/new_med" , methods=["GET" , "post"])
def new_med():
    med_name_list = db.execute("SELECT medicine FROM madicine_list ")
    i = len(med_name_list)
    
    if request.method == "POST":
        db.execute("INSERT INTO madicine_list (code ,medicine ,buy_price, sell_price, global_code )VALUES (?, ?, ?, ?, ? )",i,request.form.get("med_name"),request.form.get("med_buy"),request.form.get("med_sell"),request.form.get("med_code"))

        return redirect("/new_med")

    else :
        return render_template("new_med.html")




@app.route("/med_list" , methods=["GET" , "post"])
def med_list():
    med_name_list = []
    med_name = []
    med_buy = []
    med_sell = []
    med_code = []
    med_all = []

    med_name_list = db.execute("SELECT medicine FROM madicine_list ")
    med_buy_list = db.execute("SELECT buy_price FROM madicine_list ")
    med_sell_list = db.execute("SELECT sell_price FROM madicine_list ")
    med_code_list = db.execute("SELECT global_code FROM madicine_list ")

    for i in range( len(med_name_list) ) :
        med_name.append(med_name_list[i]["medicine"])
        med_buy.append(med_buy_list[i]["buy_price"])
        med_sell.append(med_sell_list[i]["sell_price"])
        med_code.append(med_code_list[i]["global_code"])
        med_all.append([med_name_list[i]["medicine"],med_buy_list[i]["buy_price"],med_sell_list[i]["sell_price"],med_code_list[i]["global_code"]])

    if request.method == "POST":
        db.execute("DELETE FROM madicine_list " )
        for i in range( len(med_name_list)) :
            db.execute("INSERT INTO madicine_list (code ,medicine ,buy_price, sell_price, global_code )VALUES (?, ?, ?, ?, ? )", i ,request.form.get("med_name_%s" %i),request.form.get("med_buy_%s" %i),request.form.get("med_sell_%s" %i),request.form.get("med_code_%s" %i))

        return redirect("/med_list")

    else :
        return render_template("med_list.html",med_name=med_name ,med_buy=med_buy ,med_sell=med_sell ,med_code=med_code)





@app.route("/edit" , methods=["GET", "POST"])
@login_required
def edit():

    if request.method == "POST":
        if request.form.get('action') =="one" :
            session.clear()
            return redirect("/med_list")

        if request.form.get('action') =="two" :
            session.clear()
            return redirect("/new_med")


    else :
        return render_template("edit.html" )

user_id = 404

@app.route("/history")
#@login_required
def history():
    print(checks)
    if checks == 1 :
        id = []
        dec = []
        med = []
        quan = []
        buy = []
        sell = []
        code = []
        date = []

        history = db.execute("SELECT patient_id , dec_num , med , quantity , buy_price , sell_price , global_code , date FROM patient_medicine WHERE date Like ? " , select_date_1+"%" )

        if not select_date_2 == 0 :
            history.append(db.execute("SELECT patient_id , dec_num , med , quantity , buy_price , sell_price , global_code , date FROM patient_medicine WHERE date Like ? " , select_date_2+"%" ))

        if not select_date_3 == 0 :
            history.append(db.execute("SELECT patient_id , dec_num , med , quantity , buy_price , sell_price , global_code , date FROM patient_medicine WHERE date Like ? " , select_date_3+"%" ))

        if not history == [[], []] and not history == [] :
            history = sorted(history, key=lambda d: d['dec_num']) 
            history = sorted(history, key=lambda d: d['patient_id']) 


            for i in range( len(history) ):

                if i == 0 :
                    id.append ([str(history[i]["patient_id"]) + " - " + db.execute("SELECT name FROM patient WHERE patient_id = ? " , history[i]["patient_id"] )[0]['name']])
                    dec.append ("")
                    med.append( "")
                    quan.append( "")
                    buy.append( "")
                    sell.append( "")
                    code.append( "")
                    date.append( "")

                    dec.append (history[i]["dec_num"])
                    id.append ("")
                    med.append( "")
                    quan.append( "")
                    buy.append( "")
                    sell.append( "")
                    code.append( "")
                    date.append( "")

                

                else :
                    if not history[i]["patient_id"] == history[i-1]["patient_id"] :
                        
                        id.append ("")
                        dec.append ("")
                        med.append( "")
                        quan.append( "")
                        buy.append( "")
                        sell.append( "")
                        code.append( "")
                        date.append( "")

                        id.append ([str(history[i]["patient_id"]) + " - " + db.execute("SELECT name FROM patient WHERE patient_id = ? " , history[i]["patient_id"] )[0]['name']])
                        dec.append ("")
                        med.append( "")
                        quan.append( "")
                        buy.append( "")
                        sell.append( "")
                        code.append( "")
                        date.append( "")


                    if not history[i]["dec_num"] == history[i-1]["dec_num"] :
                        

                        dec.append (history[i]["dec_num"])
                        id.append ("")
                        med.append( "")
                        quan.append( "")
                        buy.append( "")
                        sell.append( "")
                        code.append( "")
                        date.append( "")


                id.append ("")
                dec.append ("")
                med.append( history[i]["med"])
                quan.append( history[i]["quantity"])
                buy.append( history[i]["buy_price"])
                sell.append( history[i]["sell_price"])
                code.append( history[i]["global_code"])
                date.append( history[i]["date"])
                

        else :
                return render_template("history.html" ,wrong = "لا يوجد سجلات لهذه الفتره" ,id ="404",med="404",date="404",dec="404",quan="404",buy="404",sell="404",code="404")

        return render_template("history.html" ,date = date , id = id , med = med , dec = dec , quan = quan , buy = buy , sell = sell , code = code)

    if checks == 0 :
        return render_template("archive.html" )


@app.route("/archive", methods=["GET", "POST"])
#@login_required
def archive():
    session.clear()
    global select_date_1
    global select_date_2
    global select_date_3
    select_date_1 = 0
    select_date_2 = 0
    select_date_3 = 0
    global checks
    

    if request.method == "POST":
        
        if request.form.get("dateselect") == None :
            return render_template("archive.html" ,wrong = "يجب اختيار تاريخ")

        elif request.form.get("dateselect")[0:5] == "3_mon" :
            #select_date_1 : 2022-06
            select_date_1 = request.form.get("dateselect")[5:12] 
            select_date_2 = request.form.get("dateselect")[12:19] 
            select_date_3 = request.form.get("dateselect")[19:]
            
            checks = 1
            return redirect("/history")

        else:
            select_date_1 = request.form.get("dateselect")
            checks = 1
            return redirect("/history")

    else:
        return render_template("archive.html")




@app.route("/recm", methods=["GET", "POST"])
#@login_required
def recm():
    med_name_list = []
    med_name = []
    med_buy = []
    med_sell = []
    med_code = []

    med_name_list = db.execute("SELECT medicine FROM madicine_list ")
    med_buy_list = db.execute("SELECT buy_price FROM madicine_list ")
    med_sell_list = db.execute("SELECT sell_price FROM madicine_list ")
    med_code_list = db.execute("SELECT global_code FROM madicine_list ")

    for i in range( len(med_name_list) ) :
        med_name.append(med_name_list[i]["medicine"])
        med_buy.append(med_buy_list[i]["buy_price"])
        med_sell.append(med_sell_list[i]["sell_price"])
        med_code.append(med_code_list[i]["global_code"])
     
    if request.method == "POST":
        x = 0
        i = 1
        for m in range( 14 ) :            
            if not request.form.get("buy_%s" %i) == "":
                if not request.form.get("med_%s_n" %i) == "":
                    if not request.form.get("rec_num") == "":
                        if not request.form.get("dec_num") == "":
                            if not request.form.get("credit") == "":
                                x -= 1 
                                db.execute("INSERT INTO patient_medicine (med ,patient_id, quantity, user_id, rec_num, dec_num, pharmacist, section, credit, note, buy_price, sell_price, global_code , percent ,total	)VALUES (?, ?, ?, ? ,?, ? ,?, ?, ? ,?, ?, ? ,?, ?, ? )",request.form.get("med_%s" %i),float(p_id) ,float(request.form.get("med_%s_n" %i)) , user_id ,float(request.form.get("rec_num")), float(request.form.get("dec_num")) , request.form.get("pharmacist") , request.form.get("section") , float(request.form.get("credit")) , request.form.get("note") ,float(request.form.get("buy_%s" %i)) ,float(request.form.get("sell_%s" %i)), float(request.form.get("code_%s" %i)) , float(request.form.get("7_%s" %i)), float(request.form.get("buy_price_%s" %i)))
            x += 1
            i += 1
        
        if x == 14 :
            return render_template("recm.html", wrong = "يجب اكمال الفاتوره", p_name=p_name , med_name=med_name ,med_buy = med_buy ,med_sell = med_sell , med_code = med_code)
            
        patient_id = []
        patient_id_list = []

        patient_id_list = db.execute("SELECT patient_id FROM patient ")

        for i in range( len(patient_id_list) ) :
            patient_id.append(patient_id_list[i]["patient_id"])

        return render_template("index.html",done="- تم تسجيل الفاتوره -" , patient_id=patient_id)
    
    else:
        if check == 1 :
            db.execute("DELETE FROM patient_medicine WHERE patient_id  = ? and  date = ? and time LIKE  ?" , p_id , date_ch , time_ch+"%" )

        if  len(old)  == 1:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def )

        if  len(old)  == 2:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def  )

        if  len(old)  == 3:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def   )

        if  len(old)  == 4:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def   )

        if  len(old)  == 5:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            med_5_def = old[4]["med"]
            med_5_n_def = old[4]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def , med_5_def = med_5_def, med_5_n_def = med_5_n_def   )

        if  len(old)  == 6:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            med_5_def = old[4]["med"]
            med_5_n_def = old[4]["quantity"]

            med_6_def = old[5]["med"]
            med_6_n_def = old[5]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def , med_5_def = med_5_def, med_5_n_def = med_5_n_def , med_6_def = med_6_def, med_6_n_def = med_6_n_def   )

        if  len(old)  == 7:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            med_5_def = old[4]["med"]
            med_5_n_def = old[4]["quantity"]

            med_6_def = old[5]["med"]
            med_6_n_def = old[5]["quantity"]

            med_7_def = old[6]["med"]
            med_7_n_def = old[6]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def , med_5_def = med_5_def, med_5_n_def = med_5_n_def , med_6_def = med_6_def, med_6_n_def = med_6_n_def , med_7_def = med_7_def, med_7_n_def = med_7_n_def   )

        if  len(old)  == 8:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            med_5_def = old[4]["med"]
            med_5_n_def = old[4]["quantity"]

            med_6_def = old[5]["med"]
            med_6_n_def = old[5]["quantity"]

            med_7_def = old[6]["med"]
            med_7_n_def = old[6]["quantity"]

            med_8_def = old[7]["med"]
            med_8_n_def = old[7]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def , med_5_def = med_5_def, med_5_n_def = med_5_n_def , med_6_def = med_6_def, med_6_n_def = med_6_n_def , med_7_def = med_7_def, med_7_n_def = med_7_n_def , med_8_def = med_8_def, med_8_n_def = med_8_n_def   )

        if  len(old)  == 9:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            med_5_def = old[4]["med"]
            med_5_n_def = old[4]["quantity"]

            med_6_def = old[5]["med"]
            med_6_n_def = old[5]["quantity"]

            med_7_def = old[6]["med"]
            med_7_n_def = old[6]["quantity"]

            med_8_def = old[7]["med"]
            med_8_n_def = old[7]["quantity"]

            med_9_def = old[8]["med"]
            med_9_n_def = old[8]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def , med_5_def = med_5_def, med_5_n_def = med_5_n_def , med_6_def = med_6_def, med_6_n_def = med_6_n_def , med_7_def = med_7_def, med_7_n_def = med_7_n_def , med_8_def = med_8_def, med_8_n_def = med_8_n_def , med_9_def = med_9_def, med_9_n_def = med_9_n_def   )

        if  len(old)  == 10:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            med_5_def = old[4]["med"]
            med_5_n_def = old[4]["quantity"]

            med_6_def = old[5]["med"]
            med_6_n_def = old[5]["quantity"]

            med_7_def = old[6]["med"]
            med_7_n_def = old[6]["quantity"]

            med_8_def = old[7]["med"]
            med_8_n_def = old[7]["quantity"]

            med_9_def = old[8]["med"]
            med_9_n_def = old[8]["quantity"]

            med_10_def = old[9]["med"]
            med_10_n_def = old[9]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def , med_5_def = med_5_def, med_5_n_def = med_5_n_def , med_6_def = med_6_def, med_6_n_def = med_6_n_def , med_7_def = med_7_def, med_7_n_def = med_7_n_def , med_8_def = med_8_def, med_8_n_def = med_8_n_def , med_9_def = med_9_def, med_9_n_def = med_9_n_def , med_10_def = med_10_def, med_10_n_def = med_10_n_def  )

        if  len(old)  == 11:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            med_5_def = old[4]["med"]
            med_5_n_def = old[4]["quantity"]

            med_6_def = old[5]["med"]
            med_6_n_def = old[5]["quantity"]

            med_7_def = old[6]["med"]
            med_7_n_def = old[6]["quantity"]

            med_8_def = old[7]["med"]
            med_8_n_def = old[7]["quantity"]

            med_9_def = old[8]["med"]
            med_9_n_def = old[8]["quantity"]

            med_10_def = old[9]["med"]
            med_10_n_def = old[9]["quantity"]

            med_11_def = old[10]["med"]
            med_11_n_def = old[10]["quantity"]


            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def , med_5_def = med_5_def, med_5_n_def = med_5_n_def , med_6_def = med_6_def, med_6_n_def = med_6_n_def , med_7_def = med_7_def, med_7_n_def = med_7_n_def , med_8_def = med_8_def, med_8_n_def = med_8_n_def , med_9_def = med_9_def, med_9_n_def = med_9_n_def , med_10_def = med_10_def, med_10_n_def = med_10_n_def , med_11_def = med_11_def, med_11_n_def = med_11_n_def  )

        if  len(old)  == 12:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            med_5_def = old[4]["med"]
            med_5_n_def = old[4]["quantity"]

            med_6_def = old[5]["med"]
            med_6_n_def = old[5]["quantity"]

            med_7_def = old[6]["med"]
            med_7_n_def = old[6]["quantity"]

            med_8_def = old[7]["med"]
            med_8_n_def = old[7]["quantity"]

            med_9_def = old[8]["med"]
            med_9_n_def = old[8]["quantity"]

            med_10_def = old[9]["med"]
            med_10_n_def = old[9]["quantity"]

            med_11_def = old[10]["med"]
            med_11_n_def = old[10]["quantity"]

            med_12_def = old[11]["med"]
            med_12_n_def = old[11]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def , med_5_def = med_5_def, med_5_n_def = med_5_n_def , med_6_def = med_6_def, med_6_n_def = med_6_n_def , med_7_def = med_7_def, med_7_n_def = med_7_n_def , med_8_def = med_8_def, med_8_n_def = med_8_n_def , med_9_def = med_9_def, med_9_n_def = med_9_n_def , med_10_def = med_10_def, med_10_n_def = med_10_n_def , med_11_def = med_11_def, med_11_n_def = med_11_n_def , med_12_def = med_12_def, med_12_n_def = med_12_n_def  )

        if  len(old)  == 13:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            med_5_def = old[4]["med"]
            med_5_n_def = old[4]["quantity"]

            med_6_def = old[5]["med"]
            med_6_n_def = old[5]["quantity"]

            med_7_def = old[6]["med"]
            med_7_n_def = old[6]["quantity"]

            med_8_def = old[7]["med"]
            med_8_n_def = old[7]["quantity"]

            med_9_def = old[8]["med"]
            med_9_n_def = old[8]["quantity"]

            med_10_def = old[9]["med"]
            med_10_n_def = old[9]["quantity"]

            med_11_def = old[10]["med"]
            med_11_n_def = old[10]["quantity"]

            med_12_def = old[11]["med"]
            med_12_n_def = old[11]["quantity"]

            med_13_def = old[12]["med"]
            med_13_n_def = old[12]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def , med_5_def = med_5_def, med_5_n_def = med_5_n_def , med_6_def = med_6_def, med_6_n_def = med_6_n_def , med_7_def = med_7_def, med_7_n_def = med_7_n_def , med_8_def = med_8_def, med_8_n_def = med_8_n_def , med_9_def = med_9_def, med_9_n_def = med_9_n_def , med_10_def = med_10_def, med_10_n_def = med_10_n_def , med_11_def = med_11_def, med_11_n_def = med_11_n_def , med_12_def = med_12_def, med_12_n_def = med_12_n_def , med_13_def = med_13_def, med_13_n_def = med_13_n_def  )

        if  len(old)  == 14:
            dec_num_def = old[0]["dec_num"]
            pharmacist_def = old[0]["pharmacist"]
            section_def = old[0]["section"]
            credit_def = old[0]["credit"]
            note_def = old[0]["note"]

            med_1_def = old[0]["med"]
            med_1_n_def = old[0]["quantity"]

            med_2_def = old[1]["med"]
            med_2_n_def = old[1]["quantity"]

            med_3_def = old[2]["med"]
            med_3_n_def = old[2]["quantity"]

            med_4_def = old[3]["med"]
            med_4_n_def = old[3]["quantity"]

            med_5_def = old[4]["med"]
            med_5_n_def = old[4]["quantity"]

            med_6_def = old[5]["med"]
            med_6_n_def = old[5]["quantity"]

            med_7_def = old[6]["med"]
            med_7_n_def = old[6]["quantity"]

            med_8_def = old[7]["med"]
            med_8_n_def = old[7]["quantity"]

            med_9_def = old[8]["med"]
            med_9_n_def = old[8]["quantity"]

            med_10_def = old[9]["med"]
            med_10_n_def = old[9]["quantity"]

            med_11_def = old[10]["med"]
            med_11_n_def = old[10]["quantity"]

            med_12_def = old[11]["med"]
            med_12_n_def = old[11]["quantity"]

            med_13_def = old[12]["med"]
            med_13_n_def = old[12]["quantity"]

            med_14_def = old[13]["med"]
            med_14_n_def = old[13]["quantity"]

            return render_template("recm.html",med_buy = med_buy ,med_sell = med_sell , med_code = med_code,note_def=note_def,credit_def=credit_def,section_def=section_def,dec_num_def=dec_num_def ,pharmacist_def=pharmacist_def , p_name=p_name , med_name=med_name , med_1_def = med_1_def, med_1_n_def = med_1_n_def , med_2_def = med_2_def, med_2_n_def = med_2_n_def , med_3_def = med_3_def, med_3_n_def = med_3_n_def , med_4_def = med_4_def, med_4_n_def = med_4_n_def , med_5_def = med_5_def, med_5_n_def = med_5_n_def , med_6_def = med_6_def, med_6_n_def = med_6_n_def , med_7_def = med_7_def, med_7_n_def = med_7_n_def , med_8_def = med_8_def, med_8_n_def = med_8_n_def , med_9_def = med_9_def, med_9_n_def = med_9_n_def , med_10_def = med_10_def, med_10_n_def = med_10_n_def , med_11_def = med_11_def, med_11_n_def = med_11_n_def , med_12_def = med_12_def, med_12_n_def = med_12_n_def , med_13_def = med_13_def, med_13_n_def = med_13_n_def  , med_14_def = med_14_def, med_14_n_def = med_14_n_def )



        return render_template("recm.html", p_name=p_name , med_name=med_name,med_buy = med_buy ,med_sell = med_sell , med_code = med_code)



@app.route("/his", methods=["GET", "POST"])
#@login_required
def his():
    dates=[]
    global date_ch 
    global time_ch
    global check
    global old
    
    if request.method == "POST":
        if not request.form.get("dates+"):
            dates_l = db.execute("SELECT date , time FROM patient_medicine WHERE patient_id  = ? " , p_id )
            for i in range( len(dates_l)) :
                dates.append(dates_l[i]['date'] + " | "+ dates_l[i]['time'][0:5])
            dates.sort(reverse = True)
            dates = list(dict.fromkeys(dates))
            return render_template("his.html", wrong = "يجب اختيار تاريخ" , dates=dates ,p_name=p_name)

        time_ch = request.form.get("dates+")[13:21]
        date_ch =  request.form.get("dates+")[0:10]
        old =db.execute("SELECT med , quantity , dec_num ,pharmacist, section ,credit, note FROM patient_medicine WHERE patient_id  = ? and  date = ? and time LIKE  ?" , p_id , date_ch , time_ch+"%" )

        if request.form.get('action') =="one" :
            check = 0
            return redirect("/recm")

        if request.form.get('action') =="two" :
            db.execute("DELETE FROM patient_medicine WHERE patient_id  = ? and  date = ? and time LIKE  ?" , p_id , date_ch , time_ch+"%" )
            return redirect("/his")
        
        if request.form.get('action') =="three" :
            check = 1
            return redirect("/recm")



    else :
        dates_l = db.execute("SELECT date , time FROM patient_medicine WHERE patient_id  = ? " , p_id )
        for i in range( len(dates_l)) :
            dates.append(dates_l[i]['date'] + " | "+ dates_l[i]['time'][0:5])
        dates.sort(reverse = True)
        dates = list(dict.fromkeys(dates))
        print(dates)
        return render_template("his.html", dates=dates ,p_name=p_name )

    




@app.route("/rec", methods=["GET", "POST"])
#@login_required
def rec():
    med_name_list = []
    med_name = []
    med_buy = []
    med_sell = []
    med_code = []

    med_name_list = db.execute("SELECT medicine FROM madicine_list ")
    med_buy_list = db.execute("SELECT buy_price FROM madicine_list ")
    med_sell_list = db.execute("SELECT sell_price FROM madicine_list ")
    med_code_list = db.execute("SELECT global_code FROM madicine_list ")

    for i in range( len(med_name_list) ) :
        med_name.append(med_name_list[i]["medicine"])
        med_buy.append(med_buy_list[i]["buy_price"])
        med_sell.append(med_sell_list[i]["sell_price"])
        med_code.append(med_code_list[i]["global_code"])


    if request.method == "POST":
        x = 0
        i = 1
        for m in range( 14 ) :            
            if not request.form.get("buy_%s" %i) == "":
                if not request.form.get("med_%s_n" %i) == "":
                    if not request.form.get("rec_num") == "":
                        if not request.form.get("dec_num") == "":
                            if not request.form.get("credit") == "":
                                x -= 1 
                                db.execute("INSERT INTO patient_medicine (patient_id, med, quantity, user_id, rec_num, dec_num, pharmacist, section, credit, note, buy_price, sell_price, global_code , percent ,total	)VALUES (?, ?, ?, ? ,?, ? ,?, ?, ? ,?, ?, ? ,?, ?, ? )",float(p_id) , request.form.get("med_%s" %i),float(request.form.get("med_%s_n" %i)) , user_id ,float(request.form.get("rec_num")), float(request.form.get("dec_num")) , request.form.get("pharmacist") , request.form.get("section") , float(request.form.get("credit")) , request.form.get("note") ,float(request.form.get("buy_%s" %i)) ,float(request.form.get("sell_%s" %i)), float(request.form.get("code_%s" %i)) , float(request.form.get("7_%s" %i)), float(request.form.get("buy_price_%s" %i)))
            x += 1
            i += 1
        
        if x == 14 :
            return render_template("rec.html", wrong = "يجب اكمال الفاتوره", p_name=p_name , med_name=med_name ,med_buy = med_buy ,med_sell = med_sell , med_code = med_code)

        patient_id = []
        patient_id_list = []

        patient_id_list = db.execute("SELECT patient_id FROM patient ")

        for i in range( len(patient_id_list) ) :
            patient_id.append(patient_id_list[i]["patient_id"])

        return render_template("index.html",done="- تم تسجيل الفاتوره -" , patient_id=patient_id)

    else:
    
        return render_template("rec.html", p_name=p_name , med_name=med_name ,med_buy = med_buy ,med_sell = med_sell , med_code = med_code)



@app.route("/register", methods=["GET", "POST"])
#@login_required
def register():
    session.clear()
    patient_id = []
    patient_id_list = []

    if request.method == "POST":
        id_c = request.form.get("new_id")
        name_c = request.form.get("new_name")

        if request.form.get('action') =="one" :

            patient_id_list = db.execute("SELECT patient_id FROM patient ")
            
            for i in range( len(patient_id_list) ) :
                patient_id.append(patient_id_list[i]["patient_id"])

            
            if not request.form.get("new_name"):
                if not request.form.get("new_id"):
                    return render_template("register.html", wrong = "يجب كتابة الاسم والرقم القومي")

            if not request.form.get("new_name"):
                return render_template("register.html", wrong = "يجب كتابة الاسم" , id_copy=id_c )

            if not request.form.get("new_id"):
                return render_template("register.html", wrong = "يجب كتابة الرقم القومي", name_copy = name_c)

            if not len( request.form.get("new_id") ) == 14 :
                return render_template("register.html", wrong = "الرقم القومي يجب ان يتكون من 14 رقم", id_copy=id_c , name_copy = name_c)

            for i in patient_id :
                if int(request.form.get("new_id")) == i :
                    return render_template("register.html", wrong = "هذا الرقم القومي مسجل بالفعل", id_copy=id_c , name_copy = name_c)

            db.execute("INSERT INTO patient (patient_id, name, 	user_id)VALUES (?, ?, ? )",int(request.form.get("new_id")) ,request.form.get("new_name") ,user_id )
            global p_name
            global p_id
            p_id = int(request.form.get("new_id"))
            p_name = request.form.get("new_name")
            return redirect("/rec")
        
        if request.form.get('action') =="three" :
            if not request.form.get("new_name"):
                if id_copy != 0 :
                    return render_template("register.html",id_copy=id_copy)
                else : 
                    return render_template("register.html")
            else :
                if id_copy != 0 :
                    return render_template("register.html",id_copy=id_copy,name_copy = name_c)
                else : 
                    return render_template("register.html", name_copy = name_c)

    else :
        return render_template("register.html")





@app.route("/", methods=["GET", "POST"])
#@login_required
def index():
    session.clear()
    patient_id = []
    patient_id_list = []
    global id_copy

    patient_id_list = db.execute("SELECT patient_id FROM patient ")

    for i in range( len(patient_id_list) ) :
        patient_id.append(patient_id_list[i]["patient_id"])

    
    if request.method == "POST":
        if not request.form.get("patient_id") or not request.form.get("patient_id").isdigit() :
            return render_template("index.html",patient_id=patient_id, wrong = "يجب كتابة الرقم القومي")

        if request.form.get('action') =="three" :
            id_copy = request.form.get("patient_id")
            print (id_copy)
            return render_template("index.html",patient_id=patient_id,p_d = request.form.get("patient_id"),  done = "تم النسخ")

        for i in patient_id :
            if int(request.form.get("patient_id")) == i :
                name = db.execute("SELECT name FROM patient WHERE patient_id = ? " , int(request.form.get("patient_id")) )
                global p_name
                global p_id
                p_id = int(request.form.get("patient_id"))
                p_name = name[0]['name']
                if request.form.get('action') =="one" :
                    return redirect("/rec")
                if request.form.get('action') =="two" :
                    return redirect("/his")
                        
        
        return render_template("index.html",patient_id=patient_id,p_d = request.form.get("patient_id"),  wrong = "يجب كتابة رقم قومي صحيح مسجل")

        

    else:
        # Ensure username was submitted
    
        return render_template("index.html", patient_id=patient_id)

        




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", wrong = "*must provide username*")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", wrong = "*must provide password*")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", wrong = "*invalid username and/or password*")

        global user_id
        user_id = rows[0]["id"]
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/edit")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=false)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

