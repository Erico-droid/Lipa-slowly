from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, Comment


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)
    image2 = forms.ImageField(label='Image 2', required=False, widget=CustomClearableFileInput)
    image3 = forms.ImageField(label='Image 3', required=False, widget=CustomClearableFileInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['subcategory'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':2,'placeholder':'Add your review...','required':'required','class':'form-control rounded-0 border-black'}))
    class Meta:
        model = Comment
        fields = ('body','rating')
