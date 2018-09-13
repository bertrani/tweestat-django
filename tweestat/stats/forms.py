from django import forms

class StatForm(forms.Form):
    field = forms.CharField(max_length=100)
    start = forms.DateField
    end = forms.DateField

    def clean_field(self):
        print(self.cleaned_data["field"])
        return self.cleaned_data["field"]

    def clean_start(self):
        print(self.cleaned_data["start"])
        return self.cleaned_data["start"]

    def clean_end(self):
        return self.cleaned_data["end"]