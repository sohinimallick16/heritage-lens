#!/usr/bin/env python
import os
import argparse
from src.heritage_scribe.core import HeritageScribe

def main():
    parser = argparse.ArgumentParser(
        description="Annotate an Ajanta image with HeritageScribe."
    )
    parser.add_argument("--data_dir",    required=True,
                        help="Folder containing .jpg and .txt files")
    parser.add_argument("--img_file",    required=True,
                        help="Image filename, e.g. ajanta_1.jpg")
    parser.add_argument("--prompt_file", required=True,
                        help="Prompt filename, e.g. ajanta_1.txt")
    parser.add_argument("--out_md",     default="output.md",
                        help="Path to save generated markdown")
    args = parser.parse_args()

    model_dir = os.path.join("models", "gemma-3n-e4b-it")
    scribe    = HeritageScribe(model_dir=model_dir, device="auto")
    result    = scribe.annotate(
        img_filename=args.img_file,
        prompt_filename=args.prompt_file,
        data_dir=args.data_dir,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        repetition_penalty=1.1,
        eos_token_id=None
    )

    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"✅ Annotation written → {args.out_md}")

if __name__ == "__main__":
    main()
