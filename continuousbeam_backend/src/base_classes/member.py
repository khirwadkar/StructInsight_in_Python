class Member(object):
    """ Superclass to identify any structural member.

        The member can be a beam in a continuous beam,
        beam or column in a plane frame,
        member of a truss, a space frame, or a grid. 
    """

    def __init__(self, type, id):
        self.type = type    # beam, column, truss_member, etc.
        self.id = id

    def __str__(self):
        return self.type + " " + str(self.id)


