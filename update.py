# Imports:
#Pyyaml library: "https://github.com/yaml/pyyaml/"
import yaml
#Allows me to remove pack.mcmeta
from os import remove, path, rename, mkdir
from os import path
#Import gitpython library: "https://gitpython.readthedocs.io/en/stable/"
from git import Git
import shutil
# Main function. Controls rest of file
def main():
    file = open("update.yml", "r")
    info = yaml.load(file, Loader=yaml.FullLoader)
    version = str(info['version'])
    mkdir(version)
    repo = info['github'][1]['repository']
    rungit(info['github'][0]['owner'], repo, version)
    writemcmeta(info['mcmeta'], repo, version)
    zip(str(repo), str(info['output'][0]['zipname']), version)
    updatepackversion(info)
    file.close()
    remove("update.yml")
    rename("update2.yml", "update.yml")

#Retrives repository from github
def rungit(owner, repo, version):
    dir_path = path.dirname(path.realpath(__file__))
    Git(dir_path + "/" + version + "/").clone("https://github.com/" + owner + "/" + repo + ".git")
#Writes mcmeta retrieved earlier
def writemcmeta(info2, repo, version):
    text = updatemcmeta(info2)
    remove(version + "/" + repo +"/pack.mcmeta")
    file2 = open(version + "/" + repo +"/pack.mcmeta", "a")
    file2.write(text)
    file2.close()
#Parses list into values    
def updatemcmeta(mcmeta):
    version = str(mcmeta[0]['packversion'])
    desc = str(mcmeta[1]['description'])
    update = ('{' + '\n' + '"pack": {\n"pack_format": ' + version + ',\n' + '"description": "' + desc + '"\n}\n}')
    return update
#Zips and packages folder for use
def zip(repo, zipName, version):
    shutil.make_archive(zipName, 'zip', path.dirname(path.realpath(__file__)) + "/" + version + "/" + repo)
#Updates folder version for next use (has to be deleted by an adminsistrator, not a script)
def updatepackversion(info):
    info['version'] = info['version'] + 1
    file2 = open("update2.yml", "a")
    file2.write(yaml.dump(info))
    file2.close()
#run script
main()