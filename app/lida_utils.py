import sys
from lida import Manager, TextGenerationConfig, llm
import logging

class LidaManager:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.lida_mgr = Manager(text_gen=llm("openai", api_key=self.api_key))
        self.summary = None
        self.goals = []
        self.example_personas = []
        self.persona = ""
        self.selected_goal = None
        self.selected_visualization = None
        self.evaluations = []
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        self.logger = logging.getLogger(__name__)

    def summarize(self, df):
        self.logger.info("Summarizing")
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0,
            model=self.model
        )
        self.summary = self.lida_mgr.summarize(df, summary_method="llm", textgen_config=textgen_config)

    def personas(self):
        self.logger.info("Generating Personas")
        textgen_config = TextGenerationConfig(
            n=3,
            temperature=0.7,
            model=self.model
        )

        self.example_personas = self.lida_mgr.personas(
            summary=self.summary,
            textgen_config=textgen_config
        )
    
    def generate_goals(self, persona: str, n: int = 3):
        self.logger.info(f"Generating Goals for persona: {persona}")
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
    
    def update_goal_selection(self, goal):
        self.selected_goal = goal
        self.selected_visualization = None
        self.evaluations = []

    def chart(self):
        self.logger.info("Generating Chart")
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

        self.selected_visualization = chart_result[0]
    
    def edit_chart(self, modifications: list[str]):
        self.logger.info("Editing Chart")
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

        self.selected_visualization = chart_result[0]
    
    def evaluate(self):
        self.logger.info("Evaluating Chart")
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0.4,
            model=self.model
        )

        self.evaluations = self.lida_mgr.evaluate(
            code=self.selected_visualization.code,
            goal=self.selected_goal,
            textgen_config=textgen_config
        )
    
    def repair(self, feedback):
        filtered_feedback = [f["rationale"] for f in feedback if f["score"] < 10]
        self.logger.info(f"Repairing Chart with feedback : {filtered_feedback}")
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0.1,
            model=self.model
        )

        repaired_viz = self.lida_mgr.repair(
            code=self.selected_visualization.code,
            feedback=filtered_feedback,
            goal=self.selected_goal,
            summary=self.summary,
            textgen_config=textgen_config
        )

        self.selected_visualization = repaired_viz[0]
    
    def recommend(self, n: int = 2):
        self.logger.info("Generating Recommendations")
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
