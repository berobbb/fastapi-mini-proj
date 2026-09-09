from datetime import date
class Event:
    id: int
    title: str
    event_date: date
    organizer: str
    city: str
    email: str
    def __init__(self, id, title, date, organizer, city, email):
        self.id = id
        self.title = title
        self.event_date = date
        self.organizer = organizer
        self.city = city
        self.email = email
