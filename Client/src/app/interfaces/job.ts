export interface Job{
    title : string,
    url : string,
    description : string,
    organization : string,
    location: string,
    job_type: string //full-time , part-time
    job_preference: string //on site, remote, hybrid
    experience: number | null;
    applied: boolean;
}

export interface UserJob{
    job : Job,
    job_id: string,
    score : number,
    applied : boolean,
}