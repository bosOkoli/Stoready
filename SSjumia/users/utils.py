from flask import url_for
import ezgmail




def send_reset_email(user):
    token=user.get_reset_token()
    msg_body=f'''To reset your password visit the following link:
    {url_for('users.reset_token',token=token,_external=True)}
    
    If you didn't make this this request you can ignore and no changes will be made.'''
    ezgmail.send(user.email,'Reset Password',msg_body)