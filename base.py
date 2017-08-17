import requests

try:
	import urlparse as parse
except:
	from urllib import parse


class InvalidApiPathException(Exception):
	pass


class Base(object):
	
	available_paths = []
	separator = '/'

	def __init__(self, base_url, path='', **kwargs):
		self.base_url = base_url
		self.path = path
		self.kwargs = kwargs
		self._prepare_request()
		
	@property
	def full_path(self):
		return parse.urljoin(self.base_url, self.path)
		
	def __getattr__(self, name):
		new_path =self.separator.join((self.path, name)) if self.path else name
		return self.__class__(self.base_url, new_path, **self.kwargs)
		
	def _check_if_valid_path(self, method):
		if self.available_paths and '{} {}'.format(method, self.path) not in self.available_paths:
			raise InvalidApiPathException('{} {} is not a valid path'.format(method, self.path))
			
	def _prepare_request(self):
		self.request = requests.Request()
		
	def _send_request(self, method, **kwargs):
		self._check_if_valid_path(method)
		self.request.url = self.full_path
		self.request.method = method
		self.request.data = kwargs
		return requests.session().send(self.request.prepare())
		
	def post(self, **kwargs):
		return self._send_request('POST', **kwargs)
		
	def get(self, **kwargs):
		return self._send_request('GET', **kwargs)
		
