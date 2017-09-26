from functools import partial
import requests

try:
	import urlparse as parse
except:
	from urllib import parse


class InvalidEndpointException(Exception):
	pass


class BaseClient(object):
	
	endpoints = []
	separator = '/'
	base_url = ''

	def __init__(self, path='', path_params=None, **kwargs):
		self.path = path
		self.path_params = path_params
		if not self.path_params:
			self.path_params = {}

		self.kwargs = kwargs
		self.__define_convenience_methods()
		self._prepare_request()
		
	def __call__(self, value):
		path_param_key = self.path.split(self.separator)[-1]
		self.path_params[path_param_key] = str(value)
		return self
		
	def __getattr__(self, name):
		new_path = self.separator.join((self.path, name)) if self.path else name
		return self.__class__(new_path, self.path_params, **self.kwargs)

	def _find_endpoint(self, method):
		endpoint = None
		to_match = '{} {}'.format(method, self.path)

		for e in self.endpoints:
			if e.match(to_match):
				endpoint = e

		if not endpoint:
			raise InvalidEndpointException('{} is not a valid endpoint.'.format(to_match))

		return endpoint
			
	def _prepare_request(self):
		self.request = requests.Request()

	def _finalize_request(self, method, **kwargs):
		endpoint = self._find_endpoint(method)
		endpoint.validate(kwargs, self.path_params)

		url = parse.urljoin(self.base_url, endpoint.path)

		for param, value in self.path_params.items():
			url = url.replace('<{}>'.format(param), value)

		self.request.url = url
		self.request.method = method
		self.request.data = kwargs
		
	def _send_request(self, method, **kwargs):
		self._finalize_request(method, **kwargs)
		return requests.session().send(self.request.prepare())

	def __define_convenience_methods(self):
		actions = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']

		for action in actions:
			setattr(self, action.lower(), partial(self._send_request, action))


