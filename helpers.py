import os

def create_subject_from_file(SUBJ):
    for i in os.listdir(os.getcwd() + '/outputs/'):
        if "SUBJ" not in i:
            os.rename(os.getcwd()+ "/outputs/" + i, os.getcwd()+ "/outputs/" + "SUBJ" + str(SUBJ) + "-" + i)



def make_next():
    last = 0
    try:
        (os.listdir(os.getcwd() + '/outputs/')[0].split('-')[0].split('SUBJ')[1])
    except IndexError:
        return 0
    for i in range(len(os.listdir(os.getcwd() + '/outputs/'))):
        if last <= int(os.listdir(os.getcwd() + '/outputs/')[i].split('-')[0].split('SUBJ')[1]):
            last = int(os.listdir(os.getcwd() + '/outputs/')[i].split('-')[0].split('SUBJ')[1])
    return last + 1
