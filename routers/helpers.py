from http import HTTPStatus
from io import BytesIO
from PIL import Image
from fastapi.responses import Response, StreamingResponse

def image_response(image: Image):
    if image is None:
        return Response(status_code=HTTPStatus.NO_CONTENT)

    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    response = StreamingResponse(img_buffer, media_type="image/png")
    response.headers['Cache-Control'] = 'no-cache'
    return response
