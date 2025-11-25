import copy

class PourWater:
    def __init__(self, bucket1, bucket2, target):
        self.buckets = (bucket1, bucket2)
        self.target = target
        self.back = [[0, 0]]
        self.step = [[0, 0]]

    def bfs(self):
        while self.step:
            temp = []
            for i in self.step:
                a, b = i
                b1, b2 = self.buckets
                for j in [[b1]+[b],
                    [a]+[b2],
                    [0]+[b],
                    [a]+[0],
                    [max(0, a+b-b2)]+[min(sum(i), b2)],
                    [min(sum(i), b1)]+[max(0, a+b-b1)]
                         ]:
                    if j not in self.back:
                        self.back.append(j)
                        if j not in temp:
                            temp.append(j)
            print(temp)
            self.step = copy.deepcopy(temp)
            for i in self.back:
                if self.target in i:
                    print('Find a solution')
                    return
        print('Fail')
                        

PourWater(7, 10, 5).bfs()
