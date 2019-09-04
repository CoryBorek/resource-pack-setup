# Imports:
#Pyyaml library: "https://github.com/yaml/pyyaml/"
import yaml
#Allows me to remove pack.mcmeta
from os import remove, path, rename, mkdir, system
from pathlib import Path
#Import gitpython library: "https://gitpython.readthedocs.io/en/stable/"
# Main function. Controls rest of file
def main():
	settingsfile = open("settings.yml", "r")
	settings = yaml.load(settingsfile, Loader=yaml.FullLoader)
	print(settings)
	config = input("Name your configuration file: " )
	file = open(str(settings['config-folder']) + config,"r")
	info = yaml.load(file, Loader=yaml.FullLoader)
	repo = info['github'][1]['repository']
	rungit(info['github'][0]['owner'], repo)
	writemcmeta(info['mcmeta'], repo,)
	file.close()
	if(str(info['mcmeta'][2]['doversion']) == "true"):
		info['mcmeta'][3]['version'] = info['mcmeta'][3]['version'] + 1
		upload = open(str(settings['config-folder']) + "config2.yml", "a")
		upload.write(yaml.dump(info))
		upload.close()
		remove(str(settings['config-folder']) + config)
		rename(str(settings['config-folder']) + "config2.yml", str(settings['config-folder']) + config)
	zip(str(repo), str(info['output'][0]['zipname']), settings)
	settingsfile.close()

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
def zip(repo, zipName, settings):
	if(str(settings['output-all-folder']) == 'true'):
		outputfolder = str(settings['output-folder'])
		if(Path(outputfolder + zipName + ".zip").exists()):
			rename(outputfolder + zipName + ".zip",outputfolder + zipName + "2.zip")
			remove(outputfolder +zipName + "2.zip")
		system("cd " + repo +'&& git add -A && git commit -m "Updating Pack"&& git archive --format zip --output ' + zipName + '.zip master && rename "' + zipName + '.zip" "' + outputfolder + zipName + '.zip"')
	else:
		if(Path(zipName + ".zip").exists()):
			rename(zipName + ".zip", zipName + "2.zip")
			remove(zipName + "2.zip")
		system("cd " + repo +'&& git add -A && git commit -m "Updating Pack"&& git archive --format zip --output ' + zipName + '.zip master && rename "' + zipName + '.zip" "../' + zipName + '.zip"')
#run script
main()