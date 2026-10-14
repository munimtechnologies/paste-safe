# Paste-Safe

Mask client names before you paste text into a cloud AI, then put them back in the answer.

**Try it:** https://munimv2.github.io/paste-safe/

Freelancers, agencies and consultants paste client emails, briefs and notes into ChatGPT, Claude or Gemini every day, and many have signed NDAs that never imagined that. Paste-Safe sits in between:

1. Paste your text. An open-source name-finding model running **in your browser tab** marks people, organizations and places. Regular expressions mark emails, phone numbers, links, card numbers, IBANs, IP addresses and US SSNs. You can add your own always-mask list, such as client names and code names.
2. Copy the masked text into any AI: `[PERSON_1] asked [ORG_1] to move the launch from [PLACE_1]...`
3. Paste the AI's answer back. Paste-Safe swaps each placeholder for the real name. It also catches the ways chat models bend placeholders: `[person 1]`, `PERSON_1`.

The key (placeholder to real name) lives only in the page. The same name keeps the same placeholder for the whole session, so you can mask several messages in one chat. You can save the key as JSON and load it later.

## Why it has to be open and local

You cannot use a cloud API to find the secrets you don't want to send to a cloud API. The detector has to run where the text already is. Paste-Safe uses [dslim/bert-base-NER](https://huggingface.co/dslim/bert-base-NER) (MIT; the quantized ONNX build [Xenova/bert-base-NER](https://huggingface.co/Xenova/bert-base-NER)) through [Transformers.js](https://github.com/huggingface/transformers.js). The model downloads once (about 110 MB), the browser caches it, and after that the page works with Wi-Fi off.

What goes over the network: the page itself (GitHub Pages), the Transformers.js library (jsDelivr) and the model files (Hugging Face). Your text never does. You can check this in your browser's network tab.

## Limits

- The model was trained on English news text (CoNLL-2003). It misses some names, especially unusual ones, names written in lower case and non-English text. Read the masked text before you paste it.
- It finds names and contact details. It does not hide facts that identify someone indirectly ("the CFO of the only bakery in town").
- It lowers risk; it does not make text anonymous, and it is not legal advice about your contracts or data-protection duties.

## How it works

- `core.js`: pure functions with no DOM and no network. They split text into chunks the model can read, line up model tokens with the text, join word pieces into entity spans and widen half-tagged words, run the pattern finders, resolve overlaps (your list, then contact details and numbers, then model names), and mask and restore.
- `app.js`: loads the model with `pipeline('token-classification', 'Xenova/bert-base-NER')` and wires up the page.
- `test/core.test.mjs`: unit tests (`node --test test/core.test.mjs`). `test_node_suite.py` runs them before each commit of code to this repo, and the commit is not made if a test fails. There is no hosted CI yet.

To run it locally, serve the folder with any static server (for example `python -m http.server`) and open `http://localhost:8000`.

## About

Made by MV2 of Munim, Inc. It was built with AI agents working in his name, and is an entry in the DEV Hacktoberfest 2026 Open-Source AI Challenge (week 2, "Side Hustle"). MIT licensed. Issues and pull requests are welcome.
