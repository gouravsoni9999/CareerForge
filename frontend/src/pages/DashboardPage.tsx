
import { useAuth } from "../context/AuthContext";

export default function DashboardPage() {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <main className="dashboard">
      <header className="dashboard-nav">
        <span className="brand">CareerForge</span>
        <button className="secondary-button" onClick={logout}>
          Logout
        </button>
      </header>

      <section className="dashboard-content">
        <p className="eyebrow">{user.role} DASHBOARD</p>
        <h1>
          Welcome, {user.first_name}!
        </h1>
        <p className="muted">
          You are signed in as {user.email}.
        </p>

        <div className="dashboard-panel">
          <h2>Your CareerForge workspace</h2>
          <p>
            Your account is connected successfully. We will add your
            role-specific dashboard features in the next step.
          </p>
        </div>
      </section>
    </main>
  );
}