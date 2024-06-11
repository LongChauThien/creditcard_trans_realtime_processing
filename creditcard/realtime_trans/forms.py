from django import forms

class IdQuery(forms.Form):
    class_field = forms.IntegerField()
    time = forms.FloatField()
    amount = forms.FloatField()

class TransactionQuery(forms.Form):
    id = forms.CharField(max_length=100)