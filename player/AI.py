from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr


    def calculateb(self, gametiles):
        # list of reference: 
        # https://en.wikipedia.org/wiki/Chess_piece_relative_value#:~:text=Lasker%20adjusts%20some%20of%20these,%2C%20h%2Dfile%20rook%20%3D%205.25
        # https://arxiv.org/pdf/2009.04374.pdf
        # "Chess Board Option" by Larry Kaufman, ISBN: 978-9056919337
        value = 0
        
        # Determine game phase based on queens count
        ai_queens = sum(1 for x in range(8) for y in range(8) if gametiles[y][x].pieceonTile.tostring() == 'Q')
        opponent_queens = sum(1 for x in range(8) for y in range(8) if gametiles[y][x].pieceonTile.tostring() == 'q')
        total_queens = ai_queens + opponent_queens
        
        #check the number of pieces that doesnt overlap with original position to determine the number of moves
        origin = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]
        
        if total_queens == 0:
            game_phase = "endgame"
        elif ai_queens == opponent_queens: #queen 1v1 or 2v2 
            game_phase = "middle game"
        else: #uneven queen numbers
            game_phase = "threshold"
            
            
        
        # Define piece values based on the game phase
        inner_centers = [(3,3),(3,4),(4,3),(4,4)]
        outter_centers = [(2,2),(2,3),(2,4),(2,5),(3,2),(4,2),(5,2),(3,5),(4,5),(5,5),(5,3),(5,4)]
        piece_values = {
            "middle game": {
                'p': 8, 'P': 8,
                'n': 32, 'N': 32,
                'b': 33, 'B': 33,
                'r': 47, 'R': 47,  # considering first rook
                'q': 100, 'Q': 100,
                'k':10000, 'K':10000
            },
            "threshold": {
                'p': 9, 'P': 9,
                'n': 32, 'N': 32,
                'b': 33, 'B': 33,
                'r': 48, 'R': 48,  # considering first rook
                'q': 94, 'Q': 94,
                'k':10000, 'K':10000
            },
            "endgame": {
                'p': 10, 'P': 10,
                'n': 32, 'N': 32,
                'b': 33, 'B': 33,
                'r': 53, 'R': 53,  # considering first rook
                'q': 100, 'Q': 100,
                'k':10000, 'K':10000     
            }
        }
        
        bishops_count = {'ai': 0, 'opponent': 0}
        rooks_count = {'ai': 0, 'opponent': 0}
        #black is capital, white is lowercase
        for x in range(8):
            for y in range(8):
                total_piece_value = 0
                total_pawn_modifier = 0
                total_bishop_modifier = 0
                total_rook_modifier = 0
                piece = gametiles[y][x].pieceonTile.tostring()
                # Counting bishops and rooks for bonuses or second piece adjustment
                if piece == 'b':
                    bishops_count['ai'] += 1
                elif piece == 'B':
                    bishops_count['opponent'] += 1
                elif piece == 'r':
                    rooks_count['ai'] += 1
                elif piece == 'R':
                    rooks_count['opponent'] += 1
                
                temp_value = piece_values[game_phase].get(piece, 0)
                
                if piece == 'B' or piece == 'b':
                    # Central control bonus
                    if (y, x) in inner_centers:
                        total_bishop_modifier += 2
                    elif (y, x) in outter_centers:
                        total_bishop_modifier += 1

                    # Diagonal control bonus
                    diagonal_control = sum(1 for i in range(8) if gametiles[y][i].pieceonTile.tostring() in ['p', 'P'] or gametiles[i][x].pieceonTile.tostring() in ['p', 'P'])
                    total_bishop_modifier += diagonal_control*0.2
                    total_piece_value = temp_value + total_bishop_modifier

                # Rook modification
                if piece == 'R' or piece == 'r':
                    # open file bonus
                    file_occupied_by_pawns = any(gametiles[i][x].pieceonTile.tostring() in ['p', 'P'] for i in range(8))
                    if not file_occupied_by_pawns:
                        total_rook_modifier += 2

                    # Seventh rank bonus
                    if (piece == 'r' and y == 1) or (piece == 'R' and y == 6):
                        total_rook_modifier += 1

                    total_piece_value = temp_value + total_rook_modifier

                # Queen modification
                if piece == 'Q' or piece == 'q':
                    total_queen_modifier = 0
                    # Central control bonus
                    if (y, x) in inner_centers:
                        total_queen_modifier += 2
                    elif (y, x) in outter_centers:
                        total_queen_modifier += 1
                    
                    # Mobility bonus
                    queen_mobility = 0
                    # Calculate mobility in all directions from the queen's position
                    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
                    for dy, dx in directions:
                        ny, nx = y + dy, x + dx
                        while 0 <= ny < 8 and 0 <= nx < 8:
                            if gametiles[ny][nx].pieceonTile.tostring() == '-':
                                queen_mobility += 1
                            else:
                                # Stop counting in this direction if another piece is encountered
                                break
                            ny += dy
                            nx += dx
                    total_queen_modifier += queen_mobility *0.2  # Modify this divisor to scale the mobility effect

                    total_piece_value = temp_value + total_queen_modifier
                if piece == 'K' or piece == 'k':
                    total_piece_value = temp_value

                #knight center square modifucation:
                if piece == 'N' or piece == 'n':
                    total_knight_modifier = 0

                    # center
                    if (y, x) in inner_centers:
                        total_knight_modifier += 2
                    elif (y, x) in outter_centers:
                        total_knight_modifier += 1

                    # protected bonus
                    pawn_directions = [(-1, -1), (-1, 1)] if piece == 'n' else [(1, -1), (1, 1)]
                    for pdy, pdx in pawn_directions:
                        if 0 <= y + pdy < 8 and 0 <= x + pdx < 8:
                            if gametiles[y + pdy][x + pdx].pieceonTile.tostring() in ['p', 'P']:
                                total_knight_modifier += 1

                    # Mobility bonus
                    knight_moves = [(2, 1), (1, 2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, -2), (2, -1)]
                    mobility = sum(1 for dy, dx in knight_moves if 0 <= y + dy < 8 and 0 <= x + dx < 8)
                    total_knight_modifier += mobility*0.3

                    total_piece_value = temp_value + total_knight_modifier
                        
                #pawn modification
                if piece == "p" or piece == "P": 
                    
                    #blocked pawn modifier
                    if piece == 'p':
                        if y >= 1:
                            if gametiles[y-1][x].pieceonTile.tostring() != '-':#blocked
                                total_pawn_modifier -= 2
                    elif piece == 'P':
                        if y <= 0:
                            if gametiles[y+1][x].pieceonTile.tostring() != '-':#blocked
                                total_pawn_modifier -= 2

                    # Passed Pawn Modifier 
                    if piece == "p": #white, lowercase, start at y = 7
                        passed = True
                        for i in range(y-1, 0, -1):
                            if x == 0: #left most column, check for same column and column at right
                                if gametiles[i][x].pieceonTile.tostring() == 'P' or gametiles[i][x+1].pieceonTile.tostring() == 'P' :
                                    passed = False
                                    break
                            elif x == 7: #right most
                                if gametiles[i][x].pieceonTile.tostring() == 'P' or gametiles[i][x-1].pieceonTile.tostring() == 'P' :
                                    passed = False
                                    break
                            else:
                                if gametiles[i][x].pieceonTile.tostring() == 'P' or gametiles[i][x-1].pieceonTile.tostring() == 'P' or gametiles[i][y+1].pieceonTile.tostring() == 'P' :
                                    passed = False
                                    break
                        if passed:
                            passed_pawn_modifier = 0.5 if y < 4 else 0.3
                            total_pawn_modifier += temp_value * passed_pawn_modifier
                    elif piece == "P": 
                        passed = True
                        for i in range(y+1, 7, 1):
                            if x == 0: #left most column, check for same column and column at right
                                if gametiles[i][x].pieceonTile.tostring() == 'p' or gametiles[i][x+1].pieceonTile.tostring() == 'p' :
                                    passed = False
                                    break
                            elif x == 7: #right most
                                if gametiles[i][x].pieceonTile.tostring() == 'p' or gametiles[i][x-1].pieceonTile.tostring() == 'p' :
                                    passed = False
                                    break
                            else:
                                if gametiles[i][x].pieceonTile.tostring() == 'p' or gametiles[i][x-1].pieceonTile.tostring() == 'p' or gametiles[i][y+1].pieceonTile.tostring() == 'p' :
                                    passed = False
                                    break
                                
                        if passed:
                            passed_pawn_modifier = 0.5 if y > 3 else 0.3
                            total_pawn_modifier += temp_value * passed_pawn_modifier
                        #passed pawn modifier end
                                
                    #lone pawn modifier
                    if piece == "p": #white, lowercase, start at x = 7
                        lone = True
                        for i in range(1,7):
                            if x == 0: #left most column, check for same column and column at right
                                if gametiles[i][x].pieceonTile.tostring() == 'p' or gametiles[i][x+1].pieceonTile.tostring() == 'p' :
                                    lone = False
                                    break
                            elif x == 7: #right most
                                if gametiles[i][x].pieceonTile.tostring() == 'p' or gametiles[i][x-1].pieceonTile.tostring() == 'p' :
                                    lone = False
                                    break
                            else:
                                if gametiles[i][x].pieceonTile.tostring() == 'p' or gametiles[i][x-1].pieceonTile.tostring() == 'p' or gametiles[i][x+1].pieceonTile.tostring() == 'p' :
                                    lone = False
                                    break
                        if lone:
                            lone_pawn_modifier = 0.3 
                            total_pawn_modifier -= temp_value * lone_pawn_modifier
                    elif piece == "P":
                        lone = True
                        for i in range(1,7):
                            if x == 0: #left most column, check for same column and column at right
                                if gametiles[i][x].pieceonTile.tostring() == 'P' or gametiles[i][x+1].pieceonTile.tostring() == 'P' :
                                    lone = False
                                    break
                            elif x == 7: #right most
                                if gametiles[i][x].pieceonTile.tostring() == 'P' or gametiles[i][x-1].pieceonTile.tostring() == 'P' :
                                    lone = False
                                    break
                            else:
                                if gametiles[i][x].pieceonTile.tostring() == 'P' or gametiles[i][x-1].pieceonTile.tostring() == 'P' or gametiles[i][x+1].pieceonTile.tostring() == 'P' :
                                    lone = False
                                    break
                        if lone:
                            lone_pawn_modifier = 0.3 
                            total_pawn_modifier -= temp_value * lone_pawn_modifier
                        
                    #advancement modifier
                    if piece == 'p':
                        if y == 6:
                            total_pawn_modifier -= 2 
                        elif y == 5:
                            total_pawn_modifier -=1.5
                            if x == 0:
                                if gametiles[4][1].pieceonTile.tostring() == 'p':
                                   total_pawn_modifier +=1.5 
                            elif x == 7:
                                if gametiles[4][7].pieceonTile.tostring() == 'p':
                                   total_pawn_modifier +=1.5
                            else:
                                if gametiles[4][x + 1].pieceonTile.tostring() == 'p':
                                   total_pawn_modifier +=1
                                elif gametiles[4][x - 1].pieceonTile.tostring() == 'p':
                                   total_pawn_modifier +=1
                        elif y == 4:
                            total_pawn_modifier += 2
                        elif y == 3:
                            total_pawn_modifier += 0.5*temp_value
                        elif y == 2:
                            total_pawn_modifier += 1*temp_value
                        elif y == 1:
                            total_pawn_modifier += 2*temp_value      
                    if piece == 'P':
                        if y == 1:
                            total_pawn_modifier -= 2 
                        elif y == 2:
                            total_pawn_modifier -=1.5
                            if x == 0:
                                if gametiles[3][1].pieceonTile.tostring() == 'p':
                                   total_pawn_modifier +=1.5 
                            elif x == 7:
                                if gametiles[3][7].pieceonTile.tostring() == 'p':
                                   total_pawn_modifier +=1.5
                            else:
                                if gametiles[3][x + 1].pieceonTile.tostring() == 'p':
                                   total_pawn_modifier +=1
                                elif gametiles[3][x - 1].pieceonTile.tostring() == 'p':
                                   total_pawn_modifier +=1
                        elif y == 3:
                            total_pawn_modifier += 2
                        elif y == 4:
                            total_pawn_modifier += 0.5*temp_value
                        elif y == 5:
                            total_pawn_modifier += 1*temp_value
                        elif y == 6:
                            total_pawn_modifier += 2*temp_value

                    #mid game pawn modifier
                    if game_phase == "middle game": 
                        if x == 0 or x == 7: #rook pawn
                            total_pawn_modifier -= temp_value * 0.3
                        elif x == 1 or x == 6:
                            total_pawn_modifier -= temp_value * 0.15 #bishop pawn
                        elif x == 2 or x == 5:
                            total_pawn_modifier -= temp_value * 0.1 #knight pawn
                                            
                    #pawn structure modifier
                    if 0<y<7 : 
                        pawn_structure_modifier = temp_value*0.2
                        if piece == 'p':
                            if x ==  0 : #left most column pawns
                                if gametiles[y + 1][x + 1].pieceonTile.tostring() == 'p' :
                                    total_pawn_modifier += pawn_structure_modifier
                            elif x == 7   : #right most
                                if gametiles[y + 1][x - 1].pieceonTile.tostring() == 'p' :
                                    total_pawn_modifier += pawn_structure_modifier
                            else:
                                if gametiles[y + 1][x + 1].pieceonTile.tostring() == 'p' :
                                    total_pawn_modifier += pawn_structure_modifier
                                if gametiles[y + 1][x - 1].pieceonTile.tostring() == 'p' :
                                    total_pawn_modifier += pawn_structure_modifier      
                        elif piece == 'P':
                            if x ==  0 : #left most column pawns
                                if gametiles[y - 1][x + 1].pieceonTile.tostring() == 'P' :
                                    total_pawn_modifier += pawn_structure_modifier
                            elif x == 7   : #right most
                                if gametiles[y - 1][x - 1].pieceonTile.tostring() == 'P':
                                    total_pawn_modifier += pawn_structure_modifier
                            else:
                                if gametiles[y - 1][x + 1].pieceonTile.tostring() == 'P' :
                                    total_pawn_modifier += pawn_structure_modifier
                                if gametiles[y - 1][x - 1].pieceonTile.tostring() == 'P' :
                                    total_pawn_modifier += pawn_structure_modifier      
                                                
                    #mid game pawnvalue difference
                    total_piece_value = temp_value + total_pawn_modifier
                
                if gametiles[y][x].pieceonTile.alliance == "Black":
                    total_piece_value *= -1
                value +=  total_piece_value
                
        # Adding Bishop Pair Bonuses
        if game_phase == "middle game":
            if bishops_count['ai'] == 2:
                value -= 3
            if bishops_count['opponent'] == 2:
                value += 3
        elif game_phase == "threshold":
            if bishops_count['ai'] == 2:
                value -= 4
            if bishops_count['opponent'] == 2:
                value += 4
        elif game_phase == "endgame":
            if bishops_count['ai'] == 2:
                value -= 5
            if bishops_count['opponent'] == 2:
                value += 5
        return value


    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
