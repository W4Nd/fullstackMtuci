import React, { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode } from "react";
import type { User } from "../types";
import { apiService } from "../services/api";

interface AuthContextType {
    user: User | null;
    roles: string[];
    loading: boolean;
    login: (credentials: { username: string; password: string }) => Promise<any>;  // 🔥 НОВЫЙ тип
    logout: () => Promise<void>;  // 🔥 async logout
    checkAuth: () => Promise<void>;
    hasPermission: (permission: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [roles, setRoles] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);

    const hasPermission = (permission: string): boolean => {  // 🔥 Возвращаем тип
        if (roles.includes("admin")) return true;
        if (permission.includes("_own") && user) return true;
        return false;
    };

    // 🔥 НОВЫЙ login с credentials
    const login = async (credentials: { username: string; password: string }) => {
        try {
            const data = await apiService.login(credentials);
            setUser(data.user);
            setRoles(data.roles || ['user']);
            return data;
        } catch (error) {
            throw error;
        }
    };

    const checkAuth = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('auth_access_token');
            if (!token) throw new Error('No token');
            
            const me = await apiService.getMe();
            setUser(me.user);
            setRoles(me.roles);
        } catch (error) {
            setUser(null);
            setRoles([]);
            localStorage.removeItem('auth_access_token');
            localStorage.removeItem('auth_refresh_token');
        } finally {
            setLoading(false);
        }
    };

    const logout = async () => {
        await apiService.logout();
        setUser(null);
        setRoles([]);
    };

    useEffect(() => {
        checkAuth();
        const handleAuthChange = () => checkAuth();
        window.addEventListener("authChange", handleAuthChange);
        return () => window.removeEventListener("authChange", handleAuthChange);
    }, []);

    const value: AuthContextType = {  // 🔥 Явно типизируем
        user,
        roles,
        loading,
        login,
        logout,
        checkAuth,
        hasPermission,
    };

    return (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    );
};
