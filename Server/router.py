from Server.url import URL_TABLE


def router(url, request):
    if url in URL_TABLE:
        return URL_TABLE[url](request)
    else:
        return "No Response"