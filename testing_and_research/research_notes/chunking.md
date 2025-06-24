# Chunking
Your instinct is right — what you need next is **syntactic “chunking” (a.k.a. shallow parsing)** so you can split each machine-translated sentence into meaningful **segments (noun-phrases, verb-phrases, clauses, etc.)** and then surface alternative phrasings for *each* segment in sequence.  Chunking gives you structure that is richer than raw tokens but lighter-weight (and faster) than full constituency trees, making it a sweet spot for an interactive CAT backend.

Main Concept in short is here:
https://en.wikipedia.org/wiki/Shallow_parsing

---

## Why “chunking” is the missing link

Chunking groups adjacent tokens into the **base phrases a linguist would recognise**—NPs, VPs, PPs—without trying to build an entire parse tree.  It tells you “these six words jointly form the subject NP”; you can then fetch log-prob alternatives for that whole span and regenerate the rest of the sentence after the user swaps it.

* In classical NLP tutorials, chunking is introduced exactly for “noun-phrase extraction” – turning `[DET the] [ADJ black] [N cat]` into one NP chunk.
* Modern libraries such as spaCy expose `.noun_chunks` and similar helpers that yield the span offsets you need in **O(#tokens)** time.
* Compared with full constituency parsing, chunking is orders-of-magnitude faster and more robust on very long sentences—one reason it is still favoured in interactive MT tools.

Because every chunk stores its **start/end token indices**, you can map it back to the log-prob rows from OpenAI and compile candidate phrasings for that exact span.

---

## Core terminology you’ll see in the code

| Unit         | Formal meaning                       | Typical label(s)                           | Why you care                                    |
| ------------ | ------------------------------------ | ------------------------------------------ | ----------------------------------------------- |
| **Token**    | Smallest surface unit                | `"良好"`, `"healthy"`                        | Where log-probs live                            |
| **Phrase**   | Flat chunk with one grammatical head | **NP**, **VP**, **PP**, **AdjP**, **AdvP** | UI “segment” users click                        |
| **Clause**   | Contains its own subject + predicate | **independent / dependent**                | Swap of one clause may force rewrite of another |
| **Sentence** | Complete thought                     | (root of parse)                            | Level returned to translator                    |

Dependency or constituency *parsers* build the full tree; a **chunker** just marks the phrase spans, which is enough for your interactive pipeline.

---

## How chunking powers your alt-phrasing workflow

1. **Translate** Mandarin → English with GPT, requesting `logprobs` / `top_logprobs`.
2. **Chunk** the English draft (spaCy, NLTK RegExpChunker, or a transformer parser).

   * NP 1: “An 80-year-long study”
   * VP 1: “has shown”
   * NP 2: “good interpersonal relationships”
   * VP 2: “make people happier and healthier”
3. **Harvest alternatives** for each span:

   * For NP 1, combine token-level `top_logprobs` or issue a follow-up prompt (“Give me 5 alternative phrasings for *<<\<An 80-year-long study>>>* in context…”).
4. Present those variants in the UI. When one is chosen, **regenerate** forward (rewrite the rest) or backward (rewrite the pre-context) with a second GPT call that freezes the selected span—mirroring the paper’s bidirectional flow.

Dependency-aware regeneration has been shown to outperform naive string substitutions in MT evaluation, because it respects grammatical links (subjects agree with verbs, etc.).

---

## Tooling options you can drop into your backend

| Library / Model               | Strengths                                                                 | Notes                                                |
| ----------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------- |
| **spaCy v3**                  | Fast CNN/transformer pipelines, `.noun_chunks`, `.sents`, dependency arcs | MIT-licensed, Python-native                          |
| **Stanza / Stanford CoreNLP** | Full constituency + dependency parsing, multilingual                      | Good for clause extraction; Java server mode         |
| **NLTK RegExpChunker**        | Simple rule-based prototypes                                              | Classic tutorial starter                             |
| **ClausIE / OpenIE**          | Explicit clause boundary extractor                                        | Handy for isolating dependent vs independent clauses |

Start shallow (spaCy) and move to deeper parses only if translators demand finer control.

---

## Designing the data contract

A minimal JSON payload your backend can send to the frontend after chunking:

```jsonc
{
  "sentence": "An 80-year-long study has shown that good interpersonal relationships make people happier.",
  "chunks": [
    { "id": 1, "label": "NP", "span": [0, 5], "text": "An 80-year-long study",
      "alts": ["A study spanning 80 years", "An eight-decade-long study"] },
    { "id": 2, "label": "VP", "span": [6, 8], "text": "has shown",
      "alts": ["has demonstrated", "indicates"] },
    ...
  ]
}
```

Every time the user swaps an `alt`, call `/regenerate` with the locked chunk IDs; GPT rewrites the unlocked spans, and you re-chunk the new sentence.  Because chunks are cheap to compute, the UI feels instant.

---

## Next steps

1. **Prototype a spaCy chunker** on a handful of Chinese-→English test sentences and verify the spans align with human intuition.
2. **Pipe the spans** into your log-prob combiner to score alt phrasings (beam search or second prompt).
3. **Add regeneration endpoints** and wire a simple dropdown UI.
4. Iterate with real translators to see if chunk granularity feels right; you can always fall back on full parse trees for edge cases.

With chunking in place, you’ll have the systematic, linguistically-grounded backbone that lets translators explore alternative phrasings segment-by-segment—exactly the “search-based” interaction model your research paper envisions.
