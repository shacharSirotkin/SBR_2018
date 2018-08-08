from SymbolicPlanRecognition import NodeFactory
from TreeNode import TreeNode
import xml.etree.ElementTree as Et


class Parser(object):
    def __init__(self, node_creator):
        self._id_counter = 0
        self._hmap = {}
        self._goals = []
        self._recipes = []
        self._doc = None
        self._nodeFactory = node_creator

    def parse(self, path):
        root = TreeNode(self.generate_ID(), "root")
        root.set_root(True)
        tree = Et.parse(path)
        self._doc = tree.getroot()
        self.read_non_terminal_letters(root)
        self.read_recipes(root)
        return root

    def read_non_terminal_letters(self, root):
        non_terminal_letters = self._doc.find("Letters").find("Non-Terminals").findall("Letter")
        # find root's children (those with the attribute 'goal = yes' in the xml)
        for letter in non_terminal_letters:
            if letter.get("goal") == "yes":
                self._goals.append(letter.get("id"))
                # TODO:this is the critical section. The node creator should create a node with the right properties
                p = self._nodeFactory(self.generate_ID(), letter.get("id"))
                root.add_child(p)
                self._hmap[letter.get("index")] = p

    def read_recipes(self, root):
        recipes_as_node_list = self._doc.find("Recipes").findall("Recipe")
        for i in recipes_as_node_list:
            self._recipes.append(i)
        # run over each recipe till find a recipe start with an existing node in the PL
        # when an existing node is found, create its children and their sequential connections
        while self._recipes:
            recipe = self._recipes.pop(0)
            if root.find_by_label(recipe.get("lhs")) is not None:
                p = root.find_by_label(recipe.get("lhs"))
            else:
                self._recipes.insert(len(self._recipes), recipe)
                continue
            # create node's children according to recipe
            self.read_single_recipe(recipe, p)
            # create node's children's sequential connections according to recipe
            self.read_order_cons(recipe)

    # create node's children according to recipe
    def read_single_recipe(self, recipe, p):
        letters = recipe.findall("Letter")
        for letter in letters:
            id = self.generate_ID()
            child = self._nodeFactory(self.generate_ID(), letter.get("id"))
            p.add_child(child)
            self._hmap[letter.get("index")] = child

    # create node's children's sequential connections according to recipe, adding interleaving ability
    def read_interleaving_order_cons(self, recipe):
        order = recipe.find("Order")
        if order is not None:
            order_conses = order.findall("OrderCons")
            for order_cons in order_conses:
                p = self._hmap[order_cons.get("firstIndex")]
                self._hmap[order_cons.get("secondIndex")].add_seq_of(p.get_ID(), p)
                self._hmap[order_cons.get("secondIndex")].set_first_sequential(p.get_first_sequential())

    # create node's children's sequential connections according to recipe
    def read_order_cons(self, recipe):
        order = recipe.find("Order")
        if order is not None:
            order_conses = order.findall("OrderCons")
            for order_cons in order_conses:
                p = self._hmap[order_cons.get("firstIndex")]
                self._hmap[order_cons.get("secondIndex")].add_seq_of(p.get_ID(), p)

    # create node's children's sequential connections according to recipe, adding duration ability
    def read_duration_order_cons(self, recipe):
        order = recipe.find("Order")
        if order is not None:
            order_conses = order.findall("OrderCons")
            for order_cons in order_conses:
                p = self._hmap[order_cons.get("firstIndex")]
                self._hmap[order_cons.get("secondIndex")].add_seq_of(p.get_ID(), p)

    def generate_ID(self):
        self._id_counter += 1
        return self._id_counter
