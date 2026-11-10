
import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import { apiRequest } from "../lib/api";

export type User = {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: "STUDENT" | "RECRUITER" | "ADMIN";
};

type AuthContextType = {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (
    details: RegisterDetails,
  ) => Promise<void>;
  logout: () => void;
};

type RegisterDetails = {
  email: string;
  first_name: string;
  last_name: string;
  role: "STUDENT" | "RECRUITER";
  password: string;
  password2: string;
};

type LoginResponse = {
  access: string;
  refresh: string;
  user: User;
};

const AuthContext = createContext<AuthContextType | undefined>(
  undefined,
);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setLoading(false);
      return;
    }

    apiRequest<User>("/api/auth/me/")
      .then(setUser)
      .catch(() => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  async function login(email: string, password: string) {
    const response = await apiRequest<LoginResponse>(
      "/api/auth/login/",
      {
        method: "POST",
        body: JSON.stringify({ email, password }),
      },
    );

    localStorage.setItem("access_token", response.access);
    localStorage.setItem("refresh_token", response.refresh);
    setUser(response.user);
  }

  async function register(details: RegisterDetails) {
    await apiRequest<User>("/api/auth/register/", {
      method: "POST",
      body: JSON.stringify(details),
    });
  }

  function logout() {
    const refresh = localStorage.getItem("refresh_token");

    if (refresh) {
      apiRequest("/api/auth/logout/", {
        method: "POST",
        body: JSON.stringify({ refresh }),
      }).catch(() => {
        // Clear local session even if server logout fails.
      });
    }

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{ user, loading, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
