# Team Task Split — 2 People

## Nguyên tắc chia
- **Person A**: Backend code (middleware, logging, PII) + validate
- **Person B**: Observability infra (Langfuse, dashboard, alerts) + report

Hai người làm **hoàn toàn độc lập**, không đụng chung file nào.

---

## Files ownership

| File | Owner |
|---|---|
| `app/middleware.py` | Person A |
| `app/main.py` | Person A |
| `app/logging_config.py` | Person A |
| `app/pii.py` | Person A |
| `config/slo.yaml` | Person B |
| `config/alert_rules.yaml` | Person B |
| `docs/blueprint-template.md` | Person B (Person A cung cấp số liệu) |

---

## Dependency duy nhất
Person B cần **validate_logs score** và **screenshots từ app đang chạy** từ Person A.
→ Person A chạy app trước, Person B lấy số liệu sau.

---

## Xem chi tiết
- [Person A Tasks](person-a-tasks.md)
- [Person B Tasks](person-b-tasks.md)
