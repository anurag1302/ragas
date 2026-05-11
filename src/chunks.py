import re


def find_last_sentence_break(text):
    matches = list(re.finditer(r"[.!?]", text))
    if not matches:
        return -1
    return matches[-1].start()


def split_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:].strip())
            break

        window = text[start:end]
        sentence_break = find_last_sentence_break(window)

        if sentence_break != -1:
            actual_end = start + sentence_break + 1
        else:
            actual_end = end
        chunk = text[start:actual_end].strip()

        if chunk:
            chunks.append(chunk)

        # safer overlap logic
        new_start = actual_end - overlap

        # prevent infinite loop
        if new_start <= start:
            new_start = actual_end
        start = new_start

    return chunks
