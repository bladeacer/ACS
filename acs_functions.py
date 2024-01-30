from datetime import *


staff_positions = ['CEO', 'COO', 'Front-end Developer', 'Inventory Manager', 'Intern', ]
genders = ["M", "F", "O"]


def convert_multiline_string_to_list(multiline_string):
    current_line = ""
    final_list = []
    for character in multiline_string:
        if character == "\n":
            final_list.append(current_line)
            current_line = ""
        else:
            current_line += character
    else:
        final_list.append(current_line)
    return final_list


def check_staff_errors(staff):
    errors = []
    if not staff.get_name():
        errors.append("Staff name is invalid")
    if not is_email(staff.get_email()):
        errors.append("Staff email is invalid")
    if not is_valid_password(staff.get_password()):
        errors.append("Staff password is invalid")
    new_start_date = convert_to_date(staff.get_start_date())
    if new_start_date:
        staff.set_start_date(new_start_date)
    else:
        errors.append("Staff start date is invalid")
    if staff.get_position() not in staff_positions:
        errors.append("Staff position is invalid")
    new_total_earnings = staff.get_total_earnings()
    if "$" == new_total_earnings[0]:
        new_total_earnings = new_total_earnings[1:]
    new_total_earnings = convert_to_float(new_total_earnings)
    if type(new_total_earnings) is float:
        staff.set_total_earnings(new_total_earnings)
    else:
        errors.append("Staff total earnings is invalid")
    if staff.get_gender() not in genders:
        errors.append("Staff gender is invalid")
    if not is_phone_number(staff.get_phone_number()):
        errors.append("Staff phone number is invalid")
    if not staff.get_mailing_address():
        errors.append("Staff mailing_address is invalid")
    return errors


def check_customer_errors(customer):
    errors = []
    if not customer.get_name():
        errors.append("Customer name is invalid")
    if not is_email(customer.get_email()):
        errors.append("Staff email is invalid")
    if not is_valid_password(customer.get_password()):
        errors.append("Customer password is invalid")
    if customer.get_gender() not in genders:
        errors.append("Customer gender is invalid")
    if not is_phone_number(customer.get_phone_number()):
        errors.append("Customer phone number is invalid")
    if not customer.get_mailing_address():
        errors.append("Customer mailing_address is invalid")
    return errors


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


def convert_to_float(number_string):
    try:
        return float(number_string)
    except ValueError:
        return False


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


def is_valid_password(password):
    if not password:
        return False
    if len(password) < 8 or len(password) > 16:
        return False
    if not contains_special_character(password):
        return False
    if not contains_uppercase(password):
        return False
    if not contains_lowercase(password):
        return False
    if not contains_number(password):
        return False
    if " " in password:
        return False
    return True


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
