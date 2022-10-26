def prepare_check_response(results: list[dict]) -> dict:
    response = {
    "response_type": "in_channel",
    "text": '\n'.join((result['message'] for result in results))
    }
    return response
