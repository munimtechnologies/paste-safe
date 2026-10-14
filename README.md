# Paste-Safe

Mask client names before you paste text into a cloud AI, then put them back in the answer.

**Try it:** https://munimv2.github.io/paste-safe/

Freelancers, agencies and consultants paste client emails, briefs and notes into ChatGPT, Claude or Gemini every day, and many have signed NDAs that never imagined that. Paste-Safe sits in between:

1. Paste your text. An open-source name-finding model running **in your browser tab** marks people, organizations and places. A few fixed rules catch names the words around them give away (after Mr, Dr or Madame, after Dear or Hi, under "Kind regards,"). Regular expressions mark emails, phone numbers, links, card numbers, IBANs, IP addresses and US SSNs. You can add your own always-mask list, such as client names and code names. If you tick it, a small open language model (Gemma 3 270M), also in your tab, takes a second look for names the first model missed.
2. Copy the masked text into any AI: `[PERSON_1] asked [ORG_1] to move the launch from [PLACE_1]...`
3. Paste the AI's answer back. Paste-Safe swaps each placeholder for the real name. It also catches the ways chat models bend placeholders: `[person 1]`, `PERSON_1`.

The key (placeholder to real name) lives only in the page. The same name keeps the same placeholder for the whole session, so you can mask several messages in one chat. A first or last name used on its own gets the same placeholder as the full name it belongs to ("Daniel's line" after "Daniel Okafor"), so the AI reads one person, not two; if two people in the text share that name, it keeps a placeholder of its own. You can save the key as JSON and load it later.

## Why it has to be open and local

You cannot use a cloud API to find the secrets you don't want to send to a cloud API. The detector has to run where the text already is. Paste-Safe uses [dslim/bert-base-NER](https://huggingface.co/dslim/bert-base-NER) (MIT; the quantized ONNX build [Xenova/bert-base-NER](https://huggingface.co/Xenova/bert-base-NER)) through [Transformers.js](https://github.com/huggingface/transformers.js). The model downloads once (about 110 MB), the browser caches it, and after that the page works with Wi-Fi off.

The optional second look uses [onnx-community/gemma-3-270m-it-ONNX](https://huggingface.co/onnx-community/gemma-3-270m-it-ONNX) (the 4-bit build, about 323 MB, downloaded only if you tick the box). Gemma is provided under and subject to the [Gemma Terms of Use](https://ai.google.dev/gemma/terms). Gemma is asked to list the people, organizations and places in the text; Paste-Safe keeps only names that really appear in it, so a made-up or reworded name in Gemma's answer changes nothing.

What goes over the network: the page itself (GitHub Pages), the Transformers.js library (jsDelivr) and the model files (Hugging Face). Your text never does. You can check this in your browser's network tab.

## Limits

- The NER model was trained on English news text (CoNLL-2003). It misses some names, especially unusual ones, names written in lower case and non-English text. The name rules help only where a title, greeting or sign-off gives the name away, and the Gemma second look is a small model that can miss names and list ordinary words too. Read the masked text before you paste it.
- It finds names and contact details. It does not hide facts that identify someone indirectly ("the CFO of the only bakery in town").
- It lowers risk; it does not make text anonymous, and it is not legal advice about your contracts or data-protection duties.

## How well it works

**Test set:** https://munimv2.github.io/paste-safe/eval.html

The test page runs the same masking over 30 made-up requests of the kind people paste into a chat AI (`eval-data.js`), with every person, company, place, email, phone number and account number labelled. Some are meant to be hard: lower-case names, names that are also ordinary words ("Rose", "Grant") and names from outside the model's English news training. A name counts as hidden only if every letter of every mention is masked. The page scores three settings (the default; the model with the name rules off; a lower model confidence of 0.4), plus a fourth with the Gemma second look when that box is ticked. It lists what was missed and which ordinary words were masked by mistake, and writes the results as a Markdown section you can copy. It runs in your browser like the main page, so you can check the numbers yourself.

The messages were written by the AI agents that built Paste-Safe, not taken from real clients. The name rules (0.2.0) and the Gemma prompt (0.3.0) were added after the test set was written, by the same agents, so those scores on this set are a best case. The Gemma prompt's one worked example uses a lower-case name because lower-case names are the first model's best-known gap. The 0.2.1 change only decides which placeholder a name gets, not whether it is masked, so it does not move the scores.

## How it works

- `core.js`: pure functions with no DOM and no network. They split text into chunks the model can read, line up model tokens with the text, join word pieces into entity spans and widen half-tagged words, apply the name rules, build the Gemma prompt and read its reply, run the pattern finders, resolve overlaps (your list, then contact details and numbers, then names), and mask and restore.
- `app.js`: loads the model with `pipeline('token-classification', 'Xenova/bert-base-NER')` and wires up the page.
- `gemma.js`: loads Gemma 3 270M with `pipeline('text-generation', ...)` for the optional second look; used by both pages.
- `eval.html`, `eval.js`, `evalcore.js`, `eval-data.js`: the test set page, its scoring and write-up (pure functions) and the labelled messages.
- `test/core.test.mjs`, `test/eval.test.mjs`: unit tests (`npm test`). `test_node_suite.py` runs them before each commit of code to this repo, and the commit is not made if a test fails. There is no hosted CI yet. The model calls themselves are checked by running the pages in a browser.

To run it locally, serve the folder with any static server (for example `python -m http.server`) and open `http://localhost:8000`.

## Changes

- 0.3.0: an optional second look by Gemma 3 270M, running in the browser tab: it lists the names it sees, and Paste-Safe masks those that really appear in the text. Names whose kind Gemma does not say become `[NAME_n]`. The test page scores it as a fourth setting and says in the write-up what it newly hid and newly masked by mistake.
- 0.2.1: a first or last name used on its own shares the placeholder of the one full name it belongs to, so "Daniel Okafor" and a later "Daniel's" are both `[PERSON_2]` instead of two different people. A name two people share, or one the key already holds on its own, keeps its own placeholder. Found by a browser test of the sample on the live page.
- 0.2.0: name rules for titles, greetings and sign-offs (a "Names after Mr, Dr, Dear, Hi or above a sign-off" option, on by default); the test page scores the model with and without them and writes a Markdown summary.
- 0.1.0: first release, then the 30-message test set.

## About

Made by MV2 of Munim, Inc. It was built with AI agents working in his name, and is an entry in the DEV Hacktoberfest 2026 Open-Source AI Challenge (week 2, "Side Hustle"). MIT licensed. Issues and pull requests are welcome.
