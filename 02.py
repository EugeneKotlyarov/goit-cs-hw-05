import string
import asyncio
from collections import defaultdict, Counter
import httpx
from matplotlib import pyplot as plt


async def get_text(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None


def map_function(text):
    text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    return [(word, 1) for word in words]


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


async def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


async def map_reduce(url):
    text = await get_text(url)
    mapped_result = map_function(text)
    shuffled_words = shuffle_function(mapped_result)
    reduced_result = await asyncio.gather(
        *[reduce_function(values) for values in shuffled_words]
    )
    return dict(reduced_result)


def visualize_top_words(result, top_n=10):
    top_words = Counter(result).most_common(top_n)
    words, counts = zip(*top_words)
    plt.figure(figsize=(12, 9))
    plt.barh(words, counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title("TOp 10 Most Frequent Words")
    plt.gca().invert_yaxis()
    plt.show()


def main():
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    res = asyncio.run(map_reduce(url))
    visualize_top_words(res)


if __name__ == "__main__":
    main()
