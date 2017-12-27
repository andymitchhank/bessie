from getpass import getpass
from bessie import BaseClient

import config 


class MicroBlogApi(BaseClient):

	endpoints = config.available_endpoints
	base_url='https://micro.blog'

	def __init__(self, path='', path_params=None, token=''):
		self.token = token
		super().__init__(path, path_params, token=token)

	# override method from BaseClient to inject Authorization header
	def _create_request(self):
		super()._create_request()
		self.request.headers['Authorization'] = 'Token {}'.format(self.token)


if __name__ == '__main__':
	token = getpass('Token... ')
	mba = MicroBlogApi(token=token)

	# GET - https://micro.blog/posts/all
	posts = mba.posts.all.get()

	print(posts.status_code, posts.reason)
	print(posts.json())
