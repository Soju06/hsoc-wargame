from flask import session
from flask_babel import lazy_gettext as _l
from wtforms import PasswordField, SelectField, StringField, TextAreaField
from wtforms.fields.html5 import DateField, URLField, EmailField, IntegerField
from wtforms.validators import InputRequired, NumberRange

from CTFd.constants.languages import SELECT_LANGUAGE_LIST
from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.forms.users import attach_custom_user_fields, build_custom_user_fields
from CTFd.utils.countries import SELECT_COUNTRIES_LIST
from CTFd.utils.user import get_current_user


def SettingsForm(*args, **kwargs):
    class _SettingsForm(BaseForm):
        name = StringField(_l("닉네임"))
        email = StringField(_l("이메일"))
        language = SelectField(_l("Language"), choices=SELECT_LANGUAGE_LIST)
        password = PasswordField(_l("비밀번호"))
        confirm = PasswordField(_l("현재 비밀번호"))

        phone = StringField(_l("전화번호"))
        birthdate = DateField(_l("생년월일"), format="%Y-%m-%d")

        realname = StringField(_l("이름"))
        affiliation = StringField(_l("소속 또는 학교명"))
        grade = IntegerField(
            _l("학년"),
            validators=[NumberRange(min=1, max=3)],
            render_kw={"min": 1, "max": 3},
        )
        classroom = IntegerField(
            _l("반"),
            validators=[InputRequired(), NumberRange(min=1, max=15)],
            render_kw={"min": 1, "max": 15},
        )
        number = IntegerField(
            _l("번호"),
            validators=[InputRequired(), NumberRange(min=1, max=40)],
            render_kw={"min": 1, "max": 40},
        )

        website = URLField(_l("웹사이트"))
        country = SelectField(_l("Country"), choices=SELECT_COUNTRIES_LIST)
        submit = SubmitField(_l("저장"))

        @property
        def extra(self):
            fields_kwargs = _SettingsForm.get_field_kwargs()
            return build_custom_user_fields(
                self,
                include_entries=True,
                fields_kwargs=fields_kwargs,
                field_entries_kwargs={"user_id": session["id"]},
            )

        @staticmethod
        def get_field_kwargs():
            user = get_current_user()
            field_kwargs = {"editable": True}
            if user.filled_all_required_fields is False:
                # Show all fields
                field_kwargs = {}
            return field_kwargs

    field_kwargs = _SettingsForm.get_field_kwargs()
    attach_custom_user_fields(_SettingsForm, **field_kwargs)

    return _SettingsForm(*args, **kwargs)


class TokensForm(BaseForm):
    expiration = DateField(_l("Expiration"))
    description = TextAreaField("Usage Description")
    submit = SubmitField(_l("Generate"))
