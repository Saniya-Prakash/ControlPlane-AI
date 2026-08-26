import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [metrics, setMetrics] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ============================================================
  // LOAD METRICS
  // ============================================================

  const loadMetrics = async () => {
    try {
      const response = await fetch(`${API_URL}/metrics`);

      if (!response.ok) {
        throw new Error("Failed to load metrics");
      }

      const data = await response.json();

      setMetrics(data);
      setError("");
    } catch (err) {
      setError(
        "Backend is not reachable. Make sure FastAPI is running."
      );
    }
  };

  useEffect(() => {
    loadMetrics();

    const interval = setInterval(loadMetrics, 5000);

    return () => clearInterval(interval);
  }, []);

  // ============================================================
  // ANALYZE PROMPT
  // ============================================================

  const analyzePrompt = async () => {
    if (!prompt.trim()) {
      return;
    }

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
        }),
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data = await response.json();

      setResult(data);

      loadMetrics();
    } catch (err) {
      setError(
        "Unable to analyze request. Check the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // Allow Ctrl + Enter to analyze
  const handleKeyDown = (event) => {
    if (event.ctrlKey && event.key === "Enter") {
      analyzePrompt();
    }
  };

  return (
    <div className="app">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <header className="header">

        <div>
          <h1>
            ◈ ControlPlane<span>.ai</span>
          </h1>

          <p>
            AI Reliability & Governance Layer
          </p>
        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          SYSTEM OPERATIONAL
        </div>

      </header>


      {/* ======================================================
          ERROR
      ====================================================== */}

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      {/* ======================================================
          METRICS
      ====================================================== */}

      <section className="metrics-grid">

        <MetricCard
          title="TOTAL REQUESTS"
          value={metrics?.total_requests ?? 0}
        />

        <MetricCard
          title="BLOCKED"
          value={metrics?.blocked ?? 0}
        />

        <MetricCard
          title="REWRITTEN"
          value={metrics?.rewritten ?? 0}
        />

        <MetricCard
          title="AVG RISK"
          value={metrics?.average_risk_score ?? 0}
        />

      </section>


      {/* ======================================================
          ANALYTICS
      ====================================================== */}

      <section className="analytics-grid">

        {/* RISK DISTRIBUTION */}

        <div className="panel">

          <div className="panel-title">

            <span>
              DECISION DISTRIBUTION
            </span>

            <span className="panel-indicator">
              LIVE
            </span>

          </div>

          <RiskBar
            label="Allowed"
            value={metrics?.allowed ?? 0}
            total={metrics?.total_requests ?? 0}
          />

          <RiskBar
            label="Rewritten"
            value={metrics?.rewritten ?? 0}
            total={metrics?.total_requests ?? 0}
          />

          <RiskBar
            label="Blocked"
            value={metrics?.blocked ?? 0}
            total={metrics?.total_requests ?? 0}
          />

        </div>


        {/* MODEL USAGE */}

        <div className="panel">

          <div className="panel-title">

            <span>
              MODEL USAGE
            </span>

            <span className="panel-indicator">
              LIVE
            </span>

          </div>

          <ModelUsage
            name="Fast Model"
            value={
              metrics?.model_usage?.["fast-model"] ?? 0
            }
            total={
              metrics?.total_requests ?? 0
            }
          />

          <ModelUsage
            name="Balanced Model"
            value={
              metrics?.model_usage?.["balanced-model"] ?? 0
            }
            total={
              metrics?.total_requests ?? 0
            }
          />

          <ModelUsage
            name="Advanced Model"
            value={
              metrics?.model_usage?.["advanced-model"] ?? 0
            }
            total={
              metrics?.total_requests ?? 0
            }
          />

        </div>

      </section>


      {/* ======================================================
          REQUEST ANALYZER
      ====================================================== */}

      <section className="panel analyzer">

        <div className="panel-title">

          <span>
            REQUEST ANALYZER
          </span>

          <span className="panel-indicator">
            CONTROLPLANE
          </span>

        </div>

        <textarea
          value={prompt}
          onChange={(e) =>
            setPrompt(e.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Enter a prompt to analyze..."
        />

        <div className="analyzer-footer">

          <span>
            Ctrl + Enter to analyze
          </span>

          <button
            onClick={analyzePrompt}
            disabled={loading || !prompt.trim()}
          >
            {loading
              ? "ANALYZING..."
              : "ANALYZE REQUEST"}
          </button>

        </div>

      </section>


      {/* ======================================================
          RESULT
      ====================================================== */}

      {result && (

        <section className="panel result-panel">

          <div className="panel-title">
            <span>
              REQUEST RESULT
            </span>

            <span className="panel-indicator">
              {result.request_id?.slice(0, 8)}
            </span>
          </div>


          {/* RESULT SUMMARY */}

          <div className="result-grid">

            <ResultItem
              label="REQUEST ID"
              value={result.request_id ?? "-"}
            />

            <ResultItem
              label="RISK SCORE"
              value={
                result.preflight?.risk_score ?? 0
              }
            />

            <ResultItem
              label="RISK LEVEL"
              value={
                result.preflight?.risk_level ?? "-"
              }
              badge
            />

            <ResultItem
              label="COMPLEXITY"
              value={
                result.routing?.complexity ?? "-"
              }
            />

            <ResultItem
              label="MODEL"
              value={
                result.routing?.model?.model ?? "-"
              }
            />

            <ResultItem
              label="DECISION"
              value={
                result.final?.decision ?? "-"
              }
              badge
            />

          </div>


          {/* ==================================================
              PRE-FLIGHT SECURITY
          ================================================== */}

          {result.preflight?.risks && (

            <SecurityPanel
              risks={result.preflight.risks}
            />

          )}


          {/* ==================================================
              FINAL RESPONSE
          ================================================== */}

          <div className="response-section">

            <div className="section-heading">

              <span>
                FINAL RESPONSE
              </span>

              <span className="response-status">
                {result.final?.decision ?? "-"}
              </span>

            </div>

            <div className="response-box">

              {result.final?.response ?? (
                <span className="blocked-message">
                  Request blocked by ControlPlane security policy.
                </span>
              )}

            </div>

          </div>


          {/* ==================================================
              RELIABILITY
          ================================================== */}

          {result.reliability && (

            <ReliabilityPanel
              reliability={result.reliability}
            />

          )}

        </section>

      )}


      <footer>
        ControlPlane.ai · Adaptive AI Reliability Infrastructure
      </footer>

    </div>
  );
}


// ============================================================
// METRIC CARD
// ============================================================

function MetricCard({ title, value }) {
  return (
    <div className="metric-card">

      <span>
        {title}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}


// ============================================================
// RISK BAR
// ============================================================

function RiskBar({
  label,
  value,
  total,
}) {
  const percentage =
    total > 0
      ? (value / total) * 100
      : 0;

  return (
    <div className="bar-row">

      <div className="bar-label">

        <span>
          {label}
        </span>

        <span>
          {value}
        </span>

      </div>

      <div className="bar">

        <div
          className="bar-fill"
          style={{
            width: `${percentage}%`,
          }}
        />

      </div>

    </div>
  );
}


// ============================================================
// MODEL USAGE
// ============================================================

function ModelUsage({
  name,
  value,
  total,
}) {
  const percentage =
    total > 0
      ? Math.round((value / total) * 100)
      : 0;

  return (
    <div className="model-row">

      <div>

        <span>
          {name}
        </span>

        <span>
          {percentage}%
        </span>

      </div>

      <div className="bar">

        <div
          className="bar-fill"
          style={{
            width: `${percentage}%`,
          }}
        />

      </div>

    </div>
  );
}


// ============================================================
// RESULT ITEM
// ============================================================

function ResultItem({
  label,
  value,
  badge = false,
}) {
  return (
    <div className="result-item">

      <span>
        {label}
      </span>

      {badge ? (
        <RiskBadge level={value} />
      ) : (
        <strong>
          {value}
        </strong>
      )}

    </div>
  );
}


// ============================================================
// SECURITY PANEL
// ============================================================

function SecurityPanel({ risks }) {

  const injection = risks?.prompt_injection;
  const privacy = risks?.privacy;
  const safety = risks?.safety;

  return (
    <div className="security-panel">

      <div className="security-header">

        <div>

          <span className="section-label">
            PRE-FLIGHT SECURITY
          </span>

          <h2>
            Threat Analysis
          </h2>

        </div>

        <span className="security-engine">
          ACTIVE
        </span>

      </div>


      <div className="security-cards">

        <SecurityCard
          title="Prompt Injection"
          icon="◈"
          data={injection}
          type="injection"
        />

        <SecurityCard
          title="Privacy"
          icon="◎"
          data={privacy}
          type="privacy"
        />

        <SecurityCard
          title="Safety"
          icon="◇"
          data={safety}
          type="safety"
        />

      </div>

    </div>
  );
}


// ============================================================
// SECURITY CARD
// ============================================================

function SecurityCard({
  title,
  icon,
  data,
  type,
}) {

  const detected = data?.detected ?? false;
  const score = data?.risk_score ?? 0;
  const level = data?.level ?? "LOW";

  return (
    <div className={`security-card ${type}`}>

      <div className="security-card-header">

        <div className="security-card-title">

          <span className="security-icon">
            {icon}
          </span>

          {title}

        </div>

        <RiskBadge level={level} />

      </div>


      <div className="security-score">

        <span>
          Risk Score
        </span>

        <strong>
          {score}
        </strong>

      </div>


      <div className="check-bar">

        <div
          className="check-bar-fill"
          style={{
            width: `${score}%`,
          }}
        />

      </div>


      <div className="security-status">

        {detected ? (
          <>
            <span className="status-warning">
              ⚠
            </span>

            Threat detected
          </>
        ) : (
          <>
            <span className="status-safe">
              ✓
            </span>

            No threats detected
          </>
        )}

      </div>


      {/* Privacy types */}

      {data?.types && detected && (

        <div className="detected-items">

          {Object.entries(data.types).map(
            ([key, value]) => (

              <div
                className="detected-item"
                key={key}
              >

                <span>
                  {key}
                </span>

                <strong>
                  {value}
                </strong>

              </div>

            )
          )}

        </div>

      )}


      {/* Injection matches */}

      {data?.matches?.length > 0 && (

        <div className="match-list">

          {data.matches.map(
            (match, index) => (

              <div
                className="match-item"
                key={index}
              >
                {match}
              </div>

            )
          )}

        </div>

      )}

    </div>
  );
}


// ============================================================
// RELIABILITY PANEL
// ============================================================

function ReliabilityPanel({
  reliability,
}) {

  const {
    reliability_risk_score,
    reliability_risk_level,
    checks,
  } = reliability;

  const privacy = checks?.privacy;
  const safety = checks?.safety;
  const grounding = checks?.grounding;

  return (
    <div className="reliability-panel">

      {/* HEADER */}

      <div className="reliability-header">

        <div>

          <span className="section-label">
            POST-GENERATION ANALYSIS
          </span>

          <h2>
            Reliability Analysis
          </h2>

        </div>

        <RiskBadge
          level={reliability_risk_level}
        />

      </div>


      {/* SCORE */}

      <div className="reliability-score-section">

        <div className="score-circle">

          <div className="score-number">
            {reliability_risk_score}
          </div>

          <div className="score-label">
            RISK
          </div>

        </div>


        <div className="score-details">

          <div className="score-title">
            Reliability Risk Score
          </div>

          <div className="score-description">
            ControlPlane evaluated the generated
            response across privacy, safety, and
            grounding checks.
          </div>

          <div className="score-bar">

            <div
              className={`score-fill ${getRiskClass(
                reliability_risk_level
              )}`}
              style={{
                width: `${reliability_risk_score}%`,
              }}
            />

          </div>

        </div>

      </div>


      {/* CHECK CARDS */}

      <div className="reliability-checks">

        {/* PRIVACY */}

        <ReliabilityCheckCard
          title="Privacy"
          icon="◎"
          level={privacy?.level ?? "LOW"}
          score={privacy?.risk_score ?? 0}
          type="privacy"
        >

          {privacy?.detected ? (

            <div className="detected-items">

              {privacy.types?.email > 0 && (
                <div className="detected-item">

                  <span>
                    Email
                  </span>

                  <strong>
                    {privacy.types.email}
                  </strong>

                </div>
              )}

              {privacy.types?.phone > 0 && (
                <div className="detected-item">

                  <span>
                    Phone
                  </span>

                  <strong>
                    {privacy.types.phone}
                  </strong>

                </div>
              )}

            </div>

          ) : (

            <div className="safe-message">
              No sensitive information detected.
            </div>

          )}

        </ReliabilityCheckCard>


        {/* SAFETY */}

        <ReliabilityCheckCard
          title="Safety"
          icon="◇"
          level={safety?.level ?? "LOW"}
          score={safety?.risk_score ?? 0}
          type="safety"
        >

          {safety?.detected ? (

            <div className="warning-message">
              Safety concerns detected.
            </div>

          ) : (

            <div className="safe-message">
              No safety threats detected.
            </div>

          )}

        </ReliabilityCheckCard>


        {/* GROUNDING */}

        <ReliabilityCheckCard
          title="Grounding"
          icon="◎"
          level={grounding?.level ?? "LOW"}
          score={grounding?.grounding_score ?? 0}
          type="grounding"
        >

          {grounding?.grounded ? (

            <div className="safe-message">
              Response supported by trusted
              knowledge sources.
            </div>

          ) : (

            <div className="warning-message">
              {grounding?.message ||
                "No supporting evidence found."
              }
            </div>

          )}

        </ReliabilityCheckCard>

      </div>


      {/* SUPPORTED FACTS */}

      {grounding?.supported_facts?.length > 0 && (

        <div className="supported-facts">

          <div className="facts-title">
            SUPPORTED FACTS
          </div>

          {grounding.supported_facts.map(
            (fact, index) => (

              <div
                className="fact"
                key={index}
              >

                <span>
                  ✓
                </span>

                {fact}

              </div>

            )
          )}

        </div>

      )}

    </div>
  );
}


// ============================================================
// RELIABILITY CHECK CARD
// ============================================================

function ReliabilityCheckCard({
  title,
  icon,
  level,
  score,
  type,
  children,
}) {

  return (
    <div
      className={`reliability-card ${type}`}
    >

      <div className="check-header">

        <div className="check-name">

          <span className="check-icon">
            {icon}
          </span>

          {title}

        </div>

        <RiskBadge level={level} />

      </div>


      <div className="check-score">

        <span>
          Risk Score
        </span>

        <strong>
          {score}
        </strong>

      </div>


      <div className="check-bar">

        <div
          className="check-bar-fill"
          style={{
            width: `${score}%`,
          }}
        />

      </div>


      <div className="check-content">
        {children}
      </div>

    </div>
  );
}


// ============================================================
// RISK BADGE
// ============================================================

function RiskBadge({ level }) {

  return (
    <span
      className={`risk-badge ${getRiskClass(level)}`}
    >

      <span className="risk-dot"></span>

      {level}

    </span>
  );
}


// ============================================================
// RISK CLASS
// ============================================================

function getRiskClass(level) {

  if (!level) {
    return "low";
  }

  switch (level.toUpperCase()) {

    case "CRITICAL":
      return "critical";

    case "HIGH":
      return "high";

    case "MEDIUM":
      return "medium";

    case "LOW":
      return "low";

    case "ALLOW":
      return "low";

    case "BLOCK":
      return "critical";

    case "REWRITE":
      return "medium";

    default:
      return "low";
  }
}


export default App;