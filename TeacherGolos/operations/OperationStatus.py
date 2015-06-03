__author__ = 'kole0114'


class OperationStatus(object):

    def __init__(self,token,**extra):
        self.token=token
        if 'redirect' in extra:
            self.redirect=extra['redirect']
        else:
            self.redirect=None

        if 'status' in extra:
            self.status=extra['status']
        else:
            self.status=True

        if 'render' in extra:
            self.render=extra['render']
        else:
            self.render=None

    def need_redirect(self):
        if self.redirect is not None and self.redirect is not '':
            return True
        else:
            return False

    def need_render(self):
        if self.render is not None and self.redirect is not '':
            return True
        else:
            return False

    def ok(self):
        return self.status is not None and self.status is not '' and self.status is not False

    def finish(self):
        return self.status is not None and self.token is not None and self.token.state=='finish'