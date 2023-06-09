class UserModel:
    def __init__(self, name:str, email:str, username:str, password:str, phoneNumber:str, address:str):
        super().__init__(name, email, username, password, phoneNumber, address)
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.phoneNumber = phoneNumber
        self.address = address

    def __repr__(self):
        return f"UserModel(name= {self.name}, email={self.email}, username={self.username}, password={self.password})"