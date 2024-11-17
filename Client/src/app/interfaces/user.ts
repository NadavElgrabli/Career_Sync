export interface User {
    first_name: string;
    last_name: string;
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