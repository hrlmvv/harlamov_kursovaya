from django import forms
from django.contrib.auth.models import User
from .models import Profile, Article, News

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        if commit:
            profile.user.save()
            profile.save()
        return profile


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'precontent', 'content', 'image', 'category']

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(ArticleForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ArticleForm, self).save(commit=False)
        if self.author:
            instance.author = self.author
        if commit:
            instance.save()
        return instance


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'precontent', 'content', 'image', 'category']

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(NewsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(NewsForm, self).save(commit=False)
        if self.author:
            instance.author = self.author
        if commit:
            instance.save()
        return instance
