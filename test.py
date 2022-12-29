

pt = ['a','b','c']
class Types():
    def __init__(self):
        self.data = []
        for i in pt:
            self.data.append(i)
    def aslist(self):
        return self.data
    def __iter__(self):
        return iter(self.aslist())


g=Types()
for i in g:
    print(i)