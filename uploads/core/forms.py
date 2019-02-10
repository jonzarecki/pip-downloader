from django import forms

ABI_VERSION = (
    ('cp36m', 'cp36m'),
    ('cp35m', 'cp35m'),
    ('cp27m', 'cp27m'),
)
OS_CHOICES = (
    ('win_amd64', 'win_amd64'),
    ('manylinux1_x86_64', 'manylinux1_x86_64'),
    ('win32', 'win32'),
    # ('none', 'none - can try if no wheel exists')
)


class NameForm(forms.Form):
    package = forms.CharField(label='package', max_length=100)
    # package2 = forms.CharField(label='package2', max_length=100)

    abi_ver = forms.ChoiceField(choices=ABI_VERSION)
    os_version = forms.ChoiceField(choices=OS_CHOICES)
