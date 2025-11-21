import { useMutation, useQueryClient } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

export function useImportQuestions() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (file) => {
            const formData = new FormData();
            formData.append("file", file);

            const response = await axiosClient.post("/import-excel", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["questions"] });
        },
    });
}