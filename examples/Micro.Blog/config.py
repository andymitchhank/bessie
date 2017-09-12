from bessie import Endpoint

endpoints = {
	'POST': {
		'account/signin': None,
		'posts/favorites': None,
		'posts/reply': None,
		'users/follow': None,
		'users/unfollow': None,
		'micropub': None
	},
	'GET': {
		'posts/all': None,
		'posts/mentions': None,
		'posts/favorites': None,
		'posts/<username>': None,
		'posts/conversation': ['id'],
		'posts/check': ['since_id']
	},
	'DELETE': {
		'posts/favorites/<id>': None,
		'posts/<id>': None
	}
}

available_endpoints = [Endpoint(method, path, params) for method, paths in endpoints.items()
										   			  for path, params in paths.items()]
