from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **inikwargs):
        # 调用父类的的as_view
        view = super(LoginRequiredMixin, cls).as_view(**inikwargs)
        return login_required(view)
