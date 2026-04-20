# Person A — Backend Code & Logging

## Mục tiêu
Làm cho app chạy đúng, log đúng chuẩn, đạt validate_logs ≥ 80/100.

---

## TASK A1 — Fix Correlation ID
**File:** `app/middleware.py`

Sửa hàm `dispatch`, bỏ comment và hoàn thiện:

```python
async def dispatch(self, request: Request, call_next):
    clear_contextvars()
    
    correlation_id = request.headers.get(
        "x-request-id",
        f"req-{uuid.uuid4().hex[:8]}"
    )
    
    bind_contextvars(correlation_id=correlation_id)
    request.state.correlation_id = correlation_id
    
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = int((time.perf_counter() - start) * 1000)
    
    response.headers["x-request-id"] = correlation_id
    response.headers["x-response-time-ms"] = str(elapsed)
    return response
```

---

## TASK A2 — Enrich Logs
**File:** `app/main.py`

Trong hàm `chat()`, bỏ comment và điền:

```python
bind_contextvars(
    user_id_hash=hash_user_id(body.user_id),
    session_id=body.session_id,
    feature=body.feature,
    model=agent.model,
    env=os.getenv("APP_ENV", "dev"),
)
```

---

## TASK A3 — Bật PII Scrubbing
**File:** `app/logging_config.py`

Bỏ comment dòng `scrub_event` trong processors:

```python
processors=[
    merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso", utc=True, key="ts"),
    scrub_event,          # ← bỏ comment dòng này
    ...
]
```

---

## TASK A4 — Thêm PII Patterns
**File:** `app/pii.py`

Thêm vào `PII_PATTERNS`:

```python
"passport_vn": r"\b[A-Z]\d{7,8}\b",
"address_vn": r"\b(phường|quận|huyện|tỉnh|thành phố|đường|số nhà)\b",
```

---

## TASK A5 — Chạy app và validate

```bash
# Chạy app
uvicorn app.main:app --reload

# Gửi requests (terminal khác)
python scripts/load_test.py --concurrency 5

# Kiểm tra
python scripts/validate_logs.py
```

Phải thấy đủ 4 dòng PASSED và score ≥ 80/100.

---

## TASK A6 — Inject Incident & Ghi lại Root Cause

```bash
# Inject lỗi
python scripts/inject_incident.py --scenario rag_slow

# Gửi thêm requests để thấy ảnh hưởng
python scripts/load_test.py

# Tắt lỗi
python scripts/inject_incident.py --scenario rag_slow --disable
```

Ghi lại để điền vào blueprint:
- Triệu chứng quan sát được (latency tăng bao nhiêu?)
- Trace ID hoặc log line chứng minh root cause
- Fix action

---

## TASK A7 — Chụp Screenshots (phần của A)

| # | Cần chụp |
|---|---|
| 1 | Output của `validate_logs.py` — thấy score và 4 PASSED |
| 2 | JSON log có `correlation_id` (không phải "MISSING") |
| 3 | Log line có PII bị redact (ví dụ `[REDACTED_EMAIL]`) |

Gửi screenshots + validate score cho Person B để điền blueprint.

---

## Checklist hoàn thành

- [ ] A1: middleware.py — correlation_id không còn "MISSING"
- [ ] A2: main.py — log có user_id_hash, session_id, feature, model
- [ ] A3: logging_config.py — scrub_event được bật
- [ ] A4: pii.py — thêm ít nhất 1 pattern mới
- [ ] A5: validate_logs.py đạt ≥ 80/100
- [ ] A6: inject incident, ghi root cause
- [ ] A7: chụp 3 screenshots, gửi cho Person B
