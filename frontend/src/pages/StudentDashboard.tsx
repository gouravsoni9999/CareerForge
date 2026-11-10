
import { useEffect, useState, type FormEvent } from "react";
import { apiRequest } from "../lib/api";
import { useAuth } from "../context/AuthContext";

type Opportunity = {
  id: number;
  title: string;
  opportunity_type: string;
  company_name: string;
  company_location: string;
  location: string;
  work_mode: string;
  openings: number;
  compensation_min: number | null;
  compensation_max: number | null;
  compensation_period: string | null;
  application_deadline: string | null;
};

type Application = {
  id: number;
  opportunity: number;
  opportunity_title: string;
  company_name: string;
  opportunity_type: string;
  opportunity_location: string;
  cover_letter: string;
  status: string;
  applied_at: string;
};

type ListResponse<T> = T[] | { results: T[] };

function getItems<T>(data: ListResponse<T>): T[] {
  return Array.isArray(data) ? data : data.results;
}

export default function StudentDashboard() {
  const { user, logout } = useAuth();

  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [applications, setApplications] = useState<Application[]>([]);
  const [search, setSearch] = useState("");
  const [activeTab, setActiveTab] = useState<"opportunities" | "applications">(
    "opportunities",
  );
  const [selectedOpportunity, setSelectedOpportunity] =
    useState<Opportunity | null>(null);
  const [coverLetter, setCoverLetter] = useState("");
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function loadDashboard() {
    setLoading(true);
    setError("");

    try {
      const [opportunityData, applicationData] = await Promise.all([
        apiRequest<ListResponse<Opportunity>>("/api/opportunities/"),
        apiRequest<ListResponse<Application>>("/api/applications/"),
      ]);

      setOpportunities(getItems(opportunityData));
      setApplications(getItems(applicationData));
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load your dashboard.",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadDashboard();
  }, []);

  async function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const query = search.trim()
        ? `?search=${encodeURIComponent(search.trim())}`
        : "";

      const data = await apiRequest<ListResponse<Opportunity>>(
        `/api/opportunities/${query}`,
      );

      setOpportunities(getItems(data));
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Search failed.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleApply(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedOpportunity) return;

    setApplying(true);
    setError("");
    setSuccess("");

    try {
      await apiRequest("/api/applications/", {
        method: "POST",
        body: JSON.stringify({
          opportunity: selectedOpportunity.id,
          cover_letter: coverLetter,
        }),
      });

      setSuccess(`Successfully applied for ${selectedOpportunity.title}.`);
      setSelectedOpportunity(null);
      setCoverLetter("");
      setActiveTab("applications");

      await loadDashboard();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to submit application.",
      );
    } finally {
      setApplying(false);
    }
  }

  function formatDate(date: string | null) {
    if (!date) return "Not specified";

    return new Date(`${date}T00:00:00`).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  }

  function formatCompensation(opportunity: Opportunity) {
    if (
      opportunity.compensation_min == null &&
      opportunity.compensation_max == null
    ) {
      return "Not specified";
    }

    const min = opportunity.compensation_min;
    const max = opportunity.compensation_max;

    if (min != null && max != null) {
      return `₹${min.toLocaleString("en-IN")} – ₹${max.toLocaleString("en-IN")}`;
    }

    const amount = min ?? max;
    return `₹${amount!.toLocaleString("en-IN")}`;
  }

  if (!user) return null;

  return (
    <main className="student-dashboard">
      <header className="student-header">
        <a href="/" className="student-brand">CareerForge</a>

        <div className="student-user">
          <span>{user.first_name} {user.last_name}</span>
          <a href="/student/profile" className="student-profile-link">
            My Profile
          </a>
          <a href="/student/resumes" className="student-profile-link">
            My Resumes
          </a>
          <button className="student-logout" onClick={logout}>
            Logout
          </button>
        </div>
      </header>

      <section className="student-welcome">
        <p className="student-eyebrow">STUDENT WORKSPACE</p>
        <h1>Welcome back, {user.first_name}!</h1>
        <p>Discover opportunities and take the next step in your career.</p>
      </section>

      <section className="student-stats">
        <article className="student-stat">
          <span>Available opportunities</span>
          <strong>{opportunities.length}</strong>
        </article>

        <article className="student-stat">
          <span>Applications submitted</span>
          <strong>{applications.length}</strong>
        </article>

        <article className="student-stat">
          <span>Shortlisted</span>
          <strong>
            {applications.filter((app) => app.status === "SHORTLISTED").length}
          </strong>
        </article>
      </section>

      <nav className="student-tabs">
        <button
          className={activeTab === "opportunities" ? "active" : ""}
          onClick={() => setActiveTab("opportunities")}
        >
          Explore opportunities
        </button>

        <button
          className={activeTab === "applications" ? "active" : ""}
          onClick={() => setActiveTab("applications")}
        >
          My applications
        </button>
      </nav>

      {error && <p className="student-message error">{error}</p>}
      {success && <p className="student-message success">{success}</p>}

      {activeTab === "opportunities" && (
        <section className="student-section">
          <div className="student-section-heading">
            <div>
              <h2>Explore opportunities</h2>
              <p>Find internships and jobs that match your goals.</p>
            </div>

            <form className="student-search" onSubmit={handleSearch}>
              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search jobs, companies..."
              />
              <button type="submit">Search</button>
            </form>
          </div>

          {loading ? (
            <p className="student-empty">Loading opportunities...</p>
          ) : opportunities.length === 0 ? (
            <p className="student-empty">
              No opportunities found. Try another search.
            </p>
          ) : (
            <div className="opportunity-grid">
              {opportunities.map((opportunity) => (
                <article className="opportunity-card" key={opportunity.id}>
                  <div className="opportunity-card-top">
                    <span className="opportunity-type">
                      {opportunity.opportunity_type}
                    </span>
                    <span className="opportunity-mode">
                      {opportunity.work_mode}
                    </span>
                  </div>

                  <h3>{opportunity.title}</h3>
                  <p className="opportunity-company">
                    {opportunity.company_name}
                  </p>

                  <div className="opportunity-details">
                    <span>📍 {opportunity.location || "Location not specified"}</span>
                    <span>👥 {opportunity.openings} opening(s)</span>
                    <span>💰 {formatCompensation(opportunity)}</span>
                    <span>📅 Deadline: {formatDate(opportunity.application_deadline)}</span>
                  </div>

                  <button
                    className="opportunity-apply"
                    onClick={() => {
                      setSelectedOpportunity(opportunity);
                      setError("");
                      setSuccess("");
                    }}
                  >
                    Apply now
                  </button>
                </article>
              ))}
            </div>
          )}
        </section>
      )}

      {activeTab === "applications" && (
        <section className="student-section">
          <h2>My applications</h2>
          <p className="student-section-description">
            Track the progress of your submitted applications.
          </p>

          {loading ? (
            <p className="student-empty">Loading applications...</p>
          ) : applications.length === 0 ? (
            <p className="student-empty">
              You haven't applied to any opportunities yet.
            </p>
          ) : (
            <div className="application-list">
              {applications.map((application) => (
                <article className="application-card" key={application.id}>
                  <div>
                    <h3>{application.opportunity_title}</h3>
                    <p>{application.company_name}</p>
                    <small>
                      Applied on {new Date(application.applied_at).toLocaleDateString("en-IN")}
                    </small>
                  </div>

                  <span className="application-status">
                    {application.status.replaceAll("_", " ")}
                  </span>
                </article>
              ))}
            </div>
          )}
        </section>
      )}

      {selectedOpportunity && (
        <div className="student-modal-backdrop">
          <form className="student-modal" onSubmit={handleApply}>
            <button
              type="button"
              className="student-modal-close"
              onClick={() => setSelectedOpportunity(null)}
            >
              ✕
            </button>

            <p className="student-eyebrow">APPLICATION</p>
            <h2>{selectedOpportunity.title}</h2>
            <p>{selectedOpportunity.company_name}</p>

            <label htmlFor="coverLetter">Cover letter</label>
            <textarea
              id="coverLetter"
              value={coverLetter}
              onChange={(event) => setCoverLetter(event.target.value)}
              placeholder="Tell the recruiter why you're suitable for this opportunity..."
              rows={6}
            />

            <div className="student-modal-actions">
              <button
                type="button"
                className="student-cancel"
                onClick={() => setSelectedOpportunity(null)}
              >
                Cancel
              </button>

              <button
                type="submit"
                className="opportunity-apply"
                disabled={applying}
              >
                {applying ? "Submitting..." : "Submit application"}
              </button>
            </div>
          </form>
        </div>
      )}
    </main>
  );
}