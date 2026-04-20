const REFRESH_MS = 15000;
const MAX_POINTS = 120;

const history = [];

const palette = {
  cyan: "#4bd7ff",
  mint: "#74f0b7",
  orange: "#ff9a5a",
  red: "#ff6b7a",
  gold: "#ffd166",
  lavender: "#b995ff",
  slate: "#94b4c4",
  white: "#eff7fb",
};

function formatNumber(value, digits = 0) {
  return Number(value || 0).toLocaleString(undefined, {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function formatCurrency(value, digits = 4) {
  return `$${formatNumber(value, digits)}`;
}

function formatPercent(value, digits = 2) {
  return `${formatNumber(value, digits)}%`;
}

function formatMs(value) {
  return `${formatNumber(value, 0)} ms`;
}

function normalizeMetrics(raw) {
  const totalRequests = raw.total_requests ?? raw.traffic ?? 0;
  const errorBreakdown = raw.error_breakdown ?? {};
  const totalErrors = Object.values(errorBreakdown).reduce((sum, count) => sum + Number(count || 0), 0);
  const errorRatePct = raw.error_rate_pct ?? (totalRequests > 0 ? (totalErrors / totalRequests) * 100 : 0);

  return {
    latency_p50_ms: raw.latency_p50_ms ?? raw.latency_p50 ?? 0,
    latency_p95_ms: raw.latency_p95_ms ?? raw.latency_p95 ?? 0,
    latency_p99_ms: raw.latency_p99_ms ?? raw.latency_p99 ?? 0,
    total_requests: totalRequests,
    error_rate_pct: errorRatePct,
    total_errors: totalErrors,
    error_breakdown: errorBreakdown,
    total_cost_usd: raw.total_cost_usd ?? 0,
    avg_cost_usd: raw.avg_cost_usd ?? 0,
    total_tokens_in: raw.total_tokens_in ?? raw.tokens_in_total ?? 0,
    total_tokens_out: raw.total_tokens_out ?? raw.tokens_out_total ?? 0,
    avg_quality_score: raw.avg_quality_score ?? raw.quality_avg ?? 0,
  };
}

function pushHistory(point) {
  history.push(point);
  if (history.length > MAX_POINTS) {
    history.shift();
  }
}

function computeQps() {
  if (history.length < 2) {
    return 0;
  }

  const current = history[history.length - 1];
  const previous = history[history.length - 2];
  const deltaRequests = Math.max(0, current.total_requests - previous.total_requests);
  const deltaSeconds = Math.max(1, (current.ts - previous.ts) / 1000);
  return deltaRequests / deltaSeconds;
}

function peakQps() {
  if (history.length < 2) {
    return 0;
  }

  let peak = 0;
  for (let index = 1; index < history.length; index += 1) {
    const current = history[index];
    const previous = history[index - 1];
    const deltaRequests = Math.max(0, current.total_requests - previous.total_requests);
    const deltaSeconds = Math.max(1, (current.ts - previous.ts) / 1000);
    peak = Math.max(peak, deltaRequests / deltaSeconds);
  }
  return peak;
}

function linePath(values, width, height, padding, minValue, maxValue) {
  if (!values.length) {
    return "";
  }

  const xStep = values.length === 1 ? 0 : (width - padding.left - padding.right) / (values.length - 1);
  const safeMin = Number.isFinite(minValue) ? minValue : 0;
  const safeMax = Number.isFinite(maxValue) && maxValue > safeMin ? maxValue : safeMin + 1;

  return values
    .map((value, index) => {
      const x = padding.left + (xStep * index);
      const normalized = (value - safeMin) / (safeMax - safeMin);
      const y = height - padding.bottom - (normalized * (height - padding.top - padding.bottom));
      return `${index === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(" ");
}

function renderChart(targetId, config) {
  const container = document.getElementById(targetId);
  const width = 360;
  const height = 170;
  const padding = { top: 16, right: 12, bottom: 22, left: 36 };
  const series = config.series.filter((item) => item.values.length > 0);
  const allValues = series.flatMap((item) => item.values);
  const thresholdValues = (config.thresholds || []).map((item) => item.value);

  const fallbackValues = allValues.length ? allValues : [0];
  let minValue = Math.min(...fallbackValues, ...thresholdValues, config.minFloor ?? 0);
  let maxValue = Math.max(...fallbackValues, ...thresholdValues, config.maxFloor ?? 1);

  if (config.clampMin !== undefined) {
    minValue = Math.min(minValue, config.clampMin);
    minValue = Math.max(minValue, config.clampMin);
  }

  if (config.clampMax !== undefined) {
    maxValue = Math.max(maxValue, config.clampMax);
    maxValue = Math.min(maxValue, config.clampMax);
  }

  if (maxValue <= minValue) {
    maxValue = minValue + 1;
  }

  const gridLines = 4;
  const gridSvg = Array.from({ length: gridLines + 1 }, (_, index) => {
    const y = padding.top + ((height - padding.top - padding.bottom) / gridLines) * index;
    const tickValue = maxValue - ((maxValue - minValue) / gridLines) * index;
    return `
      <line x1="${padding.left}" y1="${y}" x2="${width - padding.right}" y2="${y}" stroke="rgba(148, 180, 196, 0.16)" stroke-width="1" />
      <text x="4" y="${y + 4}" class="chart-label">${config.tickFormatter(tickValue)}</text>
    `;
  }).join("");

  const thresholdSvg = (config.thresholds || []).map((item) => {
    const normalized = (item.value - minValue) / (maxValue - minValue);
    const y = height - padding.bottom - (normalized * (height - padding.top - padding.bottom));
    return `
      <line x1="${padding.left}" y1="${y}" x2="${width - padding.right}" y2="${y}" stroke="${item.color}" stroke-width="1.5" stroke-dasharray="6 5" />
      <text x="${width - padding.right - 4}" y="${y - 6}" text-anchor="end" class="chart-label">${item.label}</text>
    `;
  }).join("");

  const seriesSvg = series.map((item) => `
    <path d="${linePath(item.values, width, height, padding, minValue, maxValue)}"
      fill="none"
      stroke="${item.color}"
      stroke-width="${item.width || 2.5}"
      stroke-linecap="round"
      stroke-linejoin="round" />
  `).join("");

  const svg = `
    <svg viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" role="img" aria-label="${config.title}">
      ${gridSvg}
      ${thresholdSvg}
      ${seriesSvg}
      <text x="${padding.left}" y="${height - 4}" class="chart-label">${config.footer}</text>
    </svg>
    <div class="legend">
      ${[...series.map((item) => ({ color: item.color, label: item.label })), ...(config.thresholds || []).map((item) => ({ color: item.color, label: item.label }))].map((item) => `
        <span class="legend-item">
          <span class="legend-swatch" style="background:${item.color}"></span>
          ${item.label}
        </span>
      `).join("")}
    </div>
  `;

  container.innerHTML = svg;
}

function updateHeader(success, message) {
  const statusBar = document.getElementById("status-bar");
  const statusText = document.getElementById("status-text");
  const backendStatus = document.getElementById("backend-status");
  const lastUpdated = document.getElementById("last-updated");

  statusBar.classList.remove("ok", "error");
  statusBar.classList.add(success ? "ok" : "error");
  statusText.textContent = message;
  backendStatus.textContent = success ? "Online" : "Unavailable";
  lastUpdated.textContent = new Date().toLocaleTimeString();
}

function updateStats(current) {
  const qps = computeQps();

  document.getElementById("latency-p50-stat").textContent = formatMs(current.latency_p50_ms);
  document.getElementById("latency-p95-stat").textContent = formatMs(current.latency_p95_ms);
  document.getElementById("latency-p99-stat").textContent = formatMs(current.latency_p99_ms);
  document.getElementById("traffic-qps-stat").textContent = `${formatNumber(qps, 2)} req/s`;
  document.getElementById("traffic-total-stat").textContent = formatNumber(current.total_requests);
  document.getElementById("traffic-peak-stat").textContent = `${formatNumber(peakQps(), 2)} req/s`;
  document.getElementById("error-rate-stat").textContent = formatPercent(current.error_rate_pct);
  document.getElementById("error-total-stat").textContent = formatNumber(current.total_errors);
  document.getElementById("cost-total-stat").textContent = formatCurrency(current.total_cost_usd);
  document.getElementById("cost-avg-stat").textContent = formatCurrency(current.avg_cost_usd);
  document.getElementById("tokens-in-stat").textContent = formatNumber(current.total_tokens_in);
  document.getElementById("tokens-out-stat").textContent = formatNumber(current.total_tokens_out);
  document.getElementById("tokens-total-stat").textContent = formatNumber(current.total_tokens_in + current.total_tokens_out);
  document.getElementById("quality-stat").textContent = formatNumber(current.avg_quality_score, 2);

  const breakdown = Object.entries(current.error_breakdown);
  const breakdownTarget = document.getElementById("error-breakdown");
  breakdownTarget.innerHTML = breakdown.length
    ? breakdown.map(([name, count]) => `<span class="breakdown-item">${name}: ${formatNumber(count)}</span>`).join("")
    : '<span class="breakdown-item">No errors recorded</span>';
}

function updateCharts() {
  renderChart("latency-chart", {
    title: "Latency over time",
    footer: "Unit: milliseconds",
    tickFormatter: (value) => `${formatNumber(value, 0)}ms`,
    minFloor: 0,
    series: [
      { label: "P50", color: palette.cyan, values: history.map((point) => point.latency_p50_ms) },
      { label: "P95", color: palette.orange, values: history.map((point) => point.latency_p95_ms) },
      { label: "P99", color: palette.red, values: history.map((point) => point.latency_p99_ms) },
    ],
    thresholds: [
      { label: "P95 SLO 3000ms", value: 3000, color: palette.gold },
    ],
  });

  renderChart("traffic-chart", {
    title: "Traffic QPS over time",
    footer: "Unit: requests / second",
    tickFormatter: (value) => formatNumber(value, 2),
    minFloor: 0,
    series: [
      {
        label: "QPS",
        color: palette.mint,
        values: history.map((point, index) => {
          if (index === 0) {
            return 0;
          }
          const previous = history[index - 1];
          const deltaRequests = Math.max(0, point.total_requests - previous.total_requests);
          const deltaSeconds = Math.max(1, (point.ts - previous.ts) / 1000);
          return deltaRequests / deltaSeconds;
        }),
      },
    ],
  });

  renderChart("error-chart", {
    title: "Error rate over time",
    footer: "Unit: percent",
    tickFormatter: (value) => `${formatNumber(value, 1)}%`,
    minFloor: 0,
    series: [
      { label: "Error rate", color: palette.red, values: history.map((point) => point.error_rate_pct) },
    ],
    thresholds: [
      { label: "Error SLO 2%", value: 2, color: palette.gold },
    ],
  });

  renderChart("cost-chart", {
    title: "Cost over time",
    footer: "Unit: USD",
    tickFormatter: (value) => `$${formatNumber(value, 2)}`,
    minFloor: 0,
    series: [
      { label: "Total cost", color: palette.orange, values: history.map((point) => point.total_cost_usd) },
    ],
    thresholds: [
      { label: "Daily cost SLO $2.50", value: 2.5, color: palette.gold },
    ],
  });

  renderChart("tokens-chart", {
    title: "Token totals over time",
    footer: "Unit: tokens",
    tickFormatter: (value) => formatNumber(value, 0),
    minFloor: 0,
    series: [
      { label: "Input tokens", color: palette.cyan, values: history.map((point) => point.total_tokens_in) },
      { label: "Output tokens", color: palette.lavender, values: history.map((point) => point.total_tokens_out) },
    ],
  });

  renderChart("quality-chart", {
    title: "Quality score over time",
    footer: "Unit: score (0.00 - 1.00)",
    tickFormatter: (value) => formatNumber(value, 2),
    minFloor: 0,
    clampMin: 0,
    clampMax: 1,
    series: [
      { label: "Average quality", color: palette.mint, values: history.map((point) => point.avg_quality_score) },
    ],
    thresholds: [
      { label: "Quality SLO 0.75", value: 0.75, color: palette.gold },
    ],
  });
}

async function fetchMetrics() {
  const response = await fetch("/api/metrics", { cache: "no-store" });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `HTTP ${response.status}`);
  }
  return response.json();
}

async function refresh() {
  try {
    const raw = await fetchMetrics();
    const point = normalizeMetrics(raw);
    point.ts = Date.now();
    pushHistory(point);
    updateHeader(true, "Metrics stream healthy. Dashboard is polling every 15 seconds.");
    updateStats(point);
    updateCharts();
  } catch (error) {
    updateHeader(false, `Unable to fetch metrics: ${error.message}`);
  }
}

refresh();
setInterval(refresh, REFRESH_MS);
