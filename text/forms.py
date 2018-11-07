from django import forms


class TextForm(forms.Form):
    textfield = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'height:200px'
        }),
        max_length=100)

class AddCommentForm(forms.Form):
    comment = forms.CharField()

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if comment:
            return comment