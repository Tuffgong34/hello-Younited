# Younited App
The repository for the younited app. 

## Getting Started
You'll need Vagrant installed (see the Vagrant docs for how to do this). Navigate to the root dir of the repo and run 
`vagrant up`
This will create the virtual machine and install all necessary components. Then run:
`vagrant ssh`

I recommend running TMux using `tmux` and then the following commands

```
cd /vagrant
python3 main.py debug
```

On the host computer you should now be able to access the app by going to localhost:4500/profile - which should prompt to login or create an account.