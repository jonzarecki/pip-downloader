from django import forms

PYTHON_VERSION = (
    ('3', 'python 3.6'),
    ('2', 'python 2.7'),
)
OS_CHOICES = (
    ('manylinux1_x86_64', 'manylinux1_x86_64'),
    ('win_amd64', 'win_amd64'),
    ('win32', 'win32'),
    ('none', 'none - can try if no wheel exists')
)


class NameForm(forms.Form):
    package = forms.CharField(label='package', max_length=100)
    # package2 = forms.CharField(label='package2', max_length=100)

    python_ver = forms.ChoiceField(choices=PYTHON_VERSION)
    os_version = forms.ChoiceField(choices=OS_CHOICES)
