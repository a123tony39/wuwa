def build_response(debug: bool, canvas, rank, score, echo_results):
    if debug:
        canvas.show()
        return None

    return {
        "text": "圖片處理完成",
        "image": canvas,
        "result": {
            "rank": rank,
            "score": score,
            "echo_results": echo_results,
        }
    }