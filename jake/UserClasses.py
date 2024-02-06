class User:
    def __init__(self, user_id, name, email, password, gender="Not indicated", phone_number="Not indicated", mailing_address="Not indicated"):
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
        return self.__user_id

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
        return (f"{self.get_user_id()}, {self.get_name()}, {self.get_password()}, {self.get_email()}, "
                f"{self.get_gender()}, {self.get_phone_number()}, {self.get_mailing_address()}")


class Customer(User):
    def __init__(
            self,
            user_id,
            customer_id,
            name,
            email,
            password,
            gender="Not indicated",
            phone_number="Not indicated",
            mailing_address="Not indicated"
    ):
        super().__init__(user_id, name, email, password, gender, phone_number, mailing_address)
        self.__customer_id = customer_id
        self.__order_history = []

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_order_history(self, order_history):
        self.__order_history = order_history

    def get_customer_id(self):
        return self.__customer_id

    def get_order_history(self):
        return self.__order_history

    def __str__(self):
        return (f"{self.get_user_id()}, {self.get_customer_id()}, {self.get_name()}, {self.get_email()}, "
                f"{self.get_password()}, {self.get_gender()}, {self.get_phone_number()}, {self.get_mailing_address()}")


class Staff(User):
    def __init__(
            self,
            user_id,
            staff_id,
            name,
            email,
            password,
            start_date,
            position,
            total_earnings=0,
            gender="Not indicated",
            phone_number="Not indicated",
            mailing_address="Not indicated",
            self_description="Not indicated"
    ):
        super().__init__(user_id, name, email, password, gender, phone_number, mailing_address)
        self.__staff_id = staff_id
        self.__start_date = start_date
        self.__position = position
        self.__total_earnings = total_earnings
        self.__self_description = self_description

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
        return self.__total_earnings

    def get_self_description(self):
        return self.__self_description

    def __str__(self):
        return (f"{self.get_user_id()}, {self.get_staff_id()}, {self.get_name()}, {self.get_email()}, "
                f"{self.get_password()}, "
                f"{self.get_gender()}, {self.get_phone_number()}, {self.get_mailing_address()}, "
                f"{self.get_start_date()}, {self.get_position()}, {self.get_total_earnings()}, "
                f"{self.get_self_description()}, ")
