import { useMutation, useQueryClient } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

export function useCreateQuestion() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (questionData) => {
            const response = await axiosClient.post("/create-question", questionData);
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["questions"] });
        },
    });
}