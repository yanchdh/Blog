# -*- coding:utf-8 -*-
import copy

class RoleInfo(object):
    name2id = {}
    id2RoleInfo = {}
    ID = 1
    def __init__(self, name, x, y, x_size, y_size):
        self.name = name
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.id = RoleInfo.name2id.get(name)
        if not self.id:
            self.id = RoleInfo.ID
            RoleInfo.name2id[name] = RoleInfo.ID
            RoleInfo.id2RoleInfo[RoleInfo.ID] = self
            RoleInfo.ID += 1
    
    @staticmethod
    def getRoleInfoById(id):
        return RoleInfo.id2RoleInfo.get(id)
    
    @staticmethod
    def printBoard(board, row, col):
        s = []
        for i in range(row):
            for j in range(col):
                roleInfo = RoleInfo.getRoleInfoById(board[i * col + j])
                if roleInfo:
                    s.append(roleInfo.name + ' ')
                else:
                    s.append(u'空空' + ' ')
            s.append('\n')
        print(''.join(s))
    
    @staticmethod    
    def convertRoleInfosToBoard(roleInfos, row, col):
        board = [0 for i in range(row * col)]
        for roleInfo in roleInfos:
            for i in range(roleInfo.x, roleInfo.x + roleInfo.x_size):
                for j in range(roleInfo.y, roleInfo.y + roleInfo.y_size):
                    if i < 0 or j < 0 or i >= row or j >= col or board[i * col + j] != 0:
                        return None
                    board[i * col + j] = roleInfo.id
        return board
    
    @staticmethod
    def convertBoardToRoleInfos(board, row, col):
        temp_board = copy.deepcopy(board)
        roleInfos = []
        for i in range(row):
            for j in range(col):
                roleInfo = RoleInfo.getRoleInfoById(temp_board[i * col + j])
                if not roleInfo:
                    continue
                for x in range(i, i + roleInfo.x_size):
                    for y in range(j, j + roleInfo.y_size):
                        temp_board[x * col + y] = 0
                roleInfos.append(RoleInfo(roleInfo.name, i, j, roleInfo.x_size, roleInfo.y_size))
        return roleInfos
            
class PathNode(object):
    def __init__(self, board, self_idx, parent_idx, step, name, x, y, dir):
        self.board = board
        self.self_idx = self_idx
        self.parent_idx = parent_idx
        self.step = step
        self.name = name
        self.x = x
        self.y = y
        self.dir = dir
    
class Solution(object):
    def __init__(self):
        self.n = 10
        
    def solveHuarongRoad(self, roleInfos, row, col, target_name, target_x, target_y):
        dirs = [ [0,1,u'右'], [1,0,u'下'], [0,-1,u'左'], [-1,0,u'上'] ]
        cur_boards, nxt_boards, path, dict_board = [], [], [], {}
        board = RoleInfo.convertRoleInfosToBoard(roleInfos, row, col)
        node = PathNode(board, 0, -1, 0, '', -1, -1, [])
        path.append(node)
        cur_boards.append(node)
        str_board = ''.join(map(str, board))
        dict_board[str_board] = 1
        while cur_boards:
            while cur_boards:
                cur_node = cur_boards.pop()
                cur_roleInfos = RoleInfo.convertBoardToRoleInfos(cur_node.board, row, col)
                for roleInfo in cur_roleInfos:
                    old_x, old_y = roleInfo.x, roleInfo.y
                    for dir in dirs:
                        new_x, new_y = old_x + dir[0], old_y + dir[1]
                        x_max, y_max = new_x + roleInfo.x_size, new_y + roleInfo.y_size
                        if new_x < 0 or new_y < 0 or x_max > row or y_max > col:
                            continue
                        roleInfo.x, roleInfo.y = new_x, new_y
                        new_board = RoleInfo.convertRoleInfosToBoard(cur_roleInfos, row, col)
                        if not new_board:
                            continue
                        str_board = ''.join(map(str, new_board))
                        if dict_board.get(str_board) is None:
                            new_node = PathNode(new_board, len(path), cur_node.self_idx, cur_node.step + 1, roleInfo.name, old_x, old_y, dir)
                            path.append(new_node)
                            nxt_boards.append(new_node)
                            dict_board[str_board] = 1
                            if roleInfo.name == target_name and roleInfo.x == target_x and roleInfo.y == target_y:
                                print('step = ' + str(cur_node.step + 1))
                                self.printPath(path, new_node, row, col)
                                return
                    roleInfo.x, roleInfo.y = old_x, old_y
            cur_boards, nxt_boards = nxt_boards, []
                            
    def printPath(self, path, node, row, col):
        if not node or node.parent_idx == -1:
            return
        self.printPath(path, path[node.parent_idx], row, col)
        print node.name, node.x, node.y, node.dir[2]
        #RoleInfo.printBoard(node.board, row, col)
                    
if __name__ == "__main__":
    row = 5
    col = 4
    '''
        RoleInfo(u'张飞', 3, 0, 2, 1),
        RoleInfo(u'曹操', 0, 1, 2, 2),
        RoleInfo(u'马超', 3, 2, 2, 1),
        RoleInfo(u'黄忠', 3, 1, 2, 1),
        RoleInfo(u'关羽', 2, 1, 1, 2),
        RoleInfo(u'赵云', 2, 3, 2, 1),
        RoleInfo(u'卒卒', 0, 0, 1, 1),
        RoleInfo(u'卒卒', 1, 3, 1, 1),
        RoleInfo(u'卒卒', 2, 0, 1, 1),
        RoleInfo(u'卒卒', 0, 3, 1, 1)
    '''
    data = [
        RoleInfo(u'张飞', 0, 3, 2, 1),
        RoleInfo(u'曹操', 0, 1, 2, 2),
        RoleInfo(u'马超', 4, 1, 1, 2),
        RoleInfo(u'黄忠', 3, 1, 1, 2),
        RoleInfo(u'关羽', 2, 1, 1, 2),
        RoleInfo(u'赵云', 2, 3, 2, 1),
        RoleInfo(u'卒卒', 0, 0, 1, 1),
        RoleInfo(u'卒卒', 1, 0, 1, 1),
        RoleInfo(u'卒卒', 2, 0, 1, 1),
        RoleInfo(u'卒卒', 3, 0, 1, 1)
    ]
    target_name = u'曹操'
    target_x = 3
    target_y = 1
    s = Solution()
    s.solveHuarongRoad(data, row, col, target_name, target_x, target_y)