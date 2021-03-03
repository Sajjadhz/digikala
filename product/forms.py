from django import forms
from django.utils.translation import ugettext_lazy as _
from product.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {'content': _('افزودن دیدگاه')}
        help_texts = {'content': _('Enter your comment')}
        widgets = {'content': forms.Textarea(attrs={'class': 'myfieldclass', 'placeholder': 'دیدگاه خود را به اشتراک بگذارید'}), }


# class FilterForm(forms.Form):
#     email = forms.CheckboxSelectMultiple(label=_('ایمیل'), required=True, help_text=_('ایمیلتون رو وارد کنید'),
#                              widget=forms.CheckboxSelectMultiple())
#     last_name = forms.CharField(label=_('نام خانوادگی'), widget=forms.TextInput(
#         attrs={"placeholder": "Password", "class": "no-background border-secondary rounded"}))