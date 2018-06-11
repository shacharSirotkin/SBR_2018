import os
from os import listdir
from os.path import isfile, join

import SymbolicPlanRecognition.HSQ as HSQ
from SymbolicPlanRecognition.Main import SymbolicPlanRecognition
from SymbolicPlanRecognition.TreeNode import TreeNode
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


def main():
    for domain_name in domains.keys():
        if domain_name == 8:
            pass
        if not os.path.exists(output_folder_name + domains[domain_name]):
            os.makedirs(output_folder_name + domains[domain_name])
        onlyfiles = [join(input_folder_name + "Domains/" + domains[domain_name] + "/", f.replace("\\", "/")) for f in
                     listdir(input_folder_name + "Domains/" + domains[domain_name] + "/")
                     if isfile(join(input_folder_name + "Domains/" + domains[domain_name] + "/", f))]
        for domain_file in onlyfiles:
            print domain_file
            if domain_file.endswith(".xml"):
                plan_recognizer = SymbolicPlanRecognition(domain_file)
                obs_file = domain_file.replace("Domains", "Observations").replace("BaselineDomain", "Observations").\
                    replace(".xml", ".txt")
                run(plan_recognizer, obs_file)


def run(plan_recognizer, obs_file_name):

    read_obs_and_apply_csq(obs_file_name, plan_recognizer)

    all_paths = plan_recognizer.apply_hsq()
    print all_paths

    root = TreeNode(0, "Root")
    final_root = unite_paths(all_paths, root)


def read_obs_and_apply_csq(obs_file_name, plan_recognizer):
    with open(obs_file_name) as obs_file:
        for row in obs_file:
            if row != "\n":
                ws = row.index(" ")
                t = int(row[0:ws])
                label = row[ws + 1:]
                label = label.replace("\r", "").replace("\n", "")
                current_optional_obs = plan_recognizer.match(label)
                plan_recognizer.apply_csq(current_optional_obs, t)


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
