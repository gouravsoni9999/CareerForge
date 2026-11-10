
import { useEffect, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../lib/api";

type Resume = {
  id: number;
  title: string;
  file: string;
  is_primary: boolean;
  uploaded_at: string;
  updated_at: string;
};

export default function StudentResumesPage() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [title, setTitle] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [isPrimary, setIsPrimary] = useState(true);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function loadResumes() {
    setLoading(true);
    setError("");

    try {
      const data = await apiRequest<Resume[]>(
        "/api/students/me/resumes/",
      );
      setResumes(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load resumes.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadResumes();
  }, []);

  async function uploadResume(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!file) {
      setError("Please select a resume file.");
      return;
    }

    const formData = new FormData();
    formData.append("title", title.trim() || file.name);
    formData.append("file", file);
    formData.append("is_primary", String(isPrimary));

    setUploading(true);
    setError("");
    setMessage("");

    try {
      await apiRequest<Resume>("/api/students/me/resumes/", {
        method: "POST",
        body: formData,
      });

      setTitle("");
      setFile(null);
      setIsPrimary(true);

      const fileInput = document.getElementById(
        "resume-file",
      ) as HTMLInputElement | null;

      if (fileInput) fileInput.value = "";

      setMessage("Resume uploaded successfully.");
      await loadResumes();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Resume upload failed.");
    } finally {
      setUploading(false);
    }
  }

  async function setPrimary(resumeId: number) {
    setError("");
    setMessage("");

    try {
      await apiRequest<Resume>(
        `/api/students/me/resumes/${resumeId}/`,
        {
          method: "PATCH",
          body: JSON.stringify({ is_primary: true }),
        },
      );

      setMessage("Primary resume updated.");
      await loadResumes();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to update resume.");
    }
  }

  async function updateTitle(resume: Resume) {
    const newTitle = window.prompt("Enter a new resume title:", resume.title);

    if (newTitle === null || !newTitle.trim()) return;

    setError("");
    setMessage("");

    try {
      await apiRequest<Resume>(
        `/api/students/me/resumes/${resume.id}/`,
        {
          method: "PATCH",
          body: JSON.stringify({ title: newTitle.trim() }),
        },
      );

      setMessage("Resume title updated.");
      await loadResumes();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to rename resume.");
    }
  }

  async function deleteResume(resume: Resume) {
    if (!window.confirm(`Delete "${resume.title}"?`)) return;

    setError("");
    setMessage("");

    try {
      await apiRequest(
        `/api/students/me/resumes/${resume.id}/`,
        { method: "DELETE" },
      );

      setMessage("Resume deleted successfully.");
      await loadResumes();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to delete resume.");
    }
  }

  if (loading) {
    return <main className="resume-page"><p>Loading resumes...</p></main>;
  }

  return (
    <main className="resume-page">
      <header className="resume-header">
        <Link to="/dashboard" className="resume-brand">CareerForge</Link>
        <Link to="/student/profile" className="resume-back">
          My Profile
        </Link>
      </header>

      <section className="resume-content">
        <p className="student-eyebrow">STUDENT ACCOUNT</p>
        <h1>Resume Management</h1>
        <p className="resume-description">
          Upload and manage the resumes you use when applying for opportunities.
        </p>

        {error && <p className="profile-error">{error}</p>}
        {message && <p className="profile-success">{message}</p>}

        <form className="resume-upload-panel" onSubmit={uploadResume}>
          <h2>Upload a new resume</h2>

          <label>
            Resume title
            <input
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="e.g. Software Developer Resume"
            />
          </label>

          <label>
            Select resume file
            <input
              id="resume-file"
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={(event) =>
                setFile(event.target.files?.[0] ?? null)
              }
              required
            />
          </label>

          {file && (
            <p className="resume-file-name">
              Selected: {file.name}
            </p>
          )}

          <label className="resume-primary-option">
            <input
              type="checkbox"
              checked={isPrimary}
              onChange={(event) => setIsPrimary(event.target.checked)}
            />
            Set as my primary resume
          </label>

          <button className="profile-save" type="submit" disabled={uploading}>
            {uploading ? "Uploading..." : "Upload resume"}
          </button>
        </form>

        <section className="resume-list-section">
          <h2>My resumes ({resumes.length})</h2>

          {resumes.length === 0 ? (
            <p className="profile-empty">
              You haven't uploaded any resumes yet.
            </p>
          ) : (
            <div className="resume-list">
              {resumes.map((resume) => (
                <article className="resume-card" key={resume.id}>
                  <div className="resume-card-info">
                    <div className="resume-file-icon">PDF</div>
                    <div>
                      <h3>{resume.title}</h3>
                      <p>
                        Uploaded{" "}
                        {new Date(resume.uploaded_at).toLocaleDateString("en-IN")}
                      </p>
                      {resume.is_primary && (
                        <span className="resume-primary-badge">
                          Primary resume
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="resume-actions">
                    <a
                      href={resume.file}
                      target="_blank"
                      rel="noreferrer"
                      className="resume-action-link"
                    >
                      View
                    </a>

                    <button
                      type="button"
                      onClick={() => void updateTitle(resume)}
                    >
                      Rename
                    </button>

                    {!resume.is_primary && (
                      <button
                        type="button"
                        onClick={() => void setPrimary(resume.id)}
                      >
                        Make primary
                      </button>
                    )}

                    <button
                      type="button"
                      className="resume-delete"
                      onClick={() => void deleteResume(resume)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}