If you *only* translate ➜ chunk ➜ re-prompt for every segment, you *can* build an interactive CAT tool—but you lose three things log-probs give you “for free”: **instant alternative tokens, confidence signals, and cheap scoring/ranking** of any phrase that is swapped. Below is why those matter, what “pipe the spans into your log-prob combiner” really means, and what changes if you omit them.

---

## 1  What step 2 actually does

*(“pipe the spans into your log-prob combiner”)*

1. **Translate once with `logprobs=True, top_logprobs=K`**.
   – The response already contains *every* generated token *plus* the *K* best alternatives and their log-probabilities.
2. **Chunk the draft sentence** (spaCy noun-chunks / verb-chunks, etc.) and record each chunk’s start-end token indices.
3. **Inside each chunk** pull the corresponding rows from the log-prob array.
4. **Beam-recombine** those token-level alternatives to form candidate phrasings *without* another model call (e.g., replace ≤2 tokens at a time, sum their log-probs to score the variant).
   – This is the same idea as n-best list scoring in classical SMT/IMT research.

Result: you instantly have a short, *probability-ranked* list of alternatives for every NP/VP the user clicks.

---

## 2  Why the log-probs are useful

| Benefit                                 | With log-probs                                                                                                               | If you skip them                                                       |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Zero-latency, zero-cost suggestions** | Alt tokens already in the first response; no second API call needed.                                                         | Must prompt GPT again for *each* segment (cost ↑, latency ↑).          |
| **Confidence / hotspot highlight**      | Low-probability tokens expose “weak spots” translators should inspect first—proven helpful in IMT usability studies.         | No native measure of uncertainty; you’d guess or call the model again. |
| **Semantic closeness guarantee**        | Top-K tokens sit in the same probability mass, so replacements stay close in meaning (e.g., *shows/demonstrates/indicates*). | A fresh prompt may yield paraphrases that drift more from the source.  |
| **Ranking & filtering**                 | Sum of log-probs lets you rank phrase variants objectively (the higher the sum, the more fluent/likely).                     | You must invent a heuristics or trust GPT’s order.                     |
| **Cheap forward/backward regeneration** | After a swap, you still get log-probs for the *new* sentence in the same follow-up call, fuelling the next round.            | You can still regenerate, but again without the confidence metadata.   |

---

## 3  Where step 3 fits

*(“add regeneration endpoints”)*

1. **User picks an alt NP/VP** → backend calls `/regenerate`, freezing that span.
2. GPT rewrites the unlocked parts; you again request `logprobs` so the *next* set of alternatives is pre-baked.
3. Send the refreshed sentence + chunks + log-prob-derived suggestions back to UI.

This mirrors the “bidirectional, search-based” workflow in your paper while keeping each cycle to **one API call**.

---

## 4  Is it *wrong* to drop log-probs?

No—many CAT prototypes simply re-prompt the model for each segment.  But you should expect:

* **3-10 × more tokens billed** (one call per chunk instead of one per cycle).
* **Noticeable delay** on long sentences (each extra call \~0.3-1 s).
* **Less transparency** for translators who want to *see* why a word was suggested—probabilities are a natural explanatory aid in AI-HCI work.

Teams building production IMT systems still expose probabilities or confidence scores for exactly these reasons.

---

## 5  Practical recommendation

* Keep `logprobs` in your first prototype—it’s a **cheap optimisation** and gives you confidence data you may later need for UX (highlighting uncertain spans, auto-focusing cursor, etc.).
* Prototype the chunker + log-prob combiner; if the UX feels cluttered, you can always fall back to re-prompting for alternatives but you can’t regain confidence info you never requested.

That’s the trade-off in a nutshell. If you’d like example code for the beam recombination step or how to visualise low-confidence tokens in Streamlit, just let me know!
