
import { BrowserRouter, Link, Navigate, Route, Routes } from "react-router-dom";

import { AuthProvider, useAuth } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import StudentProfilePage from "./pages/StudentProfilePage";
import StudentResumesPage from "./pages/StudentResumesPage";

import "./App.css";

function HomePage() {
  const { user } = useAuth();

  return (
    <main className="home-page">
      <nav className="home-nav">
        <Link to="/" className="brand">CareerForge</Link>
        <div>
          {user ? (
            <Link to="/dashboard" className="nav-button">
              Dashboard
            </Link>
          ) : (
            <>
              <Link to="/login" className="nav-link">Sign in</Link>
              <Link to="/register" className="nav-button">Get started</Link>
            </>
          )}
        </div>
      </nav>

      <section className="home-hero">
        <p className="eyebrow">YOUR CAREER STARTS HERE</p>
        <h1>
          Build your future.
          <br />
          <span>Forge your career.</span>
        </h1>
        <p className="muted">
          Discover internships, explore placement opportunities,
          and manage your career journey in one place.
        </p>
        <Link to={user ? "/dashboard" : "/register"} className="primary-link">
          Explore CareerForge
        </Link>
      </section>
    </main>
  );
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/student/profile" element={<StudentProfilePage />} />
        <Route path="/student/resumes" element={<StudentResumesPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;