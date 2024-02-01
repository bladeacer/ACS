from wtforms import (TelField, DateField, StringField, SelectField, validators,
                     PasswordField, EmailField, FileField, TextAreaField, IntegerField)

from flask_wtf import FlaskForm


class CreateCustomerForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8, max=150), validators.DataRequired()])
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
    referral = SelectField("Referral:", [validators.DataRequired()],
                           choices=[
                               ("", "Select"),
                               ("Direct", "Direct"),
                               ("Social", "Social"),
                               ("Referral", "Referral")
                           ],
                           default="",
                           )


class CreateStaffForm(CreateCustomerForm):
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
    total_earnings = StringField('Total Earnings  $', [validators.Length(min=1, max=150), validators.DataRequired()],
                                 default="0.00")
    self_description = StringField("Description", [validators.Optional()])
    progress = StringField("Progress", [validators.DataRequired()])
    requests = StringField("Requests", [validators.DataRequired()])


class UpdateStaffForm(CreateStaffForm):
    new_name = StringField('New Name', [validators.Length(min=1, max=150)])
    new_email = EmailField('New Email', [validators.Length(min=1, max=150)])
    new_password = PasswordField('New Password', [validators.Length(min=8, max=150)])
    new_gender = SelectField(
        'New Gender',
        [validators.DataRequired()],
        choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')],
        default=''
    )
    new_phone_number = TelField('New Phone Number',
                                [validators.Length(min=8, max=8), validators.NumberRange(min=0, max=99999999)])
    new_mailing_address = StringField('New Mailing Address', [validators.Length(min=1, max=150)])
    new_start_date = DateField('New Start Date')
    new_position = SelectField(
        'New Position',
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
    new_total_earnings = StringField('New Total Earnings  $', [validators.Length(min=1, max=150)], default="0.00")


class LoginForm(FlaskForm):
    email = EmailField("Email", [validators.DataRequired(), validators.Length(min=1, max=150)])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(8, 150)])


class InputUserForm(FlaskForm):
    user_details = TextAreaField("Enter details here:", [validators.DataRequired()])


class ProductForm(FlaskForm):
    name = StringField("Enter product name: ", [validators.Length(min=1, max=150), validators.DataRequired()])
    price = StringField('Enter price ($): ', [validators.Length(min=1, max=150), validators.DataRequired()],
                        default="0.00")
    description = StringField("Enter description: ", [validators.Length(1, 1000), validators.DataRequired()])
    count = IntegerField("Enter stock count: ", [validators.DataRequired(), validators.NumberRange(1, 10000)])
    image = FileField("Insert product image: ", [validators.DataRequired()], name="image")
    filename = StringField("Enter filename: ", [validators.Optional(), validators.Length(1, 150)])


class UpdateProductForm(ProductForm):
    name = StringField("Enter new product name: ", [validators.Length(min=1, max=150), validators.DataRequired()])
    price = StringField('Enter new price ($): ', [validators.Length(min=1, max=150), validators.DataRequired()],
                        default="0.00")
    description = StringField("Enter new description: ", [validators.Length(1, 1000), validators.DataRequired()])
    count = IntegerField("Enter new stock count: ", [validators.DataRequired(), validators.NumberRange(1, 10000)])
    image = FileField("Insert new product image: ", [validators.DataRequired()], name="image")
    filename = StringField("Enter new filename: ", [validators.Optional(), validators.Length(1, 150)])

