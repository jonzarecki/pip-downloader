from django import forms

ABI_VERSION = (
    ('cp36m', '3.6 (cp36m)', ),
    ('cp35m', '3.5 (cp35m)'),
    ('cp27m', '2.7 (cp27m)'),
)
OS_CHOICES = (
    ('linux_win_amd64', 'linux & windows 64'),
    ('win_amd64', 'windows 64'),
    ('manylinux1_x86_64', 'linux'),
    ('win32', 'windows 32'),
    # ('none', 'none - can try if no wheel exists')
)


class NameForm(forms.Form):
    package = forms.CharField(label='Package name', max_length=100)
    # package2 = forms.CharField(label='package2', max_length=100)

    abi_ver = forms.ChoiceField(choices=ABI_VERSION, label='Python version')
    os_version = forms.ChoiceField(choices=OS_CHOICES, label='OS')
