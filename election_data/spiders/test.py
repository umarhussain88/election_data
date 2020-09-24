

class Test():

    def __init__(self,data):
        self.data = data

    @classmethod
    def check_index(cls,item):
        try:
            return item
        except:
            return ''

    
    def parse_list(self):
        {'data' : 'data',
        'item' : self.check_index(item=self.data[2])}


# i = Test([0])

# i.parse_list()

# def check_index(item):
data = [0,1]
try:
    print(data[3])
except:
    print('')

