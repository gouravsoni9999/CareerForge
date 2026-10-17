
import './App.css';

function App() {
  return (
    <main className="app">
      <header className="navbar">
        <a className="brand" href="/" aria-label="CareerForge home">
          <span className="brand-mark">C</span>
          <span>CareerForge</span>
        </a>

        <span className="environment-label">
          Development Preview
        </span>
      </header>

      <section className="hero">
        <p className="eyebrow">YOUR CAREER STARTS HERE</p>

        <h1>
          Build your future.
          <br />
          <span>Forge your career.</span>
        </h1>

        <p className="description">
          A unified platform for discovering internships, exploring
          placement opportunities, and managing your career journey.
        </p>

        <div className="status">
          <span className="status-dot" />
          Frontend is running successfully
        </div>

        <p className="footer-note">
          CareerForge · Internship & Placement Management Platform
        </p>
      </section>
    </main>
  );
}

export default App;
