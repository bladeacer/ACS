class User:
    def __init__(self, user_id, name, email, password, gender="Not indicated", phone_number="Not indicated",
                 mailing_address="Not indicated"):
        self.__user_id = user_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__gender = gender
        self.__phone_number = phone_number
        self.__mailing_address = mailing_address

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_gender(self, gender):
        self.__gender = gender

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_mailing_address(self, mailing_address):
        self.__mailing_address = mailing_address

    def get_user_id(self):
        return str(self.__user_id)

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_gender(self):
        return self.__gender

    def get_phone_number(self):
        return self.__phone_number

    def get_mailing_address(self):
        return self.__mailing_address

    def __str__(self):
        return (
            f"{self.get_user_id()}", f" {self.get_name()}", f" {self.get_password()}", f" {self.get_email()}",
            f" {self.get_gender()}", f" {self.get_phone_number()}", f" {self.get_mailing_address()}"
        )


class Customer(User):
    def __init__(
            self,
            user_id,
            customer_id,
            name,
            email,
            password,
            gender="",
            phone_number="",
            mailing_address="",
            referral=""
    ):
        super().__init__(user_id, name, email, password, gender, phone_number, mailing_address)
        self.__customer_id = customer_id
        self.__referral = referral

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def get_customer_id(self):
        return str(self.__customer_id)

    def set_referral(self, referral):
        self.__referral = referral

    def get_referral(self):
        return self.__referral

    def __str__(self):
        return (f"{self.get_user_id()}, {self.get_customer_id()}, {self.get_name()}, {self.get_email()}, "
                f"{self.get_password()}, {self.get_gender()}, {self.get_phone_number()}, {self.get_mailing_address()}, "
                f"{self.get_referral()}")


class Staff(User):
    def __init__(self, user_id, staff_id, name, email, password, start_date, position, total_earnings=0, gender="",
                 phone_number="", mailing_address="", self_description="", progress=50, requests=18):
        super().__init__(user_id, name, email, password, gender, phone_number, mailing_address)
        self.__staff_id: str = staff_id
        self.__start_date: str = start_date
        self.__position: str = position
        self.__total_earnings: float = total_earnings
        self.__self_description: str = self_description
        self.__progress = progress
        self.__requests = requests

    def set_staff_id(self, staff_id):
        self.__staff_id = staff_id

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def set_position(self, position):
        self.__position = position

    def set_total_earnings(self, total_earnings):
        self.__total_earnings = total_earnings

    def set_self_description(self, self_description):
        self.__self_description = self_description

    def get_staff_id(self):
        return self.__staff_id

    def get_start_date(self):
        return self.__start_date

    def get_position(self):
        return self.__position

    def get_total_earnings(self):
        return round(float(self.__total_earnings), 2)

    def get_self_description(self):
        return self.__self_description

    def get_requests(self):
        return self.__requests

    def get_progress(self):
        return self.__progress

    def set_progress(self, progress):
        self.__progress = progress

    def set_requests(self, requests):
        self.__requests = requests

    def __str__(self):
        return (f"{self.get_user_id()}, {self.get_staff_id()}, {self.get_name()}, {self.get_email()}, "
                f"{self.get_password()}, "
                f"{self.get_gender()}, {self.get_phone_number()}, {self.get_mailing_address()}, "
                f"{self.get_start_date()}, {self.get_position()}, {float(self.get_total_earnings()):.2f}, "
                f"{self.get_self_description()}, {self.get_requests()}, {self.get_progress()} ")


class Product:
    def __init__(self, name, price, prod_id, description, count, is_stock, filename):
        self.__name = name
        self.__price = price
        self.__description = description
        self.__count = count
        self.__is_stock = is_stock
        self.__prod_id = prod_id
        self.__filename = filename

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_description(self):
        return self.__description

    def get_count(self):
        return self.__count

    def get_is_stock(self):
        return self.__is_stock

    def get_prod_id(self):
        return str(self.__prod_id)

    def get_filename(self):
        return self.__filename

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_description(self, description):
        self.__description = description

    def set_count(self, count):
        self.__count = count

    def set_is_stock(self, stock):
        self.__is_stock = stock

    def set_prod_id(self, prod_id):
        self.__prod_id = prod_id

    def set_filename(self, filename):
        self.__filename = filename

    def __str__(self):
        return (f"{self.get_name()}, {self.get_price()}, {self.get_prod_id()}, {self.get_description()}, {self.get_count()},"
                f" {self.get_is_stock()}, {self.get_filename()}")
