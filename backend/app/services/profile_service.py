class ProfileService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_profile(self, user_id):
        """Получить профиль с расчётом BMI"""
        profile = self.user_repository.get_user_profile(user_id)
        if not profile:
            return None
        
        bmi = None
        if profile.get('height_cm') and profile.get('weight_kg'):
            try:
                height_m = float(profile['height_cm']) / 100
                weight_kg = float(profile['weight_kg'])
                bmi = round(weight_kg / (height_m ** 2), 2)
            except:
                bmi = None
        
        profile['bmi'] = bmi
        return profile

    def update_profile(self, user_id, profile_data):
        """Обновить профиль с валидацией"""
        errors = self._validate_profile(profile_data)
        if errors:
            return {'success': False, 'errors': errors}

        success = self.user_repository.update_user_profile(user_id, profile_data)
        if success:
            updated_profile = self.get_profile(user_id)
            return {'success': True, 'profile': updated_profile}
        
        return {'success': False, 'errors': ['Failed to update profile']}

    @staticmethod
    def _validate_profile(data):
        """Валидация данных профиля"""
        errors = []
        
        if 'age' in data and data['age']:
            try:
                age = int(data['age'])
                if not (1 <= age <= 150):
                    errors.append('Age must be between 1 and 150')
            except:
                errors.append('Age must be a number')
        
        if 'height_cm' in data and data['height_cm']:
            try:
                height = int(data['height_cm'])
                if not (50 <= height <= 250):
                    errors.append('Height must be between 50 and 250 cm')
            except:
                errors.append('Height must be a number')
        
        if 'weight_kg' in data and data['weight_kg']:
            try:
                weight = float(data['weight_kg'])
                if not (20 <= weight <= 500):
                    errors.append('Weight must be between 20 and 500 kg')
            except:
                errors.append('Weight must be a number')
        
        if 'target_weight_kg' in data and data['target_weight_kg']:
            try:
                target = float(data['target_weight_kg'])
                if not (20 <= target <= 500):
                    errors.append('Target weight must be between 20 and 500 kg')
            except:
                errors.append('Target weight must be a number')
        
        if 'gender' in data and data['gender']:
            if data['gender'] not in ['M', 'F', 'Other']:
                errors.append('Invalid gender value')
        
        return errors
