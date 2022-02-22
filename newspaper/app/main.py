from newspaper import Article
import logging
from jsonrpcserver import method, Success, serve, Error

logging.getLogger().setLevel(logging.INFO)


def execute_logic(articleUrl: str):
    try:
        a = Article(articleUrl, language="en")
        a.download()
        a.parse()

        return Success(a.text)
    except Exception as e:
        return Error(f"!!! Error in executing newspaper logic:\n{e}")


@method
def extract_full_text(articleUrl: str):
    logging.info(
        f"Received through JsonRPC the following parameter: articleUrl={articleUrl}"
    )

    return execute_logic(articleUrl)


if __name__ == "__main__":
    PORT = 5004
    serve(port=PORT)
