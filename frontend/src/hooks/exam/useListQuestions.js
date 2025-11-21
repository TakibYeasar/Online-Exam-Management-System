import { useQuery } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

export function useListQuestions(filters) {
    const params = new URLSearchParams(filters).toString();

    return useQuery({
        queryKey: ["questions", filters],
        queryFn: async () => {
            const response = await axiosClient.get(`/exam/all-questions?${params}`);
            return response.data;
        },
        enabled: !!localStorage.getItem("access_token"),
    });
}