from bessie import BaseClient, Endpoint


class NumbersApi(BaseClient):

	endpoints = [
		Endpoint('GET', 'random', None),
		Endpoint('GET', '<n>/trivia', None),
		Endpoint('GET', '<n>/date', None),
		Endpoint('GET', '<n1>/<n2>/date')
	]
	base_url='http://numbersapi.com'


if __name__ == '__main__':
	api = NumbersApi()
	print(api.n(4).trivia.get().text)
	print(api.n(4).date.get().text)
	print(api.n1(4).n2(3).date.get().text)
	print(api.random.get(min=10, max=20).text)


