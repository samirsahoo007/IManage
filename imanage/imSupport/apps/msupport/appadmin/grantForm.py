from django import forms
　
　
class grantForm(forms.Form):
    userName = forms.CharField()
    template_name = "msupport/appadmin_grant.html"
　
    def clean_userName(self):
        data = self.cleaned_data['userName']
        if len(data) < 8:
            raise forms.ValidationError("This doesn't appear to be a valid username, which is usually 8 characters long.")
        elif data.index(" ") > 0:
            raise forms.ValidationError("This doesn't appear to be a valid username, which do not contain spaces.")
        return data
