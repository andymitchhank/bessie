import re

class RequiredParameterMissingError(Exception):
	pass


class Endpoint(object):

	path_param_matching_regex = r'<(\w+)>'

	def __init__(self, method, path, required_params=None):
		self.method = method
		self.path = path

		self.required_params = required_params
		self.path_params = re.findall(self.path_param_matching_regex, path)

	def __repr__(self):
		return '{}({}, {})'.format(self.__class__.__name__, self.method, self.path)

	def match(self, m):
		matching_path = self.path.replace('<', '').replace('>', '')
		return m == '{} {}'.format(self.method, matching_path)

	def validate(self, params=None, path_params=None):

		if not params: 
			params = []

		if not path_params:
			path_params = []

		missing_params = [param for param in self.required_params if param not in params] if self.required_params else []
		missing_params += ['{} (path param)'.format(param) for param in self.path_params if param not in path_params] if self.path_params else []

		if missing_params:
			raise RequiredParameterMissingError('The following required parameters are missing: {}'.format(', '.join(missing_params)))