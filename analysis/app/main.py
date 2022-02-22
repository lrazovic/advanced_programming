from jsonrpcserver import method, Success, serve
import logging
import nltk
import heapq

logging.getLogger().setLevel(logging.INFO)


@method
def summarize(article_text):
    logging.info(f" Method invoked with article text: {article_text}")
    sentence_list = nltk.sent_tokenize(article_text)
    stopwords = nltk.corpus.stopwords.words("english")
    word_frequencies = {}
    for word in nltk.word_tokenize(article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / maximum_frequncy
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(" ")) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
    logging.info(" ".join(summary_sentences))
    return Success(" ".join(summary_sentences))


if __name__ == "__main__":
    nltk.download("punkt")
    nltk.download("stopwords")
    PORT = 5001
    serve(port=PORT)
