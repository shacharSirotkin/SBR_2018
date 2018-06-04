import os
import csv
from os import listdir
from os.path import isfile, join
import CSQ
import HSQ
import Parser
import PathNode
import TreeNode
import Visualizer
import global_variables
import time
import os


os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

'''and "Domain-18." in file_name:'''

domains = {1 : "full-20-1-5-1-2-3",
               2 : "full-20-1-5-1-5-1",
               4 : "full-20-1-5-3-2-1",
               5 : "full-100",
               6 : "1-5-2-3-2-full-100_baseline",
               7 : "1-5-2-3-4-full-100_or",
               8 : "1-5-2-5-2-full-100_and",
               9: "1-5-3-3-2-full-100_depth",
               # 10: "temp"
               }

input_folder_name = "/home/shachar-s/Dropbox/studies/ThirdYear/SBR_Project/SBR_git/standardization/"
output_folder_name = "/home/shachar-s/Dropbox/studies/ThirdYear/SBR_Project/SBR_git/standardization/SBR_OUTPUTS/"

all_obs = []

def main():
    for domain_name in domains.keys():
        if domain_name == 8:
            pass
        if not os.path.exists(output_folder_name + domains[domain_name]):
            os.makedirs(output_folder_name + domains[domain_name])
        csv_file = open(output_folder_name + domains[domain_name] + "/" + domains[domain_name] + "profile - time - SBR.csv", "wb")
        new_csv_reading_time = csv.writer(csv_file, delimiter=',', quotechar='"')
        new_csv_reading_time.writerow(["file name","domain reading time","observations reading time"])
        onlyfiles = [join(input_folder_name + "Domains/" + domains[domain_name] + "/", f.replace("\\","/")) for f in
                     listdir(input_folder_name + "Domains/" + domains[domain_name] + "/") if isfile(join(input_folder_name + "Domains/" + domains[domain_name] + "/", f))]
        for file_name in onlyfiles:
            print file_name
            if file_name.endswith(".xml"):
                csq = CSQ.CSQ()
                h = HSQ.HSQ()
                parser = Parser.Parser()
                run(file_name, file_name.replace("Domains", "Observations").replace("BaselineDomain", "Observations").replace(".xml", ".txt"), csq, h, parser, new_csv_reading_time, output_folder_name + domains[domain_name])

def run(domain_file_name, obs_file_name, csq, h, parser, writer, folder_name):
    global_variables.list_of_node_creations = []
    start_time_domain = float("%.20f" % time.time())
    root = parser.parse(domain_file_name)
    end_time_domain = float("%.20f" % time.time())

    plans = root.search()

    start_time_obs = float("%.20f" % time.time())
    allTags = read_obs_and_apply_CSQ(obs_file_name, plans, csq)
    end_time_obs = float("%.20f" % time.time())

    PL_tree_depth = depth_of_PL(root)

    obs_domain_and_number = obs_file_name.replace(".txt", "").replace("\\","/").split("/")
    pdf_file_name = folder_name + "/" + obs_domain_and_number[len(obs_domain_and_number) - 2] + obs_domain_and_number[len(obs_domain_and_number) - 1] + ".pdf"
    xml_file_name = folder_name + "/" + obs_domain_and_number[len(obs_domain_and_number) - 2] + obs_domain_and_number[len(obs_domain_and_number) - 1] + ".xml"

    map_of_paths = generate_paths_map(allTags, root)
    all_paths = h.hsq(map_of_paths)
    print all_paths


    vizualise_and_write_to_xml(all_paths, pdf_file_name, xml_file_name)

    writer.writerow([obs_domain_and_number[len(obs_domain_and_number) - 2] + obs_domain_and_number[len(obs_domain_and_number) - 1],
                      str(end_time_domain - start_time_domain),str(end_time_obs - start_time_obs),str(global_variables.list_of_node_creations), len(all_paths)])

    global_variables.number_of_node_creations = 0

def make_paths(leaves, tag):
    paths = []
    for p in leaves:
        new_parent = None
        if p.tagged(tag):
            new_node = PathNode.PathNode(p)
            while p.parent() != None:
                new_parent = PathNode.PathNode(p.parent())
                if new_node.get_seq() == []:
                    new_node.set_complete(True)
                new_node.set_parent(new_parent)
                p = p.parent()
                new_node = new_parent
        if new_parent != None:
            paths.append(new_parent)
    return paths

def read_obs_and_apply_CSQ(obs_file_name, plans, csq):
    global_variables.add_to_list_of_node_creations(global_variables.number_of_node_creations)
    global_variables.number_of_node_creations = 0
    all_tags = []
    with open(obs_file_name) as f:
        list_of_previous_tagged = []
        obsNum = 1
        for row in f:
            global_variables.add_to_list_of_node_creations(global_variables.number_of_node_creations)
            global_variables.number_of_node_creations = 0
            obsNum += 1
            #if obsNum == 2:
            #global_variables.set_passed_one_obs(True)
            if row != "\n":
                ws = row.index(" ")
                t = int(row[0:ws])
                all_tags.append(t)
                label = row[ws + 1:]
                label = label.replace("\r", "").replace("\n", "")
                all_obs_current_tag = []
                all_obs.append(label)
                for tmp in plans:
                    if tmp.get_label() == label:
                        all_obs_current_tag.append(tmp)
                list_of_previous_tagged = csq.csq(all_obs_current_tag, t, list_of_previous_tagged)
    return all_tags

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

def depth_of_PL(root):
    depth = 0
    root_check_depth = root
    while root_check_depth.is_not_leaf():
        root_check_depth = root_check_depth.first_child_of_node()
        depth +=1
    return depth

def vizualise_and_write_to_xml(all_paths, visualize_file_name, xml_file_name):
    root = TreeNode.TreeNode(0, "Root")
    final_root = unite_paths(all_paths, root)
    #Visualizer.make_tree_graph(final_root, visualize_file_name)
    #Xml_output_writer.xml_writer(final_root, xml_file_name)

def unite_paths(all_exps, root):
    print len(all_exps)
    for exp in all_exps:
        exp_root = TreeNode.TreeNode(1, "expRoot")
        for tree in reversed(exp):
            tree = HSQ.path_string_to_path_plan[tree]
            exp_root = unite_path_with_current(tree, exp_root)
        root.add_child(exp_root)
    return root

def unite_path_with_current(path1, root):
    root_to_return = root
    while path1.get_child() != None:
        path1_child = path1.get_child()
        root_child = None
        if root.get_children() != []:
            root_child = root.get_children()[len(root.get_children()) - 1]
        if root_child == None or (path1_child != None and root_child.get_label() != path1_child.get_label()) or \
            (path1_child != None and root_child.get_label() != path1_child.get_label() and (path1_child.get_ID() in root_child.get_seq())) or \
                (path1_child != None and str(path1_child) == str(root_child)):
            root_child = root.add_child(TreeNode.TreeNode.get_from_path_node(path1_child))
        root = root_child
        path1 = path1_child
    return root_to_return

main()
