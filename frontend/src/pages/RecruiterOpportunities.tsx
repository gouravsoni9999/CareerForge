
import { useEffect, useState, type FormEvent } from "react";
import { apiRequest } from "../lib/api";

type Opportunity = {
  id: number;
  title: string;
  opportunity_type: "INTERNSHIP" | "FULL_TIME";
  description: string;
  responsibilities: string;
  requirements: string;
  eligibility_criteria: string;
  company_name: string;
  location: string;
  work_mode: "ONSITE" | "REMOTE" | "HYBRID";
  openings: number;
  compensation_min: string | null;
  compensation_max: string | null;
  compensation_period: string;
  application_deadline: string;
  status: "DRAFT" | "PUBLISHED" | "CLOSED" | "EXPIRED";
  published_at: string | null;
  created_at: string;
};

type Applicant = {
  id: number;
  student_name: string;
  student_email: string;
  status: string;
  recruiter_notes: string;
  applied_at: string;
};

const initialForm = {
  title: "",
  opportunity_type: "INTERNSHIP",
  description: "",
  responsibilities: "",
  requirements: "",
  eligibility_criteria: "",
  location: "",
  work_mode: "ONSITE",
  openings: "1",
  compensation_min: "",
  compensation_max: "",
  compensation_period: "monthly",
  application_deadline: "",
};

const applicantStatuses = [
  "UNDER_REVIEW",
  "SHORTLISTED",
  "INTERVIEW_SCHEDULED",
  "SELECTED",
  "REJECTED",
];

export default function RecruiterOpportunities() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [form, setForm] = useState(initialForm);
  const [applicants, setApplicants] = useState<Applicant[]>([]);
  const [selectedOpportunity, setSelectedOpportunity] =
    useState<Opportunity | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function loadOpportunities() {
    setLoading(true);
    setError("");

    try {
      const data = await apiRequest<Opportunity[]>(
        "/api/opportunities/manage/"
      );
      setOpportunities(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to load opportunities."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadOpportunities();
  }, []);

  async function createOpportunity(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    setMessage("");

    try {
      const payload = {
        ...form,
        openings: Number(form.openings),
        compensation_min: form.compensation_min || null,
        compensation_max: form.compensation_max || null,
      };

      await apiRequest<Opportunity>("/api/opportunities/manage/", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      setForm(initialForm);
      setMessage("Opportunity saved successfully as a draft.");
      await loadOpportunities();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to create opportunity."
      );
    } finally {
      setSubmitting(false);
    }
  }

  async function publishOpportunity(id: number) {
    setError("");
    setMessage("");

    try {
      await apiRequest<Opportunity>(
        `/api/opportunities/manage/${id}/publish/`,
        { method: "POST" }
      );

      setMessage("Opportunity published successfully.");
      await loadOpportunities();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to publish opportunity."
      );
    }
  }

  async function viewApplicants(opportunity: Opportunity) {
    setError("");
    setMessage("");
    setSelectedOpportunity(opportunity);
    setApplicants([]);

    try {
      const data = await apiRequest<Applicant[]>(
        `/api/opportunities/manage/${opportunity.id}/applications/`
      );
      setApplicants(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to load applicants."
      );
    }
  }

  async function updateApplicant(
    applicantId: number,
    status: string,
    recruiter_notes: string
  ) {
    setError("");
    setMessage("");

    try {
      const updated = await apiRequest<Applicant>(
        `/api/applications/recruiter/${applicantId}/status/`,
        {
          method: "PATCH",
          body: JSON.stringify({ status, recruiter_notes }),
        }
      );

      setApplicants((current) =>
        current.map((applicant) =>
          applicant.id === applicantId ? updated : applicant
        )
      );

      setMessage("Applicant status updated.");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to update applicant."
      );
    }
  }

  return (
    <section className="recruiter-panel">
      <h2>Opportunity management</h2>
      <p className="recruiter-muted">
        Create job and internship listings, publish them, and manage applicants.
      </p>

      {error && <p className="profile-error">{error}</p>}
      {message && <p className="profile-success">{message}</p>}

      <form className="recruiter-opportunity-form" onSubmit={createOpportunity}>
        <h3>Create an opportunity</h3>

        <label>
          Opportunity title *
          <input
            required
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            placeholder="e.g. Backend Developer Intern"
          />
        </label>

        <div className="recruiter-form-grid">
          <label>
            Type *
            <select
              value={form.opportunity_type}
              onChange={(e) =>
                setForm({ ...form, opportunity_type: e.target.value })
              }
            >
              <option value="INTERNSHIP">Internship</option>
              <option value="FULL_TIME">Full-time job</option>
            </select>
          </label>

          <label>
            Work mode *
            <select
              value={form.work_mode}
              onChange={(e) =>
                setForm({ ...form, work_mode: e.target.value })
              }
            >
              <option value="ONSITE">On-site</option>
              <option value="REMOTE">Remote</option>
              <option value="HYBRID">Hybrid</option>
            </select>
          </label>

          <label>
            Location
            <input
              value={form.location}
              onChange={(e) => setForm({ ...form, location: e.target.value })}
              placeholder="e.g. Bhopal / Remote"
            />
          </label>

          <label>
            Number of openings *
            <input
              type="number"
              min="1"
              required
              value={form.openings}
              onChange={(e) => setForm({ ...form, openings: e.target.value })}
            />
          </label>
        </div>

        <label>
          Description *
          <textarea
            required
            rows={4}
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />
        </label>

        <label>
          Responsibilities
          <textarea
            rows={3}
            value={form.responsibilities}
            onChange={(e) =>
              setForm({ ...form, responsibilities: e.target.value })
            }
          />
        </label>

        <label>
          Requirements
          <textarea
            rows={3}
            value={form.requirements}
            onChange={(e) =>
              setForm({ ...form, requirements: e.target.value })
            }
          />
        </label>

        <label>
          Eligibility criteria
          <textarea
            rows={3}
            value={form.eligibility_criteria}
            onChange={(e) =>
              setForm({ ...form, eligibility_criteria: e.target.value })
            }
          />
        </label>

        <div className="recruiter-form-grid">
          <label>
            Minimum compensation (INR)
            <input
              type="number"
              min="0"
              value={form.compensation_min}
              onChange={(e) =>
                setForm({ ...form, compensation_min: e.target.value })
              }
            />
          </label>

          <label>
            Maximum compensation (INR)
            <input
              type="number"
              min="0"
              value={form.compensation_max}
              onChange={(e) =>
                setForm({ ...form, compensation_max: e.target.value })
              }
            />
          </label>

          <label>
            Compensation period
            <select
              value={form.compensation_period}
              onChange={(e) =>
                setForm({ ...form, compensation_period: e.target.value })
              }
            >
              <option value="monthly">Monthly</option>
              <option value="yearly">Yearly</option>
              <option value="one-time">One-time</option>
            </select>
          </label>

          <label>
            Application deadline *
            <input
              type="date"
              required
              min={new Date().toLocaleDateString("en-CA")}
              value={form.application_deadline}
              onChange={(e) =>
                setForm({ ...form, application_deadline: e.target.value })
              }
            />
          </label>
        </div>

        <button type="submit" disabled={submitting}>
          {submitting ? "Saving..." : "Save as draft"}
        </button>
      </form>

      <div className="recruiter-opportunity-list">
        <h3>Your opportunities</h3>

        {loading ? (
          <p>Loading opportunities...</p>
        ) : opportunities.length === 0 ? (
          <p className="profile-empty">You have not created any opportunities yet.</p>
        ) : (
          opportunities.map((opportunity) => (
            <article className="recruiter-opportunity-card" key={opportunity.id}>
              <div>
                <h4>{opportunity.title}</h4>
                <p>
                  {opportunity.opportunity_type.replace("_", " ")} ·{" "}
                  {opportunity.work_mode} · {opportunity.location || "Location not specified"}
                </p>
                <p>
                  Deadline: {opportunity.application_deadline}
                </p>
                <span className={`company-status ${opportunity.status.toLowerCase()}`}>
                  {opportunity.status}
                </span>
              </div>

              <div className="recruiter-opportunity-actions">
                {opportunity.status === "DRAFT" && (
                  <button onClick={() => void publishOpportunity(opportunity.id)}>
                    Publish
                  </button>
                )}

                {opportunity.status === "PUBLISHED" && (
                  <button onClick={() => void viewApplicants(opportunity)}>
                    View applicants
                  </button>
                )}
              </div>
            </article>
          ))
        )}
      </div>

      {selectedOpportunity && (
        <div className="recruiter-applicants">
          <div className="recruiter-applicants-heading">
            <div>
              <h3>Applicants</h3>
              <p>{selectedOpportunity.title}</p>
            </div>
            <button
              className="secondary-button"
              onClick={() => setSelectedOpportunity(null)}
            >
              Close
            </button>
          </div>

          {applicants.length === 0 ? (
            <p className="profile-empty">
              No applicants found for this opportunity.
            </p>
          ) : (
            applicants.map((applicant) => (
              <ApplicantRow
                key={applicant.id}
                applicant={applicant}
                onUpdate={updateApplicant}
              />
            ))
          )}
        </div>
      )}
    </section>
  );
}

function ApplicantRow({
  applicant,
  onUpdate,
}: {
  applicant: Applicant;
  onUpdate: (id: number, status: string, notes: string) => Promise<void>;
}) {
  const [status, setStatus] = useState(applicant.status);
  const [notes, setNotes] = useState(applicant.recruiter_notes || "");
  const [saving, setSaving] = useState(false);

  async function save() {
    setSaving(true);
    await onUpdate(applicant.id, status, notes);
    setSaving(false);
  }

  return (
    <article className="recruiter-applicant-card">
      <div>
        <h4>{applicant.student_name || "Student"}</h4>
        <p>{applicant.student_email}</p>
        <small>Applied: {new Date(applicant.applied_at).toLocaleDateString()}</small>
      </div>

      <div className="recruiter-applicant-controls">
        <label>
          Application status
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="APPLIED" disabled>Applied</option>
            {applicantStatuses.map((item) => (
              <option value={item} key={item}>
                {item.replaceAll("_", " ")}
              </option>
            ))}
          </select>
        </label>

        <label>
          Recruiter notes
          <textarea
            rows={2}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Internal notes..."
          />
        </label>

        <button disabled={saving} onClick={() => void save()}>
          {saving ? "Saving..." : "Update applicant"}
        </button>
      </div>
    </article>
  );
}
