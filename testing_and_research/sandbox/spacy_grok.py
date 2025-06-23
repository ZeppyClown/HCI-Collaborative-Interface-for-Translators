import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def assign_chunk_labels(doc):
    """
    Assigns chunk labels (NP, VP, PP, ADVP, etc.) to each token in a spaCy Doc object.
    Returns a list of IOB-style labels.
    """
    chunk_labels = ["O"] * len(doc)

    # Step 1: Label Noun Phrases (NP) using spaCy's noun_chunks
    for chunk in doc.noun_chunks:
        chunk_labels[chunk.start] = "B-NP"  # Beginning of NP
        for i in range(chunk.start + 1, chunk.end):
            chunk_labels[i] = "I-NP"  # Inside NP

    # Step 2: Label Verb Phrases (VP), Prepositional Phrases (PP), and Adverbial Phrases (ADVP)
    i = 0
    while i < len(doc):
        if chunk_labels[i] == "O":  # Process only unlabeled tokens
            token = doc[i]
            if token.pos_ == "ADV":
                chunk_labels[i] = "B-ADVP"  # Adverb phrase
            elif token.pos_ in ["VERB", "AUX"]:
                # Start a Verb Phrase (VP)
                chunk_labels[i] = "B-VP"
                j = i + 1
                # Include consecutive verbs, auxiliaries, or particles
                while (
                    j < len(doc)
                    and doc[j].pos_ in ["VERB", "AUX", "PART"]
                    and chunk_labels[j] == "O"
                ):
                    chunk_labels[j] = "I-VP"
                    j += 1
                i = j - 1  # Move to the end of the VP
            elif token.pos_ == "ADP":
                chunk_labels[i] = "B-PP"  # Prepositional phrase
        i += 1
    return chunk_labels


# Example usage
if __name__ == "__main__":
    # Test sentence
    text = "An 80-year-long study shows that good interpersonal relationships can make a person happier and healthier."
    doc = nlp(text)

    # Get chunk labels
    labels = assign_chunk_labels(doc)

    # Print tokens with their labels
    print("Token\t\tLabel")
    print("-" * 20)
    for token, label in zip(doc, labels):
        print(f"{token.text:<15} {label}")
