from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Client, CurrentAccount, Movement


class UserCreationForm(forms.ModelForm):
    """
    Form to create an User.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ('email', 'first_name', 'last_name', 'phone')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Client
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ClientAdmin(BaseUserAdmin):
    # The forms to add and change client instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the Client model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {
            'fields': (('is_active', 'is_admin', 'is_staff'),)}),
        ('Important dates', {
            'classes': ('collapse',),
            'fields': ('created_time', 'updated_time', 'last_login')
        }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('is_active',)

    def get_readonly_fields(self, request, obj=None):

        if obj and request.user.is_admin:
            read_only = ('created_time', 'updated_time', 'last_login')
            return read_only

        return super(ClientAdmin, self).get_readonly_fields(request, obj=None)


class MovementInline(admin.StackedInline):
    model = Movement
    readonly_fields = ('created',)


class CurrentAccountAdmin(admin.ModelAdmin):

    list_display = ('id', 'client')
    search_fields = ('id',)

    inlines = [MovementInline, ]


admin.site.register(Client, ClientAdmin)
admin.site.register(CurrentAccount, CurrentAccountAdmin)
admin.site.unregister(Group)
