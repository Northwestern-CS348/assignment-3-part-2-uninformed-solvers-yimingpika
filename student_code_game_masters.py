from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here


        output = [[], [], []]

        for fact in self.kb.facts:
            if fact.statement.predicate == 'on':
                disk = str(fact.statement.terms[0])
                disk_num = int(disk[-1])
                peg = str(fact.statement.terms[1])
                peg_num = int(peg[-1])

                output[peg_num - 1].insert(0, disk_num)

        for index, list in enumerate(output):
            list.sort()
            output[index] = tuple(list)

        result = tuple(output)
        return result
        



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        ### Student code goes here
        
        disk = str(movable_statement.terms[0])
        peg1 = str(movable_statement.terms[1])
        peg2 = str(movable_statement.terms[2])

        peg1_num = int(peg1[-1])
        peg2_num = int(peg2[-1])

        game_state = self.getGameState()

        # target peg's change
        if len(game_state[peg2_num - 1]) > 0:
            fact = Fact(['top', 'disk' + str(game_state[peg2_num - 1][0]), str(peg2)])
            self.kb.kb_retract(fact)
        else:
            fact = Fact(['empty', str(peg2)])
            self.kb.kb_retract(fact)

        # after moving disk from peg1 to peg2
        fact_retract1 = Fact(['on', str(disk), str(peg1)])
        fact_retract2 = Fact(['top', str(disk), str(peg1)])
        self.kb.kb_retract(fact_retract1)
        self.kb.kb_retract(fact_retract2)

        fact_add1 = Fact(['on', str(disk), str(peg2)])
        fact_add2 = Fact(['top', str(disk), str(peg2)])
        self.kb.kb_add(fact_add1)
        self.kb.kb_add(fact_add2)

        # after miving, the original peg's change
        if len(game_state[peg1_num - 1]) > 1:
            fact = Fact(['top', 'disk' + str(game_state[peg1_num - 1][1]), str(peg1)])
            self.kb.kb_add(fact)
        else:
            fact = Fact(['empty', str(peg1)])
            self.kb.kb_add(fact)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        output = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for fact in self.kb.facts:
            if fact.statement.predicate == 'on' and str(fact.statement.terms[0]) != 'empty':
                x = str(fact.statement.terms[1])
                y = str(fact.statement.terms[2])
                tile = str(fact.statement.terms[0])
                x_num = int(x[-1])
                y_num = int(y[-1])
                tile_num = int(tile[-1])
                output[y_num - 1][x_num-1] = tile_num
            
            if fact.statement.predicate == 'on' and str(fact.statement.terms[0]) == 'empty':
                x = str(fact.statement.terms[1])
                y = str(fact.statement.terms[2])
                x_num = int(x[-1])
                y_num = int(y[-1])
                output[y_num - 1][x_num-1] = -1

        for index, list in enumerate(output):
            output[index] = tuple(list)
        
        result = tuple(output)

        return result
        

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here


        tile = str(movable_statement.terms[0])
        x1 = str(movable_statement.terms[1])
        y1 = str(movable_statement.terms[2])
        x2 = str(movable_statement.terms[3])
        y2 = str(movable_statement.terms[4])

        # retract old fact
        fact_retract1 = Fact(['on', str(tile), str(x1), str(y1)])
        fact_retract2 = Fact(['on', 'empty', str(x2), str(y2)])
        self.kb.kb_retract(fact_retract1)
        self.kb.kb_retract(fact_retract2)

        # add new fact
        fact_add1 = Fact(['on', 'empty', str(x1), str(y1)])
        fact_add2 = Fact(['on', str(tile), str(x2), str(y2)])
        self.kb.kb_add(fact_add1)
        self.kb.kb_add(fact_add2)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
