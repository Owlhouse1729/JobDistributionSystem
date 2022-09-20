from django import forms
from .models import MasterShift, PersonalShift


class EmployerSelectionForm(forms.Form):

    chosen_worker = forms.fields.ChoiceField(
        choices = (
            ('')
        )
    )