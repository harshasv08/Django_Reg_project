from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class LogTrckFilterform(forms.Form):
    User_Id = forms.IntegerField(required=False)
    From_Date = forms.DateField(widget=DateInput, required=False)
    To_Date = forms.DateField(widget=DateInput,required=False)

class SortForm(forms.Form):
    sort = forms.ChoiceField(choices=[(x, x) for x in ['User_Id', 'From_Date', 'To_Date']])

    from django import forms
