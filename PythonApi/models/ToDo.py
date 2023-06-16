class ToDoModel():
    def __init__(self, title:str, description:str = None, is_completed:bool = False, creator:str = None, date_created:str = None):
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.creator = creator
        self.date_created = date_created

    def __repr__(self):
        return f"Todo Model: (title= {self.title}, description={self.description}, is_completed={self.is_completed}, creator={self.creator})"