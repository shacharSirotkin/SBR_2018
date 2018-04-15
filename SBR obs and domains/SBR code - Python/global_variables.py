number_of_node_creations = 0
list_of_node_creations = []

def increment_number_of_node_creations():
    global number_of_node_creations
    number_of_node_creations += 1


def add_to_list_of_node_creations(x):
    list_of_node_creations.append(x)
