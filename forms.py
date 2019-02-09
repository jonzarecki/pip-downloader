from django import forms

COLOR_CHOICES = (
    ('2','python 2'),
    ('3', 'python 3'),
)

class NameForm(forms.Form):
    package = forms.CharField(label='package', max_length=100)
    # package2 = forms.CharField(label='package2', max_length=100)

    python_ver = forms.ChoiceField(choices=COLOR_CHOICES)
