import copy
import time
goal_state = [[i for i in range((j-1)*4+1, j*4+1)] for j in range(1, 5)]


def h(state):
    loss = 0
    for row in range(4):
        for col in range(4):
            if state[row][col] == 16:
                continue
            goal_row = (state[row][col]-1) // 4
            goal_col = (state[row][col]-1) % 4
            loss += abs(row - goal_row)
            loss += abs(col - goal_col)
    return loss


def cost(node, succ):
    return 1


def is_goal(state):
    global goal_state
    return state == goal_state


def successors(state):
    for row in range(4):
        for col in range(4):
            if state[row][col] == 16:
                index_blank = [row, col]

    row, col = index_blank
    succ = {'move_node': [],  'index': [], 'direction': []}
    if row - 1 >= 0:

        succ['move_node'].append(state[row-1][col])
        succ['index'].append([row - 1, col])
        succ['direction'].append('up')
    if row + 1 <= 3:
        succ['move_node'].append(state[row+1][col])
        succ['index'].append([row + 1, col])
        succ['direction'].append('down')
    if col - 1 >= 0:
        succ['move_node'].append(state[row][col-1])
        succ['index'].append([row, col - 1])
        succ['direction'].append('left')
    if col + 1 <= 3:
        succ['move_node'].append(state[row][col+1])
        succ['index'].append([row, col + 1])
        succ['direction'].append('right')
    return [succ, index_blank]


def search(path, g, bound, move_step):
    now_state = path[-1]

    f = g + h(now_state)
    if f > bound:
        return f
    if is_goal(now_state):
        return 'FOUND'

    min = float('inf')
    successor, (blank_row, blank_col) = successors(now_state)
    successor_node, successor_index = successor['move_node'], successor['index']
    for succ in range(len(successor_node)):
        new_blank_row, new_blank_col = successor_index[succ]
        new_state = copy.deepcopy(now_state)
        new_state[blank_row][blank_col] = successor_node[succ]
        new_state[new_blank_row][new_blank_col] = 16
        if new_state not in path:
            path.append(new_state)
            move_step.append(successor_node[succ])
            t = search(path, g + cost(now_state, succ), bound, move_step)
            if t == 'FOUND':
                return 'FOUND'
            if t < min:
                min = t
            path.pop()
            move_step.pop()
    return min


def ida_star(root):
    bound = h(root)
    path = [root]
    move_step = []

    while True:
        t = search(path, 0, bound, move_step)
        if t == 'FOUND':
            return [move_step, bound]
        elif t == float('inf'):
            return 'NOT_FOUND'
        bound = t
        print(bound)


def main():
    start_time = time.time()
    test = [[14, 10, 6, 16], [4, 9, 1, 8], [2, 3, 5, 11], [12, 13, 7, 15]]
    for i in test:
        print(i)
    move_step, total_step = ida_star(test)
    end_time = time.time()
    print('The sequence of move is show below:')
    print(move_step)
    print('Cost {} steps to achieve goal state'.format(total_step))
    print('Cost {} s to solve this problem'.format(end_time - start_time))



if __name__ == '__main__':
    main()