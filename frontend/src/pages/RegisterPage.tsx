
import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    role: "STUDENT" as "STUDENT" | "RECRUITER",
    password: "",
    password2: "",
  });

  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function update(
    field: keyof typeof form,
    value: string,
  ) {
    setForm((previous) => ({ ...previous, [field]: value }));
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      await register(form);
      navigate("/login", {
        state: { message: "Registration successful. Please sign in." },
      });
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Registration failed.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <Link to="/" className="brand">CareerForge</Link>
        <p className="eyebrow">GET STARTED</p>
        <h1>Create your account</h1>
        <p className="muted">Join students and recruiters on CareerForge.</p>

        {error && <div className="error">{error}</div>}

        <label>First name</label>
        <input
          value={form.first_name}
          onChange={(e) => update("first_name", e.target.value)}
          required
        />

        <label>Last name</label>
        <input
          value={form.last_name}
          onChange={(e) => update("last_name", e.target.value)}
          required
        />

        <label>Email address</label>
        <input
          type="email"
          value={form.email}
          onChange={(e) => update("email", e.target.value)}
          required
        />

        <label>Register as</label>
        <select
          value={form.role}
          onChange={(e) =>
            update("role", e.target.value)
          }
        >
          <option value="STUDENT">Student</option>
          <option value="RECRUITER">Recruiter</option>
        </select>

        <label>Password</label>
        <input
          type="password"
          value={form.password}
          onChange={(e) => update("password", e.target.value)}
          minLength={8}
          required
        />

        <label>Confirm password</label>
        <input
          type="password"
          value={form.password2}
          onChange={(e) => update("password2", e.target.value)}
          minLength={8}
          required
        />

        <button disabled={submitting}>
          {submitting ? "Creating account..." : "Create account"}
        </button>

        <p className="auth-footer">
          Already registered? <Link to="/login">Sign in</Link>
        </p>
      </form>
    </main>
  );
}