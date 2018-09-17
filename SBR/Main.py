import os
from os import listdir
from os.path import isfile, join

import sys

from SymbolicPlanRecognition.Main import SymbolicPlanRecognition

# domains =
# "full-20-1-5-1-2-3",
# "full-20-1-5-1-5-1",
# "full-20-1-5-3-2-1",
# "full-100",
# "1-5-2-3-2-full-100_baseline",
# "1-5-2-3-4-full-100_or",
# "1-5-2-5-2-full-100_and",
# "1-5-3-3-2-full-100_depth",
# "duration_test",
# "interleaving_test"


def main():
    args = sys.argv
    domain_folder = args[1]
    tagging_type = args[2]
    onlyfiles = [join(domain_folder, f.replace("\\", "/")) for f in
                 listdir(domain_folder)
                 if isfile(join(domain_folder, f))]
    onlyfiles = [file1 for file1 in onlyfiles if file1.endswith(".xml")]
    if tagging_type == '--Duration':
        plan_recognizer = SymbolicPlanRecognition(duration=True)
    elif tagging_type == '--Interleaving':
        plan_recognizer = SymbolicPlanRecognition(interleaving=True)
    else:
        plan_recognizer = SymbolicPlanRecognition()
    for domain_file in onlyfiles:
        print domain_file
        plan_recognizer.set_domain(domain_file)
        obs_file = domain_file.replace("/Domains/", "/Observations/").replace("BaselineDomain", "Observations").\
            replace(".xml", ".txt")
        run(plan_recognizer, obs_file)


def run(plan_recognizer, obs_file_name):

    read_obs_and_apply_csq(obs_file_name, plan_recognizer)

    all_paths = plan_recognizer.apply_hsq()
    all_paths_string = all_paths.__repr__()
    all_paths_string = all_paths_string.replace(',', ',\n')
    print all_paths_string, '\n'


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
