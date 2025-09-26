from lida import Manager, TextGenerationConfig, llm

class LidaManager:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.lida_mgr = Manager(text_gen=llm("openai", api_key=self.api_key))
        self.summary = None
        self.goals = []
        self.persona = ""
        self.selected_goal = None

    def summarize_and_store(self, df):
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0,
            model=self.model
        )
        self.summary = self.lida_mgr.summarize(df, summary_method="llm", textgen_config=textgen_config)

    def generate_goals_and_store(self, persona: str, n: int = 3):
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0,
            model=self.model
        )

        self.goals = self.lida_mgr.goals(
            summary=self.summary,
            persona=str(persona),
            n=n,
            textgen_config=textgen_config
        )
        self.persona = persona
        self.selected_goal = None

    def generate_chart(self):
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0,
            model=self.model
        )

        chart_result = self.lida_mgr.visualize(
            summary=self.summary,
            goal=self.selected_goal,
            textgen_config=textgen_config,
            library="matplotlib"
        )

        return chart_result
