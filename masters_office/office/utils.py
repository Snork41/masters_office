class Ttest:
    def __init__(self, *args, **kwargs):
        self.args = args

    def s(self):
        print(self.args)


t = Ttest('yyyy', 12)

t.s()