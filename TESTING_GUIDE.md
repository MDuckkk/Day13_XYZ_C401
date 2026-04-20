# Complete Testing Guide - Frontend + Backend

## 🎯 Objective
Test the full observability lab system with interactive frontend and real-time metrics.

---

## 📋 Prerequisites

✅ Backend API running on port 8001
✅ OpenAI API key configured in .env
✅ Frontend files created (chatbot.html, dashboard.html)
✅ All dependencies installed

---

## 🚀 Step 1: Start Backend API

```bash
cd /d/Lab/Lab13/Lab13-Observability
./.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Expected output:
```
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
```

---

## 🎨 Step 2: Open Frontend UIs

### Option A: Open in Browser Directly

**Chatbot Interface:**
```
file:///d:/Lab/Lab13/Lab13-Observability/chatbot.html
```

**Metrics Dashboard:**
```
file:///d:/Lab/Lab13/Lab13-Observability/dashboard.html
```

### Option B: Use HTTP Server

```bash
# In new terminal
cd /d/Lab/Lab13/Lab13-Observability
python -m http.server 8002

# Then open:
# http://localhost:8002/chatbot.html
# http://localhost:8002/dashboard.html
```

---

## 🧪 Test Scenarios

### Test 1: Basic Chat Interaction

**Steps:**
1. Open chatbot.html
2. Type: "What is observability?"
3. Click Send or press Enter
4. Observe response from OpenAI

**Expected Results:**
```
✅ Response received in 1-3 seconds
✅ Message displayed in chat
✅ Latency, cost, quality shown
✅ Metrics panel updates
```

---

### Test 2: Real-Time Metrics Tracking

**Steps:**
1. Open chatbot.html and dashboard.html (side by side)
2. Send 5 consecutive messages
3. Watch metrics update in real-time
4. Observe dashboard trends

**Expected Results:**
```
✅ Traffic increases (requests count up)
✅ Latency P50/P95 shows reasonable values
✅ Cost accumulates correctly
✅ Quality score displayed
✅ Tokens counted accurately
```

---

### Test 3: Feature Switching

**Steps:**
1. In chatbot, click "Q&A" button
2. Send: "Explain logging"
3. Click "Summary" button
4. Send: "Summarize distributed tracing"
5. Compare responses

**Expected Results:**
```
✅ Feature button highlights when active
✅ Responses differ based on feature
✅ Both features tracked in metrics
```

---

### Test 4: Cost Tracking Accuracy

**Steps:**
1. Open chatbot.html
2. Send 3 messages and note individual costs
3. Check dashboard for total cost
4. Calculate: sum of individual costs

**Expected Results:**
```
✅ Total cost = sum of message costs
✅ Cost updates in real-time
✅ Format: $0.000xxx
```

Example:
```
Message 1: $0.000900
Message 2: $0.000363
Message 3: $0.000669
Total shown in dashboard: ~$0.0019
```

---

### Test 5: Error Rate & Quality

**Steps:**
1. Send several messages
2. Check metrics for errors (should be 0%)
3. Check quality scores
4. Verify all responses received

**Expected Results:**
```
✅ Error rate = 0%
✅ Quality score between 0.7-0.95
✅ No failed requests
```

---

### Test 6: Latency Analysis

**Steps:**
1. Send 5-10 messages rapidly
2. Note individual latencies in chat
3. Check P50 (median) and P95 (tail) in dashboard
4. Verify P95 < 3000ms (SLO target)

**Expected Results:**
```
✅ Individual latencies: 800-2900ms range
✅ P50 (median): ~1200-1500ms
✅ P95 (tail): ~2500-2900ms
✅ All within SLO target of 3000ms
```

---

### Test 7: Session & User Tracking

**Steps:**
1. Check browser console (F12)
2. Look for user ID and session ID
3. Verify they remain consistent
4. Send multiple messages

**Expected Results:**
```
✅ user-xxxxx assigned
✅ session-xxxxx created
✅ Same IDs used for all requests
✅ Correlation ID in logs
```

---

### Test 8: Dashboard Auto-Refresh

**Steps:**
1. Open dashboard.html
2. Note timestamp at bottom
3. Wait 15 seconds
4. Observe metrics and timestamp update

**Expected Results:**
```
✅ Green indicator blinking (live)
✅ Timestamp updates every 15s
✅ Chart data refreshes
✅ No manual refresh needed
```

---

### Test 9: Combined Workflow

**Steps:**
1. Open both frontends (side by side or tabs)
2. Chatbot on left, Dashboard on right
3. Send message from chatbot
4. Watch dashboard update in real-time
5. Repeat 3-5 times

**Expected Results:**
```
✅ Chatbot shows response + cost
✅ Dashboard updates within 2-15 seconds
✅ Metrics align between both UIs
✅ Trends visible in dashboard charts
```

**Visual Example:**
```
[Chatbot Tab]              [Dashboard Tab]
User: What is tracing?     Traffic: 3 → 4
Bot: [OpenAI response]     Cost: $0.002 → $0.0027
Cost: $0.000669            Quality: 0.88
Latency: 1489ms            Charts update
Quality: 0.8
```

---

### Test 10: SLO Compliance Check

**Steps:**
1. Send 10+ messages
2. Open dashboard.html
3. Compare metrics to SLO targets
4. Verify compliance

**SLO Targets:**
```
✅ Latency P95 < 3000ms (current: ~2500ms)
✅ Error Rate < 2% (current: 0%)
✅ Cost < $2.5/day (current: $0.003)
✅ Quality ≥ 0.75 (current: ~0.88)
```

---

## 📊 Data Validation Checklist

After running tests, verify:

- [ ] Total traffic count accurate
- [ ] Latency values reasonable (800-2900ms)
- [ ] P95 latency < 3000ms
- [ ] Error rate = 0%
- [ ] Total cost accumulating correctly
- [ ] Quality scores 0.7-0.95 range
- [ ] Tokens in/out counted correctly
- [ ] Messages display properly
- [ ] Metrics update in real-time
- [ ] No JavaScript errors (F12 console)
- [ ] API responding < 3 seconds
- [ ] Session IDs consistent

---

## 🔍 API Endpoint Validation

### Test /chat Endpoint

```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "session_id": "test-session",
    "feature": "qa",
    "message": "What is observability?"
  }' | python -m json.tool
```

Expected Response:
```json
{
  "answer": "Observability is the ability to...",
  "correlation_id": "xxxxx",
  "latency_ms": 1234,
  "tokens_in": 46,
  "tokens_out": 51,
  "cost_usd": 0.000903,
  "quality_score": 0.9
}
```

### Test /metrics Endpoint

```bash
curl http://127.0.0.1:8001/metrics | python -m json.tool
```

Expected Response:
```json
{
  "traffic": 10,
  "latency_p50": 1234.0,
  "latency_p95": 2500.0,
  "latency_p99": 2900.0,
  "avg_cost_usd": 0.00066,
  "total_cost_usd": 0.0066,
  "tokens_in_total": 500,
  "tokens_out_total": 350,
  "error_breakdown": {},
  "quality_avg": 0.88
}
```

### Test /health Endpoint

```bash
curl http://127.0.0.1:8001/health | python -m json.tool
```

Expected Response:
```json
{
  "ok": true,
  "tracing_enabled": true,
  "incidents": {
    "rag_slow": false,
    "tool_fail": false,
    "cost_spike": false
  }
}
```

---

## 📈 Performance Testing

### Load Test (10 Messages)

**Command:**
```bash
./.venv/Scripts/python.exe scripts/load_test.py --concurrency 5
```

**Expected Results:**
- All 10 requests: 200 OK
- Total time: ~6-8 seconds
- Error rate: 0%

---

## 🐛 Debugging Tips

### Check Browser Console (F12)
```javascript
// Look for:
- Network requests to http://127.0.0.1:8001
- No 404 or 500 errors
- WebSocket or fetch failures
```

### Check Backend Logs
```bash
# Terminal with running app should show:
INFO:     127.0.0.1:xxxxx - "POST /chat HTTP/1.1" 200 OK
```

### Check Application Logs
```bash
tail -f data/logs.jsonl
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "Connection refused" | Start backend API on port 8001 |
| "CORS error" | Add CORS middleware to app |
| "Metrics not updating" | Check /metrics endpoint works |
| "Slow responses" | Normal for OpenAI API (1-3s) |
| "0% responses" | Check OpenAI API key is valid |

---

## ✅ Success Criteria

After all tests pass:

- [x] Chatbot responds to messages
- [x] Metrics update in real-time
- [x] Dashboard shows trends
- [x] SLO targets met
- [x] No errors in responses
- [x] Cost tracking accurate
- [x] Quality scores reasonable
- [x] Latency acceptable
- [x] UI responsive
- [x] Data persists correctly

---

## 🎓 What You'll Learn

By completing these tests, you'll understand:

1. **System Architecture**
   - Frontend → Backend communication
   - Real-time metric updates
   - API integration

2. **Observability Practice**
   - Tracking latency percentiles
   - Cost per request
   - Quality metrics
   - Error tracking

3. **OpenAI API Usage**
   - Token counting
   - Cost estimation
   - Response quality

4. **Web Development**
   - Real-time UIs
   - API integration
   - Responsive design
   - WebSocket/Fetch

---

## 📝 Test Results Template

```
Test Date: 2026-04-20
Tester: [Name]
System: [Windows/Mac/Linux]

Test 1 - Basic Chat: ✅ PASS
Test 2 - Real-Time Metrics: ✅ PASS
Test 3 - Feature Switching: ✅ PASS
Test 4 - Cost Tracking: ✅ PASS
Test 5 - Error Handling: ✅ PASS
Test 6 - Latency Analysis: ✅ PASS
Test 7 - Session Tracking: ✅ PASS
Test 8 - Dashboard Refresh: ✅ PASS
Test 9 - Combined Workflow: ✅ PASS
Test 10 - SLO Compliance: ✅ PASS

Final Verdict: ✅ SYSTEM READY FOR PRODUCTION
```

---

**Ready to test?**

1. Start API: `./.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001`
2. Open chatbot: `file:///d:/Lab/Lab13/Lab13-Observability/chatbot.html`
3. Open dashboard: `file:///d:/Lab/Lab13/Lab13-Observability/dashboard.html`
4. Start testing! 🚀

