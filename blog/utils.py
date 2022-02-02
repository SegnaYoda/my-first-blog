class MyMixin(object):
    mixin_prop = ''     #свойство, которое позже будем менять

    def get_prop(self):
        return self.mixin_prop.upper()

    def get_upper(self, s):
        if isinstance(s, str):
            return s.upper()
        else:
            return s.title.upper()