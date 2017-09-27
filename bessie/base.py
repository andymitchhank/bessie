from functools import partial
from enum import Enum

import requests

try:
	import urlparse as parse
except:
	from urllib import parse


class InvalidEndpointException(Exception):
	pass

class InvalidHookException(Exception):
	pass


class Hooks(Enum):
	request_created_hook = 1

	@classmethod
	def has_value(cls, value):
		return any(value == item.value for item in cls)

	@classmethod
	def has_name(cls, name):
		return any(name == item.name for item in cls)



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

		self._create_request()
		self._run_hook(Hooks.request_created_hook.name)
		
	def __call__(self, value):
		path_param_key = self.path.split(self.separator)[-1]
		self.path_params[path_param_key] = str(value)
		return self
		
	def __getattr__(self, name):
		if not Hooks.has_name(name):
			new_path = self.separator.join((self.path, name)) if self.path else name
			return self.__class__(new_path, self.path_params, **self.kwargs)
		return object.__getattribute__(self, name)

	def _run_hook(self, name):
		if hasattr(self, name):
			getattr(self, name)()

	def _find_endpoint(self, method):
		endpoint = None
		to_match = '{} {}'.format(method, self.path)

		for e in self.endpoints:
			if e.match(to_match):
				endpoint = e

		if not endpoint:
			raise InvalidEndpointException('{} is not a valid endpoint.'.format(to_match))

		return endpoint
			
	def _create_request(self):
		self.request = requests.Request()

	def _validate_endpoint(self, endpoint, params):
		endpoint.validate(params, self.path_params)

	def _build_url(self, path):
		url = parse.urljoin(self.base_url, path)
		for param, value in self.path_params.items():
			url = url.replace('<{}>'.format(param), value)
		return url

	def _finalize_request(self, method, payload):
		endpoint = self._find_endpoint(method)
		self._validate_endpoint(endpoint, payload)

		self.request.url = self._build_url(endpoint.path)
		self.request.data = payload
		self.request.method = method
		
	def _send_request(self, method, **kwargs):
		self._finalize_request(method, kwargs)
		return requests.session().send(self.request.prepare())

	def __define_convenience_methods(self):
		actions = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']

		for action in actions:
			setattr(self, action.lower(), partial(self._send_request, action))


