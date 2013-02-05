from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    """ A form for creating new users. Includes all the
        required fields, plus a repeated password
    """
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'screen_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Password don't match!"
            raise forms.ValidationError(msg)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """ A form for the updating users. Includes all the fields
    on the user, but replaces the password field with admin's
    password hash display field
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User

    def clean_password(self):
        # Regardless of what provided return the initial value
        # Done here rather on the field, because the field does not
        # have access to the initial value
        return self.initial["password"]


class CoreUserAdmin(UserAdmin):
    # Set the add/modify forms
    add_form = UserCreationForm
    form = UserChangeForm

    # The fields to be used in displaying the User model.
    list_display = ('email', 'is_staff', 'screen_name', 'created', 'modified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'screen_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('screen_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'screen_name', 'password1', 'password2')}
        ),
    )

admin.site.register(User, CoreUserAdmin)
