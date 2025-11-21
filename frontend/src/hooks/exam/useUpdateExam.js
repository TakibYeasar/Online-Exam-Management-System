import { useMutation, useQueryClient } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

export function useUpdateExam(examId) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (updateData) => {
            const response = await axiosClient.patch(`/update-exam/${examId}`, updateData);
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["exam", examId] });
            queryClient.invalidateQueries({ queryKey: ["availableExams"] });
            queryClient.invalidateQueries({ queryKey: ["exams"] });
        },
    });
}