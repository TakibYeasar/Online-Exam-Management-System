import { useQuery } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

export function useSingleQuestion(questionId) {
    return useQuery({
        queryKey: ["question", questionId],
        queryFn: async () => {
            const response = await axiosClient.get(`/view-question/${questionId}`);
            return response.data;
        },
        enabled: !!questionId && !!localStorage.getItem("access_token"),
    });
}