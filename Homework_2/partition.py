
import functools


def partition(number):

    if not isinstance(number, int):

        raise ValueError(f"'{number}' is not an instance of {int}")

    if number <= 0:

        raise ValueError(f"'{number}' is not a positive integer")

    partitions = set()

    partitions.add((number,))

    for x in range(1, number):

        for y in partition(number - x):

            partitions.add(tuple(sorted((x,) + y, reverse=True)))

    return sorted(partitions, reverse=True)


if __name__ == '__main__':

    for number in range (1, 21):

        products = {}

        for decomposition in partition(number):

            products[decomposition] = functools.reduce(lambda a, b: a * b, decomposition)

        max_product_partition, max_product = None, 0

        for decomposition, product in products.items():

            if product >= max_product:

                max_product_partition, max_product = decomposition, product

        print(f"Decomposition: {number} = {' + '.join(map(str, max_product_partition))}\nMaximum Product: {' * '.join(map(str, max_product_partition))} = {max_product}\n")

