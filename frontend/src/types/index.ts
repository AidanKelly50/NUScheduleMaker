export interface Semester {
  code: string;
  description: string;
}

export interface Subject {
  code: string;
  description: string;
}

export interface Course {
  subject: string;
  courseNumber: string;
  courseTitle: string;
  sections: Section[];
  colorCode: number;
}

export interface Section {
  courseReferenceNumber: string;
  sequenceNumber: string;
  campusDescription: string;
  maximumEnrollment: number;
  seatsAvailable: number;
  creditHourLow: number;
  faculty: string[];
  instructionalMethod: string;
  meetingTimes: MeetingTime[];
}

export interface CalendarSection extends Section {
  subject: string;
  courseNumber: string;
  colorCode: number;
}

export interface MeetingTime {
  buildingDescription: string;
  beginTime: string;
  endTime: string;
  monday: boolean;
  tuesday: boolean;
  wednesday: boolean;
  thursday: boolean;
  friday: boolean;
}

export interface Schedule {
  sections: CalendarSection[];
}

export interface Message {
  text: string;
}
