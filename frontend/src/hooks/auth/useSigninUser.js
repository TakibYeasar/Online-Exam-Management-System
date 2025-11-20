import { useMutation, useQueryClient } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

export function useSigninUser() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (userData) => {
            const response = await axiosClient.post("/auth/sign-in/", userData);
            return response.data;
        },
        onSuccess: (data) => {
            try {
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);
            } catch (error) {
                console.error("Failed to store tokens", error);
            }

            queryClient.invalidateQueries({ queryKey: ["currentUser"] });
        },
    });
}
