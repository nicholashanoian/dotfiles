"""Nicholas Hanoian
Written 8/19/2018

Use this script to add ssh keys to github and gitlab. Run with 'hub'
argument to only add github, and 'lab' argument to only add gitlab. No
argument runs both github and gitlab.

"""

import requests
import os
import getpass
import sys
import json

username = 'nicholashanoian'

def gitlab_get_token (username,password):
    """Get auth token from gitlab. Used in gitlab_add_key to
    to add ssh key to account.
    """
    payload = {
        "grant_type" : "password",
        "username" : username,
        "password" : password
    }

    response = requests.post('https://gitlab.com/oauth/token',data=payload)
    if response.status_code == requests.codes.ok:
        data = response.json()
        token = data['access_token']
        return token
    else:
        print('Gitlab failed. Error:',response.text)
        return ''




def gitlab_add_key (token,title,ssh_key):
    """
    Add ssh key to gitlab. Token authentication required.
    See https://docs.gitlab.com/ee/api/users.html#add-ssh-key for details.
    """

    # for authentication
    params = {'access_token':token}
    payload = {
        'title':title,
        'key':ssh_key
    }
    response = requests.post('https://gitlab.com/api/v4/user/keys',data=payload,params=params)
    return response
    
        


def github_add_key (username,password,title,ssh_key):
    """
    Add ssh key to github. Uses username and password.
    See https://developer.github.com/v3/users/keys/ for details.
    """
    payload = {
        'title':title,
        'key':ssh_key
    }
    # post request to add key. json.dumps(payload) is needed or the response fails
    # citing bad json
    response = requests.post('https://api.github.com/user/keys',auth=(username,password),data=json.dumps(payload))
    return response


def response_feedback(platform, response):
    """
    Give feedback to see whether key was added successfully.
    201 is the success code for both github and gitlab.
    """
    if response.status_code == 201:
        print(platform, 'key successfully added.')
    else:
        # response.text is the json response of the failed request
        print(platform,'failed. Error:',response.text)
    
def main(arg):

    should_generate = ''
    success = False
    # get ssh key from file
    while success == False and should_generate != 'n':
        
        try:
            f=open(os.path.expanduser('~/.ssh/id_rsa.pub'))
            ssh_key=f.read().strip() # complained about bad json without strip()
            f.close()
            success = True
        except FileNotFoundError: # if file is not found
            # ask to generate ssh key with ssh-keygen command
            should_generate = input("~/.ssh/id_rsa.pub not found. Generate key? [y/n] ").lower()
            if should_generate == 'y':
                # function found on stackoverflow
                def cmd(cmd):
                    cmd = cmd.split()
                    code = os.spawnvpe(os.P_WAIT, cmd[0], cmd, os.environ)
                    if code == 127:
                        sys.stderr.write('{0}: command not found\n'.format(cmd[0]))
                    return code
                code = cmd('ssh-keygen')
                if code == 0:
                    print('SSH key generated. Continuing.\n')
                else:
                    sys.exit('Failed to generate SSH Key')

    if success == True:
        
        # get title to use for ssh key
        title = ''
        while not title:
            title = input('Computer name: ')

        # For only adding gitlab key
        if (arg != 'hub'):
            print('Adding gitlab key.')
            # get password from user
            gitlab_password = getpass.getpass("Gitlab Password: ")
            gitlab_token = gitlab_get_token(username,gitlab_password)
            if gitlab_token: # if we got token successfully
                gitlab_response = gitlab_add_key(gitlab_token,title,ssh_key)
                response_feedback('Gitlab',gitlab_response)

        # for only adding github key
        if (arg != 'lab'):
            print('Adding github key.')
            github_password = getpass.getpass("Github Password: ")
            github_response = github_add_key(username,github_password,title,ssh_key)
            response_feedback('Github',github_response)
    
    
if __name__ == '__main__':
    # if an argument is passed in for adding to just one site
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        # validate
        if not(arg == 'lab' or arg == 'hub'):
            print(arg, 'is not a valid option.')
            print('Valid options are "hub" to only add github key, "lab" to only add gitlab key,\nor no argument to add both.')
        # if valid, run with argument
        else:
            main(sys.argv[1])
    # if no argument, add to both sites
    else:
        main('')
