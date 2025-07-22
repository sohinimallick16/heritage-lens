from pathlib import Path

class PromptManager:
    def __init__(self):
        self.cat_tpl = (Path(__file__).resolve().parents[2]
                         / "templates" / "catalogue_prompt.txt").read_text()
        self.cons_tpl = (Path(__file__).resolve().parents[2]
                           / "templates" / "conservation_prompt.txt").read_text()

    def build_catalogue(self, site, loc, obj, user_note):
        filled = (
            self.cat_tpl
            .replace("{site_name}", site)
            .replace("{site_location}", loc)
            .replace("{object_type}", obj)
        )
        return f"{filled}\n\n{user_note}\n\n"

    def build_conservation(self, site, loc, obj, user_note):
        filled = (
            self.cons_tpl
            .replace("{site_name}", site)
            .replace("{site_location}", loc)
            .replace("{object_type}", obj)
        )
        return f"{filled}\n\n{user_note}\n\n"
