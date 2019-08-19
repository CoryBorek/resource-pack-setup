# Imports:
#Pyyaml library: "https://github.com/yaml/pyyaml/"
import yaml
#Allows me to remove pack.mcmeta
from os import remove, path, rename, mkdir, system
from pathlib import Path
#Import gitpython library: "https://gitpython.readthedocs.io/en/stable/"
# Main function. Controls rest of file
def main():
    file = open("config.yml", "r")
    info = yaml.load(file, Loader=yaml.FullLoader)
    repo = info['github'][1]['repository']
    rungit(info['github'][0]['owner'], repo)
    writemcmeta(info['mcmeta'], repo,)
    file.close()
    if(str(info['mcmeta'][2]['doversion']) == "true"):
        info['mcmeta'][3]['version'] = info['mcmeta'][3]['version'] + 1
        upload = open("config2.yml", "a")
        upload.write(yaml.dump(info))
        upload.close()
        remove("config.yml")
        rename("config2.yml", "config.yml")
    zip(str(repo), str(info['output'][0]['zipname']))

#Retrives repository from github
def rungit(owner, repo):
    dir_path = path.dirname(path.realpath(__file__))
    if (path.isdir(dir_path + "/" + repo)):
        system("cd " + repo + "&& git pull")
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
    version2 = str(mcmeta[3]['version'])
    if(str(mcmeta[2]['doversion']) == "true"):
        update = ('{' + '\n' + '"pack": {\n"pack_format": ' + version + ',\n' + '"description": "' + desc + version2 + '"\n}\n}')
    else:    
        update = ('{' + '\n' + '"pack": {\n"pack_format": ' + version + ',\n' + '"description": "' + desc + '"\n}\n}')
    return update
#Zips and packages folder for use
def zip(repo, zipName):
    if(Path(zipName + ".zip").exists()):
        rename(zipName + ".zip", zipName + "2.zip")
        remove(zipName + "2.zip")
    system("cd " + repo +'&& git add -A && git commit -m "Updating Pack"&& git archive --format zip --output ' + zipName + '.zip master && rename "' + zipName + '.zip" "../' + zipName + '.zip"')
#run script
main()