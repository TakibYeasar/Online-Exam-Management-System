import { useMutation, useQueryClient } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

export function useSigninUser() {
    const queryClient = useQueryClient();

    const signinUserMutation = useMutation({
        mutationFn: async (userData) => {
            const response = await axiosClient.post("/auth/sign-up/", userData);
            return response.data;
        },
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ["newUser"] });
        }
    });
    return signinUserMutation;
}