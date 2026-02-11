import asyncio
import uuid
import os
from datetime import datetime

from django.http import StreamingHttpResponse, HttpResponse
from django.views.generic import TemplateView

from skurut.clients import redis_client, REDIS_CHANNEL


class LandingPageView(TemplateView):
    template_name = 'skurut/index.html'

    def get(self, request, *args, **kwargs):
        request.session['sid'] = uuid.uuid4().hex
        return super().get(request, *args, **kwargs)


class InfoView(TemplateView):
    template_name = 'skurut/info.html'

    @staticmethod
    def _get_process_uptime():
        stat = os.stat(f"/proc/1")
        return datetime.fromtimestamp(stat.st_ctime)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["uptime"] = self._get_process_uptime()
        return ctx


def sse_view(request):
    sid = request.session.pop('sid', None)
    url_key = request.GET.get('sid')

    if not sid or not url_key or sid != url_key:
        return HttpResponse(status=404)

    pubsub = redis_client.pubsub()
    pubsub.subscribe(REDIS_CHANNEL)

    async def event_stream():
        for message in pubsub.listen():
            if message["type"] == "message":
                yield f"event: data\ndata: {message['data']}\n\n".encode()
                await asyncio.sleep(0.001)  # Doesn't work without this

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["Transfer-Encoding"] = "chunked"
    return response
