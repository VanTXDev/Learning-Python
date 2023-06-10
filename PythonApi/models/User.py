class UserModel():
    def __init__(self, name:str, email:str = None, username:str = None, password:str = None, phoneNumber:str = None, address:str = None):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.phoneNumber = phoneNumber
        self.address = address

    def __repr__(self):
        return f"UserModel(name= {self.name}, email={self.email}, username={self.username}, password={self.password})"