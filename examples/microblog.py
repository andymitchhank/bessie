from dynamic_api_client import BaseClient

class MicroBlogApi(BaseClient):

	available_paths = ['POST account/signin', 'GET posts/all']
	separator = '/'

	def __init__(self, base_url='https://micro.blog', path='', token=''):
		self.token = token
		super(self.__class__, self).__init__(base_url, path, token=token)

	# override method from BaseClient to inject Authorization header
	def _prepare_request(self):
		super(self.__class__, self)._prepare_request()
		self.request.headers['Authorization'] = 'Token {}'.format(self.token)


if __name__ == '__main__':
	mba = MicroBlogApi(token='')
	posts = mba.posts.all.get()

	print(posts.status_code, posts.reason)
	print(posts.json())