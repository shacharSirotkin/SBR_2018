import Sigma
import Tree
from NT import NT


#import math
#import itertools
#This class represents a plan library
class PL(object):
    '''
    classdocs
    '''
    plNum=0
 
    def __init__(self, sigma, NT, R, P):
        '''
        Constructor
        '''
        self._Sigma = sigma     # list of Sigmas
        self._NT = NT           # list of NTs
        self._R = R             # subset of NT
        self._P = P             # list of rules
        PL.plNum+=1
        #self._ruleProb = prob
    
 
        
    def __del__(self):
        PL.plNum-=1   
    
    def getRuleProbNotUniform(self, rule):
        if rule==() or rule==[]:
            return self._getRuleProb()
        amountOfMatchingRules = 0.0
        for rule in self._P:
            if rule._A.get() == rule._A.get():
                amountOfMatchingRules += 1
        if amountOfMatchingRules == 0:
            return 0
        else:
            return rule.getPriorProbability()/amountOfMatchingRules
 
    def getRuleProb(self, startsWith=[]):
        if startsWith==[]:
            return 1.0/len(self._P)
        amountOfMatchingRules = 0.0
        for rule in self._P:
            if rule._A.get() == startsWith.get():
                amountOfMatchingRules += 1
        if amountOfMatchingRules == 0:
            return 0.0
        else:
            return 1.0/amountOfMatchingRules
        
    
    def __repr__(self):
        res = "Plan Library: \nSigma=" + self._Sigma.__repr__() + "\nNT=" + self._NT.__repr__() + "\nR=" + self._R.__repr__() + "\nRules="
        for rule in self._P:
            res += "\t" + rule.__repr__() + "\n"
        return res
    
        #Prints the plan library in XML format
    def toXML(self):
        result="<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>\n<PL>\n\t<Letters>\n\t\t<Non-Terminals>\n"
        for nt in self._NT:
            if nt.numOfParams()==0:
                NTelement="\t\t\t<Letter name=\""+nt.get()+"\" id=\""+nt.get()+"\"/>\n"
            else:
                NTelement="\t\t\t<Letter name=\""+nt.get()+"\" id=\""+nt.get()+"\">\n\t\t\t\t<Params>\n"
                for param in nt.getParamList():
                    NTelement+="\t\t\t\t\t<Param name=\""+str(param[0])+"\"/>\n"
                NTelement+="\t\t\t\t</Params>\n\t\t\t</Letter>\n"
            result+=NTelement
        result+="\t\t</Non-Terminals>\n\t\t<Terminals>\n"
        
        for sigma in self._Sigma:
            if sigma.numOfParams()==0:
                sigmaElement="\t\t\t<Letter name=\""+sigma.get()+"\" id=\""+sigma.get()+"\"/>\n"
            else:
                sigmaElement="\t\t\t<Letter name=\""+sigma.get()+"\" id=\""+sigma.get()+"\">\n\t\t\t\t<Params>\n"
                for param in sigma.getParamList():
                    sigmaElement+="\t\t\t\t\t<Param name=\""+str(param[0])+"\"/>\n"
                sigmaElement+="\t\t\t\t</Params>\n\t\t\t</Letter>\n"
            result+=sigmaElement
        result+="\t\t</Terminals>\n\t</Letters>\n\t<Recipes>\n"
        
        for goal in self._R:
            goalElement="\t\t<Recipe prob=\"0.5\" lhs=\"root\">\n\t\t\t<Letter id=\""+goal.get()+"\" index=\"1\"/>\n\t\t</Recipe>\n"
            result+=goalElement
        
        for rule in self._P:
            ruleElement="\t\t<Recipe prob=\"0.1\" lhs=\""+rule._A.get()+"\">\n"
            if len(rule._order)!=0:
                ruleElement+="\t\t\t<Order>\n"
                for orderCons in rule._order:
                    ruleElement+="\t\t\t\t<OrderCons firstIndex=\""+str(orderCons[0]+1)+"\" secondIndex=\""+str(orderCons[1]+1)+"\"/>\n"
                ruleElement+="\t\t\t</Order>\n"
            if len(rule._paramConst)!=0:                
                ruleElement+="\t\t\t<Equals>\n"
                for eqCons in rule._paramConst:
                    if len(eqCons)==4:
                        ruleElement+="\t\t\t\t<EqualCons firstIndex=\""+str(int(eqCons[0])+1)+"\" firstParam=\""+str(eqCons[1])+"\" secondIndex=\""+str(int(eqCons[2])+1)+"\" secondParam=\""+str(eqCons[3])+"\"/>\n"
                ruleElement+="\t\t\t</Equals>\n"
            i=1
            for letter in rule._alpha:
                ruleElement+="\t\t\t<Letter id=\""+letter.get()+"\" index=\""+str(i)+"\"/>\n"
                i+=1
            ruleElement+="\t\t</Recipe>\n"
            result+=ruleElement
        result+="\t</Recipes>\n</PL>\n"
                
        return result
    
    
    def getGoals(self):
        return self._R
    
    def getRootProb(self):
        return 1.0/len(self._R)
    
# This function returns the set of generating trees whose foot is obs and root is root of the new tree
    def generatingSetForObs(self, treesBeforeSubstitute, observation):
        #treesBeforeSubstitute = self.generatingSet([root])
        treesAfterSubstitute = []
        for tree in treesBeforeSubstitute:
 
 
            footWithIndex = tree.isLeftMostTree(byIndex=True)
            #If this tree has a foot (must be true here, if false, it's a bug!) and if this foot matches the observation 
            if footWithIndex and footWithIndex[0].sameParameters(observation, '-1') :
                newCopy = tree    #myCopy - Removed
 
 
                if newCopy.substitute(observation, footWithIndex[1]):
                    treesAfterSubstitute.append(newCopy)
        return treesAfterSubstitute
     
    def generatingSet(self, generatingFrom):
        #res is a set of all leftmost trees deriving from this PL which start with a root from R or NT
        res=[] 
        for goal in generatingFrom:
            for rule in self._P:
                if goal.matchLetter(rule._A):
                    for tree in self.createTrees(rule):
                        if tree.isLeftMostTree():
                            res.append(tree)
 
 
 
                        else:
                            print "Not leftmost:"
                            print tree
                            print tree._rule
        return res                    
            
    def createTreesNew(self, rule, recursive=0):
        #if rule has only one child 
        if 1 == len(rule._alpha):
            if rule._alpha[0]._type=='Sigma':
                child = Tree.Tree("Basic", rule._alpha[0].myCopy(), (), [], self)
                root = Tree.Tree("Complex", rule._A.myCopy(), rule, [child], self)
                return [root]
#             else:
#                 print "rule._alpha[0]=",rule._alpha[0] 
#                 possibleChildrenTrees = self.generatingSetForObs([rule._alpha[0]])
#                 print "rule._alpha[0].GS:=",possibleChildrenTrees 
#                 possibleTrees = []
#                 for subTree in possibleChildrenTrees:
#                     root = Tree.Tree("Complex", rule._A, rule, [subTree], self)
#                     possibleTrees.append(root)
#                 return possibleTrees
                #return []
        
        #else, need to create all possible outcomes from tree
        trees=[]
        leftMostChilds = rule.leftMostChilds(byIndex=True)
        for childIndex in leftMostChilds:#range(len(rule._alpha)):
            #if childIndex in leftMostChilds:
            if type(rule._alpha[childIndex])==NT:
                #collect all possible derivations of this child to childTrees
                for childRule in self._P:
                    childRecursion = recursive
                    #Make sure you're not entering a possibly infinite loop (Left recursion bounding)
                    if childRule._A.get() == rule._A.get():
                        if childRecursion <= 2:
                            childRecursion += 1
                        else:
                            return trees
                        
                    if rule._alpha[childIndex].get() == childRule._A.get():
                        #to create the tree, other children should be basic tree nodes
                        otherChildren=self.otherChildrenTrees(rule, childIndex)
                        if otherChildren == []:
                            for tree in self.createTrees(childRule, childRecursion+1):
                                root = Tree.Tree("Complex", rule._A.myCopy(), rule, [tree], self)
                                trees.append(root)  
                        #for each possible combination of children:
                        else:
                            for singleOtherChildrenExp in otherChildren:
                                #add all current leftmostTrees to the list, under trees:
                                for tree in self.createTrees(childRule, childRecursion+1):
                                    allChildren=[]
                                    for childInSOC in singleOtherChildrenExp:
                                        allChildren.append(childInSOC.myCopy())
                                    allChildren.insert(childIndex,tree)
                                    root = Tree.Tree("Complex", rule._A.myCopy(), rule, allChildren, self)
                                    trees.append(root)  
        return trees
    
    def createTrees(self, rule, recursive=0):
        #if rule has only one child 
        if 1 == len(rule._alpha):
            if rule._alpha[0]._type=='Sigma':
                child = Tree.Tree("Basic", rule._alpha[0].myCopy(), (), [], self)
                root = Tree.Tree("Complex", rule._A.myCopy(), rule, [child], self)
                return [root]
#             else:
#                 print "rule._alpha[0]=",rule._alpha[0] 
#                 possibleChildrenTrees = self.generatingSetForObs([rule._alpha[0]])
#                 print "rule._alpha[0].GS:=",possibleChildrenTrees 
#                 possibleTrees = []
#                 for subTree in possibleChildrenTrees:
#                     root = Tree.Tree("Complex", rule._A, rule, [subTree], self)
#                     possibleTrees.append(root)
#                 return possibleTrees
                #return []
        
        #else, need to create all possible outcomes from tree
        trees=[]
        leftMostChilds = rule.leftMostChilds(byIndex=True)
        for childIndex in leftMostChilds:#range(len(rule._alpha)):
            #if childIndex in leftMostChilds:
            if type(rule._alpha[childIndex])==NT:
                #collect all possible derivations of this child to childTrees
                for childRule in self._P:
                    childRecursion = recursive
                    #Make sure you're not entering a possibly infinite loop (Left recursion bounding)
                    if childRule._A.get() == rule._A.get():
                        if childRecursion <= 2:
                            childRecursion += 1
                        else:
                            return trees
                        
                    if rule._alpha[childIndex].get() == childRule._A.get():
                        #to create the tree, other children should be basic tree nodes
                        otherChildren=self.otherChildrenTrees(rule, childIndex)
                        if otherChildren == []:
                            for tree in self.createTrees(childRule, childRecursion+1):
                                root = Tree.Tree("Complex", rule._A.myCopy(), rule, [tree], self)
                                trees.append(root)  
                        #for each possible combination of children:
                        else:
                            for singleOtherChildrenExp in otherChildren:
                                #add all current leftmostTrees to the list, under trees:
                                for tree in self.createTrees(childRule, childRecursion+1):
                                    allChildren=[]
                                    for childInSOC in singleOtherChildrenExp:
                                        allChildren.append(childInSOC.myCopy())
                                    allChildren.insert(childIndex,tree)
                                    root = Tree.Tree("Complex", rule._A.myCopy(), rule, allChildren, self)
                                    trees.append(root)  
        return trees
         
    def otherChildrenTrees(self, rule, specialChild):
        res=[]
        i = 0;
        for child in rule._alpha:
            if i != specialChild:
                listOfPossibleTrees = self.childWithPossibleRules(child)
                if res==[]:
                    res=listOfPossibleTrees
                else:
                    completeRes = []
                    for singleExp in res:
                        for newTree in listOfPossibleTrees:
                            newExp = singleExp  #myCopy - Removed
                            newExp.extend(newTree)
                            completeRes.append(newExp)   
                    res = completeRes  
            i += 1      
        return res   
 
    def childWithPossibleRules(self, child):
        res=[]
        if type(child)==Sigma.Sigma:
            res.append([Tree.Tree("Basic", child.myCopy(), (), PL=self)])
        else:
            childRules = []            
            for rule in self._P:    #Collect all possible rules this child might be
                if rule._A.get() == child.get():
                    childRules.append(rule)    
            res.append([Tree.Tree("Complex", child.myCopy(), childRules, PL=self)])
        return res 
 
#    def createPFFG(self):
#        PFFG=[]
#        gl=self.generatingSet()
#        for tree in gl:
#            s = tree.treeToList()
#            foot = tree.isLeftMostTree()
#            footIndex = s.index(foot)
#            s.remove(foot)
#             
#            #make constraints list according to list without the foot
#            
#            # Order Constraints
#            # simply don't add this constraint to the new list of constraints
#            if len(s) < 2:
#                order = []
#            #else
#            order = []
#            tempOrder = tree.treeConstraints()
#            for cons in tempOrder:
#                if cons[0] == footIndex or cons[1] == footIndex:
#                    continue
#                cons0 = (cons[0]-1 if cons[0] > footIndex else cons[0])
#                cons1 = (cons[1]-1 if cons[1] > footIndex else cons[1])
#                order.append((cons0, cons1))
#            
#            
#            # Parameter Constraints
#            paramCons = []
#            tempParams = tree.treeParamConstraints()
#            for cons in tempParams:
#                cons0 = (cons[0]-1 if cons[0] > footIndex else (cons[0] if cons[0] < footIndex else -2))
#                cons2 = (cons[2]-1 if cons[2] > footIndex else (cons[2] if cons[2] < footIndex else -2))
#                paramCons.append((cons0, cons[1], cons2, cons[3]))
#                                
#            #create the new rule for the PFFG
#            newRule = Rule.Y_Rule(foot, tree._root, s, order, paramCons, tree.getProbability())
#            PFFG.append(newRule)
#            
#        return PFFG