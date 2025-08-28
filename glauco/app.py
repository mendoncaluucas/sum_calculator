import os, time, logging, sys
from pythonjsonlogger import jsonlogger
from ddtrace import tracer, patch
from datadog import statsd


os.environ.setdefault("DD_SERVICE", "soma-app")
os.environ.setdefault("DD_ENV", "dev")
os.environ.setdefault("DD_VERSION", "1.0.0")


patch(logging=True)

logger = logging.getLogger("soma")
logger.setLevel(logging.INFO)
formatter = jsonlogger.JsonFormatter("%(asctime)s %(message)s")

sh = logging.StreamHandler(sys.stdout); sh.setFormatter(formatter); logger.addHandler(sh)
fh = logging.FileHandler("C:/soma/logs/soma.log", encoding="utf-8"); fh.setFormatter(formatter); logger.addHandler(fh)
logger.propagate = False

def soma(a: int, b: int) -> int:
    start = time.perf_counter()
    with tracer.trace("soma.operacao", resource="soma"):
        r = a + b
        dur_ms = (time.perf_counter() - start) * 1000
        statsd.increment("soma.requests", tags=["op:soma"])
        statsd.distribution("soma.latency_ms", dur_ms, tags=["op:soma"])
        logger.info({
            "event": "soma_executada",
            "a": a, "b": b, "resultado": r,
            "latency_ms": round(dur_ms, 2)
        })
        return r

if __name__ == "__main__":
    print(soma(2, 3))
    print(soma(40, 2))