export interface Job{
    title : string,
    url : string,
    description : string,
    organization : string,
    location: string,
    job_type: string //full-time , part-time
    job_preference: string //on site, remote, hybrid
    // experience: string;
    is_submitted: boolean;
}