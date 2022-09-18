from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class OnlyEmployerMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_employer

    def handle_no_permission(self):
        return redirect('top:index')

