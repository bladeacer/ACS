"""b"""
import shelve
import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, Response
from Forms import (CreateCustomerForm, CreateStaffForm, LoginForm, UpdateStaffForm, ProductForm, UpdateProductForm,
                   UploadDataFile)
from User import Customer, Staff, Product
from werkzeug.utils import secure_filename
import cv2
import random
import string
import weasyprint
import pandas as pd
import numpy as np
app = Flask(__name__)


def _staff_details():
    staff_id = session["id"]
    with shelve.open('user.db', 'c') as user_db:
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
                    email = staff.get_email()
                    desc = staff.get_self_description()
                    number = staff.get_phone_number()
                    position = staff.get_position()
                    earnings = f"{earn:.2f}"
                    experience = int(progress) / 10
                    session["details"] = [name, experience, requests, earnings, email, progress, desc, number, position]
                else:
                    count -= 1


def _alert_message(message: str = "", sh_msg: int = 0):
    app.config["No"] = message
    app.config["Show No"] = sh_msg


def _get_alert_msg():
    return app.config["No"]


def _get_sh_msg():
    return app.config["Show No"]


def _session_name():
    return session["details"][0]


def _login_session_handler(staff_id: int = 0):
    session.clear()
    session["id"] = staff_id


def _image_processing_fun(image_file, image_name, size: int, old_filename: str = ""):
    allowed_chars = string.ascii_letters + string.digits

    # Generate a random string of 5 characters
    random_chars = "".join(random.choice(allowed_chars.lower()) for i in range(5))
    unique_suffix = f"{random.randint(100, 999)}{random_chars}"
    filename = secure_filename(image_name + f"{unique_suffix}.jpg").lower().replace(" ", "")  # Secure filename
    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Process image using OpenCV
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img = cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA)  # Resize
    new_filename = filename.replace(".jpg", ".png")
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], new_filename),
                img)  # Save as PNG
    os.chmod(os.path.join(app.config['UPLOAD_FOLDER'], new_filename), 0o644)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if old_filename != "":
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], old_filename))

    return new_filename


def _parse_files_db(database_key, data_file, data_name, old_filename):
    allowed_chars = string.ascii_letters + string.digits
    random_chars = "".join(random.choice(allowed_chars.lower()) for i in range(5))
    unique_suffix = f"{random.randint(100, 999)}{random_chars}"

    filename = secure_filename(data_name + f"{unique_suffix}.csv").lower().replace(" ", "")
    filename = os.path.join(app.config["DATAFILE_FOLDER"], filename)

    if old_filename.endswith(".xlsx"):
        df = pd.read_excel(data_file, header=None)
    else:
        df = pd.read_csv(data_file, header=None)
    df.to_csv(filename, index=False)  # Convert Excel to CSV

    df = pd.read_csv(filename)

    with (shelve.open('user.db', 'c') as user_db):
        rows = df.shape[0]
        cols = df.shape[1]
        if database_key == "Staff" and cols == 12:
            df.columns = ["Name", "Email", "Password", "Start Date", "Position", "Total Earnings", "Gender",
                          "Phone Number", "Mailing Address", "Progress", "Requests", "Self Description"]
            user_ids = np.array([])
            staff_ids = np.array([])

            for i in range(rows):
                user_ids = np.append(user_ids, user_db["Last ID Used"][0] + i + 1)
                staff_ids = np.append(staff_ids, user_db["Last ID Used"][2] + i + 1)

            user_db["Last ID Used"] = [user_db["Last ID Used"][0] + rows + 1, user_db["Last ID Used"][1],
                                       user_db["Last ID Used"][2] + rows + 1]

            user_ids = user_ids.astype(int)

            df.insert(loc=0, column='User ID', value=user_ids)
            df.insert(loc=1, column="Staff ID", value=staff_ids)

            user_ids = list(map(str, user_ids))

            df = df.iloc[1:]
            rows = df.shape[0]
            data_items = []
            for a in range(rows):
                mini_li = df.iloc[a].tolist()
                data = Staff(mini_li[0], mini_li[1], mini_li[2], mini_li[2], mini_li[4],
                             mini_li[5], mini_li[6], mini_li[7], mini_li[8], mini_li[9], mini_li[10],
                             mini_li[11])
                data_items.append(data)
        elif database_key == "Customer" and cols == 7:
            df.columns = ["Name", "Email", "Password", "Gender", "Phone Number", "Mailing Address",
                          "Referral"]

            user_ids = np.array([])
            customer_ids = np.array([])

            for i in range(rows):
                user_ids = np.append(user_ids, user_db["Last ID Used"][0] + i + 1)
                customer_ids = np.append(customer_ids, user_db["Last ID Used"][1] + i + 1)

            user_db["Last ID Used"] = [user_db["Last ID Used"][0] + rows + 1, user_db["Last ID Used"][1] + rows + 1,
                                       user_db["Last ID Used"][2]]

            user_ids = user_ids.astype(int)

            df.insert(loc=0, column='User ID', value=user_ids)
            df.insert(loc=1, column="Customer ID", value=customer_ids)

            user_ids = list(map(str, user_ids))

            df = df.iloc[1:]
            rows = df.shape[0]
            data_items = []

            for a in range(rows):
                stub = df.iloc[a].tolist()
                data = Customer(stub[0], stub[1], stub[2], stub[3], stub[4], stub[5], stub[6], stub[7], stub[8])
                data_items.append(data)

        else:
            return EOFError

        existing_data = user_db.get(database_key, [])
        for i in range(rows):
            existing_data[user_ids[i]] = data_items[i]
        user_db[database_key] = existing_data

    return filename


@app.route("/", methods=['GET', 'POST'])
def login():
    try:
        _login_session_handler()
        referral_route = request.args.get("referral_route")
        if referral_route == "login":
            _alert_message("Invalid password or username", 1)
        elif referral_route == "session_chk":
            _alert_message("No staff created yet oh noes")
        else:
            _alert_message()
        create_login_form = LoginForm(request.form)
        with shelve.open('user.db', 'c') as user_db:
            if request.method == "POST":
                for staff in user_db["Staff"].values():
                    if (staff.get_email() == create_login_form.email.data and staff.get_password() ==
                            create_login_form.password.data):
                        staff.set_total_earnings(round(float(staff.get_total_earnings()), 0))
                        start_date = staff.get_start_date()
                        staff.set_start_date(f"{start_date.day}/{start_date.month}/{start_date.year}")
                        session["id"] = staff.get_staff_id()
                        session["user_id"] = staff.get_user_id()
                        return redirect(url_for("home"))
                    else:
                        pass
                return redirect(url_for("login", referral_route="login"))
        return render_template("login.html", title="Admin login", form=create_login_form,
                               msg=_get_alert_msg(), sh_msg=_get_sh_msg())
    except KeyError or IOError or UnboundLocalError or EOFError as error:
        print("Error encountered opening user.db:", error)


@app.route("/home")
def home():
    # TODO: Link up product purchase details to charts etc.
    referral_route = request.args.get("referral_route")
    url_fun = request.url
    if referral_route == "login" or "retrieve" in url_fun or "create" in url_fun:
        _alert_message()
    _staff_details()
    name = _session_name()
    requests = session["details"][2]
    earnings = session["details"][3]
    monthly_earnings = f"{float(earnings)/12:.2f}"
    progress = session["details"][5]
    referral_chart = [0, 0, 0]
    with shelve.open("user.db", "r") as user_db:
        for customer in user_db["Customer"].values():
            try:
                if customer.get_referral() == "Direct":
                    referral_chart[0] += 1
                elif customer.get_referral() == "Social":
                    referral_chart[1] += 1
                else:
                    referral_chart[2] += 1
            except AttributeError:
                return redirect(url_for("create_customer", referral_route="home"))

    # TODO: Connect Code to render area chart to backend (financial earnings etc), do the bar chart code
    #
    pie_chart_data = referral_chart
    area_chart_data = [0, 69420, 150000, 79825, 103159, 209475, 256081, 291080, 315000, 360000, 425000, 540000]
    user_id = session["user_id"]

    return render_template("index.html", pie_chart_data=pie_chart_data, area_chart_data=area_chart_data,
                           name=name, progress=progress, requests=requests, earnings=earnings,
                           monthly_earnings=monthly_earnings, message=_get_alert_msg(), sh_msg=_get_sh_msg(),
                           user_id=user_id)


@app.route("/profile")
def profile():
    _staff_details()
    staff_id = session["id"]
    user_id = session["user_id"]
    name = _session_name()
    experience = session["details"][1]
    requests = session["details"][2]
    earnings = session["details"][3]
    email = session["details"][4]
    connections = session["details"][5]
    desc = session["details"][6]
    number = session["details"][7]
    position = session["details"][8]

    return render_template("profile.html", name=name, experience=experience, requests=requests,
                           earnings=earnings, email=email, connections=connections, desc=desc, number=number,
                           staff_id=staff_id, position=position, user_id=user_id)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    name = _session_name()
    user_id = session["user_id"]
    referral_route = request.args.get("referral_route")
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == "POST":
        user_db = shelve.open('user.db', 'c')
        new_user_id = user_db["Last ID Used"][0] + 1
        new_customer_id = user_db["Last ID Used"][1] + 1
        customer = Customer(
            user_id=new_user_id,
            customer_id=new_customer_id,
            name=create_customer_form.name.data,
            email=create_customer_form.email.data,
            password=create_customer_form.password.data,
            gender=create_customer_form.gender.data,
            phone_number=create_customer_form.phone_number.data,
            mailing_address=create_customer_form.mailing_address.data,
            referral=create_customer_form.referral.data
        )
        customer_dict = user_db["Customer"]
        customer_dict[str(new_user_id)] = customer
        user_db["Customer"] = customer_dict
        user_db["Last ID Used"] = [new_user_id, new_customer_id, user_db["Last ID Used"][2]]
        user_db.close()
        return redirect(url_for("retrieve_customer", referral_route="create_customer"))
    if referral_route == "home":
        _alert_message()
    return render_template('createCustomer.html', form=create_customer_form, message=_get_alert_msg(),
                           sh_msg=_get_sh_msg(), name=name, user_id=user_id)


@app.route('/retrieveCustomer')
def retrieve_customer():
    name = _session_name()
    user_id = session["user_id"]

    referral_route = request.args.get("referral_route")
    try:
        with shelve.open("user.db", "r") as user_db:
            customer_list = user_db["Customer"].values()
            count = len(customer_list)
            if count == 0:
                _alert_message("No customer created yet, create one", 1)
                return redirect(url_for('create_customer', referral_route=retrieve_customer))
        if referral_route == "create_customer" or "home":
            _alert_message("Retrieve successful", 1)
        return render_template('retrieveCustomer.html', count=count, customer_list=customer_list,
                               message=_get_alert_msg(), sh_msg=_get_sh_msg(), name=name, user_id=user_id)
    except KeyError:
        _alert_message("Error retrieving customer", 1)
        return redirect(url_for("create_customer", referral_route="retrieve_customer"))


@app.route('/searchCustomer', methods=['POST'])
def search_customer():
    name = _session_name()
    user_id = session["user_id"]

    user_search_item = request.get_data(as_text=True)[12:]
    with shelve.open("user.db", "c") as user_db:
        customer_list = user_db["Customer"].values()
        if user_search_item in customer_list:
            # customer = customer_list[], probably retrieve and index everything e
            # TODO: Make search index retrieve customer and staff
            pass
        else:
            return render_template('searchCustomer.html', customer=None, name=name)
    return render_template('searchCustomer.html', name=name, user_id=user_id)


@app.route('/deleteCustomer/<int:user_id>', methods=['POST'])
def delete_customer(user_id):
    name = _session_name()
    use_id = session["user_id"]

    with shelve.open('user.db', 'w') as user_db:
        temporary_dict = user_db['Customer']
        temporary_dict.pop(str(user_id))
        user_db["Customer"] = temporary_dict
    return redirect(url_for('retrieve_customer', referral_route="delete_customer", name=name, user_id=use_id))


@app.route('/clearCustomer')
def clear_customer():

    with shelve.open('user.db', 'w') as user_db:
        user_db['Customer'] = {}
    _alert_message("No customer created yet, create one")
    return redirect(url_for('create_customer'))


@app.route('/createStaff', methods=['GET', 'POST'])
def create_staff():
    user_id = session["user_id"]
    name = _session_name()

    create_staff_form = CreateStaffForm(request.form)
    referral_route = request.args.get("referral_route")
    if referral_route == "login":
        _alert_message("Redirected from login page", 1)
        return redirect(url_for("login", referral_route="create_staff"))
    elif referral_route == "retrieve_staff":
        _alert_message("Redirected from retrieve staff", 1)
    elif referral_route == "home":
        _alert_message("Redirected from homepage", 1)
    else:
        _alert_message()
    if request.method == 'POST':
        # TODO: Retrieve and compare emails
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
            create_staff_form.total_earnings.data,
            create_staff_form.gender.data,
            create_staff_form.phone_number.data,
            create_staff_form.mailing_address.data,
            create_staff_form.self_description.data,
            create_staff_form.progress.data,
            create_staff_form.requests.data
        )
        staff_dict[staff.get_user_id()] = staff
        user_db["Staff"] = staff_dict
        user_db["Last ID Used"] = [new_user_id, user_db["Last ID Used"][1], new_staff_id]
        user_db.close()
        return redirect(url_for('retrieve_staff', referral_route="create_staff"))
    elif referral_route == "create_staff":
        _alert_message("Error in validating staff form", 1)
        return redirect(url_for("create_staff"))

    return render_template('createStaff.html', form=create_staff_form, message=_get_alert_msg(),
                           sh_msg=_get_sh_msg(), user_id=user_id, name=name)


@app.route('/retrieveStaff')
def retrieve_staff():
    name = _session_name()
    user_id = session["user_id"]

    try:
        referral_route = request.args.get("referral_route")
        with shelve.open("user.db", "r") as user_db:
            staff_list = []
            count = 0
            for staff in user_db["Staff"].values():
                staff.set_total_earnings(float(staff.get_total_earnings()))
                start_date = staff.get_start_date()
                staff.set_start_date(f"{start_date.day}/{start_date.month}/{start_date.year}")
                staff_list.append(staff)
                count += 1

        if count != 0 and _get_alert_msg() == "Error in updating staff":
            pass

        elif count != 0 and referral_route == "update_staff":
            _alert_message("Redirected from update staff", 1)

        elif count != 0:
            _alert_message("Retrieve successful", 1)
        else:
            _alert_message("No staff created yet, create one.", 1)
            return redirect(url_for("create_staff", referral_route="retrieve_staff"))
        return render_template('retrieveStaff.html', count=count, staff_list=staff_list,
                               message=_get_alert_msg(), sh_msg=_get_sh_msg(), name=name, user_id=user_id)
    except EOFError or KeyError:
        _alert_message("No staff created yet, create one.", 1)
        return redirect(url_for("create_staff", referral_route="retrieve_staff"))


@app.route('/searchStaff', methods=['POST'])
def search_staff():
    name = _session_name()
    user_id = session["user_id"]

    user_search_item = int(request.get_data(as_text=True)[12:])
    with shelve.open("user.db", "r") as user_db:
        staff_dict = user_db['Staff']
        if user_search_item in staff_dict:
            staff = staff_dict[user_search_item]
            staff.set_total_earnings(float(staff.get_total_earnings()))
            start_date = staff.get_start_date()
            staff.set_start_date(f"{start_date.day}/{start_date.month}/{start_date.year}")
        else:
            staff = None
    return render_template('searchStaff.html', staff=staff, name=name, user_id=user_id)


@app.route('/updateStaff/<int:user_id>', methods=['GET', 'POST'])
def update_staff(user_id):
    name = _session_name()
    use_id = session["user_id"]

    try:
        update_staff_form = UpdateStaffForm(request.form)
        if request.method == 'POST':
            with shelve.open('user.db', 'c') as user_db:
                staff_dict = user_db['Staff']
                staff = staff_dict.get(str(user_id))
                staff.set_name(update_staff_form.new_name.data)
                staff.set_email(update_staff_form.new_email.data)
                staff.set_password(update_staff_form.new_password.data)
                staff.set_start_date(update_staff_form.new_start_date.data)
                staff.set_position(update_staff_form.new_position.data)
                staff.set_total_earnings(float(update_staff_form.new_total_earnings.data))
                staff.set_gender(update_staff_form.new_gender.data)
                staff.set_phone_number(update_staff_form.new_phone_number.data)
                staff.set_mailing_address(update_staff_form.new_mailing_address.data)
                staff_dict[str(user_id)] = staff
                user_db['Staff'] = staff_dict
                return redirect(url_for('retrieve_staff', referral_route="update_staff"))
        else:
            with shelve.open('user.db', 'r') as user_db:
                staff_dict = user_db['Staff']
            staff = staff_dict[str(user_id)]
            update_staff_form.new_name.data = staff.get_name()
            update_staff_form.new_email.data = staff.get_email()
            update_staff_form.new_password.data = "*****"
            update_staff_form.new_start_date.data = staff.get_start_date()
            update_staff_form.new_position.data = staff.get_position()
            update_staff_form.new_total_earnings.data = staff.get_total_earnings()
            update_staff_form.new_gender.data = staff.get_gender()
            update_staff_form.new_phone_number.data = int(staff.get_phone_number())
            update_staff_form.new_mailing_address.data = staff.get_mailing_address()
        return render_template('updateStaff.html', form=update_staff_form, name=name, user_id=use_id)

    except EOFError or KeyError:
        _alert_message("Error in updating staff", 1)
        return redirect(url_for("retrieve_staff", referral_route="update_staff"))


@app.route('/deleteStaff/<int:user_id>', methods=['POST'])
def delete_staff(user_id):

    with shelve.open('user.db', 'w') as user_db:
        temporary_dict = user_db['Staff']
        temporary_dict.pop(str(user_id))
        user_db['Staff'] = temporary_dict
    return redirect(url_for('retrieve_staff', referral_route="delete_staff"))


@app.route("/createProduct", methods=["GET", "POST"])
def create_product():
    name = _session_name()
    user_id = session["user_id"]

    referral_route = request.args.get("referral_route")
    if referral_route == "login":
        _alert_message("Redirected from login page", 1)
    elif referral_route == "retrieve_product":
        pass
    elif referral_route == "home":
        _alert_message("Redirected from homepage", 1)
    else:
        _alert_message()
    if app.config["Route"] == "login":
        return redirect(url_for("login", referral_route="create_staff"))

    try:
        prod_form = ProductForm(request.form)
        if request.method == "POST":
            image_file = request.files["image"]
            image_name = prod_form.filename.data

            img_comp = False
            for img in app.config["UPLOADED_IMAGES"]:
                if img == image_name:
                    img_comp = True
                else:
                    continue

            if image_file and image_name and img_comp is False:
                new_filename = _image_processing_fun(image_file, image_name, 150)
            else:
                allowed_chars = string.ascii_letters + string.digits
                image_name = "".join(random.choice(allowed_chars.lower()) for i in range(20))
                new_filename = _image_processing_fun(image_file, image_name, 150)
            app.config["UPLOADED_IMAGES"].append(new_filename)
            _alert_message("Image upload successfully!", 1)

            with shelve.open('user.db', 'c') as user_db:
                prod_dict = user_db["Product"]
                new_product_id = user_db["Product Pointer"]+1
                if int(prod_form.count.data) > 0:
                    is_stock = True
                else:
                    is_stock = False
                product = Product(prod_form.name.data,
                                  prod_form.price.data,
                                  new_product_id,
                                  prod_form.description.data,
                                  prod_form.count.data,
                                  is_stock,
                                  new_filename
                                  )
                prod_dict[product.get_prod_id()] = product
                user_db["Product"] = prod_dict
                user_db["Product Pointer"] = new_product_id
                return redirect(url_for("retrieve_product", referral_route="create_product"))
        elif referral_route == "create_product":
            _alert_message("Error in validating product form", 1)
            return redirect(url_for("create_product"))

    except EOFError or KeyError or IOError:
        _alert_message("Error in product form", 1)
        return redirect(url_for("create_product", referral_route="create_product"))

    return render_template("createProduct.html", form=prod_form, message=_get_alert_msg(),
                           sh_msg=_get_sh_msg(), name=name, user_id=user_id)


@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/retrieveProduct")
def retrieve_product():
    name = _session_name()
    user_id = session["user_id"]

    try:
        referral_route = request.args.get("referral_route")
        with shelve.open("user.db", "r") as user_db:
            product_list = []
            count = 0
            for product in user_db["Product"].values():
                product.set_price(f"{float(product.get_price()):.2f}")
                product_list.append(product)

                count += 1
        if count != 0 and _get_alert_msg() == "Error in updating product":
            pass

        elif count != 0 and referral_route == "update_product":
            _alert_message("Redirected from update product", 1)
        elif count != 0 and referral_route == "create_product":
            pass
        elif count != 0:
            _alert_message("Retrieve successful", 1)
        else:
            _alert_message("No product created yet, create one.", 1)
            return redirect(url_for("create_product", referral_route="retrieve_product"))
        return render_template('retrieveProduct.html', count=count, product_list=product_list,
                               message=_get_alert_msg(), sh_msg=_get_sh_msg(), name=name, user_id=user_id)

    except EOFError or KeyError:
        _alert_message("No product created yet, create one.", 1)
        return redirect(url_for("create_product", referral_route="retrieve_product", count=count))


@app.route("/updateProduct/<int:prod_id>", methods=["GET", "POST"])
def update_product(prod_id):
    name = _session_name()
    user_id = session["user_id"]
    try:
        update_product_form = UpdateProductForm(request.form)
        if request.method == "POST":
            image_file = request.files["image"]
            image_name = update_product_form.name.data
            img_comp = False
            for img in app.config["UPLOADED_IMAGES"]:
                if img == image_name:
                    img_comp = True
                else:
                    continue

            with shelve.open("user.db", "c") as user_db:
                prod_dict = user_db["Product"]
                product = prod_dict.get(str(prod_id))
                product.set_name(update_product_form.name.data)
                product.set_price(update_product_form.price.data)
                product.set_description(update_product_form.description.data)
                product.set_count(update_product_form.count.data)
                if int(update_product_form.count.data) > 0:
                    product.set_is_stock(True)
                else:
                    product.set_is_stock(False)

                old_filename = product.get_filename()

                if image_file and image_name and img_comp is False:
                    new_filename = _image_processing_fun(image_file, image_name, 150)
                else:
                    allowed_chars = string.ascii_letters + string.digits
                    image_name = "".join(random.choice(allowed_chars.lower()) for i in range(20))
                    new_filename = _image_processing_fun(image_file, image_name, 150)

                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_filename))

                product.set_filename(new_filename)
                for image, i in enumerate(app.config["UPLOADED_IMAGES"]):
                    if image == old_filename:
                        app.config["UPLOADED_IMAGES"][i] = new_filename
                    else:
                        continue
                _alert_message("Image updated successfully!", 1)
                prod_dict[str(prod_id)] = product
                user_db["Product"] = prod_dict
                return redirect(url_for("retrieve_product", referral_route="update_product"))
        else:
            with shelve.open("user.db", "r") as user_db:
                prod_dict = user_db["Product"]
            product = prod_dict[str(prod_id)]
            update_product_form.name.data = product.get_name()
            update_product_form.price.data = product.get_price()
            update_product_form.description.data = product.get_description()
            update_product_form.count.data = product.get_count()
            stub = str(product.get_filename())
            update_product_form.filename.data = stub[:-12]
        return render_template("updateProduct.html", form=update_product_form,
                               name=name, prod_id=prod_id, user_id=user_id)

    except EOFError or KeyError:
        _alert_message("Error in updating product", 1)
        return redirect(url_for("retrieve_product", referral_route="update_product"))


@app.route("/deleteProduct/<int:prod_id>", methods=["POST"])
def delete_product(prod_id):
    try:
        with shelve.open('user.db', 'w') as user_db:
            temp_dict = user_db["Product"]
            temp_prod = temp_dict[str(prod_id)]
            filename = temp_prod.get_filename()
            app.config["UPLOADED_IMAGES"].remove(filename)
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            print(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            temp_dict.pop(str(prod_id))
            user_db["Product"] = temp_dict

            _alert_message("Product successfully deleted!")
        return redirect(url_for('retrieve_product', referral_route="delete_product"))
    except Exception as exception:
        print(exception)
        _alert_message("Error in deleting product", 1)
        return redirect(url_for("retrieve_product", referral_route="delete_product"))

# TODO: Changing a profile picture etc
# TODO: Searching of product
# TODO: Make report generation not look goofy and generate pdf form, can select various html pages
# TODO: Input excel file, render it and then ask if they want to store the details in the database.
# TODO: Update Customer


@app.route("/generatePDF")
def generate_pdf():
    try:
        if request.method == "GET":
            name = _session_name()
            requests = session["details"][2]
            earnings = session["details"][3]
            monthly_earnings = f"{float(earnings)/12:.2f}"
            progress = session["details"][5]
            referral_chart = [0, 0, 0]
            with shelve.open("user.db", "r") as user_db:
                for customer in user_db["Customer"].values():
                    if customer.get_referral() == "Direct":
                        referral_chart[0] += 1
                    elif customer.get_referral() == "Social":
                        referral_chart[1] += 1
                    else:
                        referral_chart[2] += 1

            # TODO: Connect Code to render area chart to backend (financial earnings etc), do the bar chart code
            #
            pie_chart_data = referral_chart
            area_chart_data = [0, 69420, 150000, 79825, 103159, 209475, 256081, 291080, 315000, 360000, 425000, 540000]

            rendered_html = render_template("index.html", pie_chart_data=pie_chart_data,
                                            area_chart_data=area_chart_data, name=name, progress=progress,
                                            requests=requests, earnings=earnings, monthly_earnings=monthly_earnings)
            # TODO: Custom pdf and python pre-rendering of charts
            document = weasyprint.HTML(string=rendered_html)
            # HTML(string=HTML_CONTENT, base_url='.').write_pdf(stylesheets=["styles.css"])  # Path to CSS file
            pdf = document.write_pdf()
            response = Response(pdf, mimetype='application/pdf')
            response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
            _alert_message("Successfully downloaded report!", 1)
            return response
    except ValueError or IOError or KeyError:
        _alert_message("Error in downloading PDF", 1)
        return redirect(url_for("home", referral_route="generate_pdf"))


@app.route("/uploadData", methods=["GET", "POST"])
def upload_data():
    _alert_message()
    name = _session_name()

    # TODO: Referral route code for upload data
    try:
        data_form = UploadDataFile(request.form)
        if request.method == "POST":
            data_file = request.files["data_file"]
            filename = data_form.filename.data
            database = data_form.database.data
            old_filename = data_file.filename

            data_comp = False
            for data in app.config['UPLOADED_DATAFILES']:
                if data == filename:
                    data_comp = True
                else:
                    continue

            if not (data_file and filename and database) and data_comp is True:
                allowed_chars = string.ascii_letters + string.digits
                filename = "".join(random.choice(allowed_chars.lower()) for i in range(20))

            new_filename = _parse_files_db(database, data_file, filename, old_filename)

            app.config['UPLOADED_DATAFILES'].append(new_filename)
            if database == "Staff":
                return redirect(url_for("retrieve_staff", referral_route="upload_data"))
            else:
                return redirect(url_for("retrieve_customer", referral_route="upload_data"))

    except EOFError or KeyError or IOError:
        _alert_message("Error in uploading data", 1)
        return redirect(url_for("upload_data", referral_route="upload_data"))

    return render_template("uploadFile.html", form=data_form,
                           message=_get_alert_msg(), sh_msg=_get_sh_msg(), name=name)


if __name__ == '__main__':
    app.jinja_env.autoescape = True
    app.secret_key = "hj^&!Hh12h3828hc7ds8f9asd82nc"
    app.config["Show No"] = 0
    app.config["No"] = ""
    app.config["Route"] = ""
    app.config['UPLOAD_FOLDER'] = './static/uploads'  # Set upload folder
    app.config["UPLOADED_IMAGES"] = []
    app.config["DATAFILE_FOLDER"] = './static/datafiles'
    app.config["UPLOADED_DATAFILES"] = []

    try:
        with shelve.open('user.db', 'c') as user_database:
            if not user_database:
                user_database["Customer"] = {}
                user_database["Staff"] = {}
                user_database["Product"] = {}
                user_database["Last ID Used"] = [0, 0, 0]  # [Users, Customers, Staff]
                user_database["Product Pointer"] = 0  # used to create unique product ids
    except KeyError or IOError or UnboundLocalError or EOFError as database_error:
        print("Error encountered opening user.db:", database_error)
    app.run(debug=True)
