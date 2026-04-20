# Frontend Setup & Usage Guide

## 🎯 Overview

Two interactive frontends for the Observability Lab:

1. **chatbot.html** - Interactive chatbot with live metrics
2. **dashboard.html** - Real-time metrics dashboard

---

## 🚀 Quick Start

### Step 1: Start the Backend API

```bash
cd /d/Lab/Lab13/Lab13-Observability
./.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Output should show:
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
```

### Step 2: Open Frontend in Browser

**Option A - Direct File (Recommended)**
```
Open file:///d:/Lab/Lab13/Lab13-Observability/chatbot.html
```

**Option B - HTTP Server**
```bash
cd /d/Lab/Lab13/Lab13-Observability
python -m http.server 8002
# Then visit: http://localhost:8002/chatbot.html
```

---

## 💬 Chatbot Frontend (chatbot.html)

### Features

✅ **Real-time Chat Interface**
- Type questions and get immediate responses from OpenAI API
- Messages grouped by user/bot with timestamps
- Auto-scroll to latest messages

✅ **Feature Selection**
- Switch between "Q&A" and "Summary" modes
- Different prompting strategies for each mode

✅ **Inline Metrics**
- Latency shown per response
- Cost tracked per request
- Quality score displayed
- Session ID and user tracking

✅ **Live Metrics Panel**
- Real-time metrics updated every 2 seconds
- Traffic count
- Latency P50 and P95
- Error rate
- Total cost
- Quality score
- Token usage (in/out)

### How to Use

1. **Ask a Question**
   ```
   Select feature (Q&A or Summary)
   Type your question
   Press Enter or click Send
   ```

2. **Example Questions**
   ```
   "What is observability?"
   "Explain the three pillars of observability"
   "What are best practices for logging?"
   "How do you set up distributed tracing?"
   ```

3. **Monitor Metrics**
   - Right panel updates in real-time
   - Green indicator shows live connection
   - Shows cost per message
   - Tracks quality of responses

### Screenshot Example
```
┌─────────────────────────────┬──────────────────────────┐
│  💬 Chatbot                 │  📊 Real-Time Metrics    │
├─────────────────────────────┼──────────────────────────┤
│ Bot: Hi! Ask me anything    │  Total Requests:  5      │
│ You: What is observability? │  Avg Latency:    1.2s   │
│ Bot: Observability is...    │  Error Rate:     0%      │
│      ⏱️ 2925ms • 💰 $0.0009 │  Total Cost:   $0.0035  │
│      ⭐ 0.9                 │  Quality:      0.88/1.0 │
├─────────────────────────────┤  P95 Latency:    2.9s   │
│ [Q&A] [Summary]             │  Tokens: 📥 226  📤 127  │
│ [Type message...]  [Send]   │                          │
└─────────────────────────────┴──────────────────────────┘
```

---

## 📊 Dashboard Frontend (dashboard.html)

### Features

✅ **6 Metric Panels**
1. Latency Percentiles (P50/P95/P99)
2. Traffic (QPS)
3. Error Rate
4. Cost Over Time
5. Token Usage (In/Out)
6. Quality Score

✅ **Auto-Refresh**
- Updates every 15 seconds
- Shows timestamp of last update
- Historical trends with charts

✅ **SLO Thresholds**
- Visual SLO target lines
- Color-coded status indicators
- Performance comparison

✅ **Interactive Charts**
- Chart.js visualizations
- Responsive grid layout
- Real-time data updates

### How to Use

1. **Open Dashboard**
   ```
   file:///d:/Lab/Lab13/Lab13-Observability/dashboard.html
   ```

2. **View Metrics**
   - Each panel shows current value
   - Charts display historical trends
   - SLO targets highlighted

3. **Monitor Performance**
   - Green = Healthy (below SLO)
   - Yellow = Warning (approaching SLO)
   - Red = Critical (exceeding SLO)

4. **Analyze Trends**
   - Hover over charts for details
   - Last 20 data points shown
   - Auto-refresh keeps data current

---

## 🔗 API Endpoints Used

### From Frontend

**Chatbot Frontend:**
```
POST /chat - Send message
GET  /metrics - Fetch current metrics
```

**Dashboard Frontend:**
```
GET  /metrics - Fetch current metrics (every 15s)
```

### Example Requests

**Send Chat Message**
```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "session_id": "session-456",
    "feature": "qa",
    "message": "What is observability?"
  }'
```

**Get Metrics**
```bash
curl http://127.0.0.1:8001/metrics
```

---

## 📈 Real-Time Metrics Explained

### Latency Metrics
- **P50** - Median response time (50% of requests faster)
- **P95** - Tail latency (95% of requests faster)
- **P99** - Extreme latency (99% of requests faster)

### Error Rate
- Percentage of failed requests
- Calculated from error_breakdown
- Target: < 2%

### Cost
- USD per request
- Accumulated total cost
- Driven by token usage

### Quality Score
- 0.0 - 1.0 scale
- Based on response length and relevance
- Target: ≥ 0.75

### Tokens
- **In** - Input tokens (your questions)
- **Out** - Output tokens (AI responses)
- Affects cost calculation

---

## 🎨 UI/UX Features

### Chatbot
- Gradient header (purple)
- Feature buttons with active state
- Message animations (slide-in)
- User messages right-aligned (blue)
- Bot messages left-aligned (gray)
- Auto-focus on input field
- Enter key to send

### Dashboard
- Purple/green gradient headers
- 6-panel grid layout
- Color-coded metric boxes
- Real-time status indicator
- Auto-refresh timer
- Responsive to window resize

---

## ⚙️ Configuration

### Change API Endpoint
Edit the `API_URL` in the HTML file:

**chatbot.html - Line 318:**
```javascript
const API_URL = 'http://127.0.0.1:8001'; // Change port here
```

**dashboard.html - Line 366:**
```javascript
const API_URL = 'http://127.0.0.1:8000'; // Change port here
```

### Change Refresh Rate

**Chatbot Metrics:**
```javascript
setInterval(updateMetrics, 2000); // Change 2000 to desired ms
```

**Dashboard:**
```javascript
setInterval(fetchMetrics, REFRESH_INTERVAL); // Change REFRESH_INTERVAL
```

---

## 🧪 Testing Scenarios

### Scenario 1: Basic Q&A
1. Open chatbot.html
2. Ask: "What are the three pillars of observability?"
3. Observe response + metrics update

### Scenario 2: Cost Tracking
1. Send 10 messages
2. Watch total cost increase in metrics
3. Calculate avg cost per message

### Scenario 3: Performance Analysis
1. Send questions rapidly
2. Monitor P95 latency
3. Check if SLO is met (< 3000ms)

### Scenario 4: Error Handling
1. Stop backend API
2. Try sending message
3. See error handling in place
4. Restart API and retry

### Scenario 5: Dashboard Monitoring
1. Open dashboard.html in separate tab
2. Send messages from chatbot tab
3. Watch metrics update in real-time
4. Observe trends over time

---

## 📱 Responsive Design

Both frontends are responsive:
- **Desktop** (1200px+) - 2 column layout
- **Tablet** (768-1200px) - Stacked layout
- **Mobile** (<768px) - Single column

---

## 🔐 Security Considerations

✅ **No credentials in frontend**
- API key stored server-side only
- Frontend makes authenticated requests
- CORS may need configuration

⚠️ **CORS Headers**
If running frontend on different port/domain, add to app/main.py:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Troubleshooting

### Issue: Metrics not updating
**Solution:**
1. Check backend is running: `http://127.0.0.1:8001/health`
2. Check browser console for errors (F12)
3. Verify API URL is correct
4. Check network tab in DevTools

### Issue: Messages not sending
**Solution:**
1. Verify backend is running
2. Check CORS settings if on different port
3. Check browser console for error message
4. Try sending curl request to /chat endpoint

### Issue: Slow responses
**Solution:**
1. OpenAI API calls take 1-3 seconds
2. Check internet connection
3. Check OpenAI API status
4. Review rate limits

### Issue: Incorrect metrics
**Solution:**
1. Clear browser cache
2. Restart backend API
3. Check /metrics endpoint directly
4. Verify load test data is fresh

---

## 📊 Live Monitoring Workflow

```
User opens chatbot.html
    ↓
Types question in left panel
    ↓
Sends to API at http://127.0.0.1:8001/chat
    ↓
OpenAI processes (800-2900ms)
    ↓
Response displayed with metrics
    ↓
Right panel shows real-time updates
    ↓
Right-click → Open dashboard.html in new tab
    ↓
Dashboard shows historical trends
    ↓
Both update every 2-15 seconds
```

---

## 🎓 Learning from UI

### Chatbot Tab
- See individual request/response pairs
- Understand token economics
- Monitor per-request costs
- Evaluate quality scores

### Dashboard Tab
- Analyze trends over time
- Monitor SLO compliance
- Check error rates
- Evaluate resource usage

### Combined View
- Send questions from chatbot
- Monitor impact in dashboard
- See real-time metric updates
- Understand system behavior

---

## 📝 Example Session

```
1. Open chatbot.html and dashboard.html (side by side)
2. Ask: "What is distributed tracing?"
3. Observe in chatbot: latency 1234ms, cost $0.0007, quality 0.92
4. Check dashboard: traffic increases, cost accumulates, latency updated
5. Ask 5 more questions
6. Dashboard shows: P95 latency ~1500ms, total cost ~$0.004
7. All metrics within SLO targets
```

---

## ✨ Features Checklist

- [x] Interactive chat interface
- [x] Real-time metrics display
- [x] OpenAI API integration
- [x] Cost tracking
- [x] Quality scoring
- [x] Feature selection (Q&A/Summary)
- [x] Auto-refresh dashboard
- [x] Chart visualizations
- [x] SLO threshold indicators
- [x] Responsive design
- [x] Error handling
- [x] Session tracking

---

**Status**: ✅ READY TO USE

Open now:
- Chatbot: `file:///d:/Lab/Lab13/Lab13-Observability/chatbot.html`
- Dashboard: `file:///d:/Lab/Lab13/Lab13-Observability/dashboard.html`
