### 🚦Quick alignment before we dive into code

Below is a **one-screen recap** of the agreed pipeline. Tell me which block you want to implement first and I’ll jump straight into concrete code with you.

---

#### 1️⃣ Translate + Log-probs

- **OpenAI ChatCompletion**

  - `logprobs=True`, `top_logprobs=K` (e.g. 5)
  - Output: English draft **+** per-token log-prob table

#### 2️⃣ Chunk the draft

- **spaCy (`en_core_web_trf`)** – fastest to start

  - Extract NP, VP, PP chunks
  - Record each chunk’s `(start_token, end_token)` indices

#### 3️⃣ Build alt-phrases inside each chunk

- For the token rows belonging to that chunk:

  1. Collect `top_logprobs` options
  2. Beam-recombine ≤ 2 token replacements
  3. **Score** every variant = sum of log-probs
  4. Keep top 3–5 ranked alternatives

_(This uses the data we already have—no extra API call.)_

#### 4️⃣ Return JSON to UI

```json
{
  "sentence": "...",
  "chunks":[
    {"id":1,"label":"NP","text":"An 80-year-long study",
     "alts":["A study spanning 80 years","An eight-decade-long study"]},
    ...
  ]
}
```

#### 5️⃣ Regenerate on user edit

- `/regenerate` endpoint

  - Freeze chosen chunk(s) in the prompt
  - Ask GPT to rewrite unlocked parts, again with `logprobs`
  - Go back to **2️⃣** for the new draft

---

### 📂 Suggested file layout

```
backend/
  ├─ openai_client.py          # wrapper: translate & regenerate
  ├─ chunker.py                # spaCy logic
  ├─ alt_builder.py            # log-prob beam recombination
  ├─ api.py                    # FastAPI routes
frontend/
  └─ CAT_UI.jsx                # (later) Streamlit/React prototype
```

---

### 👉 Your call

- **Start with block 1** (OpenAI wrapper) and get a working JSON payload?
- **Jump to block 2** (spaCy chunker) to see chunk offsets in action?
- Or straight into **block 3** (alt-builder) to prove the log-prob trick?

Let me know which module you want first, and we’ll code it line-by-line.
