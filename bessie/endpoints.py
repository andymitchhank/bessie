import re

class RequiredParameterMissingError(Exception):
	pass


class Endpoint(object):

	path_param_matching_regex = r'<(\w+)>'
	path_param_matching_sub = '[A-Za-z0-9]+'

	def __init__(self, method, path, required_params=None):
		self.method = method
		self.path = path

		self.required_params = required_params

	def __repr__(self):
		return '{}({}, {})'.format(self.__class__.__name__, self.method, self.path)

	def match_exact(self, m):
		return m == '{} {}'.format(self.method, self.path)

	def match_with_path_params(self, m):
		regex_substitution = re.sub(self.path_param_matching_regex, self.path_param_matching_sub, self.path)
		matching_path = re.compile('{} {}{}'.format(self.method, regex_substitution, '$'))
		return bool(matching_path.match(m))

	def validate(self, params):
		missing_params = [param for param in self.required_params if param not in params] if self.required_params else None
		
		if missing_params:
			raise RequiredParameterMissingError('The following required parameters are missing: {}'.format(', '.join(missing_params)))