from wtforms import Form, IntegerField, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField


class FeedbackForm(Form):
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    category = SelectField('Category', [validators.DataRequired()],
                           choices=[('', 'Select'), ('Product', 'Product'), ('Delivery', 'Delivery'),
                                    ('Website', 'Website'), ('General', 'General')],
                           default='')
    rating = IntegerField('Rating (1-5)', render_kw={"placeholder": "Enter a rating between 1 and 5"})
    feedback_content = TextAreaField('Feedback', [validators.DataRequired()])
