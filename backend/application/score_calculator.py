from dataclasses import dataclass
from collections import defaultdict
from domain.score.rules import ScoreRules
from domain.character.context import CharacterContext
from domain.echo.ocr_parser import get_echo_info
from domain.score.score import compute_echo_score, ECHO_SCORE_LEVELS

@dataclass
class EchoResult:
    name: str
    score: float
    message: str
    main_stats_result_list: list 
    sub_stats_result_list: list

@dataclass
class CharacterSummary:
    echo_results: list[EchoResult]
    total_score: float
    stats_total_value: dict

class Calculator:
    def __init__(self, character: CharacterContext, rules: ScoreRules):
        self.character = character
        self.rules = rules
        self.stats_total_value = defaultdict(float)

    def calc_score(self, ocr_results):
        total_score = 0.0
        character_echo_results = []
        
        for idx, ocr_result in enumerate(ocr_results):
            print(f"--------聲骸評分{idx+1}--------")
            echo = get_echo_info(ocr_result)
            echo_score, breakdown = compute_echo_score(echo, self.character, self.rules)
            self.calc_main_stats_total_value(echo)
            self.calc_sub_stats_total_value(breakdown)
            self.add_echo_result(character_echo_results, idx, echo_score, [echo.main_stat, echo.static_stat], breakdown)
            total_score += echo_score
        
        return CharacterSummary(
            total_score = total_score,
            echo_results = character_echo_results,
            stats_total_value = self.stats_total_value
        )

    def calc_main_stats_total_value(self, echo):
        for i in range(2):
            if i == 0:
                stat_name, stat_value = echo.main_stat.name, echo.main_stat.value
            elif i == 1:
                stat_name, stat_value = echo.static_stat.name, echo.static_stat.value
            self.stats_total_value[stat_name] += stat_value

    def calc_sub_stats_total_value(self, breakdown):
        for stat_name, stat_value, _ in breakdown: 
            self.stats_total_value[stat_name] += stat_value

    def add_echo_result(self, character_echo_results: list, idx: int, echo_score: float, main_stats_result_list, sub_stats_result_list):
        if echo_score >= ECHO_SCORE_LEVELS["PERFECT"]:
            message = "完美的聲骸!"
        elif echo_score >= ECHO_SCORE_LEVELS["GOOD"]:
            message = "表現出色"
        else:
            message = "建議加強此聲骸"
        
        character_echo_results.append(
            EchoResult(
                name = f"聲骸{idx+1}",
                score =  echo_score,
                message = message,
                main_stats_result_list = main_stats_result_list,
                sub_stats_result_list = sub_stats_result_list,
            )
        )