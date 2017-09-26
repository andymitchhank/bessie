import pytest

from bessie import *

def format_endpoint(method, path):
	return '{} {}'.format(method, path) 

def test_endpoint_match_exact():
	path = 'posts/all'
	method = 'GET'

	e = Endpoint(method, path)
	did_match = e.match_exact(format_endpoint(method, path))
	assert did_match == True

def test_endpoint_match_with_path_params():
	path = 'posts/all/<user_id>'
	path_to_match = 'posts/all/12345'
	method = 'GET'


	e = Endpoint(method, path)
	did_match_exact = e.match_exact(format_endpoint(method, path_to_match))
	assert did_match_exact == False

	did_match_with_path_params = e.match_with_path_params(format_endpoint(method, path_to_match))
	assert did_match_with_path_params == True

