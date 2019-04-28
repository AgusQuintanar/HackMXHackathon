class node:
    def _init_(self, data):
        self.data = data
        self.left =  None
        self.right = None

    def insert(self, data):
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def findval(self, val):
        if val < self.data:
            if self.left is None:
                return str(val)+" Not Found"
            return self.left.findval(val)
        elif val > self.data:
            if self.right is None:
                return str(val)+" Not Found"
            return self.right.findval(val)
        else:
            print(str(self.data) + ' is found')

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.data),
        if self.right:
            self.right.PrintTree()

root = node(12)
root.insert(6)
root.insert(14)
root.insert(3)
print(root.findval(7))
print(root.findval(14))