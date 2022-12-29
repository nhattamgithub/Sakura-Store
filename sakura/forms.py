from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from sakura.models import User, ProductType

class RegistrationForm(FlaskForm):
    username = StringField('Họ và tên của bạn', validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Nhập mật khẩu', validators=[DataRequired()])
    confirm_password = PasswordField('Nhập lại mật khẩu', validators=[DataRequired(), EqualTo('password')])
    phone_num = StringField('Số điện thoại',validators=[DataRequired()])    
    address = StringField('Vui lòng nhập địa chỉ',validators=[DataRequired()])                
    submit = SubmitField('Đăng ký ngay')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email này đã có người sử dụng~! Chọn email khác bạn nhé ~kyun~')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember = BooleanField('Ghi nhớ tui~')
    submit = SubmitField('Đăng nhập')


class UpdateAccountForm(FlaskForm):
    username = StringField('Họ và tên của bạn', validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Ảnh đại diện', validators=[FileAllowed(['jpg', 'png'])])
    phone_num = StringField('Số điện thoại',validators=[DataRequired()])    
    address = StringField('Địa chỉ',validators=[DataRequired()])  
    submit = SubmitField('Cập nhật thông tin')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email này đã có người sử dụng~! Chọn email khác bạn nhé ~kyun~')



class ProductTypeForm(FlaskForm):
    type = StringField('Loại sản phẩm', validators=[DataRequired(), Length(min=2, max=60)])
    submit = SubmitField('Thêm loại sản phẩm')
    
class Types():
    def __init__(self):
        self.data = []
        pt = ProductType.query.all()
        for i in pt:
            self.data.append(i.type)
    def aslist(self):
        return self.data
    def __iter__(self):
        return iter(self.aslist())

class ProductForm(FlaskForm):
    title  = StringField('Tên sản phẩm', validators=[DataRequired(), Length(min=2, max=100)])
    product_img = FileField('Hình ảnh', validators=[FileAllowed(['jpg', 'png'])])
    desc =  StringField('Mô tả sản phẩm',validators=[DataRequired(),Length(min=2, max=500)]) 
    import_price = StringField('Giá nhập',validators=[DataRequired()])  
    price = StringField('Giá bán',validators=[DataRequired()])  
    quantity = IntegerField('Số lượng',validators=[DataRequired(),NumberRange(min=1,max=10)]) 
    supplier = StringField('Nhà cung cấp', validators=[DataRequired(), Length(min=2, max=50)])
    material = StringField('Chất liệu', validators=[DataRequired(), Length(min=2, max=50)])
    size = StringField('Kích thước', validators=[DataRequired(), Length(min=2, max=10)])
    mass = IntegerField('Khối lượng',validators=[DataRequired()]) 
    type = SelectField('Loại sản phẩm',validators=[DataRequired()],choices=Types())
    submit = SubmitField('Cập nhật')

class SearchForm(FlaskForm):
    product_title = StringField('Tên sản phẩm', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Tìm kiếm')