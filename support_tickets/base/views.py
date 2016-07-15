# -*- coding: utf-8 -*-
from braces.views import UserPassesTestMixin


class AuthorPermissionTestMixin(UserPassesTestMixin):
    raise_exception = True
    redirect_unauthenticated_users = True

    def test_func(self, user):
        the_object = self.get_object()

        return user == the_object.author
