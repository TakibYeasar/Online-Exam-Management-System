import { useQuery } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

export function useAvailableExams() {
    return useQuery({
        queryKey: ["availableExams"],
        queryFn: async () => {
            const response = await axiosClient.get(`/exam/available-exam`);
            return response.data;
        },
        enabled: !!localStorage.getItem("access_token"),
        staleTime: 5 * 60 * 1000,
    });
}