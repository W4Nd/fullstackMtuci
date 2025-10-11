export interface Medication {
  name: string;
  dosage: string;
}

export interface Reminder {
  id: number;
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