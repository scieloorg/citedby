exception ServerError{
    1: string message;
}

service Citedby{
    string citedby_pid(1:required string q, 2:bool metaonly) throws (1:ServerError error_message)

    string citedby_doi(1:required string q, 2:bool metaonly) throws (1:ServerError error_message)

    string citedby_meta(1:required string title, 2:string author_surname, 3:i32 year, 4:bool metaonly) throws (1:ServerError error_message)
}