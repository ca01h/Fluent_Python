def str2unicode():
	symbols = '$¢£¥€¤'
	codes = []
	for symbol in symbols:
		codes.append(ord(symbol))

	print(codes)

def str_to_unicode():
	symbols = '$¢£¥€¤'
	codes = [ord(symbol) for symbol in symbols]
	print(codes)

str2unicode()
str_to_unicode()