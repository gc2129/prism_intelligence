import { useEffect, useState } from "react";
import {
  Shield,
  Activity,
  AlertTriangle,
  Brain,
  Zap,
  Network,
  RefreshCw,
  ChevronRight,
} from "lucide-react";
import "./App.css";

const API = "https://prism-intelligence-64q8.onrender.com";

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [stress, setStress] = useState(1);
  const [stressResult, setStressResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [redTeamLoading, setRedTeamLoading] = useState(false);
  const [incident, setIncident] = useState(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const response = await fetch(`${API}/dashboard`);
      const data = await response.json();
      setDashboard(data);
    } catch (error) {
      console.error("Backend connection failed:", error);
    }
  };

  const runStressTest = async () => {
    setLoading(true);

    try {
      const response = await fetch(
        `${API}/stress-test?stress_level=${stress}`
      );

      const data = await response.json();
      setStressResult(data);
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  const runRedTeam = async () => {
    setRedTeamLoading(true);

    try {
      const response = await fetch(`${API}/red-team`);
      const data = await response.json();
      setIncident(data);
    } catch (error) {
      console.error(error);
    }

    setRedTeamLoading(false);
  };

  const trustScore = stressResult
    ? stressResult.trust_score
    : dashboard?.trust_score || 0;

  const trustLevel = stressResult
    ? stressResult.trust_level
    : dashboard?.trust_level || "LOADING";

  return (
    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">
        <div className="logo">
          <div className="logo-icon">
            <Shield size={24} />
          </div>
          <span>PRISM</span>
        </div>

        <div className="nav-section">
          <p>INTELLIGENCE</p>

          <div className="nav-item active">
            <Activity size={18} />
            Dashboard
          </div>

          <div className="nav-item">
            <Brain size={18} />
            AI Models
          </div>

          <div className="nav-item">
            <Network size={18} />
            Correlation Map
          </div>
        </div>

        <div className="nav-section">
          <p>ADVERSARIAL LAB</p>

          <div className="nav-item">
            <Zap size={18} />
            Stress Testing
          </div>

          <div className="nav-item">
            <AlertTriangle size={18} />
            Red Team Agent
          </div>
        </div>

        <div className="sidebar-footer">
          <div className="status-dot"></div>
          System Online
        </div>
      </aside>


      {/* MAIN */}

      <main className="main">

        <header className="header">
          <div>
            <p className="breadcrumb">
              PAYMENT INTELLIGENCE / OVERVIEW
            </p>
            <h1>System Trust Overview</h1>
          </div>

          <button className="refresh-btn" onClick={loadDashboard}>
            <RefreshCw size={18} />
            Refresh
          </button>
        </header>


        {/* HERO */}

        <section className="hero-grid">

          <div className="trust-card">

            <div className="card-header">
              <span>PRISM TRUST SCORE</span>
              <Shield size={20} />
            </div>

            <div className="score-container">
              <div className="score-circle">
                <span className="score">
                  {Number(trustScore).toFixed(1)}
                </span>
                <span className="out-of">/100</span>
              </div>
            </div>

            <div className="trust-status">
              <span className="pulse"></span>
              {trustLevel}
            </div>

            <p>
              Composite intelligence score based on model
              performance, confidence calibration and
              systemic correlation risk.
            </p>

          </div>


          <div className="system-card">

            <div className="card-header">
              <span>SYSTEM SIGNALS</span>
              <Activity size={20} />
            </div>

            <div className="signal-list">

              <div className="signal">
                <span>Transactions Analyzed</span>
                <strong>
                  {dashboard?.total_transactions || "--"}
                </strong>
              </div>

              <div className="signal">
                <span>Correlation Risk</span>
                <strong className="warning">
                  {dashboard?.correlated_failure_rate || "--"}%
                </strong>
              </div>

              <div className="signal">
                <span>AI Models Active</span>
                <strong>3 / 3</strong>
              </div>

            </div>

          </div>

        </section>


        {/* MODEL CARDS */}

        <section className="section">

          <div className="section-title">
            <div>
              <p>MODEL INTELLIGENCE</p>
              <h2>AI Decision Systems</h2>
            </div>

            <span className="live">
              <span></span>
              LIVE
            </span>
          </div>


          <div className="models-grid">

            {dashboard?.model_metrics &&
              Object.entries(dashboard.model_metrics).map(
                ([name, model]) => (
                  <div className="model-card" key={name}>

                    <div className="model-top">
                      <div className="model-icon">
                        <Brain size={20} />
                      </div>

                      <span className="healthy">
                        HEALTHY
                      </span>
                    </div>

                    <h3>
                      {name.replace("_", " ").toUpperCase()}
                    </h3>

                    <div className="metric-row">
                      <span>Accuracy</span>
                      <strong>{model.accuracy}%</strong>
                    </div>

                    <div className="progress">
                      <div
                        className="progress-fill"
                        style={{
                          width: `${model.accuracy}%`
                        }}
                      ></div>
                    </div>

                    <div className="metric-row small">
                      <span>AUC Score</span>
                      <strong>{model.auc}</strong>
                    </div>

                  </div>
                )
              )}

          </div>

        </section>


        {/* ADVERSARIAL LAB */}

        <section className="section">

          <div className="section-title">
            <div>
              <p>ADVERSARIAL INTELLIGENCE</p>
              <h2>Stress Testing Lab</h2>
            </div>
          </div>

          <div className="lab-card">

            <div className="stress-control">

              <div>
                <span className="label">
                  STRESS INTENSITY
                </span>

                <h2>{stress.toFixed(1)}x</h2>
              </div>

              <input
                type="range"
                min="0.2"
                max="2"
                step="0.1"
                value={stress}
                onChange={(e) =>
                  setStress(Number(e.target.value))
                }
              />

              <button
                className="primary-btn"
                onClick={runStressTest}
              >
                <Zap size={18} />

                {loading
                  ? "ANALYZING..."
                  : "RUN STRESS TEST"}
              </button>

            </div>


            {stressResult && (

              <div className="stress-results">

                <div>
                  <span>TRUST SCORE</span>
                  <strong>
                    {stressResult.trust_score}
                  </strong>
                </div>

                <div>
                  <span>CORRELATION RISK</span>
                  <strong className="danger">
                    {stressResult.correlated_failure_rate}%
                  </strong>
                </div>

                <div>
                  <span>STATUS</span>
                  <strong>
                    {stressResult.trust_level}
                  </strong>
                </div>

              </div>

            )}

          </div>

        </section>


        {/* RED TEAM */}

        <section className="red-team-card">

          <div>

            <div className="red-team-title">
              <AlertTriangle size={22} />
              AI RED TEAM AGENT
            </div>

            <h2>
              Discover hidden AI failure combinations
            </h2>

            <p>
              PRISM autonomously explores adversarial
              conditions and identifies systemic blind spots
              before deployment.
            </p>

          </div>

          <button
            className="red-btn"
            onClick={runRedTeam}
          >
            {redTeamLoading
              ? "AGENT EXPLORING..."
              : "LAUNCH AGENT"}

            <ChevronRight size={18} />
          </button>

        </section>


        {/* INCIDENT */}

        {incident && (

          <section className="incident-card">

            <div className="incident-header">
              <div>
                <span className="incident-label">
                  🚨 BLIND SPOT DISCOVERED
                </span>

                <h2>
                  {incident.incident.incident_id}
                </h2>
              </div>

              <div className="severity">
                {incident.incident.severity}
              </div>
            </div>


            <div className="incident-grid">

              <div>
                <span>Worst Stress Level</span>
                <strong>
                  {incident.worst_scenario.stress_level}x
                </strong>
              </div>

              <div>
                <span>Trust Score</span>
                <strong>
                  {incident.worst_scenario.trust_score}
                </strong>
              </div>

              <div>
                <span>Correlation Risk</span>
                <strong>
                  {incident.worst_scenario.correlated_failure_rate}%
                </strong>
              </div>

              <div>
                <span>Scenarios Tested</span>
                <strong>
                  {incident.scenarios_tested}
                </strong>
              </div>

            </div>

          </section>

        )}

      </main>
    </div>
  );
}

export default App;