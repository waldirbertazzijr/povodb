import axios from "axios";

// Use local proxy instead of direct API URL to avoid CORS issues
const apiClient = axios.create({
    baseURL: `/api/v1`,
    headers: {
        "Content-Type": "application/json",
    },
});
console.log("Using API through local proxy");

// Request interceptor for API calls
apiClient.interceptors.request.use(
    (config) => {
        // You can add auth token here if needed
        // const token = localStorage.getItem('auth_token');
        // if (token) {
        //   config.headers['Authorization'] = `Bearer ${token}`;
        // }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    },
);

// Response interceptor for API calls
apiClient.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        // Handle 401 Unauthorized errors
        if (error.response?.status === 401 && !originalRequest._retry) {
            // Handle token refresh or redirect to login
            // Example: return refreshTokenAndRetry(originalRequest);
        }

        // Log detailed error information for debugging
        console.error("API Error:", {
            url: originalRequest?.url,
            method: originalRequest?.method,
            status: error.response?.status,
            data: error.response?.data,
            message: error.message,
        });

        // Handle other errors
        return Promise.reject(error);
    },
);

export default apiClient;

export const handleApiError = (error: unknown): string => {
    if (axios.isAxiosError(error)) {
        // Handle Axios errors
        const message = error.response?.data?.detail || error.message;
        return message;
    }

    // Handle other errors
    return error instanceof Error ? error.message : "An unknown error occurred";
};

// Type for pagination params
export interface PaginationParams {
    skip?: number;
    limit?: number;
    page?: number;
}

// Type for common filter params
export interface FilterParams {
    [key: string]: string | number | boolean | undefined;
}

// Helper function to build query params
export const buildQueryParams = (
    params: PaginationParams & FilterParams,
): string => {
    const queryParams = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== "") {
            queryParams.append(key, String(value));
        }
    });

    return queryParams.toString();
};
