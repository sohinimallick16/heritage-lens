# HeritageScribe

HeritageScribe is a lightweight web application for creating AI‑generated catalogue entries and conservation assessments of archaeological sites and artworks. Users upload an image, provide a few details, and the Gemma3n language model streams back structured Markdown text in real time. The app is built with [Gradio](https://www.gradio.app/) and runs the `unsloth/gemma-3n-E2B-it` model in 4‑bit mode for efficient inference.

## Features

- **Home** – introduction and instructions for new users.
- **Generate** – upload an image and generate two types of reports:
  - **Catalogue Entry** with sections for visual description, artistic details, cultural context, comparisons, and a JSON field log.
  - **Conservation Assessment** with damage and recommendation notes.
  Generation parameters (temperature, beam search, and max tokens) are adjustable.
- **Dashboard** – displays all generated entries in one place for easy review.

## Installation

1. Clone this repository.
2. Install Python 3.10 or later.
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

A CUDA‑capable GPU is recommended for running the model.

## Usage

Launch the Gradio interface with:

```bash
python app.py
```

Open the provided local URL in your browser. From the **Generate** tab you can fill in site details, upload a heritage image, and start generating. Results are streamed to the page and stored so you can view them later in the **Dashboard** tab.

## Project Layout

- `app.py` – entry point that creates the Gradio interface.
- `helpers/` – UI components and utility classes.
- `templates/` – text templates that build prompts for the Gemma model.
- `requirements.txt` – Python package requirements.

## License

See the `LICENSE` file for licensing information.

## Contributing

Contributions and issues are welcome. Feel free to open a pull request or file an issue if you encounter problems or have suggestions.
