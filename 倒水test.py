import copy
import collections

class PourWater:
    def __init__(self, *buckets, target):
        self.buckets = tuple(buckets)
        self.target = target
        self.back = set()
        self.step = collections.deque()
        self.path = dict()

    def get_next_states(self, water):
        next_states = []
        for idx, bucket in enumerate(self.buckets):
            next_states.append(water[:idx]+(bucket,)+water[idx+1:])
            next_states.append(water[:idx]+(0,)+water[idx+1:])
            for i, b in enumerate(self.buckets):
                if i != idx:
                    pour = min(water[idx], b-water[i])
                    if i < idx:
                        next_states.append(water[:i]+(water[i]+pour,)+
                            water[i+1:idx]+(water[idx]-pour,)+water[idx+1:])
                    else:
                        next_states.append(water[:idx]+(water[idx]-pour,)+
                            water[idx+1:i]+(water[i]+pour,)+water[i+1:])

        return next_states

    def bfs(self):
        start = tuple([0 for i in range(len(self.buckets))])
        self.back.add(start)
        self.step.append(start)
        self.path[start] = None

        while self.step:
            cur = self.step.popleft()

            if self.target in cur:
                print('Find a solution!')
                self.print_solution(cur)
                return True

            for state in self.get_next_states(cur):
                if state not in self.back:
                    #print(state, end=' ')
                    self.back.add(state)
                    self.step.append(state)
                    self.path[state] = cur
                    if self.target in state:
                        #print('')
                        print('Find a solution!')
                        self.print_solution(state)
                        return True
            #print('')
            #print(self.step)

        print('Fail to solve')
        return False

    def print_solution(self, final):
        steps = []
        cur = final

        while cur is not None:
            steps.append(cur)
            cur = self.path[cur]

        steps.reverse()

        print(f'{len(steps)-1} steps')
        for i, state in enumerate(steps, 0):
            print(f'Step {i}: {state}')

PourWater(*[100, 103, 10086], target=10085).bfs()
