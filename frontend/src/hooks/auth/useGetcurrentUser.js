import { useQuery } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

export function useCurrentAuthenticatedUser() {
    return useQuery({
        queryKey: ["currentUser"],
        queryFn: async () => {
            const token = localStorage.getItem("access_token");

            if (!token) {
                throw new Error("No access token found");
            }

            const response = await axiosClient.get("/auth/current-user/");
            return response.data;
        },
        retry: false,
        enabled: !!localStorage.getItem("access_token"),
    });
}
