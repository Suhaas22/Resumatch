import { useState, useRef, useCallback, useEffect } from "react";
import "./Home.css";

function pct(v) { return `${Math.round(v ?? 0)}%`; }
function round1(v) { return Math.round((v ?? 0) * 10) / 10; }

function Confetti({ score }) {
  const [particles, setParticles] = useState([]);
  useEffect(() => {
    if (score < 75) return;
    const cols = ["#bf7fff","#4de8b8","#ffc844","#ff5f5f","#e040fb"];
    const ps = Array.from({ length: 60 }, (_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      color: cols[Math.floor(Math.random() * cols.length)],
      duration: `${1.5 + Math.random() * 2}s`,
      delay: `${Math.random() * 1}s`,
      size: `${4 + Math.random() * 6}px`,
    }));
    setParticles(ps);
    const t = setTimeout(() => setParticles([]), 3500);
    return () => clearTimeout(t);
  }, [score]);

  if (!particles.length) return null;
  return (
    <div className="confetti-wrap">
      {particles.map(p => (
        <div key={p.id} className="confetti-p" style={{
          left: p.left, background: p.color,
          width: p.size, height: p.size,
          animationDuration: p.duration,
          animationDelay: p.delay,
        }} />
      ))}
    </div>
  );
}

function CountUp({ target, duration = 1400, suffix = "" }) {
  const [val, setVal] = useState(0);
  const [done, setDone] = useState(false);
  useEffect(() => {
    let start = null;
    const step = ts => {
      if (!start) start = ts;
      const p = Math.min((ts - start) / duration, 1);
      const ease = 1 - Math.pow(1 - p, 3);
      setVal(Math.round(ease * target));
      if (p < 1) requestAnimationFrame(step);
      else setDone(true);
    };
    requestAnimationFrame(step);
  }, [target, duration]);
  return <span className={done ? "" : "counting"}>{val}{suffix}</span>;
}

function Ring({ score }) {
  const r    = 48;
  const circ = 2 * Math.PI * r;
  const s    = Math.round(score ?? 0);
  const col  = s >= 75 ? "#bf7fff" : s >= 50 ? "#4de8b8" : "#ff5f5f";
  const [offset, setOffset] = useState(circ);
  useEffect(() => {
    const t = setTimeout(() => setOffset(circ - (s / 100) * circ), 80);
    return () => clearTimeout(t);
  }, [s, circ]);
  return (
    <div className="ring-wrap">
      <svg viewBox="0 0 120 120">
        <circle className="ring-bg"  cx="60" cy="60" r={r} />
        <circle className="ring-arc" cx="60" cy="60" r={r}
          stroke={col} strokeDasharray={circ} strokeDashoffset={offset} />
      </svg>
      <div className="ring-inner">
        <span className="ring-num" style={{ color: col }}>
          <CountUp target={s} />
        </span>
        <span className="ring-sub">/ 100</span>
      </div>
      <div className="ring-pulse" style={{ borderColor: col }} />
    </div>
  );
}

function getVerdict(s) {
  if (s >= 85) return { label: "Excellent Match",  desc: "Your resume aligns strongly with this role. You're a standout candidate worth interviewing.",   col: "#bf7fff", badge: "Top Tier", badgeBg: "rgba(191,127,255,0.1)", badgeBorder: "rgba(191,127,255,0.3)" };
  if (s >= 70) return { label: "Strong Match",      desc: "Good compatibility. A few targeted improvements will make your application bulletproof.",         col: "#4de8b8", badge: "Above Average", badgeBg: "rgba(77,232,184,0.08)", badgeBorder: "rgba(77,232,184,0.25)" };
  if (s >= 50) return { label: "Moderate Match",    desc: "Some relevant experience detected, but notable gaps need attention before applying.",             col: "#ffc844", badge: "Needs Work", badgeBg: "rgba(255,200,68,0.08)", badgeBorder: "rgba(255,200,68,0.25)" };
  return        { label: "Low Match",               desc: "Significant gaps between your resume and this role. Use the suggestions below to get ready.",     col: "#ff5f5f", badge: "Needs Improvement", badgeBg: "rgba(255,95,95,0.08)", badgeBorder: "rgba(255,95,95,0.25)" };
}

function Divider({ label }) {
  return (
    <div className="sec-divider">
      <span className="sec-divider-label">{label}</span>
      <span className="sec-divider-line" />
    </div>
  );
}

function BdItem({ label, value, color, desc, delay = 0 }) {
  const v = Math.round(value ?? 0);
  const [width, setWidth] = useState(0);
  useEffect(() => {
    const t = setTimeout(() => setWidth(v), 200 + delay);
    return () => clearTimeout(t);
  }, [v, delay]);
  return (
    <div className="bd-item">
      <div className="bd-item-glow" style={{ background: `linear-gradient(90deg, ${color}, transparent)` }} />
      <div className="bd-label">{label}</div>
      <div className="bd-pct" style={{ color }}>
        <CountUp target={v} suffix="%" duration={1200} />
      </div>
      <div className="bd-track">
        <div className="bd-fill" style={{ width: `${width}%`, background: color }} />
      </div>
      <div className="bd-desc">{desc}</div>
    </div>
  );
}

function CursorGlow() {
  const ref = useRef(null);
  useEffect(() => {
    const move = e => {
      if (ref.current) {
        ref.current.style.left = e.clientX + "px";
        ref.current.style.top  = e.clientY + "px";
      }
    };
    window.addEventListener("mousemove", move);
    return () => window.removeEventListener("mousemove", move);
  }, []);
  return <div ref={ref} className="cursor-glow" />;
}

function useCardMouse(ref) {
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const move = e => {
      const r = el.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width * 100).toFixed(1);
      const y = ((e.clientY - r.top)  / r.height * 100).toFixed(1);
      el.style.setProperty("--mx", x + "%");
      el.style.setProperty("--my", y + "%");
    };
    el.addEventListener("mousemove", move);
    return () => el.removeEventListener("mousemove", move);
  }, []);
}

const LOAD_STEPS = ["Parsing Resume", "Extracting Skills", "Scoring Fit", "Building Report"];
function LoadingBar() {
  const [step, setStep] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setStep(s => (s + 1) % LOAD_STEPS.length), 900);
    return () => clearInterval(t);
  }, []);
  return (
    <div className="load-wrap">
      <div className="load-bar"><div className="load-fill" /></div>
      <div className="load-status">
        {LOAD_STEPS.map((s, i) => (
          <div key={s} className={`load-step ${i === step ? "active" : ""}`}>
            <div className="load-step-dot" />
            {s}
          </div>
        ))}
      </div>
    </div>
  );
}

async function callAPI(file, jd) {
  const fd = new FormData();
  fd.append("resume", file);
  fd.append("job_description", jd);
  const res = await fetch("https://resumatch-backend-hbfn.onrender.com/api/match/", { method: "POST", body: fd });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}


export default function Home() {
  const [file,    setFile]    = useState(null);
  const [jd,      setJd]      = useState("");
  const [drag,    setDrag]    = useState(false);
  const [loading, setLoading] = useState(false);
  const [result,  setResult]  = useState(null);
  const [error,   setError]   = useState(null);
  const fileRef  = useRef(null);
  const card1Ref = useRef(null);
  const card2Ref = useRef(null);
  useCardMouse(card1Ref);
  useCardMouse(card2Ref);

  const pickFile = f => {
    if (!f) return;
    if (f.type !== "application/pdf") { setError("Please upload a PDF file."); return; }
    setFile(f); setError(null);
  };

  const onDrop = useCallback(e => {
    e.preventDefault(); setDrag(false); pickFile(e.dataTransfer.files[0]);
  }, []);

  const submit = async () => {
    if (!file || !jd.trim()) return;
    setLoading(true); setError(null); setResult(null);
    try   { setResult(await callAPI(file, jd)); }
    catch { setError("Failed to connect to backend. Make sure Django is running on port 8000."); }
    finally { setLoading(false); }
  };

  const canGo = file && jd.trim().length > 20 && !loading;
  const score   = result ? Math.round(result.score ?? 0) : null;
  const verdict = score !== null ? getVerdict(score) : null;

  return (
    <>

      {/* Background layers */}
      <div className="bg-anim">
        <div className="orb orb1" /><div className="orb orb2" /><div className="orb orb3" />
      </div>
      <div className="grid-lines" />
      <CursorGlow />
      {result && <Confetti score={score} />}

      <div className="app">

        {/* header */}
        <header className="hdr">
          <div className="logo">
            <span className="logo-name">Resu<em>match</em></span>
          </div>
          <div className="hdr-right">
            <div className="hdr-dot-group">
              <div className="hdr-dot" /><div className="hdr-dot" /><div className="hdr-dot" />
            </div>
            <span className="hdr-pill">AI Powered</span>
          </div>
        </header>

        {/* hero */}
        <div className="hero">
          <div className="eyebrow">
            <span className="eyebrow-line" />
            Resume Intelligence
          </div>
          <h1 className="hero-h1">
            Know your<br />
            <span className="grad">perfect fit score.</span>
          </h1>
          <p className="hero-p">
            Upload your resume and a job description. Our engine extracts skills,
            scores compatibility, and tells you exactly where to improve — in seconds.
          </p>
          <div className="hero-badge">
            <div className="hero-badge-dot">✦</div>
            Powered by semantic skill extraction + TF-IDF analysis
          </div>
        </div>

        {/* inputs */}
        <div className="input-grid">
          <div className="card" ref={card1Ref}>
            <div className="card-lbl">
              <span className="pip" style={{ background: "var(--acc)" }} />
              Resume Upload
            </div>
            <div
              className={`drop ${drag ? "over" : ""}`}
              onClick={() => fileRef.current?.click()}
              onDrop={onDrop}
              onDragOver={e => { e.preventDefault(); setDrag(true); }}
              onDragLeave={() => setDrag(false)}
            >
              <div className="drop-ring" />
              <div className="drop-ico">📎</div>
              <div className="drop-title">Drop PDF or click to browse</div>
              <div className="drop-hint">PDF only · max 10 MB</div>
            </div>
            <input ref={fileRef} type="file" accept=".pdf" hidden
              onChange={e => pickFile(e.target.files[0])} />
            {file && (
              <div className="file-pill">
                <span className="fp-ico">📋</span>
                <div className="fp-body">
                  <div className="fp-name">{file.name}</div>
                  <div className="fp-meta">{(file.size / 1024).toFixed(1)} KB · PDF</div>
                </div>
                <button className="fp-rm" onClick={e => { e.stopPropagation(); setFile(null); }}>✕</button>
              </div>
            )}
          </div>

          <div className="card" ref={card2Ref}>
            <div className="card-lbl">
              <span className="pip" style={{ background: "var(--acc2)" }} />
              Job Description
            </div>
            <textarea
              placeholder={"Paste the full job description here…\n\nInclude requirements, responsibilities, and preferred qualifications for best results."}
              value={jd}
              onChange={e => setJd(e.target.value)}
            />
            <div className="ta-meta">
              {jd.length} chars{jd.length > 0 && jd.length < 80 ? " · add more for better accuracy" : ""}
            </div>
          </div>
        </div>

        {/* cta */}
        <div className="cta-wrap">
          <button className="btn-go" disabled={!canGo} onClick={submit}>
            {loading
              ? <><div className="spin" />&nbsp;Analysing…</>
              : <><span className="btn-icon">⚡</span> Analyse Match</>}
          </button>
        </div>

        {loading && <LoadingBar />}
        {error && <div className="err-bar">⚠️&nbsp; {error}</div>}

        {/* Results */}
        {result && verdict && (
          <div className="results">

            {/* overall score */}
            <Divider label="Overall Score" />
            <div className="score-card">
              <div className="score-card-bg" />
              <Ring score={result.score} />
              <div className="score-info">
                <div className="score-tag">Compatibility Score</div>
                <div className="score-verdict" style={{ color: verdict.col }}>{verdict.label}</div>
                <div className="score-desc">{verdict.desc}</div>
                <div className="score-badge" style={{ background: verdict.badgeBg, borderColor: verdict.badgeBorder, color: verdict.col }}>
                  <div className="score-badge-dot" style={{ background: verdict.col }} />
                  {verdict.badge}
                </div>
              </div>
            </div>

            {/* breakdown */}
            <Divider label="Score Breakdown" />
            <div className="breakdown-card">
              <div className="bd-grid">
                <BdItem label="Skill Match"    value={result.skill_score}      color="#bf7fff" delay={0}   desc="How well your skills overlap with the job requirements" />
                <BdItem label="Text Relevance" value={result.text_score}       color="#4de8b8" delay={150} desc="Overall textual similarity between your resume and the JD" />
                <BdItem label="Experience Fit" value={result.experience_score} color="#ffc844" delay={300} desc="How your years of experience align with the expected level" />
                <BdItem label="Projects Score" value={result.projects_score}   color="#ff7eb3" delay={450} desc="Strength and relevance of your project portfolio to this role" />
              </div>
            </div>

            {/* stats */}
            <Divider label="Profile at a Glance" />
            <div className="stats-row">
              <div className="stat-card">
                <div className="stat-card-glow" style={{ background: "radial-gradient(circle, rgba(255,200,68,0.12) 0%, transparent 70%)" }} />
                <div className="stat-icon-wrap">🗓️</div>
                <div className="stat-body">
                  <div className="stat-value" style={{ color: "#ffc844" }}>
                    <CountUp target={Math.round(round1(result.experience_years) * 10) / 10} duration={1000} />
                    <span className="stat-unit">yrs</span>
                  </div>
                  <div className="stat-label">Experience Detected</div>
                  <div className="stat-sub">
                    {result.experience_years >= 5 ? "Senior-level experience" : result.experience_years >= 2 ? "Mid-level experience" : "Junior-level experience"}
                  </div>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-card-glow" style={{ background: "radial-gradient(circle, rgba(77,232,184,0.1) 0%, transparent 70%)" }} />
                <div className="stat-icon-wrap">🗂️</div>
                <div className="stat-body">
                  <div className="stat-value" style={{ color: "#4de8b8" }}>
                    <CountUp target={result.projects_count ?? result.project_count ?? 0} duration={900} />
                  </div>
                  <div className="stat-label">Projects Found</div>
                  <div className="stat-sub">
                    {(result.projects_count ?? result.project_count ?? 0) >= 4 ? "Strong project portfolio" : (result.projects_count ?? result.project_count ?? 0) >= 2 ? "Moderate project experience" : "Consider adding more projects"}
                  </div>
                </div>
              </div>
            </div>

            {/* skills */}
            <Divider label="Skill Analysis" />
            <div className="skills-grid">
              <div className="sk-card">
                <div className="sk-hdr">
                  <span className="sk-title">Resume Skills</span>
                  <span className="sk-count">{result.resume_skills?.length ?? 0}</span>
                </div>
                <div className="chip-wrap">
                  {result.resume_skills?.length > 0
                    ? result.resume_skills.map((s, i) => (
                        <span key={i} className="chip chip-n" style={{ animationDelay: `${i * .04}s` }}>{s}</span>
                      ))
                    : <span className="sk-empty">None detected</span>}
                </div>
              </div>

              <div className="sk-card">
                <div className="sk-hdr">
                  <span className="sk-title" style={{ color: "var(--acc)" }}>Matched Skills</span>
                  <span className="sk-count">{result.matched_skills?.length ?? 0}</span>
                </div>
                <div className="chip-wrap">
                  {result.matched_skills?.length > 0
                    ? result.matched_skills.map((s, i) => (
                        <span key={i} className="chip chip-v" style={{ animationDelay: `${i * .05}s` }}>{s}</span>
                      ))
                    : <span className="sk-empty">No matches found</span>}
                </div>
              </div>

              <div className="sk-card">
                <div className="sk-hdr">
                  <span className="sk-title" style={{ color: "#ffaaaa" }}>Missing Skills</span>
                  <span className="sk-count">{result.missing_skills?.length ?? 0}</span>
                </div>
                <div className="chip-wrap">
                  {result.missing_skills?.length > 0
                    ? result.missing_skills.map((s, i) => (
                        <span key={i} className="chip chip-r" style={{ animationDelay: `${i * .05}s` }}>{s}</span>
                      ))
                    : <span className="sk-empty">No gaps — great match!</span>}
                </div>
              </div>
            </div>

            {/* suggestions */}
            <Divider label="Improvement Suggestions" />
            <div className="sugg-card">
              <div className="sugg-hdr">
                <div className="sugg-hdr-ico">💡</div>
                <span className="sugg-hdr-txt">Action Items to Boost Your Score</span>
              </div>
              {result.suggestions?.length > 0
                ? result.suggestions.map((s, i) => (
                    <div key={i} className="sugg-item" style={{ animationDelay: `${i * .08}s` }}>
                      <span className="sugg-num">
                        0{i + 1}
                        <span className="sugg-num-bar" />
                      </span>
                      <span className="sugg-txt">{s}</span>
                    </div>
                  ))
                : <span className="sk-empty">No suggestions — your resume looks great!</span>}
            </div>

          </div>
        )}
      </div>
    </>
  );
}