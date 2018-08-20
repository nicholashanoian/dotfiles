git clone --depth=1 https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
chsh -s $(grep /zsh$ /etc/shells | tail -1)
