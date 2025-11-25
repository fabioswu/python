import copy
from collections import deque

class PourWater:
    def __init__(self, bucket1, bucket2, target):
        self.buckets = (bucket1, bucket2)
        self.target = target
        self.visited = set()  # 使用集合而不是列表来存储访问过的状态，提高查找效率
        self.queue = deque()  # 使用队列而不是列表来进行BFS
        self.path = {}  # 记录路径，用于最终输出解决方案
        
    def get_next_states(self, current):
        """获取从当前状态可以到达的所有下一个状态"""
        a, b = current
        capacity_a, capacity_b = self.buckets
        next_states = []
        
        # 1. 填满第一个桶
        next_states.append((capacity_a, b))
        
        # 2. 填满第二个桶
        next_states.append((a, capacity_b))
        
        # 3. 倒空第一个桶
        next_states.append((0, b))
        
        # 4. 倒空第二个桶
        next_states.append((a, 0))
        
        # 5. 从第一个桶倒到第二个桶
        pour_amount = min(a, capacity_b - b)
        next_states.append((a - pour_amount, b + pour_amount))
        
        # 6. 从第二个桶倒到第一个桶
        pour_amount = min(b, capacity_a - a)
        next_states.append((a + pour_amount, b - pour_amount))
        
        return next_states
    
    def bfs(self):
        """使用BFS算法寻找解决方案"""
        start = (0, 0)
        self.visited.add(start)
        self.queue.append(start)
        self.path[start] = None  # 起始状态没有前驱
        
        while self.queue:
            current = self.queue.popleft()
            
            # 检查是否找到目标
            if self.target in current:
                print("找到解决方案!")
                self.print_solution(current)
                return True
            
            # 生成所有可能的下一个状态
            for next_state in self.get_next_states(current):
                if next_state not in self.visited:
                    self.visited.add(next_state)
                    self.queue.append(next_state)
                    self.path[next_state] = current  # 记录路径
        
        print("无法找到解决方案")
        return False
    
    def print_solution(self, final_state):
        """打印解决方案的步骤"""
        steps = []
        current = final_state
        
        # 回溯路径
        while current is not None:
            steps.append(current)
            current = self.path[current]
        
        # 反转步骤顺序（从开始到结束）
        steps.reverse()
        
        print(f"需要 {len(steps)-1} 步:")
        for i, state in enumerate(steps):
            if i == 0:
                print(f"步骤 {i}: 初始状态 {state}")
            else:
                prev_state = steps[i-1]
                action = self.get_action_description(prev_state, state)
                print(f"步骤 {i}: {action} -> 当前状态 {state}")
    
    def get_action_description(self, prev, current):
        """获取动作描述"""
        prev_a, prev_b = prev
        curr_a, curr_b = current
        
        if prev_a == 0 and curr_a == self.buckets[0]:
            return f"填满第一个桶 ({self.buckets[0]}L)"
        elif prev_b == 0 and curr_b == self.buckets[1]:
            return f"填满第二个桶 ({self.buckets[1]}L)"
        elif prev_a > 0 and curr_a == 0:
            return "倒空第一个桶"
        elif prev_b > 0 and curr_b == 0:
            return "倒空第二个桶"
        elif prev_a > curr_a:  # 从第一个桶倒到第二个桶
            amount = prev_a - curr_a
            return f"从第一个桶倒 {amount}L 到第二个桶"
        else:  # 从第二个桶倒到第一个桶
            amount = prev_b - curr_b
            return f"从第二个桶倒 {amount}L 到第一个桶"

# 测试
if __name__ == "__main__":
    solver = PourWater(7, 10, 5)
    solver.bfs()
