import shelve

import bcrypt
from flask import Flask, render_template, request, redirect, url_for

from Forms import *
from user_validators import *
from UserClasses import Customer, Staff

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('user_database_home.html')


@app.route('/customerLogin', methods=['GET', 'POST'])
def customer_login():
    customer_login_form = CustomerForm(request.form)
    if request.method == "GET" or (request.method == "POST" and customer_login_form.validate()):
        return render_template('customerLogin.html', form=CustomerForm())
    with shelve.open('user.db', 'c') as user_db:
        login_error = "Incorrect email or password"
        customer_dict = user_db['Customer']
        customer_email = customer_login_form.email.data
        # returns user_id if customer exists
        customer = check_existing_email(customer_email, customer_dict)
        if not customer:
            return render_template('customerLogin.html', form=CustomerForm(), error=login_error)
        stored_password = customer.get_password()
        customer_password = bytes(customer_login_form.password.data, 'utf-8')
        if bcrypt.hashpw(customer_password, stored_password.salt) != stored_password.hash:
            return render_template('customerLogin.html', form=CustomerForm(), error=login_error)
        return render_template('customerHome.html', user=customer)


@app.route('/customerRegister')
def customer_register():
    customer_login_form = CustomerForm(request.form)
    if request.method == "POST" and customer_login_form.validate():
        pass
    return render_template('customerRegister.html', form=customer_login_form)


@app.route('/inputCustomer', methods=["GET", "POST"])
def input_customers():
    input_customer_form = InputUserForm(request.form)
    if not (request.method == "POST" and input_customer_form.validate()):
        return render_template("inputUser.html", form=input_customer_form, user="Customer", error_list="")
    customer_input_list = convert_multiline_string_to_list(input_customer_form.user_details.data)
    with shelve.open('user.db', 'c') as user_db:
        main_error_list = []
        new_customer = []
        customer_dict = user_db['Customer']
        if customer_dict:
            last_user_id = list(customer_dict.keys())[-1]
            last_customer_id = list(customer_dict.values())[-1].get_customer_id()
        else:
            last_user_id = 0
            last_customer_id = 0
        for i, line in enumerate([(last_customer_id+i, last_user_id+i, customer_input_list[i-1]) for i, x in enumerate(customer_input_list, 1)]):
            customer_details = line[2].split(', ')
            if len(customer_details) != 6:
                main_error_list.append((i+1, f"list index out of range: {len(customer_details)} items"))
                continue
            customer_mailing_address = customer_details[5]
            if customer_mailing_address[-2:] == "\r":
                customer_mailing_address = customer_mailing_address[:-2]
            customer = Customer(
                line[0],  # user id
                line[1],  # customer id
                customer_details[0],  # name
                customer_details[1],  # email
                customer_details[2],  # password
                customer_details[3],  # gender
                customer_details[4],  # phone number
                customer_mailing_address  # mailing address
            )
            # returns customer object if inputs are valid, else returns list of errors
            valid_customer = check_customer_errors(customer, customer_dict)
            if isinstance(valid_customer, Customer):
                new_customer.append(valid_customer)
            else:
                customer_errors = valid_customer
                if len(customer_errors) > 1:
                    customer_errors = ", ".join(customer_errors)
                else:
                    customer_errors = customer_errors[0]
                main_error_list.append(tuple([line[0], customer_errors]))
        if main_error_list:
            send_error_list = main_error_list.copy()
            main_error_list.clear()
            return render_template('inputUser.html', form=input_customer_form, error_list=send_error_list, user="Customer")
        for customer in new_customer:
            customer_dict[customer.get_user_id()] = customer
            user_db["Customer"] = customer_dict
    return redirect(url_for('retrieve_customer'))


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CustomerForm(request.form)
    if request.method == 'POST':
        with shelve.open('user.db', 'c') as user_db:
            customer_dict = user_db["Customer"]
            if customer_dict:
                new_user_id = list(customer_dict.keys())[-1] + 1
                new_customer_id = list(customer_dict.values())[-1].get_customer_id() + 1
            else:
                new_user_id = 1
                new_customer_id = 1
            customer_email = create_customer_form.email.data
            if check_existing_email(customer_email, customer_dict):
                return render_template('createCustomer.html', form=create_customer_form, email_error="Email already exists")
            customer_password = create_customer_form.password.data
            password_errors = check_password_errors(customer_password)
            if password_errors:
                return render_template('createCustomer.html', form=create_customer_form, password_errors=password_errors)
            customer = Customer(
                new_user_id,
                new_customer_id,
                create_customer_form.name.data,
                customer_email,
                HashedPassword(customer_password),
                create_customer_form.gender.data,
                create_customer_form.phone_number.data,
                create_customer_form.mailing_address.data
            )
            customer_dict[new_user_id] = customer
            user_db["Customer"] = customer_dict
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


@app.route('/inputStaff', methods=["GET", "POST"])
def input_staff():
    input_staff_form = InputUserForm(request.form)
    if not (request.method == "POST" and input_staff_form.validate()):
        return render_template("inputUser.html", form=input_staff_form, user="Staff", error_list="")
    staff_input_list = convert_multiline_string_to_list(input_staff_form.user_details.data)
    with shelve.open('user.db', 'c') as user_db:
        main_error_list = []
        new_staff = []
        staff_dict = user_db['Staff']
        if staff_dict:
            last_user_id = list(staff_dict.keys())[-1]
            last_staff_id = list(staff_dict.values())[-1].get_staff_id()
        else:
            last_user_id = 0
            last_staff_id = 0
        for i, line in enumerate([(last_staff_id+i, last_user_id+i, staff_input_list[i-1]) for i, x in enumerate(staff_input_list, 1)]):
            staff_details = line[2].split(', ')
            if len(staff_details) != 9:
                main_error_list.append((i+1, f"list index out of range: {len(staff_details)} items"))
                continue
            staff_mailing_address = staff_details[8]
            if staff_mailing_address[-2:] == "\r":
                staff_mailing_address = staff_mailing_address[:-2]
            staff = Staff(
                line[0],  # user id
                line[1],  # staff id
                staff_details[0],  # name
                staff_details[1],  # email
                staff_details[2],  # password
                staff_details[3],  # start date
                staff_details[4],  # position
                staff_details[5],  # total earnings
                staff_details[6],  # gender
                staff_details[7],  # phone number
                staff_mailing_address  # mailing address
            )
            # returns customer object if inputs are valid, else returns list of errors
            valid_staff = check_staff_errors(staff, staff_dict)
            if isinstance(valid_staff, Staff):
                new_staff.append(valid_staff)
            else:
                main_error_list.append(tuple([line[0], valid_staff]))
        if main_error_list:
            send_error_list = main_error_list.copy()
            main_error_list.clear()
            return render_template('inputUser.html', form=input_staff_form, error_list=send_error_list, user="Staff")
        for staff in new_staff:
            staff_dict[staff.get_user_id()] = staff
            user_db["Staff"] = staff_dict
    return redirect(url_for('retrieve_staff'))


@app.route('/createStaff', methods=['GET', 'POST'])
def create_staff():
    create_staff_form = StaffForm(request.form)
    if request.method == 'POST':
        user_db = shelve.open('user.db', 'c')
        staff_dict = user_db["Staff"]
        if staff_dict:
            new_user_id = list(staff_dict.keys())[-1] + 1
            new_staff_id = list(staff_dict.values())[-1].get_staff_id() + 1
        else:
            new_user_id = 1
            new_staff_id = 1
        customer_email = create_staff_form.email.data
        if check_existing_email(customer_email, staff_dict):
            return render_template('createCustomer.html', form=create_staff_form, email_error="Email already exists")
        customer_password = create_staff_form.password.data
        password_errors = check_password_errors(customer_password)
        if password_errors:
            return render_template('createCustomer.html', form=create_staff_form, password_errors=password_errors)
        staff = Staff(
            new_user_id,
            new_staff_id,
            create_staff_form.name.data,
            customer_email,
            HashedPassword(customer_password),
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
            # do the hashing thing, don't need to show user their old password to change it
            staff.set_password(staff.get_password())
            staff.set_total_earnings(float(staff.get_total_earnings()))
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
    update_staff_form = StaffForm(request.form)
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
        print(update_staff_form.data)
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
    app.run(debug=True)
    try:
        with shelve.open('user.db', 'c') as user_database:
            if not user_database:
                user_database["Customer"] = {}
                user_database["Staff"] = {}
    except KeyError or IOError as database_error:
        print("Error encountered opening users.db:", database_error)
