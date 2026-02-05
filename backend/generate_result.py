from PIL import Image
from memory_profiler import profile
from config.paths import IMG_PATH
from application.ocr.service import OCRService, OCR_CROP_AREAS
from application.builder import prepare_character_analysis_context
from application.score_calculator import Calculator
from application.renderer import RenderAgent
from application.responsor import build_response
from infrastructure.google_ocr.ocr import GoogleOCR

def process_image(
    source: Image.Image,
    ocr_service: OCRService,
    background_image: Image.Image = None,
    debug: bool = False
):
    # ocr
    ocr_results = ocr_service.recognize(source, OCR_CROP_AREAS)
    # character及canvas參數初始化
    prepare_data = prepare_character_analysis_context(ocr_results.player_block)
    # 計算結果
    calculator = Calculator(
        rules = prepare_data.score_rules,
        character = prepare_data.character
    )
    character_summary = calculator.calc_score(ocr_results.echo_block)
    # 渲染
    agent = RenderAgent(
        score_rules = prepare_data.score_rules,
        character_ctx = prepare_data.character,
        character_summary = character_summary,
        background_image = background_image,
    )
    agent.render_top_left(prepare_data.player_info)
    agent.render_echo(source)
    agent.render_rank()
    agent.render_top_right()
    # 回傳結果
    return build_response(
        debug = debug,
        canvas = agent.get_canvas(),
        rank = agent.rank,
        score = character_summary.total_score,
        echo_results = character_summary.echo_results,
    )
    
@profile
def main():
    source_files = [
        # IMG_PATH / "input/Cartethyia.png",
        # IMG_PATH / "input/Chisa.png",
        IMG_PATH / "input/Zani.png",
        # IMG_PATH / "input/Aemeath.png",
        # IMG_PATH / "input/Cantarella.png",
        # IMG_PATH / "input/Lupa.png",
        # IMG_PATH / "input/Changli.png",
    ]
    ocr_service = GoogleOCR("ocr_api_key.json")
    for _, src_file in enumerate(source_files, start=1):
        src = Image.open(src_file)
        process_image(src, ocr_service, debug=True)

if __name__ == "__main__":
    main()