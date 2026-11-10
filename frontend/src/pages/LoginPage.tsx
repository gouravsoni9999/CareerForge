
import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
    const { login } = useAuth();
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(event: FormEvent) {
        event.preventDefault();
        setError("");
        setSubmitting(true);

        try {
            await login(email, password);
            navigate("/dashboard");
        } catch (err) {
            setError(
                err instanceof Error ? err.message : "Login failed.",
            );
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <main className="auth-page">
            <form className="auth-card" onSubmit={handleSubmit}>
                <Link to="/" className="brand">CareerForge</Link>
                <p className="eyebrow">WELCOME BACK</p>
                <h1>Sign in to your account</h1>
                <p className="muted">Continue your career journey.</p>

                {error && <div className="error">{error}</div>}

                <label>Email address</label>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    required
                />

                <label>Password</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    required
                />

                <button disabled={submitting}>
                    {submitting ? "Signing in..." : "Sign in"}
                </button>

                <p className="auth-footer">
                    Don't have an account? <Link to="/register">Register</Link>
                </p>
            </form>
        </main>
    );
}