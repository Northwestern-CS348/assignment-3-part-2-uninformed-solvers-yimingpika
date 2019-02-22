from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        while True:

            if self.currentState not in self.visited or self.currentState.state == self.victoryCondition:
                self.visited[self.currentState] = True
                
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    return False

            # start point
            if self.currentState.nextChildToVisit == 0: 
                self.helper()            

            if self.currentState.nextChildToVisit >= len(self.currentState.children):
                # continue
                self.currentState.nextChildToVisit += 1
                reverse = self.currentState.requiredMovable
                self.gm.reverseMove(reverse)
                self.currentState = self.currentState.parent
                
            else:
                
                state = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(state.requiredMovable)
                self.currentState = state

    def helper(self):
        movements = self.gm.getMovables()
        for index in movements:
            self.gm.makeMove(index)
                       
            child = GameState(self.gm.getGameState(), self.currentState.depth + 1, index)  
            if child not in self.visited:
                child.parent = self.currentState
                self.currentState.children.append(child)
            self.gm.reverseMove(index)






class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        
        if self.currentState.state == self.victoryCondition:
            self.visited[self.currentState] = True
            return True

        depth = self.currentState.depth
        
        while True:
            # print self.recursion(depth)
            judge = self.recursion(depth)
            
            if not judge:

                return False
                
            if self.currentState.state != self.victoryCondition:
                depth += 1
                # print('depth: ')
                # print(depth)
        
            else:

                return True
            

    def helper(self):
        movements = self.gm.getMovables()
        for index in movements:
            self.gm.makeMove(index)
                       
            child = GameState(self.gm.getGameState(), self.currentState.depth + 1, index)  
            if child not in self.visited:
                child.parent = self.currentState
                self.currentState.children.append(child)
            self.gm.reverseMove(index)


    def recursion(self, depth):
        if self.currentState.depth < depth:

            if self.currentState.nextChildToVisit > len(self.currentState.children):
                self.currentState.nextChildToVisit = 0

            if self.currentState.nextChildToVisit < len(self.currentState.children):
                newState = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(newState.requiredMovable)
                self.currentState = newState
                return self.recursion(depth)

            else:
                self.currentState.nextChildToVisit += 1
                if self.currentState.depth == 0: 
                    return True

                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.recursion(depth)        

        elif self.currentState.depth == depth:
            if self.currentState not in self.visited or depth == 0:
                if not self.currentState.children:
                    self.helper()

            if self.currentState.state == self.victoryCondition or self.currentState not in self.visited:
                self.visited[self.currentState] = True
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    return False

            else:
                if self.currentState.depth == 0: 
                    return True
                reverse = self.currentState.requiredMovable
                self.gm.reverseMove(reverse)
                self.currentState = self.currentState.parent
                return self.recursion(depth)

        else:     
            reverse = self.currentState.requiredMovable
            self.gm.reverseMove(reverse)
            self.currentState = self.currentState.parent
            return self.recursion(depth)
        

   
