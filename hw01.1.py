import redis
from redis_lru import RedisLRU
import connect
from model import Quote, Author


redis_client = redis.StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(redis_client, max_size=1000, default_ttl=60)


def build_result(quotes):
    return [q.quote for q in quotes]


@cache
def get_quotes_by_author(author_name: str):
    print(f"Get author: {author_name}")
    authors = Author.objects(name__iregex=author_name)
    result = {}
    for auth_obj in authors:
        quotes = Quote.objects(author_id=auth_obj.id)
        result[auth_obj.name] = build_result(quotes)
    return result


@cache
def get_quotes_by_tag(tag: str) -> list[str | None]:
    quotes = Quote.objects(tags__name__iregex=tag)
    return build_result(quotes)


def get_quotes_by_tags(tags: str):
    quotes = Quote.objects(tags__name__in=tags)
    return build_result(quotes)


def parse_command(user_input):
    if ':' not in user_input:
        return user_input.strip().lower(), []
    else:
        command, values = user_input.split(":")
        args = values.split(",")
        return command.strip().lower(), args


if __name__ == '__main__':
    while True:
        user_input = input('Enter command: ')
        command, args = parse_command(user_input)

        if command == 'exit':
            break
        elif command == 'name':
            res = get_quotes_by_author(args[0].strip())
        elif command == 'tag':
            res = get_quotes_by_tag(args[0].strip())
        elif command == 'tags':
            res = get_quotes_by_tags(args)
        else:
            res = 'Invalid command'
        print(res)
    """
        name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
        name:st
        tag:li
        tag:life — знайти та повернути список цитат для тега life;
        tags:life,live — знайти та повернути список цитат, де є теги life або live 
            (примітка: без пробілів між тегами life, live);
    """
