from django import forms

from apps.admin_panel.forms.users.user_base_form import BaseAdminUserForm


class AdminUserUpdateForm(BaseAdminUserForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank to keep the current password."
    )

    class Meta(BaseAdminUserForm.Meta):
        fields = BaseAdminUserForm.Meta.fields + ['username', 'password',]
