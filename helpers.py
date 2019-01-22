import os

def create_subject_from_file(SUBJ):
    for i in os.listdir(os.getcwd() + '/outputs/'):
        if "SUBJ" not in i:
            os.rename(os.getcwd()+ "/outputs/" + i, os.getcwd()+ "/outputs/" + "SUBJ" + str(SUBJ) + "-" + i)
