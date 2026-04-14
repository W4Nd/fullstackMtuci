import { apiService } from './api';
import type { UserProfile } from '../types';

export const profileService = {
  getProfile: async (): Promise<UserProfile> => {
    try {
        console.log('📡 Fetching profile...');
        // @ts-expect-error
      const response = await apiService.get('/profile/me');
      console.log('✅ Profile fetched:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('❌ Error fetching profile:', error);
      throw error;
    }
  },

  updateProfile: async (profileData: Partial<UserProfile>): Promise<UserProfile> => {
    try {
        console.log('📡 Updating profile...', profileData);
        // @ts-expect-error
      const response = await apiService.put('/profile/me', profileData);
      console.log('✅ Profile updated:', response.data);
      return response.data.profile;
    } catch (error: any) {
      console.error('❌ Error updating profile:', error);
      throw error;
    }
  }
};
