### What value of **K** ( `top_logprobs=K` ) makes sense?

| Factor               | Implication                                                                                                                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API limit**        | OpenAI currently caps `top_logprobs` at **5** — you can’t ask for more. ([cookbook.openai.com][1])                                                                                        |
| **Usability**        | Translators rarely want to scan > 3-5 options per token; beyond that is cognitive overload.                                                                                               |
| **UI combinatorics** | A typical chunk is ≈ 4–6 tokens. With K = 5 and allowing ≤ 2 substitutions in your beam, you end up with \~25–50 phrase variants — plenty to surface 3-5 good alternatives after scoring. |
| **Payload size**     | K = 5 adds \~5 × (#tokens) JSON rows. For a 30-token sentence that’s ≈ 150 entries—well under a few-KB response.                                                                          |
| **Cost / latency**   | The log-probs are computed anyway; adding K up to the limit has negligible extra latency or billing.                                                                                      |

**Recommendation for your prototype**

_Set `top_logprobs=5` (the maximum)._
That gives you the richest signal the API will return; you can always **filter** or **rank** down in your alt-builder. If you later discover that showing five synonyms per token overwhelms users, you can simply slice the list down to 3 in post-processing—no need to rerun the model.

---

[1]: https://cookbook.openai.com/examples/using_logprobs?utm_source=chatgpt.com "Using logprobs | OpenAI Cookbook"
