class dynamicProgramming:
    def __init__(self, items, maximum):
        self.table = [[0 for _ in range(maximum)] for _ in range(len(items))]
        self.items = items
        self.maximum = maximum

    def DP(self):
        for i in range(len(self.table)):
            price, cost = self.items[i]
            for j in range(len(self.table[i])):
                if cost <= j+1:
                    if i == 0:
                        self.table[i][j] = price
                    else:
                        higher_price = price
                        if j-cost >= 0:
                            higher_price += self.table[i-1][j-cost]
                        '''
                        print(self.table[i-1][j], higher_price,
                              max(self.table[i-1][j], higher_price),
                              i, j)
                        '''
                        self.table[i][j] = max(self.table[i-1][j],
                                               higher_price)
                else:
                    self.table[i][j] = self.table[i-1][j]
            #print((price, cost), self.table)
        self.show()

    def show(self):
        for i in self.table:
            for j in i:
                print(f'{j:>4}', end=' ')
            print()
        print(self.table[-1][-1])

items = [(350, 3), (1000, 8), (500, 5), (200, 3), (300, 4)]
maximum = 10
dynamicProgramming(items, maximum).DP()
