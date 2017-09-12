import re

class RequiredParameterMissingError(Exception):
	pass


class Endpoint(object):

	def __init__(self, method, path, required_params=None):
		self.method = method
		self.path = path

		self.required_params = required_params

	def __repr__(self):
		return '{}({}, {})'.format(self.__class__.__name__, self.method, self.path)

	def match_exact(self, m):
		return m == '{} {}'.format(self.method, self.path)

	def match_with_path_params(self, m):
		matching_path = re.compile('{} {}{}'.format(self.method, re.sub(r'<(\w+)>', '[A-Za-z0-9]+', self.path), '$'))
		return bool(matching_path.match(m))

	def validate(self, params):
		missing_params = [param for param in self.required_params if param not in params] if self.required_params else None
		
		if missing_params:
			raise RequiredParameterMissingError('The following required parameters are missing: {}'.format(', '.join(missing_params)))