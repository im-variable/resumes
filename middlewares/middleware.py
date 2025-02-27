import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from settings.config import ALLOWED_IPS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("middleware")


class GlobalMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host

        # ✅ Allow Only Specific IPs
        if "*" not in ALLOWED_IPS and client_ip not in ALLOWED_IPS:
            return Response(content="⛔ Access Denied", status_code=403)

        # ⏳ Process Request
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"❌ Exception: {e}")
            return Response(content="🚨 Internal Server Error", status_code=500)

        # ⏱️ Track Request Time
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-App-Version"] = "1.0.0"

        logger.info(f"✅ {request.method} {request.url} - {response.status_code} ({process_time:.4f}s)")
        return response
