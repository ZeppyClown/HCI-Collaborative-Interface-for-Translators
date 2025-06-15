# Step 2: Detokenization
## Summary

Step 2 in our pipeline is **detokenization** (reconstructing the plain-text sentence from BPE tokens) and **character‐span mapping**, not text normalization in the traditional NLP sense. It reverses the tokenization step by joining subword tokens back into readable words and records where each token falls in the reconstructed text (character offsets). Text normalization, by contrast, refers to cleaning and standardizing text (lowercasing, removing accents, stemming, etc.) before tokenization.

---

## What Step 2 Actually Does

* **Detokenization (Inverse Tokenization):** Step 2 takes the list of GPT’s BPE tokens (which include markers like “Ġ” to indicate leading spaces) and joins them into a coherent, human‐readable sentence. This is precisely the reverse of tokenization, restoring subwords to their original form in context ([sycurio.com][1]).
* **Character‐Span Mapping:** Simultaneously, it tracks each token’s start and end character index in the reconstructed text. These spans allow us to align spaCy’s chunk boundaries (expressed in characters) back to the original token indices, enabling precise segment‐level operations ([huggingface.co][2]).
* **Not Normalization:** This process does **not** perform any of the typical normalization steps (e.g., lowercasing, accent removal, punctuation stripping) that prepare raw text for modeling. It merely decodes tokens into text and maps their positions.

---

## What Text Normalization Is

* **Definition:** Text normalization is the process of converting text into a consistent, canonical form, often involving operations like lowercasing, Unicode normalization, accent removal, and mapping numbers or dates to a standard representation ([en.wikipedia.org][3]).
* **Common Techniques:**

  * **Case folding:** Converting all characters to lowercase.
  * **Unicode normalization:** Applying NFC/NFKC to unify equivalent characters.
  * **Accent stripping:** Removing diacritics from letters (e.g., “résumé” → “resume”).
  * **Stemming/Lemmatization:** Reducing words to their base or root forms (e.g., “running” → “run”) ([analyticsvidhya.com][4]).
* **Purpose:** Normalization reduces variability (different spellings, inflections) so that downstream models see fewer distinct tokens and can generalize better ([spotintelligence.com][5]).

---

## Key Differences: Detokenization vs. Normalization

| Aspect                   | Detokenization & Span Mapping                                            | Text Normalization                                 |
| ------------------------ | ------------------------------------------------------------------------ | -------------------------------------------------- |
| **Goal**                 | Reconstruct original sentence from subword tokens                        | Clean and standardize raw text                     |
| **Operations**           | Strip BPE markers, join tokens with spaces, record offsets               | Lowercase, remove accents, strip punctuation, stem |
| **When it occurs**       | After model output (post‐processing GPT’s tokens)                        | Before or during tokenization (pre‐processing)     |
| **Output**               | Exact readable text + token-to-character mapping                         | Canonicalized text that may differ from source     |
| **Use case in pipeline** | Enables chunking and segment‐level operations by mapping tokens to spans | Prepares raw inputs for consistent tokenization    |

* Detokenization is a **decoding** step, restoring tokens to text form and enabling alignment (our Step 2).
* Normalization is a **preprocessing** step, applied before tokenization to reduce noise and variability in the input ([linkedin.com][6]).

---

**In short**, Step 2 is **not** normalization; it’s the inverse of GPT’s BPE tokenization plus span mapping (detokenization), which prepares the sentence for syntactic chunking. If you need true normalization (e.g., case-folding or accent removal), you would insert those steps **before** tokenization—not during this reconstruction phase.

[1]: https://sycurio.com/knowledge/glossaries/tokenize-detokenize-payment-card-personally-identifible-data-pii?utm_source=chatgpt.com "What Is Tokenization and Detokenization? | Sycurio Glossary"
[2]: https://huggingface.co/learn/llm-course/en/chapter6/4?utm_source=chatgpt.com "Normalization and pre-tokenization - Hugging Face LLM Course"
[3]: https://en.wikipedia.org/wiki/Text_normalization?utm_source=chatgpt.com "Text normalization"
[4]: https://www.analyticsvidhya.com/blog/2021/03/tokenization-and-text-normalization/?utm_source=chatgpt.com "Tokenization and Text Normalization - Analytics Vidhya"
[5]: https://spotintelligence.com/2023/01/25/text-normalization-techniques-nlp/?utm_source=chatgpt.com "How To Use Text Normalization Techniques (NLP) [9 Ways Python]"
[6]: https://www.linkedin.com/pulse/tokenization-text-preprocessing-nlp-bushra-akram-jmf0f?utm_source=chatgpt.com "Tokenization and Text Preprocessing in NLP - LinkedIn"
