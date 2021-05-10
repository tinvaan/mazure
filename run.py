
from mazure.services import app


app.run(
    debug=True,
    port=app.config.get('MAZURE_PORT'),
    host=app.config.get('MAZURE_SERVER')
)
