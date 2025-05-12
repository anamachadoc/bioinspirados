
class Item():
    def __init__(self, ID, weight, utility_value):
        self.ID = ID
        self.weight = weight
        self.utility_value = utility_value

    def get_ID(self):
        return self.ID
    
    def get_weight(self):
        return self.weight
    
    def get_utility_value(self):
        return self.utility_value
    
    def get_item(self):
        print(f'ITEM: {self.get_ID()}')
        print(f'weight: {self.get_weight()} - utility: {self.get_utility_value()}')
        print()
