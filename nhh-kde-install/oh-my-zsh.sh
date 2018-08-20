sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
git --git-dir=$HOME/nhh-kde/ --work-tree=$HOME checkout -- ~/.zshrc
