from django import forms


class CodeForm(forms.Form):
    codefield = forms.CharField()
    topic = forms.CharField()
    tags = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        topic = self.data.get('topic')
        codefield = self.data.get('codefield')
        tags = self.data.get('tags')
        return cleaned_data


class AddCommentForm(forms.Form):
    comment = forms.CharField()

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if comment:
            return comment
