# Person B — Langfuse, Dashboard, Alerts & Report

## Mục tiêu
Setup Langfuse để có ≥ 10 traces, build dashboard 6 panels, hoàn thiện blueprint report.

---

## TASK B1 — Setup Langfuse (làm ngay, không cần chờ A)

Tạo tài khoản tại https://cloud.langfuse.com, lấy keys rồi điền vào `.env`:

```bash
cp .env.example .env
```

Mở `.env` và điền:
```
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
APP_NAME=day13-observability-lab
APP_ENV=dev
```

---

## TASK B2 — Tạo đủ 10 Traces
Sau khi Person A chạy app xong, chạy load test để tạo traces:

```bash
python scripts/load_test.py --concurrency 5
```

Vào Langfuse dashboard kiểm tra:
- Thấy ≥ 10 traces
- Mỗi trace có đủ: `user_id`, `session_id`, `tags`
- Waterfall hiển thị các spans

---

## TASK B3 — Chụp Screenshots Langfuse

| # | Cần chụp |
|---|---|
| 1 | Trace list — thấy rõ ≥ 10 traces với timestamp |
| 2 | Một trace waterfall đầy đủ — thấy từng span và thời gian |

---

## TASK B4 — Kiểm tra SLO config
**File:** `config/slo.yaml`

File đã có sẵn, kiểm tra và điều chỉnh target phù hợp với nhóm:

```yaml
slis:
  latency_p95_ms:
    objective: 3000      # < 3000ms
    target: 99.5
  error_rate_pct:
    objective: 2         # < 2%
    target: 99.0
  daily_cost_usd:
    objective: 2.5       # < $2.5/ngày
    target: 100.0
  quality_score_avg:
    objective: 0.75
    target: 95.0
```

---

## TASK B5 — Kiểm tra Alert Rules
**File:** `config/alert_rules.yaml`

File đã có 3 rules sẵn. Kiểm tra runbook links đúng chưa:

```yaml
alerts:
  - name: high_latency_p95
    runbook: docs/alerts.md#1-high-latency-p95   # ← verify link này đúng
  - name: high_error_rate
    runbook: docs/alerts.md#2-high-error-rate
  - name: cost_budget_spike
    runbook: docs/alerts.md#3-cost-budget-spike
```

Chụp screenshot alert rules config.

---

## TASK B6 — Build Dashboard 6 Panels
Dùng Grafana hoặc bất kỳ tool nào (Datadog, custom HTML, etc.).
Metrics lấy từ endpoint `GET http://localhost:8000/metrics`.

| Panel | Metric |
|---|---|
| 1. Latency P50/P95/P99 | `latency_p50_ms`, `latency_p95_ms`, `latency_p99_ms` |
| 2. Traffic (QPS) | `total_requests` |
| 3. Error rate | `error_rate_pct` |
| 4. Cost over time | `total_cost_usd` |
| 5. Tokens in/out | `total_tokens_in`, `total_tokens_out` |
| 6. Quality score | `avg_quality_score` |

Yêu cầu bắt buộc:
- Auto-refresh 15-30 giây
- Có SLO threshold line (ví dụ: latency P95 line ở 3000ms)
- Đơn vị rõ ràng (ms, %, $, tokens)

Chụp screenshot dashboard đủ 6 panels.

---

## TASK B7 — Điền Blueprint Report
**File:** `docs/blueprint-template.md`

Chờ Person A gửi: validate score + screenshots + root cause info, rồi điền đầy đủ:

```
[GROUP_NAME]: Tên nhóm
[REPO_URL]: Link GitHub
[MEMBERS]: Tên + vai trò

[VALIDATE_LOGS_FINAL_SCORE]: /100   ← lấy từ Person A
[TOTAL_TRACES_COUNT]:               ← đếm trên Langfuse
[PII_LEAKS_FOUND]: 0                ← phải là 0

[SCENARIO_NAME]: rag_slow
[SYMPTOMS_OBSERVED]:                ← Person A cung cấp
[ROOT_CAUSE_PROVED_BY]:             ← Trace ID hoặc log line từ Person A
[FIX_ACTION]:
[PREVENTIVE_MEASURE]:
```

Điền phần evidence (đường dẫn screenshots) cho tất cả các tag `[EVIDENCE_*]`.

---

## Checklist hoàn thành

- [ ] B1: `.env` có đủ Langfuse keys
- [ ] B2: Langfuse có ≥ 10 traces với đủ metadata
- [ ] B3: Chụp trace list + trace waterfall
- [ ] B4: `slo.yaml` đã review và điều chỉnh
- [ ] B5: `alert_rules.yaml` runbook links đúng, đã chụp screenshot
- [ ] B6: Dashboard đủ 6 panels, đã chụp screenshot
- [ ] B7: `blueprint-template.md` điền đầy đủ tất cả tags
