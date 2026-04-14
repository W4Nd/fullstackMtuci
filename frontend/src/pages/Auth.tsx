import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Auth.css";
import { useAuth } from "../contexts/AuthContext";
import { apiService } from "../services/api";
import type { RegisterData } from "../types";
import SEO from '../components/SEO';

const Auth: React.FC = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
    });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    
    const { login } = useAuth();

    useEffect(() => {
        const checkAuth = async () => {
            const accessToken = localStorage.getItem('auth_access_token');
            if (accessToken) {
                navigate("/");
            }
        };
        checkAuth();
    }, [navigate]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");

        // Проверка паролей для регистрации
        if (!isLogin && formData.password !== formData.confirmPassword) {
            setError("Пароли не совпадают");
            setLoading(false);
            return;
        }

        try {
            if (isLogin) {
                await login({ 
                    username: formData.username, 
                    password: formData.password 
                });
                navigate("/");
            } else {
                const registerData: RegisterData = {
                    username: formData.username,
                    email: formData.email,
                    password: formData.password,
                };
                
                await apiService.register(registerData);
                
                await login({ 
                    username: formData.username, 
                    password: formData.password 
                });
                navigate("/");
            }
        } catch (err: any) {
            const errorMessage = 
                err.response?.data?.detail || 
                err.response?.data?.error || 
                err.message || 
                "Произошла ошибка";
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    return (
        <>
          <SEO
            title="Вход в систему"
            description="Авторизуйтесь, чтобы управлять напоминаниями о приёме лекарств"
            canonical="/auth"
          />
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h1>{isLogin ? "Вход в систему" : "Регистрация"}</h1>
                    <p>
                        {isLogin
                            ? "Войдите в свой аккаунт"
                            : "Создайте новый аккаунт"}
                    </p>
                </div>

                <div className="auth-tabs">
                    <button
                        className={`tab ${isLogin ? "active" : ""}`}
                        onClick={() => setIsLogin(true)}
                    >
                        Вход
                    </button>
                    <button
                        className={`tab ${!isLogin ? "active" : ""}`}
                        onClick={() => setIsLogin(false)}
                    >
                        Регистрация
                    </button>
                </div>

                {error && <div className="error-message">{error}</div>}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label htmlFor="username">Имя пользователя *</label>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            placeholder="Введите имя пользователя"
                            required
                        />
                    </div>

                    {!isLogin && (
                        <div className="form-group">
                            <label htmlFor="email">Email *</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="Введите email"
                                required
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label htmlFor="password">Пароль *</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            placeholder="Введите пароль"
                            required
                            minLength={6}
                        />
                    </div>

                    {!isLogin && (
                        <div className="form-group">
                            <label htmlFor="confirmPassword">
                                Подтверждение пароля *
                            </label>
                            <input
                                type="password"
                                id="confirmPassword"
                                name="confirmPassword"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                placeholder="Повторите пароль"
                                required
                            />
                        </div>
                    )}

                    <button
                        type="submit"
                        className="submit-btn"
                        disabled={loading}
                    >
                        {loading
                            ? "Загрузка..."
                            : isLogin
                              ? "Войти"
                              : "Зарегистрироваться"}
                    </button>
                </form>

                <div className="auth-footer">
                    {isLogin ? (
                        <p>
                            Нет аккаунта?{" "}
                            <button
                                className="link-btn"
                                onClick={() => setIsLogin(false)}
                                type="button"
                            >
                                Зарегистрируйтесь
                            </button>
                        </p>
                    ) : (
                        <p>
                            Уже есть аккаунт?{" "}
                            <button
                                className="link-btn"
                                onClick={() => setIsLogin(true)}
                                type="button"
                            >
                                Войдите
                            </button>
                        </p>
                    )}
                </div>
            </div>
            </div>
        </>
    );
};

export default Auth;
