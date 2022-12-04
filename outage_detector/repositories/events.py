

class EventRepository:
    """
    Manage monitor events in the database
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory

