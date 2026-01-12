from PIL import Image
from memory_profiler import profile

from config.layout import OCR_CROP_AREAS
from application.builders.character import prepare_character_analysis_context
from application.builders.render import RenderAgent
from application.builders.responsor import build_response
from infrastructure.ocr.google_ocr import GoogleOCR

def process_image(source, ocr_service, debug=False):
    # ocr
    ocr_results = ocr_service.recognize(source, OCR_CROP_AREAS)
    # character及canvas參數初始化
    prepare_data = prepare_character_analysis_context(ocr_results)
    # RenderAgent 初始化
    agent = RenderAgent(
        source = source,
        score_rules = prepare_data.score_rules,
        character_ctx = prepare_data.character,
    )
    # 渲染
    agent.render_top_left(prepare_data.player_info)
    agent.render_echo(ocr_results)
    agent.render_rank()
    agent.render_top_right()
    # 回傳結果
    return build_response(
        debug = debug,
        canvas = agent.get_canvas(),
        rank = agent.rank,
        score = agent.total_score,
        echo_results = agent.echo_results,
    )
    
@profile
def main():
    source_files = [
        # "../img/input/Cartethyia.png",
        # "../img/input/Chisa.png",
        # "../img/input/Zani.png",
        "../img/input/Phrolova.png",
        # "../img/input/Cantarella.png",
        # "../img/input/Lupa.png",
        # "../img/input/Changli.png",
    ]
    ocr_service = GoogleOCR("config.json")
    for _, src_file in enumerate(source_files, start=1):
        src = Image.open(src_file)
        process_image(src, ocr_service, debug=True)

if __name__ == "__main__":
    main()