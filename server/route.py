from server.Server import server, jsonifyPlus, request, User, userM
from flask import redirect, render_template
from flask_login import login_user, logout_user, login_required, current_user
from AppScanM import run_cmd

@server.route('/')
def home():
    '''home page'''
    return redirect('/apidocs')

@server.route('/users/<string:id>', methods=['POST'])
def register(id):
    """
    Register
    ---
    tags:
      - register
    
    produces: application/json,
    
    parameters:
    - name: id     
      in: path
      type: str
      required: false
      description: the user's id, will be key
    - name: username     
      in: query
      type: str
      required: false
      description: the user's name
    - name: password     
      in: query
      type: str
      required: false
      description: the user's password
    
    responses:
      401:
        description: "The email has be used."
      200:
        description: success register.
        example: "{'message':'admin register success.'}"
    """
    if userM.User.get(id): return jsonifyPlus({'message':f'user: {id} has been exist.'}),401
    username = request.values.get('username')
    password = request.values.get('password')
    userM.User(id,username,password)
    return jsonifyPlus({'message':f'{id} register success.'})

@server.route('/users/<string:id>', methods=['PUT'])
@login_required
def editUser(id):
    """
    Edit User
    ---
    tags:
      - edit user
    
    produces: application/json,
    
    parameters:
    - name: id     
      in: path
      type: str
      required: false
      description: the user's id, will be key
    - name: password    
      in: query
      type: str
      required: false
      description: old password
    - name: newpassword     
      in: query
      type: str
      required: false
      description: new password
    - name: name     
      in: query
      type: str
      required: false
      description: disply name
    
    responses:
      403:
        description: "old password error."
      200:
        description: success register.
        example: "{'message':'admin change password success.'}"
    """
    ID = id
    password = request.values.get('password')
    newpassword = request.values.get('newpassword')
    name = request.values.get('name')
    server.logger.debug(f'user:{ID}; oldPassw:{password}')
    message = ''

    userData:userM.User = userM.User.get(ID)
    if userData.PASSWORD != password: return jsonifyPlus({'message':f'user: {userData.ID} password error.'}),403
    
    if newpassword: userData.set(PASSWORD=newpassword); message += f'{id} change password success.\n'
    
    if name: userData.set(NAME=name); message += f'{id} change name success.\n'

    if message == '': message += f'{id} change nothing.\n'

    return jsonifyPlus({'message':message})

@server.route('/login', methods=['GET', 'POST'])
def login():
    """
    LOGIN
    ---
    tags:
      - login
    
    produces: application/json,
    
    parameters:
    - name: id     
      in: query
      type: str
      required: false
      description: the user's id
    - name: password     
      in: query
      type: str
      required: false
      description: the user's password
    
    responses:
      401:
        description: "Not find the user."
      403:
        description: "Password error."
      200:
        description: success login.
        example: "{'message':'admin login success.'}"
    """
    if request.method == 'GET':
        return render_template("/login.html")
    id = request.values.get('id')
    if not id in userM.User.USERS: return jsonifyPlus({'message':f'not find user: {id}.'}),401
    if not (request.values.get('password') == userM.User.USERS[id].PASSWORD):
        server.logger.error(f'{id} login fail with password error: {request.values.get("password")}')
        return jsonifyPlus({'message':f'{id} login fail with password error.'}),403
    USERDATA = userM.User.USERS[id]
    user = User(**USERDATA.__dict__)
    login_user(user)
    return jsonifyPlus({'message':f'{id} login success.'})
    

@server.route('/logout')
def logout():
    """
    LOGOUT
    ---
    tags:
      - logout
    
    produces: application/json,
    
    responses:
      200:
        description: success logout current user.
        example: "{'message':'admin logout success.'}"
    """
    id = current_user.get_id()
    logout_user()
    return jsonifyPlus({'message':f'{id} logout success.'})

@server.route('/testLogger')
def testLogger():
    """
    Test Logger
    ---
    tags:
      - test logger
    
    produces: application/json,
    
    responses:
      200:
        description: success logout current user.
        example: "{'message':'admin logout success.'}"
    """
    server.logger.info("Info message")
    server.logger.warning("Warning msg")
    server.logger.error("Error msg!!!")
    server.logger.debug("Debug msg!!!")

    return jsonifyPlus({'message':'test success.'})

@server.route('/command', methods=['POST'])
def command():
    """
    Command
    ---
    tags:
      - command
    
    produces: application/json,

    parameters:
    - name: command     
      in: query
      type: str
      required: false
      description: cmd command
    
    responses:
      200:
        description: success run command.
        example: "{'result':result}"
    """
    command = request.values.get('command')
    result = 'no command input'
    if command: result = run_cmd(command)

    return jsonifyPlus({'result':result})