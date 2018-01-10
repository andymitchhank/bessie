from bessie import BaseClient, Endpoint


types = ['trivia', 'math', 'date', 'year']
numbers = ['<number>', 'random']
available_endpoints = [Endpoint('GET', f'{n}/{t}', None) for t in types for n in numbers] + [Endpoint('GET', f'{n}', None) for n in numbers]
available_endpoints.append(Endpoint('GET', '<month>/<day>/date', None))

print(available_endpoints)

class NumbersApi(BaseClient):

	endpoints = available_endpoints
	base_url='http://numbersapi.com'


if __name__ == '__main__':
	api = NumbersApi()
	print(api.number(4).trivia.get().text)
	print(api.number(4).date.get().text)
	print(api.month(4).day(3).date.get().text)
	print(api.random.get(min=10, max=20).text)


