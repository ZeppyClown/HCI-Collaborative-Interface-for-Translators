# Efficient Chunking
## Preface:
Somehow, the chunking code that I have made has been successful. Unfortunately, the problem is that the tokens that OpenAI provides in their ChatCompletion responses are Byte-Pair Encoded (BPE) formatted ones which differ from the type of tokens that are produced by spacy which are word level tokens. Why this is a problem? For one thing is that even after successfully doing the chunking, there will be a misalignment in the tokens mapped from the characters because the character ranges between spacy and openai will naturally be incorrectly offsetted (and resolving this has become a huge pain in the a**). 

## What I thought through:
So if I did this the naive way, I could match each spaCy token against the BPE tokens by OpenAI. With foresight, the runtime for doing that might go upwards of O(n^3).... not so ideal and optimal for a working prototype

## Okay... what's your idea then??
So here's my plan that i have come up with:

1. Generate the chunks from spaCy 
   - Get all the noun chunks, verb phrases and all other parts of speech in between. 
   - Sort the chunks in the order of their token ranges

2. In between here, I would just return the translated plaintext and provide the UI in identifying the segments based on the spaCy chunks. The start of the UX flow would be when the user clicks on the first chunk or when the first chunk comes into focus.

3. Upon starting with the first chunk, I thought of this simple algorithm:
From the spaCy chunk, join the entire token range to get the text. Obtain the character count of the chunk. 
From there, initiate a while loop with a "cursor" variable starting from 0 to reflect the BPE token index. 
Then, keep incrementing the "cursor" while joining the respective BPE token texts together until the character length of the BPE tokens matches the character length of the chunk. In that way, I would hypothetically be able to identify the BPE token range and then initiate the alternate phrasing builder from that point. In this way, I can also keep track of which position in the BPE tokens to continue once that chunk in focus has been settled.
By my calculations, the overall runtime for this would be O(bpe_t) where bpt_t is the number of BPE tokens. Theoretically, linear runtime.


# Consulting with ChatGPT on my idea:
Your idea— “walk once through the BPE stream, advance a cursor chunk-by-chunk, never rewind” —is exactly what good CAT back-ends do.
The high-level plan is solid; just a couple of practical refinements will make it dependable and even simpler.

---

## 0  Pre-requisite: one pass that records each BPE token’s char span

You already rebuild `plain_text` by concatenating the tokens **verbatim**.
While doing so you can collect:

```python
char_spans = [(start, end) for every BPE token]   # end exclusive
```

That array gives you the cumulative character boundaries you’ll need – no need to join strings repeatedly in the loop.

---

## 1  Chunking stage (spaCy)

* Run spaCy on the same `plain_text`.
* Save each chunk as `(label, start_char, end_char)` – these coordinates match the *same* `plain_text` you just built, so everything is in one reference frame.
* Sort the chunks by `start_char` so you can traverse them left-to-right.

---

## 2  Streaming mapping algorithm (one linear sweep)

```python
bpe_idx = 0                       # moving cursor into char_spans
token_ranges = []                 # result list

for label, s_char, e_char in sorted_chunks:
    # 1. Advance cursor to the first BPE token that overlaps the chunk
    while bpe_idx < len(char_spans) and char_spans[bpe_idx][1] <= s_char:
        bpe_idx += 1
    start_idx = bpe_idx

    # 2. Keep stepping until the token end passes the chunk end
    while bpe_idx < len(char_spans) and char_spans[bpe_idx][1] < e_char:
        bpe_idx += 1
    end_idx = bpe_idx             # inclusive

    token_ranges.append((label, start_idx, end_idx))   # save mapping

    # bpe_idx now points to the *last* token in this chunk.
    # Increment once so the next loop starts at the following token
    bpe_idx += 1
```

### Why this is correct

* `char_spans[i][1]` is the character position **right after** token *i*.
* As soon as that boundary ≥ `e_char`, token *i* is the last token touching the chunk.
* The algorithm never rewinds `bpe_idx`, so the whole sentence is scanned exactly once → **O(# BPE tokens)**.

### Runtime

* Building `char_spans`: O(T)
* Streaming mapping:   O(T)
* Total per sentence:  O(T) linear – the same as your proposal, but without repeated string joins.

---

## 3  Feed to the alt-phrase builder

Now each chunk dict can carry

```python
{
  "label": "NP",
  "span_tokens": [start_idx, end_idx],   # inclusive
  ...
}
```

and the alt-builder can slice `logprob_rows[start:end+1]`.

---

## 4  Comparison with your “count characters” idea

| Approach                                       | Edge-case safety                                                                          | Implementation effort                   | Runtime |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------- | ------- |
| **Char-span table + streaming cursor** (above) | Guaranteed: boundaries are pre-computed                                                   | \~30 lines once                         | O(T)    |
| **Accumulate token texts until lengths match** | Must handle spaces, newlines, multi-byte chars; fragile if same length but different text | Similar code length but more string ops | O(T)    |

Because you already have `char_spans`, using them directly avoids string length pitfalls and stays just as fast.

---

### Take-away

* Your high-level intuition (“advance a cursor per chunk, never rewind”) is spot-on.
* Implement it with the pre-computed `char_spans` array and you’ll get linear runtime, perfect alignment, and minimal code complexity.

Once this is in place you can forget about tokenisation mismatches and focus on the fun UI/UX parts.
