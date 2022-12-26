def return_chunks(text, max_characters, delimiter):
    chunks = []

    if delimiter == "" or delimiter not in text:
        # Split the text into chunks of max_characters
        for i in range(0, len(text), max_characters):
            chunks.append(text[i:i+max_characters])

    else:
        text = text.split(delimiter)
        # go over the split text
        # add the text + the delimiter to the chunks list, a new chunk if the length of the chunk is bigger than max_characters else add to the last chunk
        for i in range(len(text)):
            if len(chunks) == 0:
                chunks.append(text[i] + delimiter)
            elif len(chunks[-1]) + len(text[i]) + len(delimiter) > max_characters:
                chunks.append(text[i] + delimiter)
            else:
                chunks[-1] += text[i] + delimiter
        
    return chunks