git clone --bare https://github.com/nicholashanoian/dotfiles.git $HOME/nhh-kde
function config {
	/usr/bin/git --git-dir=$HOME/nhh-kde/ --work-tree=$HOME $@
}
config checkout -f master
config config status.showUntrackedFiles no
