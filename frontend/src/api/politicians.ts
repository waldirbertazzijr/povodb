import apiClient, {
    PaginationParams,
    FilterParams,
    buildQueryParams,
    handleApiError,
} from "./client";
import { useQuery } from "@tanstack/react-query";

// Types
export interface Politician {
    id: string;
    name: string;
    party: string | null;
    position: string | null;
    country: string;
    state_province: string | null;
    bio: string | null;
    website: string | null;
    photo_url: string | null;
    created_at: string;
    updated_at: string;
}

export interface PoliticianPage {
    items: Politician[];
    total: number;
    page: number;
    size: number;
    pages: number;
}

export interface PoliticianCreate {
    name: string;
    party?: string;
    position?: string;
    country: string;
    state_province?: string;
    bio?: string;
    website?: string;
    photo_url?: string;
}

export interface PoliticianUpdate {
    name?: string;
    party?: string;
    position?: string;
    country?: string;
    state_province?: string;
    bio?: string;
    website?: string;
    photo_url?: string;
}

export interface PoliticianFilters extends FilterParams {
    name?: string;
    party?: string;
    country?: string;
    state_province?: string;
}

// API functions
export const getPoliticians = async (
    params: PaginationParams & PoliticianFilters = {},
): Promise<PoliticianPage> => {
    try {
        console.log("Fetching politicians with params:", params);
        const queryString = buildQueryParams(params);
        const response = await apiClient.get<PoliticianPage>(
            `/politicians?${queryString}`,
        );
        console.log("Politicians API response:", response);
        return response.data;
    } catch (error) {
        console.error("Error fetching politicians:", error);
        throw new Error(handleApiError(error));
    }
};

export const usePoliticians = (
    params: PaginationParams & PoliticianFilters = {},
) => {
    return useQuery({
        queryKey: ["politicians", params],
        queryFn: () => getPoliticians(params),
    });
};

export const getPolitician = async (id: string): Promise<Politician> => {
    try {
        const response = await apiClient.get<Politician>(`/politicians/${id}`);
        return response.data;
    } catch (error) {
        throw new Error(handleApiError(error));
    }
};

export const getPoliticianWithRelations = async (id: string): Promise<any> => {
    try {
        const response = await apiClient.get<any>(`/politicians/${id}/details`);
        return response.data;
    } catch (error) {
        throw new Error(handleApiError(error));
    }
};

export const getPoliticianContributions = async (id: string): Promise<any> => {
    try {
        const response = await apiClient.get<any>(
            `/politicians/${id}/contributions`,
        );
        return response.data;
    } catch (error) {
        throw new Error(handleApiError(error));
    }
};

export const createPolitician = async (
    data: PoliticianCreate,
): Promise<Politician> => {
    try {
        const response = await apiClient.post<Politician>("/politicians", data);
        return response.data;
    } catch (error) {
        throw new Error(handleApiError(error));
    }
};

export const updatePolitician = async (
    id: string,
    data: PoliticianUpdate,
): Promise<Politician> => {
    try {
        const response = await apiClient.put<Politician>(
            `/politicians/${id}`,
            data,
        );
        return response.data;
    } catch (error) {
        throw new Error(handleApiError(error));
    }
};

export const deletePolitician = async (id: string): Promise<Politician> => {
    try {
        const response = await apiClient.delete<Politician>(
            `/politicians/${id}`,
        );
        return response.data;
    } catch (error) {
        throw new Error(handleApiError(error));
    }
};
