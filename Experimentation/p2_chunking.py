from __future__ import annotations
from typing import List, Tuple, Dict
import spacy
from spacy.matcher import Matcher

# ------------------------------------------------------------------
# 1.  Load a lightweight English pipeline (no NER, no parser needed)
# ------------------------------------------------------------------
# For quick prototyping `en_core_web_sm` is enough.
# Swap to 'en_core_web_trf' later for better accuracy.
_nlp = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer"])
_nlp.enable_pipe("senter")  # keep sentence boundaries

# Initialize the Matcher once (do this at module top)
_matcher = Matcher(_nlp.vocab)
# VP: optional AUX, one VERB, optional “that”
_matcher.add(
    "VP", [[{"POS": "AUX", "OP": "?"}, {"POS": "VERB"}, {"LOWER": "that", "OP": "?"}]]
)
# PP: ADP + optional DET + one or more NOUN
_matcher.add(
    "PP", [[{"POS": "ADP"}, {"POS": "DET", "OP": "?"}, {"POS": "NOUN", "OP": "+"}]]
)
# ADJP: optional ADV + one or more ADJ
_matcher.add("ADJP", [[{"POS": "ADV", "OP": "?"}, {"POS": "ADJ", "OP": "+"}]])
# ADVP: one or more ADV
_matcher.add("ADVP", [[{"POS": "ADV", "OP": "+"}]])


# ------------------------------------------------------------------
# 2.  Helpers:  BPE tokens  →  plain text + char-level spans
# Essentially, what this thing is doing is called 'Detokenization'
# ------------------------------------------------------------------
def _tokens_to_text_and_char_spans(
    bpt_tokens: List[str],
) -> Tuple[str, List[Tuple[int, int]]]:
    """
    Re-join GPT BPE tokens (with leading 'Ġ' for spaces) into plain text.
    Return the text *and* a list mapping each token to its (start, end) char span.
    """
    text_parts: List[str] = []
    char_spans: List[Tuple[int, int]] = []

    cursor = 0

    for tok in bpt_tokens:
        # OpenAI's BPE puts 'Ġ' in front of tokens that start with a space.
        if tok.startswith("Ġ"):
            surface = tok[1:]  # strip the marker
            if text_parts:  # not the first word → insert space
                text_parts.append(" ")
                cursor += 1
        else:
            surface = tok

        start = (
            cursor  # Set the starting point of the index where the token's text begins
        )
        text_parts.append(
            surface
        )  # Append the token's characters to text_parts i.e. this is one token that has been normalised
        cursor += len(
            surface
        )  # Increment the cursor by the length of the token that was just examined
        end = cursor  # Set the end index of the last character in the token
        char_spans.append(
            (start, end)
        )  # append the range of the start and end char index of the token to the char_spans

    plain_text = "".join(text_parts)
    return plain_text, char_spans


# ------------------------------------------------------------------
# 3.  Map (start_char, end_char) → (start_token_idx, end_token_idx)
# ------------------------------------------------------------------
def _char_span_to_token_span(
    start_c: int, end_c: int, token_char_spans: List[Tuple[int, int]]
) -> Tuple[int, int]:
    start_tok = end_tok = None
    for idx, (t_start, t_end) in enumerate(token_char_spans):
        if t_end <= start_c:
            continue  # token before the span
        if start_tok is None:
            start_tok = idx
        if t_start < end_c:
            end_tok = idx  # last token whose start < end_c
        else:
            break
    return start_tok, end_tok


# ------------------------------------------------------------------
# 4.  Chunk extractor (NPs + VPs)
# ------------------------------------------------------------------
def _extract_chunks(doc: "spacy.tokens.Doc") -> List[Tuple[str, int, int]]:
    """
    Return list of tuples: (label, start_char, end_char)
    for NP, VP, PP, ADJP, ADVP, **filtering out** any span
    that is entirely contained within a strictly larger span.
    """
    spans: List[Tuple[str, int, int]] = []

    # 1) Noun Phrases
    for np in doc.noun_chunks:
        spans.append(("NP", np.start_char, np.end_char))

    # 2) Other phrases via Matcher (VP, PP, ADJP, ADVP)
    for match_id, start, end in _matcher(doc):
        label = doc.vocab.strings[match_id]
        span = doc[start:end]
        spans.append((label, span.start_char, span.end_char))

    # 3) Sort by start asc, length desc
    spans = sorted(spans, key=lambda x: (x[1], -(x[2] - x[1])))

    # 4) Filter out nested spans:
    filtered: List[Tuple[str, int, int]] = []
    for label, start, end in spans:
        # if there exists a strictly larger span that fully covers this one, skip it
        is_nested = False
        for _, o_start, o_end in spans:
            if (o_start <= start and end <= o_end) and (
                (o_end - o_start) > (end - start)
            ):
                is_nested = True
                break
        if not is_nested:
            filtered.append((label, start, end))

    # 5) Return the surviving spans in order of appearance
    filtered.sort(key=lambda x: x[1])
    return filtered


def chunk_sentence(bpe_tokens: List[str]) -> Tuple[List[Dict], str]:
    """
    Parameters
    ----------
    bpe_tokens : List[str]
        The token strings exactly as returned in
        `choice.logprobs.content[i]["token"]`.

    Returns
    -------
    chunks : List[dict]
        Each dict has keys: id, label, text, span_tokens [start, end]
    plain_text : str
        The reconstructed sentence (for debugging / display)
    """
    plain_text, char_spans = _tokens_to_text_and_char_spans(bpe_tokens)
    doc = _nlp(plain_text)

    raw_spans = _extract_chunks(doc)

    results = []
    for idx, (label, start_c, end_c) in enumerate(raw_spans, start=1):
        t_start, t_end = _char_span_to_token_span(start_c, end_c, char_spans)
        if t_start is None or t_end is None:
            continue
        results.append(
            {
                "id": idx,
                "label": label,
                "text": plain_text[start_c:end_c],
                "span_tokens": [t_start, t_end],
            }
        )
    return results, plain_text
