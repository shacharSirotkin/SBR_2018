import os
from os import listdir
from os.path import isfile, join

from SymbolicPlanRecognition.Main import SymbolicPlanRecognition

domains = {
           # 1: "full-20-1-5-1-2-3",
           # 2: "full-20-1-5-1-5-1",
           # 4: "full-20-1-5-3-2-1",
           # 5: "full-100",
           # 6: "1-5-2-3-2-full-100_baseline",
           # 7: "1-5-2-3-4-full-100_or",
           # 8: "1-5-2-5-2-full-100_and",
           # 9: "1-5-3-3-2-full-100_depth",
            1: "test"
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
        onlyfiles = [file1 for file1 in onlyfiles if file1.endswith(".xml")]
        for domain_file in onlyfiles:
            print domain_file
            plan_recognizer = SymbolicPlanRecognition(domain_file)
            obs_file = domain_file.replace("Domains", "Observations").replace("BaselineDomain", "Observations").\
                replace(".xml", ".txt")
            run(plan_recognizer, obs_file)


def run(plan_recognizer, obs_file_name):

    read_obs_and_apply_csq(obs_file_name, plan_recognizer)

    all_paths = plan_recognizer.apply_hsq()
    all_paths_string = all_paths.__repr__()
    all_paths_string = all_paths_string.replace(',', ',\n')
    print all_paths_string


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


main()
