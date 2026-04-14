export interface Medication {
  name: string;
  dosage: string;
}

export interface Reminder {
  id: number;
  user_id: number; 
  medication: Medication;
  time: string;
  days: number[];
  is_active: boolean;
}

export interface NewReminder {
  medication_name: string;
  dosage: string;
  time: string;
  days: number[];
}

export interface PaginatedRemindersResponse {
  items: Reminder[];
  total: number;
  page: number;
  page_size: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string | null;
  gender?: string | null;
  age?: number | null;
  height_cm?: number | null;
  weight_kg?: number | null;
  target_weight_kg?: number | null;
  bio?: string | null;
  created_at: string;
  updated_at?: string | null;
}

export interface AuthResponse {
  message: string;
  user: User;
  token: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  confirmPassword?: string;
}

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name: string | null;
  gender: 'M' | 'F' | 'Other' | null;
  age: number | null;
  height_cm: number | null;
  weight_kg: number | null;
  target_weight_kg: number | null;
  bio: string | null;
  bmi: number | null;
  created_at: string;
  updated_at: string;
}
