import os, dotenv, json, math
from openai import OpenAI
from openai.types.chat import ChatCompletion
import spacy

nlp = spacy.load("en_core_web_sm")
dotenv.load_dotenv()
client = OpenAI()
secret_key = os.getenv("OPENAI_API_KEY")


def fanyi(input, model="gpt-4o", translate_from: str = "Chinese(Simplified)"):
    main_instruction = f"You are a translator and for this task, your objective is to translate from {translate_from} to English (United Kingdom). The response should only contain the translated text."
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": main_instruction},
            {"role": "user", "content": f"Please Translate:{input}"},
        ],
        logprobs=True,
        top_logprobs=5,
    )
    return response


def translation_processing(response: ChatCompletion):
    full_sent = response.choices[0].message.content
    logprobs_content = response.choices[0].logprobs.content

    print("Translation:", full_sent)
    print("\nExtracting logprobs...\n")

    processed_logprobs = []

    try:
        for item in logprobs_content:
            # Assuming item has fields: token, logprob, top_logprobs
            token_data = {
                "token": item.token,
                "logprob": item.logprob,
                "top_logprobs": (
                    [
                        {"token": alt.token, "logprob": alt.logprob}
                        for alt in item.top_logprobs
                    ]
                    if item.top_logprobs
                    else []
                ),
            }
            processed_logprobs.append(token_data)

            # Optional: pretty print each token's info
            print(f"TOKEN: {item.token}")
            for alt in token_data["top_logprobs"]:
                print(f"  Alt: {alt['token']}, logprob: {alt['logprob']:.3f}")
            print()

    except Exception as e:
        print(f"Error while processing logprobs: {e}")
        return

    # Return structured logprobs for downstream use
    return full_sent, processed_logprobs


def generate_candidate_sentences(logprobs, prob_threshold=-1.5):
    original_tokens = [tok["token"] for tok in logprobs]
    candidates = set()
    candidates.add("".join(original_tokens).replace("Ġ", " ").strip())

    for i, tok in enumerate(logprobs):
        for alt in tok["top_logprobs"]:
            if alt["token"] != tok["token"] and alt["logprob"] > prob_threshold:
                # Create a copy of tokens and replace one token with alternative
                alt_tokens = original_tokens.copy()
                alt_tokens[i] = alt["token"]
                alt_sentence = "".join(alt_tokens).replace("Ġ", " ").strip()
                candidates.add(alt_sentence)

    return list(candidates)


def extract_phrases(text):
    doc = nlp(text)
    return [chunk.text for chunk in doc.noun_chunks]


def generate_phrase_alternatives(full_sent, logprobs, prob_threshold=-20.0):
    doc = nlp(full_sent)

    output = []

    token_strs = [tok["token"] for tok in logprobs]

    print("\n🔍 OpenAI Tokens:")
    for idx, tok in enumerate(token_strs):
        print(f"{idx}: '{tok}'")

    for chunk in doc.noun_chunks:
        print(f"\n🧠 Analysing Phrase: '{chunk.text}'")
        print(f"  → Start Char: {chunk.start_char}, End Char: {chunk.end_char}")
        print("  → spaCy Tokens:", [t.text for t in chunk])

        phrase_tokens = []
        phrase_alts = []

        chunk_start = chunk.start_char
        chunk_end = chunk.end_char

        print("  🧩 Matching tokens in logprobs (by offset):")
        current_offset = 0

        current_offset = 0

        for i, tok in enumerate(token_strs):
            is_space = tok.startswith("Ġ")
            tok_text = tok.lstrip("Ġ")
            effective_tok = (" " if is_space else "") + tok_text
            tok_len = len(effective_tok)

            print(f"    Token: '{tok}' (offset={current_offset})")

            if chunk_start <= current_offset < chunk_end:
                print(f"    ✅ Matched token '{tok}' to phrase '{chunk.text}'")
                phrase_tokens.append((i, tok))

            current_offset += tok_len

        if not phrase_tokens:
            print("  ⚠️  No matching tokens found for phrase span.")
            output.append(
                {
                    "original_phrase": chunk.text,
                    "alternatives": ["(Phrase not matched to token span)"],
                }
            )
            continue

        for i, _ in phrase_tokens:
            tok_log = logprobs[i]
            for alt in tok_log["top_logprobs"]:
                if alt["token"] != tok_log["token"] and alt["logprob"] > prob_threshold:
                    alt_tokens = token_strs.copy()
                    alt_tokens[i] = alt["token"]
                    new_phrase = (
                        "".join([alt_tokens[j] for j, _ in phrase_tokens])
                        .replace("Ġ", " ")
                        .strip()
                    )
                    phrase_alts.append(new_phrase)

        if not phrase_alts:
            phrase_alts = ["(No good alternatives found)"]

        output.append(
            {"original_phrase": chunk.text, "alternatives": list(set(phrase_alts))}
        )

    return output


def transl_logprobs():
    t_result = fanyi("一项长达80年的研究表明良好的人际关系能让一个人更幸福、更健康。")
    full_sent, logprobs = translation_processing(t_result)
    print(json.dumps(logprobs, indent=4))


def main():
    print("Enter a complete sentence to translate")
    user_input = input()
    translation_result = fanyi(user_input)

    result = translation_processing(translation_result)
    if not result:
        print("No logprobs available for candidate generation.")
        return

    full_sent, logprobs = result

    # Token-level sentence variants
    candidates = generate_candidate_sentences(logprobs)
    print("\nGenerated Candidate Sentences (Token-level variations):")
    for candidate in candidates:
        print(f"- {candidate}")

    # Phrase-level rewrites
    phrase_variants = generate_phrase_alternatives(full_sent, logprobs)
    print("\nGenerated Phrase Alternatives:")
    for phrase in phrase_variants:
        print(f"\nOriginal Phrase: {phrase['original_phrase']}")
        if phrase["alternatives"]:
            for alt in phrase["alternatives"]:
                print(f"  - {alt}")
        else:
            print("  (No good alternatives found)")


if __name__ == "__main__":
    transl_logprobs()
