import shelve
from flask import Flask, render_template, request, redirect, url_for, session
from Forms import *
from User import Customer, Staff
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def login():
    session.clear()
    app.config["Topbar"] = 1
    session["details"] = ["", "", "", "", ""]
    session["id"] = 0
    session["defaults"] = ["", "", "", "", "", "", "", ""]
    msg = app.config["No"]
    sh_msg = app.config["Show No"]
    create_login_form = LoginForm(request.form)
    user_db = shelve.open('user.db', 'c')

    if request.method == "POST":
        for staff in user_db["Staff"].values():
            print(staff)
            if (staff.get_email() == create_login_form.email.data and staff.get_password() ==
                    create_login_form.password.data):
                staff.set_total_earnings(round(float(staff.get_total_earnings()), 0))
                start_date = staff.get_start_date()
                staff.set_start_date(f"{start_date.day}/{start_date.month}/{start_date.year}")
                session["id"] = staff.get_staff_id()
                return redirect(url_for("home"))
            else:
                continue
        app.config["No"] = "Invalid username or password!"
        app.config["Show No"] = 1
        return redirect(url_for("login"))
    user_db.close()
    return render_template("login.html", title="Admin login", form=create_login_form,
                           msg=msg, sh_msg=sh_msg)


@app.route("/home")
def home():
    staff_id = session["id"]
    referral_route = request.args.get("referral_route")
    if referral_route == "login":
        pass
    user_db = shelve.open('users.db', 'c')

    if str(staff_id).isdigit():
        count = 0
        for staff in user_db["Staff"].values():
            if staff:
                count += 1
            else:
                continue

        for staff in user_db["Staff"].values():
            if count == 0:
                redirect(url_for("login", referral_route="home"))
            elif int(staff.get_staff_id()) == int(staff_id):
                name = staff.get_name()
                progress = staff.get_progress()
                requests = staff.get_requests()
                earn = staff.get_total_earnings()
                earnings = f"{earn:.2f}"
                monthly_earnings = f"{earn/12:.2f}"
                session["details"] = [name, progress, requests, earnings, monthly_earnings]
            else:
                count -= 1

    name = session["details"][0]
    progress = session["details"][1]
    requests = session["details"][2]
    earnings = session["details"][3]
    monthly_earnings = session["details"][4]
    session["details"] = []
    data1 = 50
    data2 = 34
    data3 = 27
    data_list = [0, 69420, 150000, 79825, 103159, 209475, 256081, 291080, 315000, 360000, 425000, 540000]
    return render_template("index.html", name=name, progress=progress, requests=requests,
                           earnings=earnings, monthly_earnings=monthly_earnings, data1=data1, data2=data2,
                           data3=data3, data_list=data_list)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST':
        user_db = shelve.open('user.db', 'c')
        new_user_id = user_db["Last ID Used"][0] + 1
        new_customer_id = user_db["Last ID Used"][1] + 1
        customer = Customer(
            new_user_id,
            new_customer_id,
            create_customer_form.name.data,
            create_customer_form.email.data,
            create_customer_form.password.data,
            create_customer_form.gender.data,
            create_customer_form.phone_number.data,
            create_customer_form.mailing_address.data
        )
        customer_dict = user_db["Customer"]
        customer_dict[new_user_id] = customer
        user_db["Customer"] = customer_dict
        user_db["Last ID Used"] = [new_user_id, new_customer_id, user_db["Last ID Used"][2]]
        user_db.close()
        return redirect(url_for('retrieve_customer'))
    return render_template('createCustomer.html', form=create_customer_form)


@app.route('/retrieveCustomer')
def retrieve_customer():
    with shelve.open("user.db", "c") as user_db:
        customer_list = user_db["Customer"].values()
        count = len(customer_list)
    return render_template('retrieveCustomer.html', count=count, customer_list=customer_list)


@app.route('/searchCustomer', methods=['POST'])
def search_customer():
    user_search_item = int(request.get_data(as_text=True)[12:])
    with shelve.open("user.db", "c") as user_db:
        customer_dict = user_db['Customer']
        if user_search_item in customer_dict:
            customer = customer_dict[user_search_item]
        else:
            return render_template('searchCustomer.html', customer=None)
    return render_template('searchCustomer.html', customer=customer)


@app.route('/deleteCustomer/<int:user_id>', methods=['POST'])
def delete_customer(user_id):
    with shelve.open('user.db', 'w') as user_db:
        temporary_dict = user_db['Customer']
        temporary_dict.pop(user_id)
        user_db['Customer'] = temporary_dict
    return redirect(url_for('retrieve_customer'))


@app.route('/clearCustomer')
def clear_customer():
    with shelve.open('user.db', 'w') as user_db:
        user_db['Customer'] = {}
    return redirect(url_for('retrieve_customer'))


@app.route('/createStaff', methods=['GET', 'POST'])
def create_staff():
    create_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST':
        user_db = shelve.open('user.db', 'c')
        staff_dict = user_db["Staff"]
        new_user_id = user_db["Last ID Used"][0] + 1
        new_staff_id = user_db["Last ID Used"][2] + 1
        staff = Staff(
            new_user_id,
            new_staff_id,
            create_staff_form.name.data,
            create_staff_form.email.data,
            create_staff_form.password.data,
            create_staff_form.start_date.data,
            create_staff_form.position.data,
            # removing the '$' from field input
            float(create_staff_form.total_earnings.data[1:]),
            create_staff_form.gender.data,
            create_staff_form.phone_number.data,
            create_staff_form.mailing_address.data
        )
        staff_dict[staff.get_user_id()] = staff
        user_db["Staff"] = staff_dict
        user_db["Last ID Used"] = [new_user_id, new_staff_id, user_db["Last ID Used"][2]]
        user_db.close()
        return redirect(url_for('retrieve_staff'))
    return render_template('createStaff.html', form=create_staff_form)


@app.route('/retrieveStaff')
def retrieve_staff():
    with shelve.open("user.db", "r") as user_db:
        staff_list = []
        count = 0
        for staff in user_db["Staff"].values():
            staff.set_total_earnings(int(staff.get_total_earnings()))
            start_date = staff.get_start_date()
            staff.set_start_date(f"{start_date.day}/{start_date.month}/{start_date.year}")
            staff_list.append(staff)
            count += 1
    return render_template('retrieveStaff.html', count=count, staff_list=staff_list)


@app.route('/searchStaff', methods=['POST'])
def search_staff():
    user_search_item = int(request.get_data(as_text=True)[12:])
    with shelve.open("user.db", "r") as user_db:
        staff_dict = user_db['Staff']
        if user_search_item in staff_dict:
            staff = staff_dict[user_search_item]
            staff.set_total_earnings(int(staff.get_total_earnings()))
            start_date = staff.get_start_date()
            staff.set_start_date(f"{start_date.day}/{start_date.month}/{start_date.year}")
        else:
            return render_template('searchStaff.html', staff=None)
    return render_template('searchStaff.html', staff=staff)


@app.route('/updateStaff/<int:user_id>', methods=['GET', 'POST'])
def update_staff(user_id):
    update_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and update_staff_form.validate():
        with shelve.open('user.db', 'c') as user_db:
            staff_dict = user_db['Staff']
            staff = staff_dict.get(user_id)
            staff.set_name(update_staff_form.name.data)
            staff.set_email(update_staff_form.email.data)
            staff.set_password(update_staff_form.password.data)
            staff.set_start_date(update_staff_form.start_date.data)
            staff.set_position(update_staff_form.position.data)
            staff.set_total_earnings(float(update_staff_form.total_earnings.data[1:]))
            staff.set_gender(update_staff_form.gender.data)
            staff.set_phone_number(update_staff_form.phone_number.data)
            staff.set_mailing_address(update_staff_form.mailing_address.data)
            staff_dict[user_id] = staff
            user_db['Staff'] = staff_dict
        return redirect(url_for('retrieve_staff'))
    else:
        with shelve.open('user.db', 'c') as user_db:
            staff_dict = user_db['Staff']
        staff = staff_dict[user_id]
        update_staff_form.name.data = staff.get_name()
        update_staff_form.email.data = staff.get_email()
        update_staff_form.password.data = staff.get_password()
        update_staff_form.start_date.data = staff.get_start_date()
        update_staff_form.position.data = staff.get_position()
        update_staff_form.total_earnings.data = f"${staff.get_total_earnings()}"
        update_staff_form.gender.data = staff.get_gender()
        update_staff_form.phone_number.data = staff.get_phone_number()
        update_staff_form.mailing_address.data = staff.get_mailing_address()
        return render_template('updateStaff.html', form=update_staff_form)


@app.route('/deleteStaff/<int:user_id>', methods=['POST'])
def delete_staff(user_id):
    with shelve.open('user.db', 'w') as user_db:
        temporary_dict = user_db['Staff']
        temporary_dict.pop(user_id)
        user_db['Staff'] = temporary_dict
    return redirect(url_for('retrieve_staff'))


@app.route('/clearStaff')
def clear_staff():
    with shelve.open('user.db', 'w') as user_db:
        user_db['Staff'] = {}
    return redirect(url_for('retrieve_staff'))


if __name__ == '__main__':
    app.jinja_env.autoescape = True
    app.secret_key = "hj^&!Hh12h3828hc7ds8f9asd82nc"
    app.config["Show No"] = 0
    app.config["No"] = ""
    app.config["Route"] = ""
    app.config["Topbar"] = 0
    app.run(debug=True)
    try:
        with shelve.open('user.db', 'c') as user_database:
            if not user_database:
                user_database["Customer"] = {}
                user_database["Staff"] = {}
                user_database["Last ID Used"] = [0, 0, 0]  # [Users, Customers, Staff]
    except KeyError or IOError as database_error:
        print("Error encountered opening users.db:", database_error)
