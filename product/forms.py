from django import forms
from django.utils.translation import ugettext_lazy as _
from product.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {'content': _('Comment')}
        help_texts = {'content': _('Enter your comment')}
        widgets = {'content': forms.Textarea(attrs={'class': 'myfieldclass', 'placeholder': 'Enter your comment...'}), }
