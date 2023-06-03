from django import forms
from base.models import Category

def category():
    storage = []
    for i in Category.objects.all():
        storage.append(tuple([i, i]))
    CATEGORY_CHOICES = tuple(storage)
    return CATEGORY_CHOICES


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class AddItemForm(forms.Form):
    name = forms.CharField(max_length=200, label='Tên hàng')
    description = forms.CharField(widget=forms.Textarea, label='Mô tả')
    thumbnail = forms.ImageField(label='Hình ảnh bìa')
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'accept': 'image/*',
        'multiple': True,
    }) ,label='Hình ảnh')
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=category, required=False, label='Danh mục')
    price = forms.IntegerField(label='Giá')

    def clean(self):
        super(AddItemForm, self).clean()

        price = self.cleaned_data['price']

        if float(price) < 0:
            self._errors['price'] = self.error_class(['Giá không thể nhỏ hơn 0'])
        return self.cleaned_data
    
class AddCategoryForm(forms.Form):
    name = forms.CharField(required=True, label='Tên danh mục')