import os, sys, pdb, random
import Image, ImageGrab, ImageOps
import time, random
import win32api, win32con
from numpy import *
from copy import deepcopy
import win32gui


#todo:  fix bugs, sort vertex by clustering coeff?,
#tkinter, gui, bridge edges
#idea: sort vertexs differently for the bounded search
#code may be slightly messy, but it works
#========= CONSTANTS AND VARS============
xPad, yPad = 335, 160
ROOKBISHOP = 2593
tiles, count = [], []
ONE = {2252, 4259, 2076}
TWO = {2715, 5098, 2710}
THREE = {3177, 4246, 2655}
FOUR = {3492, 4048, 2174}
QUEEN = {2543, 5531, 2398}
ROOK = {3320, 4021, 1339}
BISHOP = {2250, 5395, 1260}
KNIGHT = {3921, 3439, 2558}
JUG = {2815, 3600}
COLORS = {2815, 3600, 2252, 4259, 2076, 2715, 5098, 2710, \
          3177, 4246, 2655, 3492, 4048, 2174, 2543, 5531, \
          2398, 3320, 4021, 1339, 2250, 5395, 1260, 3921, 3439, 2558}
          
#=============UTILITY FUNCTIONS================
def cont():
    target, color = 2728, 0 
    x = xPad -55 + 150
    y = yPad -89 + 350
    found = False
    for i in range(33):
        x+= 1
        y = yPad -89 + 350
        for j in range(33):
            y += 1
            box = (x, y, x + 169, y + 115)
            im = ImageGrab.grab(box)
            im = ImageOps.grayscale(im)
            arr = array(im.getcolors())
            color = arr.sum()
            if color == target:
                found = True
                break
        if color == target:
            break
    if found:
        win32api.SetCursorPos((x + 30, y + 8))
        leftClick()
        win32api.SetCursorPos((0, 0))
        return True
    return False

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(random.random() +.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
#===========EDGE CONSTRUCTION==================
def getMoves ( colorNum, arrayIndex ):
    moves, final = [], []    
    if colorNum in ONE or colorNum in TWO or colorNum in THREE or colorNum in FOUR:
        multiplier = 0
        if colorNum in ONE:
            multiplier = 1
        elif colorNum in TWO:
            multiplier = 2
        elif colorNum in THREE:
            multiplier = 3
        elif colorNum in FOUR:
            multiplier = 4
        if ((arrayIndex % 6) + 1 - multiplier) > 0 : # can go up
            moves.append( arrayIndex - multiplier*1)
            if ((arrayIndex//6) + 1 - multiplier )> 0 :
                moves.append( arrayIndex - multiplier*7)
            if ((arrayIndex//6) + multiplier )<= 5:
                moves.append( arrayIndex + multiplier*5)
        if ((arrayIndex % 6) + multiplier) <= 5 :    # can go down
            moves.append( arrayIndex + multiplier*1)
            if ((arrayIndex//6) + 1 - multiplier )> 0 :
                moves.append( arrayIndex - multiplier*5)
            if ((arrayIndex//6) + multiplier )<= 5:
                moves.append( arrayIndex + multiplier*7)
        if ((arrayIndex//6) + 1 - multiplier )> 0 : # can go left
            moves.append( arrayIndex - multiplier*6)
            
        if ((arrayIndex//6) + multiplier )<= 5:     #can go right
            moves.append( arrayIndex + multiplier*6) 
        
    elif colorNum in QUEEN    :
        if arrayIndex % 6 != 0:      #not first row
            moves.append( arrayIndex - arrayIndex % 6)
        if (arrayIndex + 1)% 6 != 0:    #not last row 
            moves.append( arrayIndex + (5 - arrayIndex % 6))
        if arrayIndex//6 != 0:     #not first column
            moves.append( arrayIndex % 6)
        if arrayIndex//6 != 5 :    #not last column
            moves.append( arrayIndex % 6 + 30) 
        if arrayIndex % 6 != 0:   #not first row
            if arrayIndex//6 != 0: #not first col
                temp = arrayIndex  # go NW
                while  (temp // 6 != 0 and temp % 6 != 0 ):
                    temp-=7
                moves.append(temp)
            if arrayIndex//6 != 5 :#not last col, go NE
                temp = arrayIndex
                while  (temp % 6 != 0 and temp//6 != 5 ):
                    temp+=5
                moves.append(temp)
        if (arrayIndex + 1)% 6 != 0: #not last row
            if arrayIndex//6 != 0: #not first col go SW
                temp = arrayIndex
                while (temp // 6 != 0 and (temp + 1)% 6 != 0 ):
                    temp-=5
                moves.append(temp)
        if arrayIndex//6 != 5: #not last col SE
                temp = arrayIndex
                while  (temp//6 != 5 and (temp % 6) != 5 ):
                    temp+=7
                moves.append(temp)
    elif colorNum in ROOK :
        if arrayIndex % 6 != 0:      #not first row
            moves.append( arrayIndex - arrayIndex % 6)
        if (arrayIndex + 1)% 6 != 0:    #not last row 
            moves.append( arrayIndex + (5 - arrayIndex % 6))
        if arrayIndex//6 != 0:     #not first column
            moves.append( arrayIndex % 6)
        if arrayIndex//6 != 5 :    #not last column
            moves.append( arrayIndex % 6 + 30)

    elif colorNum in BISHOP:
        if arrayIndex % 6 != 0:   #not first row
            if arrayIndex//6 != 0: #not first col
                temp = arrayIndex  # go NW
                while  (temp // 6 != 0 and temp % 6 != 0 ):
                    temp-=7
                moves.append(temp)
            if arrayIndex//6 != 5 :#not last col, go NE
                temp = arrayIndex
                while  (temp % 6 != 0 and temp//6 != 5 ):
                    temp+=5
                moves.append(temp)
        if (arrayIndex + 1)% 6 != 0: #not last row
            if arrayIndex//6 != 0: #not first col go SW
                temp = arrayIndex
                while (temp // 6 != 0 and (temp + 1)% 6 != 0 ):
                    temp-=5
                moves.append(temp)
        if arrayIndex//6 != 5: #not last col SE
                temp = arrayIndex
                while  (temp//6 != 5 and (temp % 6) != 5 ):
                    temp+=7
                moves.append(temp)
    elif colorNum in KNIGHT:
        if ( arrayIndex % 6 - 2 >= 0): # can go up 2
            if (arrayIndex//6 + 1 <=5): # can go right
                moves.append( arrayIndex + 4)# NE
            if (arrayIndex//6 - 1 >=0): # can go left
                moves.append( arrayIndex - 8)  # NW
        if ( arrayIndex % 6 + 2 <= 5): # an go down 2
            if ( arrayIndex//6 + 1 <=5):
                moves.append( arrayIndex + 8) #SE
            if ( arrayIndex//6 - 1 >= 0):
                moves.append( arrayIndex - 4)
        if ( arrayIndex//6 + 2 <= 5):  # can go E 2
            if ( arrayIndex%6 + 1 <= 5): # can go down 1
                moves.append( arrayIndex + 13)
            if ( arrayIndex%6 -1 >= 0): #can go up 1
                moves.append( arrayIndex + 11)
        if ( arrayIndex//6 -2 >= 0): # can go W 2
            if ( arrayIndex%6 + 1 <= 5): # can go down 1
                moves.append( arrayIndex - 11)
            if ( arrayIndex%6 -1 >= 0): #can go up 1
                moves.append( arrayIndex - 13)
    elif colorNum in JUG:
        for i in range(0, 36):
            if i!= arrayIndex:
                moves.append(i)
    for i in moves:
        if i <= 35 and i >= 0:
            final.append( i )
    return final

def getConnections( inputs, edges ):
    for i in range ( 0, 36):
        edges.append([])
        temp = getMoves( tiles[i], i)
        while (len(edges[i]) != 0):
            edges[i].pop()
        for j in range (0, len(temp)):
            edges[i].append(temp[j])

            
#===========TIER SPECIFICS===========================

def getTiles( ):
    for i in range ( 1, 7):
        for j in range (1, 7):
            box = (xPad + 25+ (i - 1) * 60, yPad + 25 + (j - 1) * 60,
                   xPad + (i * 60) - 25, yPad + (j * 60) - 25)
            temp = ImageGrab.grab(box)
            im = ImageOps.grayscale(temp)
            arr = array(im.getcolors())
            num = arr.sum()
            tiles.append(num)

def clickTile( index, remaining, edges ):  #bronze and grey
    i, j = (index//6) + 1, (index%6) + 1
    box = (xPad + 25+ (i - 1) * 60, yPad + 25 + (j - 1) * 60,
                   xPad + (i * 60) - 25, yPad + (j * 60) - 25)
    x = random.randint(xPad + (i - 1) * 60 + 15, xPad + (i * 60) - 15)
    y = random.randint(yPad + (j - 1) * 60 + 15, yPad + (j * 60) - 15)
    coord = [x, y]
    win32api.SetCursorPos(coord)
    leftClick()
    auxPos = [100, 100]
    win32api.SetCursorPos(auxPos)
    time.sleep(random.random() + .49)
    temp = ImageGrab.grab(box)
    im = ImageOps.grayscale(temp)
    arr = array(im.getcolors())
    num = arr.sum()
    if num not in COLORS:
        time.sleep(random.random() + .69)
        temp = ImageGrab.grab(box)
        im = ImageOps.grayscale(temp)
        arr = array(im.getcolors())
        num = arr.sum()
    if num == ROOKBISHOP:
        box = (xPad + 30+ (i - 1) * 60, yPad + 30 + (j - 1) * 60,
                   xPad + (i * 60) - 25, yPad + (j * 60) - 25)
        temp = ImageGrab.grab(box)
        im = ImageOps.grayscale(temp)
        arr = array(im.getcolors())
        num = arr.sum()
    tiles[index] = num
    if index in remaining:
        edges[index] = getMoves( num, index)
       
def basicClickTile(index, remaining, edges): #silver
    i, j = (index//6) + 1, (index%6) + 1
    box = (xPad + 25+ (i - 1) * 60, yPad + 25 + (j - 1) * 60,
                   xPad + (i * 60) - 25, yPad + (j * 60) - 25)
    x = random.randint(xPad + (i - 1) * 60 + 15, xPad + (i * 60) - 15)
    y = random.randint(yPad + (j - 1) * 60 + 15, yPad + (j * 60) - 15)
    coord = [x, y]
    win32api.SetCursorPos(coord)
    leftClick()
    auxPos = [100, 100]
    win32api.SetCursorPos(auxPos)
    time.sleep(random.random() + .69)
    if index in remaining:
        temp = ImageGrab.grab(box)
        im = ImageOps.grayscale(temp)
        arr = array(im.getcolors())
        num = arr.sum()
        if num not in COLORS:
            time.sleep(random.random() + .69)
            temp = ImageGrab.grab(box)
            im = ImageOps.grayscale(temp)
            arr = array(im.getcolors())
            num = arr.sum()
        if num == ROOKBISHOP:
            box = (xPad + 30+ (i - 1) * 60, yPad + 30 + (j - 1) * 60,
                   xPad + (i * 60) - 25, yPad + (j * 60) - 25)
            temp = ImageGrab.grab(box)
            im = ImageOps.grayscale(temp)
            arr = array(im.getcolors())
            num = arr.sum()
        tiles[index] = num
        edges[index] = getMoves( num, index)
        

#==============H PATH FUNCTIONS================            


def hPathIter(edges, start = None):
    degrees = [0]*len(edges)
    for vertex in edges:
        for tail in vertex:
            degrees[tail] += 1
    count = 0
    best, solution = 0, None
    heads= {}
    for head in range(len(edges)):
        for tail in edges[head]:
            if head not in heads:
                heads[head] = []
            heads[head].append(tail)
    stack = []
    if start:
        start.sort(key = lambda index: degrees[index], reverse = True)
        for vert in start:
            cur_heads = deepcopy(heads)
            for head in cur_heads.values():
                if vert in head:
                    head.remove(vert)
            stack.append(([vert], cur_heads))
    else:
        vertexs = [i for i in range(36)]
        vertexs.sort(key = lambda index: degrees[index], reverse = True)
        for i in vertexs:
            path = [i]
            cur_heads = deepcopy(heads)
            for head in cur_heads.values():
                if i in head:
                    head.remove(i)
            stack.append((path, cur_heads))
    while len(stack) != 0 and count < 49696 and best < 36:
        path, heads = stack.pop() #heads == vertexs with outgoing edges
        current = path[len(path) - 1]
        if len(path) > best:
                solution = path
                best = len(path)
        if current not in heads or len(heads[current]) == 0:
            continue
        keys = heads.keys()
        while len(keys) >0:
            key = keys.pop()
            if (len(heads[key]) == 0 or key in path) and key != current:
                del heads[key]
        for tail in heads[current]:
            if tail in path:
                continue
            cur_heads = deepcopy(heads)
            cur_path = deepcopy(path)
            cur_path.append(tail)
            connected = set()   #connected == vertexs reachable with cur edges
            for key in cur_heads.keys():
                head = cur_heads[key]
                if tail in head:
                    head.remove(tail)
                connected.update(set(head))
                if len(head) == 0:
                    del cur_heads[key]
            for i in range(36):
                if i in connected and i in cur_path:
                    connected.remove(i)
            if current in cur_heads:
                del cur_heads[current]
            bound = len(cur_path) + len(cur_heads) 
            if len(cur_path) + len(connected) < bound:
                bound = len(cur_path) + len(connected)
            if bound > best:
                stack.append((cur_path, cur_heads))
            elif bound >= best -3:
                remains = []
                for i in range(0, len(cur_path)):
                    if i not in cur_path:
                        remains.append(i)       
                cur_path = insertToPath(cur_path, edges, 0, remains)
                connected = set()
                keys = cur_heads.keys()
                while len(keys) != 0:
                    cur = keys.pop()
                    if cur == cur_path[-1]:
                        continue
                    if cur in cur_path:
                        del cur_heads[cur]
                for key in cur_heads.keys():
                    head = cur_heads[key]
                    index = len(head) - 1
                    while index >=0:
                        if head[index] in cur_path:
                            head.pop(index)
                        index -= 1
                    connected.update(set(head))
                bound = len(cur_path) + len(cur_heads) 
                if len(cur_path) + len(connected) < bound:
                    bound = len(cur_path) + len(connected)
                if bound > best:
                    stack.append((cur_path, cur_heads))
        count +=1
    print 'Path length: ', len(solution)
    return solution
            
                    

def insertBronze(path, edges, startIndex, remains):
    count = len(remains)
    if count >= 2:
        while( insertRemainingProto(path,edges,startIndex,remains) and count >=0):
            count-=1
    count = len(remains)
    if count >0:
        while( insertRemainingBronze(path, edges, startIndex, remains) != 0 and count>0):
            count-=1
    return path

def insertToPath(path, edges, startIndex, remains):
    count = len(remains)
    if count >= 2:
        while(insertRemainingProto(path,edges,startIndex,remains) and count >=0):
            count-=1
    count = len(remains)
    if count >0:
        while( insertRemaining(path, edges, startIndex, remains) and count>0):
            count-=1
    return path

def insertRemainingProto(path, edges, startIndex, remains):
    curPath = []
    if startIndex != 0:
        for i in range (startIndex , len(path)):
            curPath.append(path[i])
    for i in range(0, len(remains)):  # for every remains
        for pathI in range(startIndex , len(path) - 1):
            if remains[i] in edges[path[pathI]]:  #if path leads to it
                if len(path) >= 2:
                    for j in range(0, len(remains)):  # look for length two
                        if i != j and remains[j] in edges[remains[i]]:
                            if path[pathI + 1] in edges[remains[j]]:
                                path.insert(pathI + 1, remains[j])
                                path.insert(pathI + 1, remains[i])
                                remains.remove(path[pathI+1])
                                remains.remove(path[pathI+2])
                                return True

    return False
        
                            

def insertRemainingBronze(path, edges, startIndex, remains):
    auxPath = []
    for i in range ( startIndex , len(path)):
        auxPath.append(path[i])
    for i in range(0, len(remains)):
        if auxPath[0] in edges[remains[i]]:
            path.insert(i, remains[i])
            remains.pop(i)
            return True
        if remains[i] in edges[path[len(path)-1]]:
            path.append(remains[i])
            remains.pop(i)
            return True
        for j in range(startIndex, len(path) - 1):
            if remains[i] in edges[path[j]]: #if j tile leads to i tile
                if path[j+1] in edges[remains[i]]:  #if i tile leads to j+1
                    path.insert(j+1, remains[i])
                    remains.pop(i)
                    return True
    return False

def insertRemaining(path, edges, startIndex, remains):
    auxPath = []
    for i in range ( startIndex , len(path)):
        auxPath.append(path[i])    
    for i in range(0, len(remains)):
       if remains[i] in edges[path[len(path)-1]]:
            path.append(remains[i])
            remains.pop(i)
            return True
       for j in range(startIndex, len(path) - 1):
            if remains[i] in edges[path[j]]: #if j tile leads to i tile
                if path[j+1] in edges[remains[i]]:  #if i tile leads to j+1
                    path.insert(j+1, remains[i])
                    remains.pop(i)
                    return True          
    return False


#==========MAIN FUNCTION LOOPS AND HELPER FUNCTIONS=============
def edgeSort(edges):
    degrees = [0]*len(edges)
    for vertex in edges:
        for tail in vertex:
            degrees[tail] += 1
    for vertex in edges:
        vertex.sort(key = lambda index: degrees[index])

def botBronze(leftOver):
   edges = []
   getTiles()   #gets color values for tiles
   getConnections(tiles, edges)    #builds edge map
   edgeSort(edges)
   path = hPathIter(edges)
   for i in range(36):
       if i not in path:
           leftOver.append(i)
   clickPath(path, leftOver, edges, leftOver)     #clicks tile and reads innew color in til
   return edges[path[len(path)-1]]

def botGrey(begin, leftOver):
    edges = []
    getConnections(tiles, edges)    
    edgeSort(edges)
    path = hPathIter(edges, begin)
    remains = [i for i in range(36) if i not in path]
    clickPath(path, remains, edges, leftOver)
    for i in range(0, len(remains)):
        leftOver.append(remains[i])
    print remains
    return edges[path[len(path)-1]]

def botSilver(begin, leftOver):
    edges = []
    getConnections(tiles, edges)    
    edgeSort(edges)
    path = hPathIter(edges, begin)
    remains = [i for i in range(36) if i not in path]
    basicClickPath(path, remains, edges, leftOver)

    
def clickPath(path, remaining, edges, leftOver):
    i = 0
    while (i != len(path)):
        if tiles[path[i]] in JUG:
            path = insertBronze(path, edges, i + 1, remaining)
        clickTile(path[i], leftOver, edges)
        if path[i] in leftOver:
            remaining.append(path[i])
            leftOver.remove(path[i])
            passInt = i + 1
            print "clicked a leftOver Tile"
            print "old Path length" + str(len(path))
            path = insertToPath(path, edges, passInt, remaining)
            path = insertToPath(path, edges, passInt, remaining)
            print "new Path length" + str(len(path))
        i+=1

def basicClickPath(path, remaining, edges, leftOver):
    i = 0
    while (i != len(path)):
        if tiles[path[i]] in JUG:
            path = insertBronze(path, edges, i + 1, remaining)
        basicClickTile(path[i], leftOver, edges)
        if path[i] in leftOver:
            remaining.append(path[i])
            leftOver.remove(path[i])
            passInt = i + 1
            print "clicked a leftOver Tile"
            print "old Path length" + str(len(path))
            path = insertToPath(path, edges, passInt, remaining)
            path = insertToPath(path, edges, passInt, remaining)
            print "new Path length" + str(len(path))
        i+=1
        
#========================================================
def enumHandler(hwnd, lParam):
    global xPad, yPad
    if win32gui.IsWindowVisible(hwnd):
        if 'Puzzle Pirates' in win32gui.GetWindowText(hwnd):
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            xPad = x + 55
            yPad = y + 89

    
def main():
   global tiles
   win32gui.EnumWindows(enumHandler, None)
   count = 0
   boolean = True
   while boolean and count <1:
       time.sleep(random.random() + 2.69)
       del tiles[0:len(tiles)]
       leftOver = []
       grey = botBronze(leftOver)
       print leftOver
       silver = botGrey(grey, leftOver)
       print leftOver
       botSilver(silver, leftOver)
       win32gui.EnumWindows(enumHandler, None)
       count += 1
       time.sleep(random.random() + 6.69)
       boolean = cont() 
   print "Puzzles botted: " + str(count + 1) 
   
if __name__ == '__main__':
    main()
