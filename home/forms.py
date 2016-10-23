from django import forms
from django.core import validators

# class LabelErrorList(forms.util.ErrorList):
#     def __unicode__(self):              # __unicode__ on Python 2
#         return self.as_divs()
#     def as_divs(self):
#         if not self: return ''
#         return '<label class="errorlist">%s</label>' % ''.join(['<label class="error">%s</label>' % e for e in self])

class ChurchForm(forms.Form):
    username = forms.CharField(validators=[validators.MaxLengthValidator(20, "Too many characters (Less than 20)"),
                                           validators.MinLengthValidator(5, "Not enough characters (More than 5)"),
                                           validators.RegexValidator("^[a-zA-Z0-9]*$",
                                                                     "Only alphanumeric characters allowed")
                                           ])
    password = forms.CharField(validators=[validators.MaxLengthValidator(20, "Too many characters (Less than 20)"),
                                           validators.MinLengthValidator(8, "Not enough characters (More than 5)"),
                                           validators.RegexValidator("^[a-zA-Z0-9]*$",
                                                                     "Only alphanumeric characters allowed")
                                           ])
    confirm = forms.CharField()
    firstName = forms.CharField(validators=[validators.RegexValidator("^[a-zA-Z]*$", "Only letters allowed")
                                           ])
    lastName = forms.CharField(validators=[validators.RegexValidator("^[a-zA-Z]*$", "Only letters allowed")
                                           ])
    email = forms.EmailField(validators=[validators.validate_email])
    name = forms.CharField(validators=[validators.MaxLengthValidator(50, "Too many characters (Less than 50)"),
                                       validators.RegexValidator("^[a-zA-Z]*$", "Only letters allowed")
                                       ])
    phone = forms.CharField(validators=[validators.MaxLengthValidator(9, "Please enter a valid phone number"),
                                         validators.RegexValidator("^[0-9]*$", "Please enter a valid phone number")
                                       ])
    address1 = forms.CharField(required=True)
    address2 = forms.CharField(required=False)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    zipcode = forms.CharField(validators=[validators.RegexValidator("^[0-9]*$", "Please enter a valid zipcode")])

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data