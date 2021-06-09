from django import forms
from app01 import models


# 注册功能
class Reg_forms(forms.Form):
    username = forms.CharField(label='用户名', max_length=8, min_length=3, error_messages={
        'required':'用户名不能为空',
        'max_length':'用户名最多八位',
        'min_length':'用户名最少三位'
    },widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码', max_length=8, min_length=3, error_messages={
        'required':'密码不能为空',
        'max_length':'密码最多八位',
        'min_length':'密码最少三位'
    },widget=forms.widgets.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(label='确认密码', max_length=8, min_length=3, error_messages={
        'required':'确认密码不能为空',
        'max_length':'确认密码最多八位',
        'min_length':'确认密码最少三位'
    },widget=forms.widgets.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='邮箱', error_messages={
        'required':'邮箱不能为空',
        'invalid':'邮箱格式不正确'
    },widget=forms.widgets.EmailInput(attrs={'class':'form-control'}))
    # 局部钩子
    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exist = models.Userinfo.objects.filter(username=username)
        if is_exist:
            self.add_error('username', '用户名已存在')
        return username

    # 全局钩子
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not password == confirm_password:
            self.add_error('confirm_password', '两次输入的密码不一致')
        return self.cleaned_data



