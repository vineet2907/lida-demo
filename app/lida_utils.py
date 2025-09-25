import json
from lida import Manager, TextGenerationConfig, llm
import pandas as pd

class LidaManager:
    def __init__(self, api_key, model="gpt-4"):
        self.api_key = api_key
        self.model = model
        self.lida_mgr = Manager(text_gen=llm("openai", api_key=self.api_key))

    def summarize(self, df):
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0,
            model=self.model
        )
        summary = self.lida_mgr.summarize(df, summary_method="llm", textgen_config=textgen_config)
        if isinstance(summary, str):
            summary_json = json.loads(summary)
        else:
            summary_json = summary
        return summary_json
