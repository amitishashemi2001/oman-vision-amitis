from django.contrib import admin
from .models import User
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from config.helpers import check_soft_deleted_user_exists
from django.core.exceptions import ValidationError


# Register your models here.

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='پسورد', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار پسورد', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = "__all__"

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("پسورد ها یکسان نیستند")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        company_email = cleaned_data.get('company_email')
        username = cleaned_data.get('username')
        result = check_soft_deleted_user_exists(email, company_email, username)
        if result:
            raise ValidationError('کاربری با این ایمیل، ایمیل شرکتی یا نام کاربری در دیتابیس وجود دارد')
        return cleaned_data
 
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label='پسورد')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        company_email = cleaned_data.get('company_email')
        username = cleaned_data.get('username')
        result = check_soft_deleted_user_exists(email, company_email, username)
        if result:
            raise ValidationError('کاربری با این ایمیل، ایمیل شرکتی یا نام کاربری در دیتابیس وجود دارد')

        return cleaned_data

    class Meta:
        model = User
        fields = "__all__"

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
    list_display = ('email', 'birthday', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        ('Personal information', {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'email', 'birthday',
                                             'company_email', 'sex', 'profile_image')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Password', {'fields': ('password',)})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Personal information', {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'email', 'birthday',
                                             'company_email', 'sex', 'profile_image')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Password', {'fields': ('password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
