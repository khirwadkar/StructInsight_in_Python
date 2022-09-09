class Member(object):
    def __init__(self, type, id):
        self.type = type    # beam, column, truss_member, etc.
        self.id = id

    def __str__(self):
        return self.type + " " + str(self.id)


