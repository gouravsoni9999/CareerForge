
import { useAuth } from "../context/AuthContext";
import StudentDashboard from "./StudentDashboard";
import RecruiterDashboard from "./RecruiterDashboard";

export default function DashboardPage() {
  const { user } = useAuth();

  if (!user) return null;

  if (user.role === "STUDENT") {
    return <StudentDashboard />;
  }

  if (user.role === "RECRUITER") {
    return <RecruiterDashboard />;
  }

  return (
    <main className="dashboard">
      <header className="dashboard-nav">
        <span className="brand">CareerForge</span>
        <button
          className="secondary-button"
          onClick={() => {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            window.location.href = "/login";
          }}
        >
          Logout
        </button>
      </header>

      <section className="dashboard-content">
        <p className="eyebrow">{user.role} DASHBOARD</p>
        <h1>Welcome, {user.first_name}!</h1>
        <p className="muted">
          Your role-specific workspace is coming next.
        </p>
      </section>
    </main>
  );
}