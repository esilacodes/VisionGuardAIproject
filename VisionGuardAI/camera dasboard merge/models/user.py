class User:
    def __init__(self,name,password):
        self.name= name
        self.password=password

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    def display(self):
        print(f"name: {self.name}  , password:  {self.password}" )    

    