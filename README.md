# Flask-React-App
## Starting frontend
- Development:cd frontend && npm run start:development
- Production: cd frontend && npm start
## Starting backend
- cd backend && pipenv run flask run
## Github Workflow
### Pull to update local branch to include master
- git checkout master
- git pull
- git checkout 'local branch'
- git merge master
- handle merge conflicts to finish merge
### Pushing local changes
- git add 'files to add'
- git commit -m 'message'
- git push
- select on compare changes menu (base: master  compare: 'local branch name')
- create pull request on github and leave comments
- wait for 1 team member to approve
- merge changes
- delete local branch
