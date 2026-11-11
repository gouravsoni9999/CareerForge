
import { useEffect, useState, type FormEvent } from "react";
import { apiRequest } from "../lib/api";
import { useAuth } from "../context/AuthContext";
import RecruiterOpportunities from "./RecruiterOpportunities";

type RecruiterProfile = {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  company: number | null;
  company_name: string | null;
  company_verification_status: "PENDING" | "VERIFIED" | "REJECTED" | null;
  phone_number: string;
  designation: string;
};

type CompanyForm = {
  name: string;
  website: string;
  industry: string;
  description: string;
  location: string;
};

type Company = CompanyForm & {
  id: number;
  verification_status: "PENDING" | "VERIFIED" | "REJECTED";
};

const initialCompany: CompanyForm = {
  name: "",
  website: "",
  industry: "",
  description: "",
  location: "",
};

export default function RecruiterDashboard() {
  const { user, logout } = useAuth();
  const [, setProfile] = useState<RecruiterProfile | null>(null);
  const [company, setCompany] = useState<Company | null>(null);
  const [form, setForm] = useState<CompanyForm>(initialCompany);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function loadRecruiter() {
    setLoading(true);
    setError("");

    try {
      const data = await apiRequest<RecruiterProfile>("/api/recruiters/me/");
      setProfile(data);

      // The recruiter profile exposes the associated company ID and name.
      // The company registration response provides the full company details.
      if (data.company) {
        setCompany({
          ...initialCompany,
          id: data.company,
          name: data.company_name || "Registered company",
          verification_status: data.company_verification_status || "PENDING",
        });
      } else {
        setCompany(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load recruiter profile.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadRecruiter();
  }, []);

  async function registerCompany(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    setMessage("");

    try {
      const created = await apiRequest<Company>("/api/companies/", {
        method: "POST",
        body: JSON.stringify(form),
      });

      setCompany(created);
      setMessage("Company submitted successfully. Awaiting admin verification.");
      await loadRecruiter();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Company registration failed.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <main className="recruiter-page"><p>Loading recruiter workspace...</p></main>;
  }

  return (
    <main className="recruiter-page">
      <header className="recruiter-header">
        <a href="/" className="recruiter-brand">CareerForge</a>
        <div className="recruiter-user">
          <span>{user?.first_name} {user?.last_name}</span>
          <button onClick={logout}>Logout</button>
        </div>
      </header>

      <section className="recruiter-content">
        <p className="student-eyebrow">RECRUITER WORKSPACE</p>
        <h1>Welcome, {user?.first_name}!</h1>
        <p className="recruiter-subtitle">
          Manage your company and recruitment activities.
        </p>

        {error && <p className="profile-error">{error}</p>}
        {message && <p className="profile-success">{message}</p>}

        <section className="recruiter-panel">
          <h2>Company verification</h2>
          <p className="recruiter-muted">
            Register your organization before creating and publishing opportunities.
          </p>

          {company ? (
            <div className="company-summary">
              <h3>{company.name}</h3>
              <p>{company.industry || "Industry not specified"}</p>
              <p>{company.location || "Location not specified"}</p>

              <span className={`company-status ${company.verification_status.toLowerCase()}`}>
                {company.verification_status.replace("_", " ")}
              </span>

              {company.verification_status === "PENDING" && (
                <p className="recruiter-muted">
                  Your company is awaiting administrator verification.
                  You can publish opportunities after approval.
                </p>
              )}

              {company.verification_status === "REJECTED" && (
                <p className="profile-error">
                  Your company registration was rejected. Please contact the administrator.
                </p>
              )}

              {company?.verification_status === "VERIFIED" ? (
                <RecruiterOpportunities />
              ) : (
                <section className="recruiter-panel">
                  <h2>Recruitment workspace</h2>
                  <div className="recruiter-placeholder">
                    Complete company verification to unlock opportunity publishing.
                  </div>
                </section>
              )}
            </div>
          ) : (
            <form className="company-form" onSubmit={registerCompany}>
              <label>
                Company name *
                <input
                  required
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="Enter company name"
                />
              </label>

              <label>
                Website
                <input
                  type="url"
                  value={form.website}
                  onChange={(e) => setForm({ ...form, website: e.target.value })}
                  placeholder="https://example.com"
                />
              </label>

              <label>
                Industry
                <input
                  value={form.industry}
                  onChange={(e) => setForm({ ...form, industry: e.target.value })}
                  placeholder="e.g. Information Technology"
                />
              </label>

              <label>
                Company location
                <input
                  value={form.location}
                  onChange={(e) => setForm({ ...form, location: e.target.value })}
                  placeholder="City, State"
                />
              </label>

              <label className="company-description">
                Description
                <textarea
                  rows={4}
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  placeholder="Briefly describe your organization..."
                />
              </label>

              <button type="submit" disabled={submitting}>
                {submitting ? "Submitting..." : "Register company"}
              </button>
            </form>
          )}
        </section>

        <section className="recruiter-panel">
          <h2>Recruitment workspace</h2>
          <p className="recruiter-muted">
            Opportunity management and applicant tracking will be available here.
          </p>
          <div className="recruiter-placeholder">
            {company?.verification_status === "VERIFIED"
              ? "Your company is verified. You are ready to manage opportunities."
              : "Complete company verification to unlock opportunity publishing."}
          </div>
        </section>
      </section>
    </main>
  );
}