from SymbolicPlanRecognition import NodeFactory
from TreeNode import TreeNode
import xml.etree.ElementTree as Et


class Parser(object):
    def __init__(self, interleaving=False, duration=False, self_cycle=False):
        self._id_counter = 0
        self._hmap = {}
        self._goals = []
        self._recipes = []
        self._doc = None
        if interleaving:
            self._read_orders = self.read_interleaving_order_cons
            self._creator = NodeFactory.create_interleaving_tree_node
        else:
            self._read_orders = self.read_order_cons
            self._creator = NodeFactory.create_tree_node

    def parse(self, path):
        root = TreeNode(self.generate_ID(), "root")
        root.set_root(True)
        tree = Et.parse(path)
        self._doc = tree.getroot()
        # find root's children, those with the attribute 'goal = yes' in the xml
        self.read_non_terminal_letters(root)
        self._hmap.clear()
        self.read_recipes(root)
        self._set_all_self_cycles(root)
        return root

    def read_non_terminal_letters(self, root):
        non_terminal_letters = self._doc.find("Letters").find("Non-Terminals").findall("Letter")
        for letter in non_terminal_letters:
            if letter.get("goal") == "yes":
                self._goals.append(letter.get("id"))
                p = TreeNode(self.generate_ID(), letter.get("id"))
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
            ID = self.generate_ID()
            child = TreeNode(ID, letter.get("id"))
            p.add_child(child)
            self._hmap[letter.get("index")] = child

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

    def _set_all_self_cycles(self, root):
        next_seqs = root.get_next_seqs()
        children = root.get_children()
        if not next_seqs:
            if not children:
                return 1
            else:
                return max([self._set_all_self_cycles(child) for child in children])
        else:
            self.calc_seq_chain_size(root)
            return sum()

        # children_self_cycles = sum([child._self_cycle_limitation for child in children])
        # seq_path_len = self.calc_seq_path_len(root)
        # root.set_self_cycle_limitation()

    def calc_seq_chain_size(self, root):
        seqs_sizes = []
        if not root.get_next_seqs():
            return 0
        for seq in root.get_next_seqs():
            seqs_sizes.append(self._set_all_self_cycles(seq))
        max_seq = max(seqs_sizes)
        seqs_sizes = [max_seq]
        return max([self.calc_seq_chain_size(seq) for seq in root.get_next_seqs()])