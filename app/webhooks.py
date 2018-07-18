import hmac
import hashlib
from flask import request, Blueprint, jsonify, current_app
from git import Repo


webhook = Blueprint('webhook', __name__, url_prefix='')


@webhook.route('/github', methods=['POST'])
def handle_github_hook():
    """ Entry point for github webhook """

    signature = request.headers.get('X-Hub-Signature')
    sha, signature = signature.split('=')

    secret = str(current_app.config.get('GITHUB_SECRET'))
    hmac_object = hmac.new(secret, request.data, digestmod=hashlib.sha1)
    hashhex = hmac_object.hexdigest()
    if hmac.compare_digest(hashhex, str(signature)):
        repo = Repo(current_app.config.get('REPO_PATH'))
        origin = repo.remotes.origin
        origin.pull('--rebase')

        if request.json.get('after'):
        	commit = request.json['after'][0:6]
        	print('Repository updated with commit {}'.format(commit))

    return jsonify({}), 200
