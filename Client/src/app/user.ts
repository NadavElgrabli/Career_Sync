export interface User {
    firstName: string;
    lastName: string;
    password?: string;
    username: string;
    gender: string;
    jobs: string[];
    location: string;
    full_job: boolean;
    work_preference: string[];
    skills: string[];
    experience: number;
    degree: string;
}