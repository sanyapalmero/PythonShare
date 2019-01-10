from django import forms


class CodeForm(forms.Form):
    textfield = forms.CharField()
    topic = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        topic = self.data.get('topic')
        textfield = self.data.get('textfield')
        return cleaned_data


class AddCommentForm(forms.Form):
    comment = forms.CharField()

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if comment:
            return comment
