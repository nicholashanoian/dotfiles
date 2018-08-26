repoFolder="setup-repo"
scriptsFolder="setup-scripts"

git clone --bare https://github.com/nicholashanoian/dotfiles.git $HOME/$repoFolder
function config {
	/usr/bin/git --git-dir=$HOME/$repoFolder/ --work-tree=$HOME $@
}
config checkout -f master
config config status.showUntrackedFiles no
~/$scriptsFolder/confirm-logout.sh
~/$scriptsFolder/oh-my-zsh.sh


