### Test Locally
There is one single API secured using default permission
#### Prerequisites
- Start-up easyauth server exploiting docker (it is a module within docker compose)
- Build the exp module thorugh poetry for installing the needed dependencies to make easyauth client work
#### Do it
- Configure group associated to default permissions: Modify line 15 of _exp>exp>main.py_
- Create a user on the easyauth server belonging to the above mentioned group.<br />You can access to the easyauth server  on port 5003 (you have to access with an admin account)
- Launch the easyauth client<br />`poetry run uvicorn exp.main:server --host 0.0.0.0 --port 8080`
- Try accessing the following endpoint authenticating as the above mentioned user<br />_localhost:8080/default_

Only the users belonging to the above mentioned group should access the endpoint (receiving a dummy message as response). All the others should receive forbidden as response.
