from flask import *
from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = "ankit'stestingapp"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:@localhost/employee"
db = SQLAlchemy(app)


class EmployeeDetail(db.Model):
    emp_id = db.Column(db.Integer, primary_key = True, nullable=False)
    emp_name = db.Column(db.String(100), nullable=False)
    emp_desig = db.Column(db.String(100), nullable=False)

class EmployeeInfo(db.Model):
    emp_id = db.Column(db.Integer, primary_key = True, nullable=False)
    emp_city = db.Column(db.String(50), nullable = False)
    emp_email = db.Column(db.String(100), nullable = False)
    emp_ph = db.Column(db.String(15), nullable = False)
    emp_dob = db.Column(db.String(20), nullable = False)


@app.route("/",  methods=["GET", "POST"])
def home():
    if "user" in session and session['user'] == params['username']:
        employees = EmployeeDetail.query.filter_by().all()
        return render_template("dashboard.html", employees=employees)

    if request.method == "POST":
        user = request.form.get('username')
        password = request.form.get('password')

        if user == params['username'] and password == params["user_password"]:
            session['user'] = user
            employees = EmployeeDetail.query.filter_by().all()
            session.pop('error', None)
            return render_template("dashboard.html", employees = employees)
        else:
            flash("Invalid Credentials", "error")
            return redirect(url_for("home"))
    return render_template("login_page.html")


@app.route("/addnew/<string:emp_id>", methods=["GET", "POST"])
def addnew(emp_id):
    if "user" in session and session['user'] == params['username']:
        if request.method == "POST":
            name = request.form.get("employee_name")
            city = request.form.get("employee_city")
            email = request.form.get("employee_email")
            phone_no = request.form.get("employee_phone")
            designation = request.form.get("employee_desig")
            dob = request.form.get("employee_DOB")

            if emp_id == "0":
                entry = EmployeeDetail(emp_name=name, emp_desig=designation)
                db.session.add(entry)
                db.session.commit()

                latest_entry = EmployeeDetail.query.order_by(EmployeeDetail.emp_id.desc()).first()
                new_emp_id = latest_entry.emp_id

                info_entry = EmployeeInfo(
                    emp_id=new_emp_id,
                    emp_city=city,
                    emp_email=email,
                    emp_ph=phone_no,
                    emp_dob=dob
                )
                db.session.add(info_entry)
                db.session.commit()
                flash(f'Employee "{name}" added successfully.', 'success')
                return redirect(url_for("home"))

            else:
                detail = EmployeeDetail.query.filter_by(emp_id=emp_id).first()
                info = EmployeeInfo.query.filter_by(emp_id=emp_id).first()
                detail.emp_name = name
                detail.emp_desig = designation
                info.emp_city = city
                info.emp_ph = phone_no
                info.emp_email = email
                info.emp_dob = dob
                db.session.commit()
                flash(f'Employee "{name}" updated successfully.', 'success')
                return redirect(url_for("home"))

        detail = EmployeeDetail.query.filter_by(emp_id=emp_id).first()
        info = EmployeeInfo.query.filter_by(emp_id=emp_id).first()
        return render_template("edit.html", emp_id=emp_id, detail=detail, info=info)
    else:
        return redirect(url_for("home"))



@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')

@app.route("/employee/<string:emp_id>", methods=["GET", "POST"])
def profile(emp_id):
    if "user" in session and session['user'] == params['username']:
        details = EmployeeDetail.query.filter_by(emp_id = emp_id)
        infos = EmployeeInfo.query.filter_by(emp_id = emp_id)
        combined_data = zip(details, infos)
        return render_template("employee_profle.html", combined_data=combined_data)

    employees = EmployeeDetail.query.filter_by().all()
    return render_template("dashboard.html", employees=employees)





@app.route("/delete_employee/<string:emp_id>", methods=["GET", "POST"])
def delete_employee(emp_id):
    if "user" in session and session['user'] == params['username']:
        details = EmployeeDetail.query.filter_by(emp_id=emp_id).first()
        infos = EmployeeInfo.query.filter_by(emp_id=emp_id).first()
        db.session.delete(details)
        db.session.delete(infos)
        db.session.commit()

    employees = EmployeeDetail.query.filter_by().all()
    flash('Employee successfully deleted.', 'success')
    return render_template("dashboard.html", employees=employees)




if __name__=='__main__':
    app.run(debug = True)