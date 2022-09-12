from django import forms
from .models import SubscriptionEmail, JobApplication


class EmailSubscriptionForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Add your email', 'type':'email', 'name':'email', 'required':'required','class':'form-control'}))
    class Meta:
        model = SubscriptionEmail
        fields = ('email',)

class JobApplicationForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name *', 'type':'text', 'name':'name', 'required':'required','class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email *', 'type':'email', 'name':'email', 'required':'required','class':'form-control'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Phone Number *', 'type':'number', 'name':'phone', 'required':'required','class':'form-control'}))
    previous_position = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Previous position | company name or None *', 'type':'text', 'name':'position', 'required':'required','class':'form-control'}))
    education = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Institution of Learning for this position *', 'type':'text', 'name':'education', 'required':'required','class':'form-control'}))
    experience_summary = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'placeholder':'Your experience summary *','required':'required','class':'form-control'}))
    cover_letter = forms.CharField(widget=forms.Textarea(attrs={'rows':6,'placeholder':'Write your cover letter *','required':'required','class':'form-control'}))
    resume = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'file-upload-input','type':'file','onchange':'readURL(this);','accept':'.doc,.docx,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document*,application/pdf'}))
    class Meta:
        model = JobApplication
        exclude = ('job_opportunity',)
