
const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function apiRequest<T>(
    endpoint: string,
    options: RequestInit = {},
): Promise<T> {
    const token = localStorage.getItem("access_token");

    const headers = new Headers(options.headers);

    if (!(options.body instanceof FormData)) {
        headers.set("Content-Type", "application/json");
    }

    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        const message =
            data?.detail ||
            data?.email?.[0] ||
            data?.password?.[0] ||
            data?.non_field_errors?.[0] ||
            "Something went wrong. Please try again.";

        throw new Error(message);
    }

    return data as T;
}
