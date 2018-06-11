import os
from os import listdir
from os.path import isfile, join

from SymbolicPlanRecognition.CSQ_ran import CSQ
import SymbolicPlanRecognition.HSQ as HSQ
from SymbolicPlanRecognition.Parser import Parser
from SymbolicPlanRecognition.TreeNode import TreeNode
import SymbolicPlanRecognition.PathNode as PathNode

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

'''and "Domain-18." in file_name:'''

domains = {
           # 1: "full-20-1-5-1-2-3",
           # 2: "full-20-1-5-1-5-1",
           # 4: "full-20-1-5-3-2-1",
           # 5: "full-100",
           # 6: "1-5-2-3-2-full-100_baseline",
           7: "1-5-2-3-4-full-100_or",
           # 8: "1-5-2-5-2-full-100_and",
           # 9: "1-5-3-3-2-full-100_depth",
           }


input_folder_name = "/home/shachar-s/Dropbox/studies/ThirdYear/SBR_Project/SBR_git/SBR obs and domains/"
output_folder_name = "/home/shachar-s/Dropbox/studies/ThirdYear/SBR_Project/SBR_git/SBR obs and domains/SBR_OUTPUTS/"

all_obs = []


def main():
    for domain_name in domains.keys():
        if domain_name == 8:
            pass
        if not os.path.exists(output_folder_name + domains[domain_name]):
            os.makedirs(output_folder_name + domains[domain_name])
        onlyfiles = [join(input_folder_name + "Domains/" + domains[domain_name] + "/", f.replace("\\", "/")) for f in
                     listdir(input_folder_name + "Domains/" + domains[domain_name] + "/")
                     if isfile(join(input_folder_name + "Domains/" + domains[domain_name] + "/", f))]
        for file_name in onlyfiles:
            print file_name
            if file_name.endswith(".xml"):
                csq = CSQ()
                h = HSQ.HSQ()
                parser = Parser()
                run(file_name, file_name.replace("Domains", "Observations").replace("BaselineDomain", "Observations").
                    replace(".xml", ".txt"), csq, h, parser)


def run(domain_file_name, obs_file_name, csq, h, parser):
    root = parser.parse(domain_file_name)

    # get any node in the plan library
    plans = root.search()

    all_tags = read_obs_and_apply_csq(obs_file_name, plans, csq)

    # for each tag create path from obs to root
    map_of_paths = generate_paths_map(all_tags, root)

    all_paths = h.apply_hsq(map_of_paths)
    print all_paths

    root = TreeNode(0, "Root")
    final_root = unite_paths(all_paths, root)


def read_obs_and_apply_csq(obs_file_name, plans, csq):
    all_tags = []
    with open(obs_file_name) as obs_file:
        list_of_previous_tagged = []
        for row in obs_file:
            if row != "\n":
                ws = row.index(" ")
                t = int(row[0:ws])
                all_tags.append(t)
                label = row[ws + 1:]
                label = label.replace("\r", "").replace("\n", "")
                all_obs_current_tag = []
                all_obs.append(label)
                for plan_step in plans:
                    if plan_step.get_label() == label:
                        all_obs_current_tag.append(plan_step)
                list_of_previous_tagged = csq.apply_csq(all_obs_current_tag, t, list_of_previous_tagged)
    return all_tags


# create map from time-stamps to paths of each tagged node to the root
def generate_paths_map(all_tags, root):
    map_of_paths = {}
    for tag in all_tags:
        for child in root.get_children():
            if child.tagged(tag):
                leaves = child.get_leaves()
                paths = make_paths(leaves, tag)
                if tag in map_of_paths.keys():
                    map_of_paths[tag].extend(paths)
                else:
                    paths_to_put = paths
                    map_of_paths[tag] = paths_to_put
    print map_of_paths
    return map_of_paths


def make_paths(leaves, tag):
    paths = []
    for p in leaves:
        new_parent = None
        if p.tagged(tag):
            new_node = PathNode.PathNode(p)
            while p.parent() is not None:
                new_parent = PathNode.PathNode(p.parent())
                # if node has no next sequential nodes mark it as complete
                if not new_node.get_next_seqs():
                    new_node.set_complete(True)
                new_node.set_parent(new_parent)
                p = p.parent()
                new_node = new_parent
        if new_parent is not None:
            paths.append(new_parent)
    return paths


def unite_paths(all_exps, root):
    print len(all_exps)
    for exp in all_exps:
        exp_root = TreeNode(1, "expRoot")
        for tree in reversed(exp):
            tree = HSQ.path_string_to_path_plan[tree]
            exp_root = unite_path_with_current(tree, exp_root)
        root.add_child(exp_root)
    return root


def unite_path_with_current(path1, root):
    root_to_return = root
    while path1.get_child() is not None:
        path1_child = path1.get_child()
        root_child = None
        if root.get_children():
            root_child = root.get_children()[len(root.get_children()) - 1]
        if root_child is None or (path1_child is not None and root_child.get_label() != path1_child.get_label()) or \
                (path1_child is not None and root_child.get_label() != path1_child.get_label()
                 and (path1_child.get_ID() in root_child.get_seq())) or \
                (path1_child is not None and str(path1_child) == str(root_child)):
            root_child = root.add_child(TreeNode.get_from_path_node(path1_child))
        root = root_child
        path1 = path1_child
    return root_to_return


main()