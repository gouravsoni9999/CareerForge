
import { useEffect, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../lib/api";

type StudentProfile = {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  college_name: string;
  degree: string;
  branch: string;
  graduation_year: number | null;
  cgpa: string | null;
  bio: string;
};

type Skill = {
  id: number;
  name: string;
  category: string;
};

type StudentSkill = {
  id: number;
  skill: number;
  skill_name: string;
  skill_category: string;
  proficiency: string;
};

const proficiencyLevels = [
  "BEGINNER",
  "INTERMEDIATE",
  "ADVANCED",
  "EXPERT",
];

export default function StudentProfilePage() {
  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [catalogue, setCatalogue] = useState<Skill[]>([]);
  const [studentSkills, setStudentSkills] = useState<StudentSkill[]>([]);
  const [selectedSkill, setSelectedSkill] = useState("");
  const [proficiency, setProficiency] = useState("BEGINNER");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadProfile() {
    setLoading(true);
    setError("");

    try {
      const [profileData, skillData, studentSkillData] = await Promise.all([
        apiRequest<StudentProfile>("/api/students/me/"),
        apiRequest<Skill[]>("/api/skills/"),
        apiRequest<StudentSkill[]>("/api/students/me/skills/"),
      ]);

      setProfile(profileData);
      setCatalogue(skillData);
      setStudentSkills(studentSkillData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load profile.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadProfile();
  }, []);

  function updateField(
    field: keyof StudentProfile,
    value: string,
  ) {
    setProfile((previous) =>
      previous ? { ...previous, [field]: value } : previous,
    );
  }

  async function saveProfile(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!profile) return;

    setSaving(true);
    setError("");
    setMessage("");

    try {
      const updated = await apiRequest<StudentProfile>(
        "/api/students/me/",
        {
          method: "PATCH",
          body: JSON.stringify({
            phone_number: profile.phone_number,
            college_name: profile.college_name,
            degree: profile.degree,
            branch: profile.branch,
            graduation_year: profile.graduation_year || null,
            cgpa: profile.cgpa || null,
            bio: profile.bio,
          }),
        },
      );

      setProfile(updated);
      setMessage("Profile updated successfully.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to save profile.");
    } finally {
      setSaving(false);
    }
  }

  async function addSkill(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedSkill) return;

    setError("");
    setMessage("");

    try {
      const newSkill = await apiRequest<StudentSkill>(
        "/api/students/me/skills/",
        {
          method: "POST",
          body: JSON.stringify({
            skill: Number(selectedSkill),
            proficiency,
          }),
        },
      );

      setStudentSkills((previous) => [...previous, newSkill]);
      setSelectedSkill("");
      setProficiency("BEGINNER");
      setMessage("Skill added successfully.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to add skill.");
    }
  }

  async function updateSkillLevel(id: number, level: string) {
    setError("");
    setMessage("");

    try {
      const updated = await apiRequest<StudentSkill>(
        `/api/students/me/skills/${id}/`,
        {
          method: "PATCH",
          body: JSON.stringify({ proficiency: level }),
        },
      );

      setStudentSkills((previous) =>
        previous.map((skill) => skill.id === id ? updated : skill),
      );

      setMessage("Skill proficiency updated.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to update skill.");
    }
  }

  async function removeSkill(id: number) {
    if (!window.confirm("Remove this skill from your profile?")) return;

    setError("");
    setMessage("");

    try {
      await apiRequest(`/api/students/me/skills/${id}/`, {
        method: "DELETE",
      });

      setStudentSkills((previous) =>
        previous.filter((skill) => skill.id !== id),
      );

      setMessage("Skill removed successfully.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to remove skill.");
    }
  }

  if (loading) {
    return <main className="profile-page"><p>Loading profile...</p></main>;
  }

  if (!profile) {
    return (
      <main className="profile-page">
        <p className="profile-error">{error || "Profile unavailable."}</p>
        <button onClick={() => void loadProfile()}>Retry</button>
      </main>
    );
  }

  const availableSkills = catalogue.filter(
    (skill) => !studentSkills.some((item) => item.skill === skill.id),
  );

  return (
    <main className="profile-page">
      <header className="profile-header">
        <Link to="/dashboard" className="profile-brand">CareerForge</Link>
        <Link to="/dashboard" className="profile-back">Back to dashboard</Link>
      </header>

      <section className="profile-content">
        <div className="profile-heading">
          <p className="student-eyebrow">STUDENT ACCOUNT</p>
          <h1>My Profile</h1>
          <p>Keep your academic details and skills up to date.</p>
        </div>

        {error && <p className="profile-error">{error}</p>}
        {message && <p className="profile-success">{message}</p>}

        <form className="profile-panel" onSubmit={saveProfile}>
          <h2>Personal and academic information</h2>

          <div className="profile-grid">
            <label>
              First name
              <input value={profile.first_name} disabled />
            </label>

            <label>
              Last name
              <input value={profile.last_name} disabled />
            </label>

            <label>
              Email
              <input value={profile.email} disabled />
            </label>

            <label>
              Phone number
              <input
                value={profile.phone_number}
                onChange={(e) => updateField("phone_number", e.target.value)}
                placeholder="Enter phone number"
              />
            </label>

            <label>
              College / University
              <input
                value={profile.college_name}
                onChange={(e) => updateField("college_name", e.target.value)}
                placeholder="Enter college name"
              />
            </label>

            <label>
              Degree
              <input
                value={profile.degree}
                onChange={(e) => updateField("degree", e.target.value)}
                placeholder="e.g. B.Tech"
              />
            </label>

            <label>
              Branch / Specialization
              <input
                value={profile.branch}
                onChange={(e) => updateField("branch", e.target.value)}
                placeholder="e.g. CSE - Cyber Security"
              />
            </label>

            <label>
              Graduation year
              <input
                type="number"
                min="2000"
                max="2100"
                value={profile.graduation_year ?? ""}
                onChange={(e) =>
                  updateField("graduation_year", e.target.value)
                }
                placeholder="e.g. 2027"
              />
            </label>

            <label>
              CGPA
              <input
                type="number"
                min="0"
                max="10"
                step="0.01"
                value={profile.cgpa ?? ""}
                onChange={(e) => updateField("cgpa", e.target.value)}
                placeholder="e.g. 8.15"
              />
            </label>
          </div>

          <label className="profile-bio-label">
            About me
            <textarea
              rows={4}
              value={profile.bio}
              onChange={(e) => updateField("bio", e.target.value)}
              placeholder="Write a short introduction about yourself..."
            />
          </label>

          <button className="profile-save" type="submit" disabled={saving}>
            {saving ? "Saving..." : "Save profile"}
          </button>
        </form>

        <section className="profile-panel">
          <h2>My technical skills</h2>
          <p className="profile-muted">
            Add skills and specify your proficiency level.
          </p>

          <form className="skill-add-form" onSubmit={addSkill}>
            <select
              value={selectedSkill}
              onChange={(e) => setSelectedSkill(e.target.value)}
              required
            >
              <option value="">Select a skill</option>
              {availableSkills.map((skill) => (
                <option key={skill.id} value={skill.id}>
                  {skill.name}{skill.category ? ` (${skill.category})` : ""}
                </option>
              ))}
            </select>

            <select
              value={proficiency}
              onChange={(e) => setProficiency(e.target.value)}
            >
              {proficiencyLevels.map((level) => (
                <option key={level} value={level}>{level}</option>
              ))}
            </select>

            <button type="submit" disabled={!selectedSkill}>
              Add skill
            </button>
          </form>

          {studentSkills.length === 0 ? (
            <p className="profile-empty">No skills added yet.</p>
          ) : (
            <div className="skill-list">
              {studentSkills.map((skill) => (
                <article className="skill-row" key={skill.id}>
                  <div>
                    <strong>{skill.skill_name}</strong>
                    <small>{skill.skill_category || "General"}</small>
                  </div>

                  <select
                    value={skill.proficiency}
                    onChange={(e) =>
                      void updateSkillLevel(skill.id, e.target.value)
                    }
                  >
                    {proficiencyLevels.map((level) => (
                      <option key={level} value={level}>{level}</option>
                    ))}
                  </select>

                  <button
                    type="button"
                    className="skill-remove"
                    onClick={() => void removeSkill(skill.id)}
                  >
                    Remove
                  </button>
                </article>
              ))}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}