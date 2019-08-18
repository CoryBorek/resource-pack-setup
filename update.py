# Imports:
#Pyyaml library: "https://github.com/yaml/pyyaml/"
import yaml
#Allows me to remove pack.mcmeta
from os import remove, path, rename, mkdir, system
from os import path
#Import gitpython library: "https://gitpython.readthedocs.io/en/stable/"
# Main function. Controls rest of file
def main():
    file = open("update.yml", "r")
    info = yaml.load(file, Loader=yaml.FullLoader)
    repo = info['github'][1]['repository']
    rungit(info['github'][0]['owner'], repo)
    writemcmeta(info['mcmeta'], repo,)
    file.close()
    zip(str(repo), str(info['output'][0]['zipname']))

#Retrives repository from github
def rungit(owner, repo):
    dir_path = path.dirname(path.realpath(__file__))
    if (path.isdir(dir_path + "/" + repo)):
        system("cd " + dir_path + "/" + repo)
        system("git pull")
        system("cd ../")
    else:
        system("git clone https://github.com/" + owner + "/" + repo + ".git")
#Writes mcmeta retrieved earlier
def writemcmeta(info2, repo):
    text = updatemcmeta(info2)
    remove(repo +"/pack.mcmeta")
    file2 = open(repo +"/pack.mcmeta", "a")
    file2.write(text)
    file2.close()
#Parses list into values    
def updatemcmeta(mcmeta):
    version = str(mcmeta[0]['packversion'])
    desc = str(mcmeta[1]['description'])
    update = ('{' + '\n' + '"pack": {\n"pack_format": ' + version + ',\n' + '"description": "' + desc + '"\n}\n}')
    return update
#Zips and packages folder for use
def zip(repo, zipName):
    system("cd " + repo + "/")
    system("git archive --format zip --output " + zipName + ".zip master")
#run script
main()