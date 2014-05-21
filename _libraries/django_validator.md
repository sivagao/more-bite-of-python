https://docs.djangoproject.com/en/dev/ref/forms/validation/

Validation of a Form is split into several steps, which can be customized or overridden:

to_python()
The to_python() method on a Field is the first step in every validation. It coerces the value to correct datatype and raises ValidationError if that is not possible. This method accepts the raw value from the widget and returns the converted value. For example, a FloatField will turn the data into a Python float or raise a ValidationError.

valdiate()
The validate() method on a Field handles field-specific validation that is not suitable for a validator, It takes a value that has been coerced to correct datatype and raises ValidationError on any error. This method does not return anything and shouldn’t alter the value. You should override it to handle validation logic that you can’t or don’t want to put in a validator.

run_validators()
The run_validators() method on a Field runs all of the field’s validators and aggregates all the errors into a single ValidationError. You shouldn’t need to override this method.

clean()
The clean() method on a Field subclass. This is responsible for running to_python, validate and run_validators in the correct order and propagating their errors. If, at any time, any of the methods raise ValidationError, the validation stops and that error is raised. This method returns the clean data, which is then inserted into the cleaned_data dictionary of the form.

form's clean_<fieldname>()
The clean_<fieldname>() method in a form subclass – where <fieldname> is replaced with the name of the form field attribute. This method does any cleaning that is specific to that particular attribute, unrelated to the type of field that it is. This method is not passed any parameters. You will need to look up the value of the field in self.cleaned_data and remember that it will be a Python object at this point, not the original string submitted in the form (it will be in cleaned_data because the general field clean() method, above, has already cleaned the data once).

For example, if you wanted to validate that the contents of a CharField called serialnumber was unique, clean_serialnumber() would be the right place to do this. You don’t need a specific field (it’s just a CharField), but you want a formfield-specific piece of validation and, possibly, cleaning/normalizing the data.

This method should return the cleaned value obtained from cleaned_data, regardless of whether it changed anything or not.

form's clean()
The Form subclass’s clean() method. This method can perform any validation that requires access to multiple fields from the form at once. This is where you might put in things to check that if field A is supplied, field B must contain a valid email address and the like. This method can return a completely different dictionary if it wishes, which will be used as the cleaned_data.

Since the field validation methods have been run by the time clean() is called, you also have access to the form’s errors attribute which contains all the errors raised by cleaning of individual fields.

Note that any errors raised by your Form.clean() override will not be associated with any field in particular. They go into a special “field” (called __all__), which you can access via the non_field_errors() method if you need to. If you want to attach errors to a specific field in the form, you need to call add_error().

Also note that there are special considerations when overriding the clean() method of a ModelForm subclass. (see the ModelForm documentation for more information)

更好的ValidatorError
```python
raise ValidationError(
    _('Invalid value: %(value)s'),
    code='invalid',
    params={'value': '42'},
)
```

```python
import datetime
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _

def validate_date_today_or_later(value):
    'Place this in validators.py and import it to keep your model a bit cleaner'
    if value < datetime.date.today():
        raise exceptions.ValidationError(_('Date must be today or later'))

class TodayOrLaterDateField(models.DateField):
    default_validators = [validate_date_today_or_later,]
```


```python
from django.forms import CharField
from django.core import validators

class SlugField(CharField):
    default_validators = [validators.validate_slug]

slug = forms.CharField(validators=[validators.validate_slug])

class MultiEmailField(forms.Field):
    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)

        for email in value:
            validate_email(email)

class ContactForm(forms.Form):
    # Everything as before.
    ...

    def clean_recipients(self):
        data = self.cleaned_data['recipients']
        if "fred@example.com" not in data:
            raise forms.ValidationError("You have forgotten about Fred!")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data


class ContactForm(forms.Form):
    # Everything as before.
    ...

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject and "help" not in subject:
            msg = "Must put 'help' in subject when cc'ing yourself."
            self.add_error('cc_myself', msg)
            self.add_error('subject', msg)

        if cc_myself and subject:
            # Only do something if both fields are valid so far.
            if "help" not in subject:
                raise forms.ValidationError("Did not send for 'help' in "
                        "the subject despite CC'ing yourself.")

```