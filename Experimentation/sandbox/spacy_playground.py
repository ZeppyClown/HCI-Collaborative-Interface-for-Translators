import spacy
import spacy.symbols
import spacy.tokens
from spacy.tokens import Span
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
# nlp.add_pipe("merge_noun_chunks")

def get_noun_phrases(doc: spacy.tokens.Doc):
    noun_phrases = list(doc.noun_chunks)
    return noun_phrases


def get_verb_phrases(doc: spacy.tokens.Doc):
    vps = []
    for tok in doc:
        if tok.pos_ == "VERB" and tok.dep_ in ("ROOT", "conj"):
            # 1. find left-hand auxiliaries
            left_aux = [
                aux for aux in tok.lefts if aux.dep_ in ("aux", "auxpass", "aux:pass")
            ]
            start_i = left_aux[0].i if left_aux else tok.i

            # 2. include right-hand particle, if any
            right = tok.right_edge  # last token in verb subtree
            if right.pos_ == "PART":
                end_i = right.i + 1  # span end is exclusive
            else:
                end_i = tok.i + 1

            # 3. include the word "that" if it follows immediately
            if end_i < len(doc) and doc[end_i].lower_ == "that":
                end_i += 1

            # record char offsets
            span = doc[start_i:end_i]
            vps.append(("VP", span.start_char, span.end_char))

    return vps


matcher = Matcher(nlp.vocab)

# Verb phrase matching
matcher.add(
    "VP",
    [
        [{"POS": "VERB"}],
        [{"POS": "VERB"}, {"POS": "ADP", "OP": "?"}, {"POS": "SCONJ", "OP": "?"}],
        [{"POS": "PART", "OP": "?"}, {"POS": "VERB"}],
    ],
)

def chunked(doc: spacy.tokens.Doc):
    spans = []

    # 1: Noun Chunks, this one is quite straightforward
    # spans += [("NP", np.start_char, np.end_char, np.text) for np in doc.noun_chunks]
    for np in doc.noun_chunks:
        spans.append(("NP", np.start_char, np.end_char))

    # 2: Verb Chunks, this one is a bit more tricky
    for match_id, start, end in matcher(doc):
        label = doc.vocab.strings[match_id]
        span = doc[start:end]
        spans.append((label, span.start_char, span.end_char))

    # 3: Sort by start asc, length desc
    spans = sorted(spans, key=lambda x: (x[1], -(x[2] - x[1])))

    # 4: Filter out nested spans:
    maximal = []
    for label, start, end in spans: # iterate through the spans that we just sorted according to their grammatical sequence
        if any( # here, we are finding if there are any occurrences within the list of spans that overlap the current span in the iteration
            os <= start and end <= oe  # Check to see: Does the start and end of the candidate span sit within the start and end of another?
            for l , os, oe in spans
            if (oe - os) > (end - start) # Only compare against spans that are longer. This prevents a span from skipping itself
        ):
            continue
        maximal.append((label, start, end))
    return maximal


def main():
    doc = nlp(
        "An 80-year-long study shows that good interpersonal relationships can make a person happier and healthier."
    )
    chunked(doc)
    return


if __name__ == "__main__":
    main()
