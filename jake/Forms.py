from wtforms import Form, DecimalField, TelField, DateField, StringField, SelectField, TextAreaField, validators, \
    RadioField, PasswordField, \
    EmailField


class BaseForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField(
        'Gender',
        [validators.DataRequired()],
        choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')],
        default=''
    )
    phone_number = TelField(
        'Phone Number',
        [
            validators.Length(min=8, max=8),
            validators.DataRequired()
        ]
    )
    mailing_address = StringField(
        'Mailing Address',
        [validators.Length(min=1, max=150), validators.DataRequired()]
    )


class CustomerForm(BaseForm):
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={'id': 'password_input'})


class CustomerChangePasswordForm(Form):
    old_password = PasswordField('Old Password', [validators.Length(min=1, max=150), validators.DataRequired()],
                                 render_kw={'id': 'password_input'})
    new_password = PasswordField('New Password', [validators.Length(min=1, max=150), validators.DataRequired()],
                                 render_kw={'id': 'password_input_new'})


class StaffForm(BaseForm):
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={'id': 'password_input'})
    start_date = DateField('Start Date', [validators.DataRequired()])
    position = SelectField(
        'Position',
        [validators.Length(min=1, max=150), validators.DataRequired()],
        choices=[
            ('', 'Select'),
            ('Front-end Developer', 'Front-end Developer'),
            ('Inventory Manager', 'Inventory Manager'),
            ('Intern', 'Intern'),
            ('CEO', 'CEO'),
            ('COO', 'COO')
        ],
        default='',
    )
    total_earnings = StringField('Total Earnings', [validators.Length(min=1, max=150)], default="$0")


class UpdateCustomerForm(BaseForm):
    gender = SelectField(
        'Gender',
        choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')],
        default=''
    )
    phone_number = TelField(
        'Phone Number',
        [
            validators.Length(min=1, max=150),
        ]
    )
    mailing_address = StringField(
        'Mailing Address',
        [validators.Length(min=1, max=150)]
    )


class UpdateStaffForm(BaseForm):
    start_date = DateField('Start Date', [validators.DataRequired()])
    position = SelectField(
        'Position',
        [validators.Length(min=1, max=150), validators.DataRequired()],
        choices=[
            ('', 'Select'),
            ('Front-end Developer', 'Front-end Developer'),
            ('Inventory Manager', 'Inventory Manager'),
            ('Intern', 'Intern'),
            ('CEO', 'CEO'),
            ('COO', 'COO')
        ],
        default='',
    )
    total_earnings = StringField('Total Earnings', [validators.Length(min=1, max=150)], default="$0")


class InputUserForm(Form):
    user_details = TextAreaField(
        "Enter details here:",
        [validators.DataRequired()],
        render_kw={"placeholder": "Name, Email, Password etc."}
    )
