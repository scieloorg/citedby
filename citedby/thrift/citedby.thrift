exception ServerError{
    1: string message;
}

service Citedby{
    string citedbypid(1:required string q, 2:string metaonly) throws (1:ServerError error_message)

    string citedbydoi(1:required string q, 2:string metaonly) throws (1:ServerError error_message)

    string citedbymeta(1:required string title, 2:string author_surname, 3:i32 year, 4:string metaonly) throws (1:ServerError error_message)
}