from flask import g, request, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from ..models import User
from . import api
from .errors import error_response, forbidden , unauthorized
from app import db
from app.services.authenticate_user import AuthenticateUser
from app.lib.auth_token import AuthToken
from app.lib.json_request_body import JsonRequestBody
from app.services.verify_registration import VerifyRegistration

class NoTokenError(BaseException):
    pass

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')

@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password) and (user.confirmed == True):
        return user

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

@api.route('/auth/authenticate', methods=['POST'])
@basic_auth.login_required
def get_token():
    # POST /api/v1/auth/authenticate
    auth_user = AuthenticateUser.call(basic_auth.current_user())
    response = {'data': auth_user}
    return jsonify(response)

@token_auth.verify_token
def verify_token(token):
    if token == '':
        return None
        #raise NoTokenError()
    auth = AuthToken(token)
    return User.query.filter_by(email=auth.payload["email"]).first if auth else None
    #return to token_auth.current_user()

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)

@api.route('/auth/register', methods=['GET', 'POST'])
def register():
    # POST api/v1/auth/register

    request_data = JsonRequestBody.parse_json_from_request(request)
    VerifyRegistration(request_data).call()
    response = {
        "message": 'Verification email sent'
    }

    """
        rescue VerifyRegistration::InvalidRegistration => e
          routing.halt 400, { message: e.message }.to_json
        rescue VerifyRegistration::EmailProviderError
          routing.halt 500, { message: 'Error sending email' }.to_json
        rescue StandardError => e
          Api.logger.error "Could not verify registration: #{e.inspect}"
          routing.halt 500
    """

    return jsonify(response), 202


    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User(email=email,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = VerifyRegistration.generate_confirmation_token(email)
        Email.send(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

"""
@api.before_request
@basic_auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')"""
