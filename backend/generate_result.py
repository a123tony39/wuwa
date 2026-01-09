from PIL import Image
from memory_profiler import profile
from render.rank_section import paste_rank
from domain.score.score import get_rank
from application.builders.ocr import run_ocr
from application.builders.character import build_character_context
from application.builders.render import build_render_context, render_top_left_block, render_echo_block, render_top_right_block

def process_image(source, debug=False):
    # ocr
    ocr_results = run_ocr(source)
    # canvas及context參數初始化
    character_ctx, score_rules, player_info = build_character_context(ocr_results)
    render_ctx = build_render_context(character_ctx, score_rules)
    # 左上區塊渲染
    render_top_left_block(ctx = render_ctx, character = character_ctx, player_info = player_info)
    # 下方聲骸區塊渲染
    total_score, echo_results, total_stats = render_echo_block(render_ctx, character_ctx, score_rules, ocr_results, source)
    # 下方評級區塊渲染
    rank = get_rank(total_score)
    paste_rank(ctx = render_ctx, rank = rank, total_score = total_score)
    # 右上區塊渲染
    render_top_right_block(character_ctx, render_ctx, total_stats)

    # 回傳結果
    return render_ctx.canvas.show() if debug else {
        "text": "圖片處理完成", 
        "image": render_ctx.canvas, 
        "result": {
            "rank": rank,
            "score": total_score,
            "echo_results": echo_results,
        }
    }
    
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
    for _, src_file in enumerate(source_files, start=1):
        src = Image.open(src_file)
        process_image(src, debug=True)

if __name__ == "__main__":
    main()