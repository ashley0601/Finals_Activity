from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'reference', 'method_payment', 'contact_no', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'method_payment': forms.Select(
                attrs={'class': 'form-control', 'required': True},
                choices=[
                    ('Cash', 'Cash'),
                    ('Bank Transfer', 'Bank Transfer'),
                    ('Online Payment', 'Online Payment'),
                    ('Check', 'Check'),
                ]
            ),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': True}),
        }

    def clean_reference(self):
        reference = self.cleaned_data.get('reference')
        if Payment.objects.filter(reference=reference).exists():
            raise forms.ValidationError(f"Reference '{reference}' already exists. Please use a unique reference number.")
        return reference

class PaymentEditForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'reference', 'method_payment', 'contact_no', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'method_payment': forms.Select(
                attrs={'class': 'form-control', 'required': True},
                choices=[
                    ('Cash', 'Cash'),
                    ('Bank Transfer', 'Bank Transfer'),
                    ('Online Payment', 'Online Payment'),
                    ('Check', 'Check'),
                ]
            ),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        self.instance_id = kwargs.pop('instance_id', None)
        super().__init__(*args, **kwargs)

    def clean_reference(self):
        reference = self.cleaned_data.get('reference')
        queryset = Payment.objects.filter(reference=reference)
        if self.instance_id:
            queryset = queryset.exclude(id=self.instance_id)
        if queryset.exists():
            raise forms.ValidationError(f"Reference '{reference}' already exists. Please use a unique reference number.")
        return reference