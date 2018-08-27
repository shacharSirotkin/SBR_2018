# create node's children's sequential connections according to recipe, adding interleaving ability
def read_interleaving_order_cons(recipe_dict, recipe):
    order = recipe.find("Order")
    if order is not None:
        order_conses = order.findall("OrderCons")
        for order_cons in order_conses:
            p = recipe_dict[order_cons.get("firstIndex")]
            recipe_dict[order_cons.get("secondIndex")].add_seq_of(p.get_ID(), p)
            recipe_dict[order_cons.get("secondIndex")].set_first_sequential(p.get_first_sequential())


# create node's children's sequential connections according to recipe
def read_order_cons(recipe_dict, recipe):
    order = recipe.find("Order")
    if order is not None:
        order_conses = order.findall("OrderCons")
        for order_cons in order_conses:
            p = recipe_dict[order_cons.get("firstIndex")]
            recipe_dict[order_cons.get("secondIndex")].add_seq_of(p.get_ID(), p)
