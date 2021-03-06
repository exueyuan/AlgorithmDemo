import copy


class Solution:
    # 上，右，下，左
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def checkIsValidStep(self, maze, x, y, dp_already = None):
        """
        验证 x，y点在maze上是不是有效的
        :param dp_already:
        :param maze: 地图
        :param x:
        :param y:
        :return: 是否有效，人是否可以站在这里
        """
        if x < 0 or x >= len(maze):
            return False
        if y < 0 or y >= len(maze[0]):
            return False
        if maze[x][y] == "#":
            return False
        if dp_already and dp_already[x][y] == 1:
            return False
        return True
    def minStepFromStartToTargetList(self, maze, startTuple, targetTupleList):
        """
        检测从start到各个target的最短步数
        :param maze:
        :param startTuple:
        :param stargetTupleList:
        :return: [5, 3, 8]
        """
        m = len(maze)
        n = len(maze[0])
        dp = [[-1] * n for _ in range(m)]
        dp_already = [[0] * n for _ in range(m)]
        currentDistance = 0
        dp[startTuple[0]][startTuple[1]] = 0
        dp_already[startTuple[0]][startTuple[1]] = 1
        alreadyHaveDistancePositionList = [startTuple]
        targetDistanceList = [-1]*len(targetTupleList)

        while alreadyHaveDistancePositionList:
            alreadyHaveDistancePositionListCopy = []
            alreadyHaveDistancePositionListCopy.extend(alreadyHaveDistancePositionList)
            alreadyHaveDistancePositionList.clear()
            currentDistance += 1
            for position in alreadyHaveDistancePositionListCopy:
                for dir in Solution.dirs:
                    new_position = position[0] + dir[0], position[1] + dir[1]
                    if self.checkIsValidStep(maze, new_position[0], new_position[1], dp_already):
                        dp[new_position[0]][new_position[1]] = currentDistance
                        dp_already[new_position[0]][new_position[1]] = 1
                        if new_position in targetTupleList:
                            index = targetTupleList.index(new_position)
                            if targetDistanceList[index] < 0:
                                targetDistanceList[index] = currentDistance
                        alreadyHaveDistancePositionList.append(new_position)
        return targetDistanceList

    def minStepFromStartToTarget(self, maze, startTuple, targetTuple):
        """
        检测从start 到 target的最短路径步数
        :param maze 地图 ["S#O", "M..", "M.T"]
        :param startTuple: X的起始点坐标 (0, 1)
        :param targetTuple: Y的目标点坐标 (3, 4)
        :return: 5
        """
        m = len(maze)
        n = len(maze[0])
        dp = [[-1] * n for _ in range(m)]
        dp_already = [[0] * n for _ in range(m)]
        currentDistance = 0
        dp[startTuple[0]][startTuple[1]] = 0
        dp_already[startTuple[0]][startTuple[1]] = 1
        alreadyHaveDistancePositionList = [startTuple]

        while alreadyHaveDistancePositionList:
            alreadyHaveDistancePositionListCopy = []
            alreadyHaveDistancePositionListCopy.extend(alreadyHaveDistancePositionList)
            alreadyHaveDistancePositionList.clear()
            currentDistance += 1
            for position in alreadyHaveDistancePositionListCopy:
                for dir in Solution.dirs:
                    new_position = position[0] + dir[0], position[1] + dir[1]
                    if self.checkIsValidStep(maze, new_position[0], new_position[1], dp_already):
                        dp[new_position[0]][new_position[1]] = currentDistance
                        dp_already[new_position[0]][new_position[1]] = 1
                        if new_position == targetTuple:
                            return currentDistance
                        alreadyHaveDistancePositionList.append(new_position)
        return -1

    def getSimplifyDistanceDict(self, distanceDict, start_position, target_position, stone_position_list, gear_position_list):
        simplifyDistanceDict = {}
        # 先算起始点到所有机关点的距离
        for stone_position in stone_position_list:
            for gear_position in gear_position_list:
                distance1 = distanceDict[(start_position, stone_position)]
                distance2 = distanceDict[(gear_position, stone_position)]
                if distance1 >= 0 and distance2 >= 0:
                    distance = simplifyDistanceDict.get((start_position, gear_position), -1)
                    sumDistance = distance1 + distance2
                    if sumDistance <= distance or distance == -1:
                        simplifyDistanceDict[(start_position, gear_position)] = sumDistance
                else:
                    if simplifyDistanceDict.get((start_position, gear_position),None) is None:
                        simplifyDistanceDict[(start_position, gear_position)] = -1
        # 计算所有机关点到机关点的距离
        for gear_position_1 in gear_position_list:
            for gear_position_2 in gear_position_list:
                for stone_position in stone_position_list:
                    if gear_position_1 == gear_position_2:
                        break
                    distance1 = distanceDict[(gear_position_1, stone_position)]
                    distance2 = distanceDict[(gear_position_2, stone_position)]
                    if distance1 >= 0 and distance2 >= 0:
                        distance = simplifyDistanceDict.get((gear_position_1, gear_position_2), -1)
                        sumDistance = distance1 + distance2
                        if sumDistance <= distance or distance == -1:
                            simplifyDistanceDict[(gear_position_1, gear_position_2)] = sumDistance
                    else:
                        if simplifyDistanceDict.get((gear_position_1, gear_position_2),None) is None:
                            simplifyDistanceDict[(gear_position_1, gear_position_2)] = -1
        # 计算所有机关点到终点的距离
        for gear_position in gear_position_list:
            simplifyDistanceDict[(gear_position, target_position)] = distanceDict[(gear_position, target_position)]
        return simplifyDistanceDict

    def getDistanceDict(self, maze, start_position, target_position, stone_position_list, gear_position_list):
        distanceDict = {}
        # 首先起始点到终点的距离
        distanceDict[(start_position, target_position)] = self.minStepFromStartToTarget(maze, start_position, target_position)
        # 计算起始点到每个石堆的距离
        distanceList = self.minStepFromStartToTargetList(maze, start_position, stone_position_list)
        for i, stone_position in enumerate(stone_position_list):
            distanceDict[(start_position, stone_position)] = distanceList[i]
        # 计算所有石堆到M的距离
        for stone_position in stone_position_list:
            distanceList = self.minStepFromStartToTargetList(maze, stone_position, gear_position_list)
            for i, gear_position in enumerate(gear_position_list):
                distanceDict[(gear_position, stone_position)] = distanceList[i]
        # 计算所有M到target的距离
        distanceList = self.minStepFromStartToTargetList(maze, target_position, gear_position_list)
        for i, gear_position in enumerate(gear_position_list):
            distanceDict[(gear_position, target_position)] = distanceList[i]
        return distanceDict

    def getMinimalStepsFromAToBRoutC(self, startPosition, targetPosition, routPositionList:list, simplifyDistanceDict):
        print(routPositionList)
        if not routPositionList:
            return simplifyDistanceDict[startPosition, targetPosition]

        m = len(routPositionList)
        dp = [[-1] * m for _ in range(1 << m)]

        for i in range(m):
            dp[1 << i][i] = simplifyDistanceDict[startPosition, routPositionList[i]]


        for s in range(1 << m):
            for j in range(m):
                if s & (1 << j) == 0: continue
                for k in range(m):
                    if s & (1 << k) != 0: continue
                    ns = s | (1 << k)
                    routPosition1 = routPositionList[j]
                    routPosition2 = routPositionList[k]
                    distance = simplifyDistanceDict[(routPosition1,routPosition2)]
                    if distance >= 0 and dp[s][j] >=0:
                        addNum = distance + dp[s][j]
                        if dp[ns][k] < 0:
                            dp[ns][k] = addNum
                        else:
                            dp[ns][k] = min(dp[ns][k], addNum)
        # print(dp)
        stateList = dp[-1]
        miniStep = -1
        for i, step1 in enumerate(stateList):
            if step1 >= 0:
                position1 = routPositionList[i]
                step2 = simplifyDistanceDict[(position1, targetPosition)]
                if step2 >= 0:
                    if miniStep == -1:
                        miniStep = step1 + step2
                    else:
                        miniStep = min(miniStep, step1+step2)
        return miniStep


    def minimalSteps(self, maze: list) -> int:
        """
        :param maze: ["S#O", "M..", "M.T"]
        :return:
        """
        start_position = None
        target_position = None
        stone_position_list = []
        gear_position_list = []
        for i, line in enumerate(maze):
            for j, item_str in enumerate(line):
                if item_str == "S":
                    start_position = (i, j)
                elif item_str == "T":
                    target_position = (i, j)
                elif item_str == "O":
                    stone_position_list.append((i, j))
                elif item_str == "M":
                    gear_position_list.append((i, j))
        distanceDict = self.getDistanceDict(maze, start_position, target_position, stone_position_list, gear_position_list)

        # print(distanceDict)

        if not gear_position_list:
            return distanceDict[(start_position, target_position)]

        simplifyDistanceDict = self.getSimplifyDistanceDict(distanceDict, start_position, target_position, stone_position_list, gear_position_list)
        print(simplifyDistanceDict)
        return self.getMinimalStepsFromAToBRoutC(start_position, target_position, gear_position_list, simplifyDistanceDict)





solution = Solution()
# print(solution.minimalSteps(
#     ["......",
#      "M....M",
#      ".M#...",
#      "....M.",
#      "##.TM.",
#      "...O..",
#      ".S##O.",
#      "M#..M.",
#      "#....."]))
# print(solution.minimalSteps(
#     ["M...M",
#      "MS#MM",
#      "MM#TO"]))
# print(solution.minimalSteps(
#     [".#....M#.M",
#      "#.O...#O#O",
#      ".##..##..#",
#      "...#O#.M.#",
#      "..S#..OO..",
#      "#..T#M.###",
#      ".O.....#.#",
#      "...O..##..",
#      ".....O.#.M",
#      "...#......"]
# ))
# print(solution.minimalSteps(
#     ["S#O", "M..", "M.T"]
# ))
# print(solution.minimalSteps(
#     ["TMM",
#      "..M",
#      "OOS",
#      "#O.",
#      ".#O",
#      "O##"]
# ))
# print(solution.minimalSteps(
#     ["S#O",
#      "M.#",
#      "M.T"]
# ))


# a = tuple({(3, 2), (5, 7)})
# print(a)
# b = tuple({(5, 7), (3, 2)})
# print(a == b)
#
# c = {a:"8"}
aaa = ["...#............#.....#.#.#...###...................#....#.........#...##........#..................",  "...O......##..............#......#.........#...........#...#....#.........#.........................","..#.#.........#....#........##..............#...................#........O.#...#.........#....#.....",".....#......#..#.#..#........##...........#.....#..................#........#....#..#...............",".#........................#...#...#..#..................................#........#.....#............",".........##......#........##.......#....................#..........O...........#.#.#......#........#","......#....#.......#.......#..#..................#.#............#............#..............#.......","............#..#......#.........#........#......#......#....#.............................#.........","#.#.##....................#...................................#...............#..#..#............#..","..................................................##.#........#...#..................#......#O.....#","#.............M................#..#.......................##.....#..........#..............#.#......","O....#.....#............#...##..........#.......#......#...................#........#...............","O.........................#.#....#..#............................#..........#.......#..........#....",".....O.........#.#..........#..........#.................#........##............#....#.......#......","#......#....#..............#....#............#............#.#.#....#................................","............##..#.....................#.......##..#.#.#........................................#....","...........#.......#...#..#............##..#.........#..#..#..#.........#..#.....#...........##.....","........#......#..#.#...O.....#....#....#............#..........#......#.....................#......","..#.....#..........#....##.#.....................#.#............##...#........##..........#O...#....","........#....#.#..........#..#..................................#..#....#...#.....#.....#.........#.",".#.........#.....................#..#.....#............#.....#.#.........#.......................#..",".....#............................#......##....#....................................#.#........#..#.",".#....#.#.........#............#.......................#.......................#.........#......#...",".......#..........#......................#..#..........#......O.......#..#....#...........O.........",".#O........M....#.##......O.....#......#.#..#...........#..#...#..#..............................#..","....................O...M..........#..........#...#.........#.............#...........#.#...........","#...#.#.....#........#......#.....#...........#...............#.##.....................#..#.........",".....#................#...................##.......#..#.............##...#..#.......................",".....##..........................##............#.............#..........#.#..................#......",".#.....................##.#......#.#.#..........#.#....#................#........#......#...#...#..#",".........#..........#.........O..............#.....M.................#.....#....#...................","...........#......#......##..........#....#.....#..........M...........#....#....##.......#.........","##...................................................#.....#.......##.#.............................","..........#........##..........#..................#......M.#.#.#.........#..........................","....#..#..M#.....M.....#..........M...........#.#............................#......................","..#......#..........#......#..#...##..................#..#...#...................#.......#...#..###.","..................#..#.#.................T..................#.............#..................#......","........#.#...#............#.................#...##.#......#..............#.........................","....#.............#.##.#.........#..##......#.#.#..................................................#","..#.......#.............#.#....#.#.......................#.....#..........#................#........","....#.......................#....#.............#....#....#..........##........#..............#......","#..................#.....O................#....#.#......#.........#......#......................#...","..........#...........#.......O.......##...........#.....................#.........................#","..#................................#.............................#.........#...........#............","..........#.....#.......#..................#............#.........#...#.........O.....#.............","#...#.............#....#........#......#..#........#..........#.............................#.#.....",".......#..........#........O#....#...#.........#...........................................#........",".....##.....#...#..#..#...#....................#......#..#......#...##......O.........#....##.......","................#.....#.........#.............................O.......#............................#",".........#.#.................#.....#....#.........#....#............................................","...#.#...........................#.......#......#............#.#......................###.....O..#..","...................#.#.#......#.......#...............................#......#....#....#............","#.#......#....#........#.#..#.#..........##...##.................#..........#.....................#.",".#....#.......................................#.....#..........#.....M#..........#.....#............","........#.....................#.#............#...............#.#..O.......#...................#.....","....#............................#.......#....#.................................................#...","..................#.#.......#..........#.....#.......#..............#...............#...............",".........................##.........#......#...............#.O..................##............#.....","..##......#..#........#.....................#....#......#.................#...........##.......#....","#..#..#............###..#...............#....#........#..........#..#...........#...............#O..","#..............................#...............#.#....#..#..#..#......#.......#.##............#.....","#.......S.......##.....#...........................###.#...........................#.#............#.",".................................#...........#...........#..........#.....#..#.#...#............#...","...........#....##.....#.............#..#...................................##....................#.","M.#....................#.#...O...............................M......O..................#....#.......","....M#.####........#......................................................#........#................","......#.#..................#................................................##....#.................","...#.............................................###..#...#........................#..#.......#.#...","........#.............O#..#.#....................#..#..#..........#....#.....#......#...#.......#...",".#..##..................#........#..........#........#....#.........##O...............#.....#.......","#.....#.#.#........#.......##....................#..........#.............#...#...#....##........#.#","................#.........#...........#.....#.......##....#..............#..........................","......O........#................##......#.#..................#.........#.............##.............",".#....#.#.........#...#...............#...........##.....#...........#..........M....#............#.","..............#...............O.......#......................#....................#...O..#..........","................#...#.#...#....................#.......#...#..............O.........................",".#................................##.............#...#.#.....#.#................#..#...#............",".....#..............#...............#...............................................................",".......................#....................##..#................#......................#..#.....#..",".........#..#....................#.............#..#......................#.......#..................","#..#........#....................................#.....#..............#..........#......#.#.......#.",".#......................#.....#......#........#....#...#......O#....#.........#....##...............","...........................#.....#...#.........#..#......#.....M......#....#...#............##...O##",".......................#...##............#.........#..............#....#....#..#...#.....#.#........",".#....#.......................#.....#O...#.............................#............#...............","...#.#..............#....M..............#.#.......#...#...#...#..........#........................##",".....#................#.#........#......#....................#.....#................................","....O.....#..................#.#..O...#.........#.......#.#..............#.....#.............#....#.",".......#..#.#..##......#...................#...............#.#.......#.........#....#......#..#....#",".....#.............#...#.......#.#.#........##.....#.#.....#....#......#.#...#................#.....","...............#..........#.#.##...................#.......................#.......##.....#..#.#....",".................#......#............................#...#...##........................#............","#........#........#..........#...#........#.#..#..............#...#.#.....#.#.#.#...................",".........#.#.......###.......#..........#.......#..........................................#........",".#..................#.....#......##.#...........#..........#.....#..................#............#.#","..................................................#.........#..#.#.....##....#...........#..........","......#...........#......#.......#...#.....................#.#............##................#....#..",".#..........................#........#........#.......#........#...#...........###...........#......","#...#...#.......#...................................##........O.........#.....#......#...#..........","#.......#.....#.#....#...#................O...................#..................#.......##........."]
print(solution.minimalSteps(aaa))


