"""b"""
import shelve
import os
from flask import Flask, render_template, request, redirect, url_for, session
from Forms import CreateCustomerForm, CreateStaffForm, LoginForm, UpdateStaffForm, ProductForm
from User import Customer, Staff, Product
from werkzeug.utils import secure_filename
from PIL import Image
import io
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


def login_session_handler(staff_id: int = 0):
    session.clear()
    app.config["Topbar"] = 1
    session["id"] = staff_id


@app.route("/", methods=['GET', 'POST'])
def login():
    try:
        login_session_handler()
        referral_route = request.args.get("referral_route")
        if referral_route == "login":
            _alert_message("Invalid password or username", 1)
        elif referral_route == "session_chk":
            _alert_message("No staff created yet oh noes")
        else:
            _alert_message()
        create_login_form = LoginForm(request.form)
        with shelve.open('user.db', 'c') as user_db:
            if request.method == "POST" and create_login_form.validate():
                for staff in user_db["Staff"].values():
                    if (staff.get_email() == create_login_form.email.data and staff.get_password() ==
                            create_login_form.password.data):
                        staff.set_total_earnings(round(float(staff.get_total_earnings()), 0))
                        start_date = staff.get_start_date()
                        staff.set_start_date(f"{start_date.day}/{start_date.month}/{start_date.year}")
                        session["id"] = staff.get_staff_id()
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
    # TODO: Take chunk of code below and yeet it to all app route by encapsulating as function
    # TODO: Create product inventory, link up to charts etc.
    referral_route = request.args.get("referral_route")
    if referral_route == "login":
        _alert_message()

    _staff_details()
    name = _session_name()
    requests = session["details"][2]
    earnings = session["details"][3]
    monthly_earnings = f"{float(earnings)/12:.2f}"
    progress = session["details"][5]

    # TODO: Connect Code to render charts to backend, do the bar chart code
    pie_chart_data = [50, 34, 27]
    area_chart_data = [0, 69420, 150000, 79825, 103159, 209475, 256081, 291080, 315000, 360000, 425000, 540000]

    return render_template("index.html", pie_chart_data=pie_chart_data, area_chart_data=area_chart_data, name=name,
                           progress=progress, requests=requests, earnings=earnings, monthly_earnings=monthly_earnings)


@app.route("/profile")
def profile():
    _staff_details()
    staff_id = session["id"]
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
                           staff_id=staff_id, position=position)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    name = _session_name()

    create_customer_form = CreateCustomerForm(request.form)
    if request.method == "POST" and create_customer_form.validate():
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
            mailing_address=create_customer_form.mailing_address.data
        )
        customer_dict = user_db["Customer"]
        customer_dict[str(new_user_id)] = customer
        user_db["Customer"] = customer_dict
        user_db["Last ID Used"] = [new_user_id, new_customer_id, user_db["Last ID Used"][2]]
        user_db.close()
        return redirect(url_for("retrieve_customer", referral_route="create_customer"))
    else:
        pass
        # TODO: Alert message for invalid create customer
    return render_template('createCustomer.html', form=create_customer_form, message=_get_alert_msg(),
                           sh_msg=_get_sh_msg(), name=name)


@app.route('/retrieveCustomer')
def retrieve_customer():
    name = _session_name()

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
                               message=_get_alert_msg(), sh_msg=_get_sh_msg(), name=name)
    except KeyError:
        _alert_message("Error retrieving customer", 1)
        return redirect(url_for("create_customer", referral_route="retrieve_customer"))


@app.route('/searchCustomer', methods=['POST'])
def search_customer():
    name = _session_name()

    user_search_item = request.get_data(as_text=True)[12:]
    with shelve.open("user.db", "c") as user_db:
        customer_list = user_db["Customer"].values()
        if user_search_item in customer_list:
            # customer = customer_list[], probably retrieve and index everything e
            # TODO: Make search index retrieve customer and staff
            pass
        else:
            return render_template('searchCustomer.html', customer=None, name=name)
    return render_template('searchCustomer.html', name=name)


@app.route('/deleteCustomer/<int:user_id>', methods=['POST'])
def delete_customer(user_id):
    name = _session_name()

    with shelve.open('user.db', 'w') as user_db:
        temporary_dict = user_db['Customer']
        temporary_dict.pop(str(user_id))
        user_db["Customer"] = temporary_dict
    return redirect(url_for('retrieve_customer', referral_route="delete_customer", name=name))


@app.route('/clearCustomer')
def clear_customer():

    with shelve.open('user.db', 'w') as user_db:
        user_db['Customer'] = {}
    _alert_message("No customer created yet, create one")
    return redirect(url_for('create_customer'))


@app.route('/createStaff', methods=['GET', 'POST'])
def create_staff():

    create_staff_form = CreateStaffForm(request.form)
    referral_route = request.args.get("referral_route")
    if referral_route == "login":
        _alert_message("Redirected from login page", 1)
        app.config["Topbar"] = 0
    elif referral_route == "retrieve_staff":
        _alert_message("Redirected from retrieve staff", 1)
        app.config["Topbar"] = 0
    elif referral_route == "home":
        _alert_message("Redirected from homepage", 1)
        app.config["Topbar"] = 0
    else:
        _alert_message()
        app.config["Topbar"] = 0
    if app.config["Route"] == "login":
        return redirect(url_for("login", referral_route="create_staff"))
    if request.method == 'POST':
        # TODO: Make the validation stuff work
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
                           sh_msg=_get_sh_msg(), sh_topbar=app.config["Topbar"], footer=1)
    # TODO: Check if email and password are already taken, if yes try again.
    # TODO: So now createstaff works like update if we do not increment the ID by 1


@app.route('/retrieveStaff')
def retrieve_staff():
    name = _session_name()

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
                               message=_get_alert_msg(), sh_msg=_get_sh_msg(), name=name)
    except EOFError or KeyError:
        _alert_message("No staff created yet, create one.", 1)
        return redirect(url_for("create_staff", referral_route="retrieve_staff"))


@app.route('/searchStaff', methods=['POST'])
def search_staff():
    name = _session_name()

    user_search_item = int(request.get_data(as_text=True)[12:])
    with shelve.open("user.db", "r") as user_db:
        staff_dict = user_db['Staff']
        if user_search_item in staff_dict:
            staff = staff_dict[user_search_item]
            staff.set_total_earnings(float(staff.get_total_earnings()))
            start_date = staff.get_start_date()
            staff.set_start_date(f"{start_date.day}/{start_date.month}/{start_date.year}")
        else:
            return render_template('searchStaff.html', staff=None, name=name)
    return render_template('searchStaff.html', staff=staff, name=name)


@app.route('/updateStaff/<int:user_id>', methods=['GET', 'POST'])
def update_staff(user_id):
    name = _session_name()

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
        return render_template('updateStaff.html', form=update_staff_form, name=name)

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

    referral_route = request.args.get("referral_route")
    if referral_route == "login":
        _alert_message("Redirected from login page", 1)
    elif referral_route == "retrieve_product":
        _alert_message("Redirected from retrieve product", 1)
    elif referral_route == "home":
        _alert_message("Redirected from homepage", 1)
    else:
        _alert_message()
    if app.config["Route"] == "login":
        return redirect(url_for("login", referral_route="create_staff"))

    try:
        prod_form = ProductForm(request.form)
        if request.method == "POST":
            if 'image' not in request.files:
                return "No image uploaded", 400

            image = request.files['image']
            filename = secure_filename(prod_form.filename.data)

            # Read the image contents as bytes to work with Pillow
            image_bytes = image.read()

            # Open the image from bytes using Pillow
            img = Image.open(io.BytesIO(image_bytes))

            # Downsize the image to 500x500 pixels, adjust filter based on PIL version
            if hasattr(Image, "ANTIALIAS"):
                resized_img = img.resize((500, 500), Image.ANTIALIAS)
            else:
                # Use alternative filter if ANTIALIAS is not available in your Pillow version
                resized_img = img.resize((500, 500), Image.BILINEAR)

            # Save the resized image
            resized_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            _alert_message("Image uploaded successfully!", 1)

            user_db = shelve.open('user.db', 'c')
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
                              prod_form.filename.data
                              )
            prod_dict[product.get_prod_id()] = product
            user_db["Product"] = prod_dict
            user_db["Product Pointer"] = new_product_id
            user_db.close()
            return redirect(url_for("retrieve_product", referral_route="create_product"))
        elif referral_route == "create_product":
            _alert_message("Error in validating product form", 1)
            return redirect(url_for("create_product"))

    except EOFError or KeyError:
        _alert_message("Error in product form", 1)
        return redirect(url_for("retrieve_product", referral_route="update_product"))

    return render_template("createProduct.html", form=prod_form,
                           message=_get_alert_msg(), sh_msg=_get_sh_msg(), name=name)


@app.route("/retrieveProduct")
def retrieve_product():
    name = _session_name()

    try:
        referral_route = request.args.get("referral_route")
        with shelve.open("user.db", "r") as user_db:
            product_list = []
            count = 0
            for product in user_db["Product"].values():
                product.set_price(float(product.get_price()))
                product_list.append(product)

                count += 1
        if count != 0 and _get_alert_msg() == "Error in updating product":
            pass

        elif count != 0 and referral_route == "update_staff":
            _alert_message("Redirected from update product", 1)
        elif count != 0:
            _alert_message("Retrieve successful", 1)
        else:
            _alert_message("No product created yet, create one.", 1)
            return redirect(url_for("create_product", referral_route="retrieve_product"))
        return render_template('retrieveProduct.html', count=count, product_list=product_list,
                               message=_get_alert_msg(), sh_msg=_get_sh_msg(), name=name)

    except EOFError or KeyError:
        _alert_message("No product created yet, create one.", 1)
        return redirect(url_for("create_product", referral_route="retrieve_product"))


@app.route("/updateProduct/<int:prod_id>", methods=["GET", "POST"])
def update_product(prod_id):
    pass


@app.route("/deleteProduct/<int:prod_id>", methods=["POST"])
def delete_product(prod_id):
    pass


# TODO: Search product ???
# TODO: Create goofy "server is down maintenance notice page"


if __name__ == '__main__':
    app.jinja_env.autoescape = True
    app.secret_key = "hj^&!Hh12h3828hc7ds8f9asd82nc"
    app.config["Show No"] = 0
    app.config["No"] = ""
    app.config["Route"] = ""
    app.config["Topbar"] = 0
    app.config['UPLOAD_FOLDER'] = 'uploads'
    try:
        with shelve.open('user.db', 'c') as user_database:
            if not user_database:
                user_database["Customer"] = {}
                user_database["Staff"] = {}
                user_database["Product"] = {}
                user_database["Last ID Used"] = [0, 0, 0]  # [Users, Customers, Staff]
                user_database["Product Pointer"] = 0  # used to create unique product ids
                # TODO: Use the product pointer e

    except KeyError or IOError or UnboundLocalError or EOFError as database_error:
        print("Error encountered opening user.db:", database_error)
    app.run(debug=True)
