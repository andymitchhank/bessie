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

	def __init__(self, path='', **kwargs):
		self.path = path
		self.kwargs = kwargs
		self.__define_convenience_methods()
		self._prepare_request()
		
	@property
	def full_path(self):
		return parse.urljoin(self.base_url, self.path)
		
	def __getattr__(self, name):
		new_path = self.separator.join((self.path, name)) if self.path else name
		return self.__class__(new_path, **self.kwargs)

	def _find_endpoint(self, method):
		endpoint = None
		to_match = '{} {}'.format(method, self.path)

		for e in self.endpoints:
			if e.match_exact(to_match):
				endpoint = e

		if not endpoint:
			for e in self.endpoints:
				if e.match_with_path_params(to_match):
					endpoint = e

		if not endpoint:
			raise InvalidEndpointException('{} is not a valid endpoint.'.format(to_match))

		return endpoint
			
	def _prepare_request(self):
		self.request = requests.Request()
		
	def _send_request(self, method, **kwargs):
		endpoint = self._find_endpoint(method)
		endpoint.validate(kwargs)

		self.request.url = self.full_path
		self.request.method = method
		self.request.data = kwargs

		return requests.session().send(self.request.prepare())

	def __define_convenience_methods(self):
		actions = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']

		for action in actions:
			setattr(self, action.lower(), partial(self._send_request, action))


