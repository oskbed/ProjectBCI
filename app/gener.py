def my_generator(data):
    count = 0
    while data > count:
        yield data
        count = 1
        print(count)