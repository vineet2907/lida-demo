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
        self.selected_visualization = None

    def summarize(self, df):
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0,
            model=self.model
        )
        self.summary = self.lida_mgr.summarize(df, summary_method="llm", textgen_config=textgen_config)

    def personas(self):
        textgen_config = TextGenerationConfig(
            n=3,
            temperature=0.7,
            model=self.model
        )

        return self.lida_mgr.personas(
            summary=self.summary,
            textgen_config=textgen_config
        )
    
    def generate_goals(self, persona: str, n: int = 3):
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0.7,
            model=self.model
        )

        self.goals = self.lida_mgr.goals(
            summary=self.summary,
            persona=persona,
            n=n,
            textgen_config=textgen_config
        )
        self.persona = persona
        self.selected_goal = None

    def chart(self):
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0.4,
            model=self.model
        )

        chart_result = self.lida_mgr.visualize(
            summary=self.summary,
            goal=self.selected_goal,
            textgen_config=textgen_config
        )

        return chart_result
    
    def edit_chart(self, modifications: list[str]):
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0.4,
            model=self.model
        )

        chart_result = self.lida_mgr.edit(
            code=self.selected_visualization.code,
            summary=self.summary,
            instructions=modifications,
            textgen_config=textgen_config
        )

        return chart_result
    
    def evaluate(self):
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0.4,
            model=self.model
        )

        return self.lida_mgr.evaluate(
            code=self.selected_visualization.code,
            goal=self.selected_goal,
            textgen_config=textgen_config
        )
    
    def recommend(self, n: int = 2):
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0.7,
            model=self.model
        )

        return self.lida_mgr.recommend(
            code=self.selected_visualization.code,
            summary=self.summary,
            n=n,
            textgen_config=textgen_config
        )
    
    # def infographics(self, style_prompt: str = "line art"):
    #     """Uses large amount of memory as it downloads stable diffusion open source models."""
    #     infographic_result = self.lida_mgr.infographics(
    #         visualization=self.selected_visualization.raster,
    #         style_prompt=style_prompt
    #     )

    #     return infographic_result
