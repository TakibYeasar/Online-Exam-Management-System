import { useMutation, useQueryClient } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

export function useCreateExam() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (examData) => {
            const response = await axiosClient.post("/create-exam", examData);
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["availableExams"] });
            queryClient.invalidateQueries({ queryKey: ["exams"] });
        },
    });
}