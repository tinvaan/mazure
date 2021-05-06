
from .services import app
from .proxy import GlobalProxy


GlobalProxy.enable('http://%s:%s' % (
    app.config.get('MAZURE_SERVER'), app.config.get('MAZURE_PORT')))

app.run(
    debug=True,
    port=app.config.get('MAZURE_PORT'),
    host=app.config.get('MAZURE_SERVER')
)
