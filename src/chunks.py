# import re


# def find_last_sentence_break(text):
#     matches = list(re.finditer(r"[.!?]", text))
#     if not matches:
#         return -1
#     return matches[-1].start()


# def split_text(text, chunk_size=1000, overlap=200):
#     chunks = []
#     start = 0

#     while start < len(text):
#         end = start + chunk_size
#         if end >= len(text):
#             chunks.append(text[start:].strip())
#             break

#         window = text[start:end]
#         sentence_break = find_last_sentence_break(window)

#         if sentence_break != -1:
#             actual_end = start + sentence_break + 1
#         else:
#             actual_end = end
#         chunk = text[start:actual_end].strip()

#         if chunk:
#             chunks.append(chunk)

#         # safer overlap logic
#         new_start = actual_end - overlap

#         # prevent infinite loop
#         if new_start <= start:
#             new_start = actual_end
#         start = new_start

#     return chunks

import re


def clean_text(text):
    """
    Clean extracted text before chunking.

    Problems this fixes:
    - too many newlines
    - broken spaces
    - weird PDF formatting
    """

    # normalize windows/mac line endings
    text = text.replace("\r\n", "\n")

    # remove excessive empty lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # remove excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def split_into_paragraphs(text):
    """
    Split text into paragraphs.

    We treat double newline as paragraph separator.
    """

    paragraphs = text.split("\n\n")

    # remove empty paragraphs
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    return paragraphs


def find_last_sentence_break(text):
    """
    Find last sentence ending punctuation.
    """

    matches = list(re.finditer(r"[.!?]", text))

    if not matches:
        return -1

    return matches[-1].start()


def split_large_paragraph(paragraph, chunk_size, overlap):
    """
    If one paragraph itself is too large,
    split it safely.
    """

    chunks = []

    start = 0

    while start < len(paragraph):

        end = start + chunk_size

        # remaining text fits
        if end >= len(paragraph):
            chunks.append(paragraph[start:].strip())
            break

        window = paragraph[start:end]

        sentence_break = find_last_sentence_break(window)

        if sentence_break != -1:
            actual_end = start + sentence_break + 1
        else:
            actual_end = end

        chunk = paragraph[start:actual_end].strip()

        if chunk:
            chunks.append(chunk)

        # overlap logic
        new_start = actual_end - overlap

        # prevent infinite loop
        if new_start <= start:
            new_start = actual_end

        start = new_start

    return chunks


def split_text(text, chunk_size=1000, overlap=200):
    """
    Main chunking function.

    Strategy:
    1. Clean text
    2. Split into paragraphs
    3. Combine paragraphs into chunks
    4. Split huge paragraphs if needed
    """

    text = clean_text(text)

    paragraphs = split_into_paragraphs(text)

    chunks = []

    current_chunk = ""

    for paragraph in paragraphs:

        # paragraph itself is too large
        if len(paragraph) > chunk_size:

            # save existing chunk first
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # split large paragraph separately
            large_chunks = split_large_paragraph(paragraph, chunk_size, overlap)

            chunks.extend(large_chunks)

            continue

        # try adding paragraph to current chunk
        candidate = current_chunk + "\n\n" + paragraph

        # still fits
        if len(candidate) <= chunk_size:
            current_chunk = candidate

        else:
            # save previous chunk
            if current_chunk:
                chunks.append(current_chunk.strip())

            # start new chunk
            current_chunk = paragraph

    # leftover chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
