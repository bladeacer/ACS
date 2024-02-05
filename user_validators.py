from datetime import *

import bcrypt

from Password import HashedPassword
staff_positions = ['CEO', 'COO', 'Front-end Developer', 'Inventory Manager', 'Intern', ]
genders = ["M", "F", "O"]


def matching_passwords(new_password, old_password):
    password = bytes(new_password, "utf-8")
    if bcrypt.hashpw(password, old_password.salt) == old_password.hash:
        return True
    return False


def check_staff_errors(staff, staff_dict):
    errors = []

    if not staff.get_name():
        errors.append("Staff name is invalid")

    email = staff.get_email()
    if check_existing_email(email, staff_dict):
        errors.append("Email already exists")
    elif not is_email(email):
        errors.append("Staff email is invalid")

    password = staff.get_password()
    password_errors = check_password_errors(password)
    if password_errors:
        errors.append(", ".join(password_errors))
    else:
        staff.set_password(HashedPassword(password))

    if staff.get_gender() not in genders:
        errors.append("Customer gender is invalid")

    new_start_date = convert_to_date(staff.get_start_date())
    if new_start_date:
        staff.set_start_date(new_start_date)
    else:
        errors.append("Staff start date is invalid")

    if staff.get_position() not in staff_positions:
        errors.append("Staff position is invalid")

    # returns total earnings as float if valid, else returns empty string or error
    new_total_earnings = convert_total_earnings_to_float(staff.get_total_earnings())
    if type(new_total_earnings) is float:
        staff.set_total_earnings(new_total_earnings)
    else:
        # in this case, new_total_earnings is storing the error, either default error (empty string), or currency error
        errors.append(f"Staff total earnings is invalid{new_total_earnings}")

    if staff.get_gender() not in genders:
        errors.append("Staff gender is invalid")

    if not is_phone_number(staff.get_phone_number()):
        errors.append("Staff phone number is invalid")

    if not staff.get_mailing_address():
        errors.append("Staff mailing_address is invalid")

    if errors:
        return errors
    else:
        return staff


def check_customer_errors(customer, customer_dict):
    errors = []

    if not customer.get_name():
        errors.append("Customer name is invalid")

    email = customer.get_email()
    if check_existing_email(email, customer_dict):
        errors.append("Email already exists")
    elif not is_email(email):
        errors.append("Staff email is invalid")

    password = customer.get_password()
    password_errors = check_password_errors(password)
    if password_errors:
        errors.append(", ".join(password_errors))
    else:
        customer.set_password(HashedPassword(password))

    if customer.get_gender() not in genders:
        errors.append("Customer gender is invalid")

    if not is_phone_number(customer.get_phone_number()):
        errors.append("Customer phone number is invalid")

    if not customer.get_mailing_address():
        errors.append("Customer mailing_address is invalid")

    if errors:
        return errors
    else:
        return customer


def check_existing_email(email, dictionary):
    for user in dictionary.values():
        if email == user.get_email():
            return user
    return False


def convert_multiline_string_to_list(multiline_string):
    current_line = ""
    final_list = []
    for character in multiline_string:
        if character == "\r":
            final_list.append(current_line)
            current_line = ""
        elif character != "\n":
            current_line += character
    else:
        final_list.append(current_line)
    return final_list


def convert_to_date(date_string):
    try:
        connector = ""
        for symbol in ["/", "-", "."]:
            if symbol in date_string:
                connector = symbol
                break
        split_date = date_string.split(connector)
        return datetime(int(split_date[2]), int(split_date[1]), int(split_date[0]))
    except ValueError:
        return False


def convert_total_earnings_to_float(total_earnings):
    try:
        if "$" == total_earnings[0]:
            return float(total_earnings[1:])
        elif not is_float(total_earnings[0]):
            return ". We only accept SGD currency"
        else:
            return float(total_earnings)
    except ValueError:
        return ""


def is_float(number_string):
    try:
        float(number_string)
        return True
    except ValueError:
        return False


def is_email(email):
    if "@" in email:
        username = email[:email.rfind("@")]
        domain = email[email.rfind("@"):]
        if not (domain.endswith(".com") or domain.endswith(".net") or domain.endswith(".sg")):
            return False
        if not (username.isalnum() and username.islower()):
            return False
        return True
    else:
        return False


def is_phone_number(phone_number):
    if is_float(phone_number) and len(phone_number) == 8:
        return True
    return False


def check_password_errors(password):
    error_list = []
    if not password:
        error_list.append("Empty password")
    if len(password) < 8 or len(password) > 16:
        error_list.append("Password length must be 8-16 characters")
    if not contains_special_character(password):
        error_list.append("Password missing special character")
    if not contains_uppercase(password):
        error_list.append("Password missing uppercase character")
    if not contains_lowercase(password):
        error_list.append("Password missing lowercase character")
    if not contains_number(password):
        error_list.append("Password missing numeric character (0-9)")
    if " " in password:
        error_list.append("Whitespaces not allowed in password")
    if error_list:
        return error_list
    return []


def contains_special_character(string):
    special_characters = "!@#$%^&*())-+={}[]|/><.,:;')("
    for character in string:
        if character in special_characters:
            return True
    return False


def contains_uppercase(string):
    for character in string:
        if character.isupper():
            return True
    return False


def contains_lowercase(string):
    for character in string:
        if character.islower():
            return True
    return False


def contains_number(string):
    for character in string:
        if character.isdigit():
            return True
    return False


# staff1 = Staff(1, 1, "Jake", "jake", "Test123$", "x", "x", "x")
# print(is_email(staff1.get_email()))
