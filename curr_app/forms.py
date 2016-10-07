# Imports ####################################################################
from flask.ext.wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, IntegerField, FloatField, TextAreaField,\
    SubmitField, SelectField
from wtforms.validators import Optional, Length, DataRequired, InputRequired

# Form Class Definitions #####################################################

## Catalog Form ##############################################################
# Used for adding & editing the basic catalog record


class CatalogForm(Form):
    catalog_name = StringField('Catalog Name',
                               validators=[DataRequired(),
                                           Length(1, 250)])
    catalog_description = TextAreaField('Description',
                                        validators=[DataRequired(),
                                                    Length(1, 1000)])
    catalog_id = IntegerField('ID', validators=[Optional()])
    submit = SubmitField("Save")

## Category Form #############################################################
# Used for adding & editing the category record


class CategoryForm(Form):
    category_name = StringField('Category Name',
                                validators=[DataRequired(),
                                            Length(1, 250)])
    category_description = TextAreaField('Description',
                                         validators=[DataRequired(),
                                                     Length(1, 1000)])
    category_id = IntegerField('ID', validators=[Optional()])
    submit = SubmitField("Save")

## Item Form #################################################################
# Used for adding & editing the item record


class ItemForm(Form):
    item_id = IntegerField('Item ID',
                           validators=[Optional()])
    item_name = StringField('Item Name',
                            validators=[Optional(),
                                        Length(0, 128,
                                               message='Name too long')])
    item_description = StringField(
        'Description', validators=[
            InputRequired(message='Description missing'),
            Length(0, 512, message='Description too long')])
    item_categories = SelectField(
        'Category', coerce=int, validators=[
            DataRequired(message='Category Missing')])
    item_price = FloatField('Price', validators=[Optional()])
    item_catalog_id = IntegerField('Catalog ID',
                                   validators=[Optional()])
    item_catalog_name = StringField('Item Name',
                                    validators=[
                                        Optional(), Length(
                                            0, 128, message='Name too long')])
    item_photo = FileField('Item Photo', )
    submit = SubmitField("Save")
