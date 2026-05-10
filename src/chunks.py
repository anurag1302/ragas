import re
from typing import List


def _find_last_sentence_break(text: str, start: int, end: int) -> int:
    """
    Return the position (index) of the last sentence-ending punctuation
    (. ! ? followed by whitespace) within text[start:end].
    If no such punctuation is found, return -1.
    """
    # Extract the window we're looking at
    window = text[start:end]

    # Search for a dot, exclamation, or question mark followed by a space/tab/newline
    # We want the *last* occurrence, so we search from the end backwards.
    # The reversed string trick: find the first such pattern when reading backwards.
    match = re.search(r"[.!?]\s+", window[::-1])
    if not match:
        return -1

    # match.start() is the position of the pattern in the *reversed* string.
    # Convert it to the forward position inside the window.
    position_in_window = len(window) - match.start() - 1
    # Return the absolute position in the original text
    return start + position_in_window


def split_text(
    text: str, chunk_size: int = 1000, chunk_overlap: int = 200
) -> List[str]:
    """
    Split a long text into overlapping chunks, trying to break at sentence boundaries.
    Chunks will be around `chunk_size` characters, sharing `chunk_overlap` characters
    with the previous chunk.

    Parameters:
        text: The input string.
        chunk_size: Target maximum length of each chunk (in characters).
        chunk_overlap: How many characters consecutive chunks should overlap.

    Returns:
        A list of text chunks.
    """
    chunks = []
    chunk_start = 0  # Start of the current chunk
    total_length = len(text)

    while chunk_start < total_length:
        # 1. Where would we cut if we didn't care about sentence boundaries?
        ideal_end = chunk_start + chunk_size

        # 2. If we've reached the very end of the text, take what's left and stop.
        if ideal_end >= total_length:
            chunks.append(text[chunk_start:].strip())
            break

        # 3. Try to find a natural sentence break inside the current window.
        break_pos = _find_last_sentence_break(text, chunk_start, ideal_end)

        # 4. Determine the actual cut point.
        actual_end = ideal_end  # Default: cut exactly at the chunk size limit

        if break_pos != -1:
            # We found a sentence break. Check if it's not too close to the start.
            # We want chunks to be at least half the chunk_size (e.g., 500 chars).
            break_distance_from_start = break_pos - chunk_start
            if break_distance_from_start > chunk_size * 0.5:
                actual_end = break_pos + 1  # +1 to include the punctuation

        # 5. Extract the chunk and add it to our list.
        chunk = text[chunk_start:actual_end].strip()
        if chunk:  # Avoid adding empty strings
            chunks.append(chunk)

        # 6. Move the start forward, but keep the overlap by stepping back.
        chunk_start = actual_end - chunk_overlap
        if chunk_start < 0:
            chunk_start = 0

    return chunks
