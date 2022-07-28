from flask import jsonify
from app import db
from app.controller import api
from app.controller.authentication import basic_auth, token_auth
from app.services.authenticate_user import AuthenticateUser

@api.route('/auth/authenticate', methods=['POST'])
@basic_auth.login_required
def get_token():
    # POST /api/v1/auth/authenticate
    auth_user = AuthenticateUser.call(basic_auth.current_user())
    response = {'data': auth_user}
    return jsonify(response)

@api.route('/auth/authenticate', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204